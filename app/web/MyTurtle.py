import HuobiServices as houbi
import talib
import numpy as numpy
import pandas as pa
import threading
import time

'''
定义全局变量，初始化基本信息
'''
context = {
    'base': 'eos',            # 交易的币种
    'quote': 'btc',           # 计价的币种
    'price_precision': 0,     # 交易对价格精度
    'amount_precision': 0,    # 交易对数量精度
    'period': '4hour',         # 策略的时间粒度
    'short_in_date': 14,      # 系统1入市的trailing date
    'long_in_date': 55,       # 系统2入市的trailing date
    'short_out_date': 10,     # 系统1 exiting market trailing date
    'long_out_date': 20,      # 系统2 exiting market trailing date
    'dollars_per_share': 0,   # dollars_per_share是标的股票每波动一个最小单位，1手股票的总价格变化量
    'loss': 0.1,              # 可承受的最大损失率
    'adjust': 0.8,            # 若超过最大损失率，则调整率为
    'number_days': 20,        # 计算N值的天数
    'unit_limit': 4,          # 最大允许单元
    'ratio': 0.8,             # 系统1所配金额占总金额比例
    'sys1': True,             # 系统1执行
    'base_amount': 0,         # base coin的数量
    'quote_amount': 0,        # quote coin的数量
    'init_context' : False,  # 是否初始化账户
    'hold_flage' : False,      # 是否已经持有
    'add_time' : 0,              # 加仓次数
    'break_price': 0,           # 突破价格
}

def init_context():
    precision_data = houbi.get_symbol_precision(context['base'], context['quote'])
    context['price_precision'] = precision_data['price-precision']
    context['amount_precision'] = precision_data['amount-precision']
    context['dollars_per_share'] = (1.0 / (10 ** context['price_precision'])) * 100
    context['symbol'] = context['base'] + context['quote']

    # 获取账号的信息
    context['base_amount'] = houbi.get_symbol_balance(context['base'])
    context['quote_amount'] = houbi.get_symbol_balance(context['quote'])

    #pa.set_option('display.precision', 8)

def handel_data():
    if context['sys1']:
        size = context['short_in_date']

    # 获取最新的市场数据
    market_data = houbi.get_kline(context['symbol'], context['period'], size + 1)['data']
    # 获取当前行情数据
    price = float(houbi.get_current_price(context['symbol']))
    # 计算ATR
    atr = cal_atr(market_data)

    # 2 判断加仓或止损
    if context['hold_flage'] is True and float(context['base_amount']) > 0:  # 先判断是否持仓
        temp = add_or_stop(price, float(context['break_price']), atr)
        if temp == 1:  # 判断加仓
            if int(context['add_time']) < int(context['unit_limit']):  # 判断加仓次数是否超过上限
                print(f"产生加仓信号,加仓价格是：{price}")
                buy(atr,price)
                context['add_time'] += 1
                context['break_price'] = price
            else:
                print("加仓次数已经达到上限，不会加仓")
        elif temp == -1:  # 判断止损
            # 卖出止损
            print("产生止损信号")
            sell(price)
    else:
        # 根据当前价格判断入场还是出场
        in_out_flage = in_out(price, market_data, size)
        if in_out_flage == 1:  # 入场
            if context['hold_flage'] is False and float(context['quote_amount'])> 0:
                # 有买入信号，执行买入
                print(f"产生入场信号, 突破价格是{price}")
                buy(atr,price)
                context['add_time'] = 1
                context['hold_flage'] = True
                context['break_price'] = price
            else:
                print("已经入场，不产生入场信号")
        elif in_out_flage == -1:  # 离场
            if context['hold_flage'] is True:
                if float(context['base_amount']) > 0:
                    print("产生离场信号")
                    sell(price)
            else:
                print("尚未入场或已经离场，不产生离场信号")


def in_out(price, market_data, T):
    df = pa.DataFrame(market_data)
    df = df.iloc[: len(market_data) - 1]

    high = df['high'].iloc[-T:]
    # 这里是T/2唐奇安下沿，在向下突破T/2唐奇安下沿卖出而不是在向下突破T唐奇安下沿卖出，这是为了及时止损
    low = df['low'].iloc[-int(T / 2):]

    up = numpy.max(high)
    down = numpy.min(low)

    print("当前价格为: " + str(price) +" , 唐奇安上轨为: "+str(up)+", 唐奇安下轨为: "+str(down))

    if price > up:
        print('价格突破唐奇安上轨')
        return 1
    # 当前价格跌破唐奇安下沿，产生出场信号
    elif price < down:
        print('价格跌破唐奇安下轨')
        return -1
    # 未产生有效信号
    else:
        print('未产生有效信号')
        return 0

# 用户自定义的函数，可以被handle_data调用
# 判断是否加仓或止损:当价格相对上个买入价上涨 0.5ATR时，再买入一个unit; 当价格相对上个买入价下跌 2ATR时，清仓
def add_or_stop(price, lastprice, atr):
    if price >= lastprice + 0.5 * atr:
        print('当前价格比上一个购买价格上涨超过0.5个ATR')
        return 1
    elif price <= lastprice - 2 * atr:
        print('当前价格比上一个购买价格下跌超过2个ATR')
        return -1
    else:
        return 0

def buy(atr, price):
    unit = float(cal_per_unit(atr))
    if unit > 0:
        # 计算购买unit 所需要的money
        need_money = cal_position_btc(unit, price)
        print(f'购买的unit 是{unit} 需要的money 是{need_money} ')
        value = min(need_money, float(context['quote_amount']))
        print(f'实际需要的money数量是{value}')

        print(f"下单金额为 {value} 元")
        baseCoin = cal_get_base_coin(price, value)
        context['base_amount'] = float(context['base_amount']) + baseCoin
        context['quote_amount'] = float(context['quote_amount']) - value

        print(f"能够得到的baseCoin is {baseCoin} ")
        print(
            f"context['base_amount'] is {context['base_amount']} context['quote_amount'] is {context['quote_amount']}")
    else:
        print(f'账户余额不足，购买的unit 0, 不产生订单信息 ')

def sell(price):
    # 有卖出信号，且持有仓位，则市价单全仓卖出
    print(f"卖出数量为{context['base_amount']}")
    print(f"卖出价格为{price}")

    quoteCoin = cal_get_quote_coin(price, context['base_amount'])
    print(f"得到的quoteCoin is {quoteCoin}")
    context['base_amount'] = 0
    context['quote_amount'] = quoteCoin
    context['add_time'] = 0
    context['hold_flage'] = False


def as_num(x,precision):
    format_str = "{:."+str(precision)+"f}"
    r_y = format_str.format(float(x))
    return r_y
'''
def cal_atr(market_data):
    size = len(market_data)
    high_price = []
    low_price = []
    close_price = []
    for i in range(0, size):
        t_price = market_data[i]
        high_price.append(t_price['high'])
        low_price.append(t_price['low'])
        close_price.append(t_price['close'])

    # 反转得的的价格数据， 时间按照有小到大排序
    high_price = list(reversed(high_price))
    low_price = list(reversed(low_price))
    close_price = list(reversed(close_price))
    #print(high_price)

    np_hight = numpy.asarray(high_price, numpy.float64)
    np_low = numpy.asarray(low_price, numpy.float64)
    np_close = numpy.asarray(close_price, numpy.float64)
    #print(high_price)


    atr_array = talib.ATR(np_hight, np_low, np_close, size - 1)

    #print(atr_array)
    atr = atr_array[len(atr_array) - 1]
    atr = as_num(atr, int(context['price_precision']))
    context['ATR'] = float(atr)
    return float(atr)
'''
def cal_atr(market_data):
    df = pa.DataFrame(market_data)
    size = len(market_data)
    high_price = df['high'].iloc[::-1]
    low_price = df['low'].iloc[::-1]
    close_price = df['close'].iloc[::-1]

    atr_array = talib.ATR(high_price, low_price, close_price, size - 1)
    atr = atr_array[0]
    atr = as_num(atr, int(context['price_precision']))
    context['ATR'] = float(atr)
    return float(atr)
'''
def cal_art1(market_data):
    df = pa.DataFrame(market_data)
    data = df.iloc[: len(market_data) - 1]
    tr_list = []
    for i in range(len(data)):
        tr = max(data['high'].iloc[i] - data['low'].iloc[i], data['high'].iloc[i] - data['close'].iloc[i - 1],
                 data['close'].iloc[i - 1] - data['low'].iloc[i])
        tr_list.append(tr)

    print(tr_list)
    atr = numpy.array(tr_list).mean()
    return atr
'''
def cal_per_unit(atr):
    position = (float(context['quote_amount']) * 0.01) / atr
    position = as_num(position, int(context['amount_precision']))
    context['position'] = position
    return position

def cal_position_btc(position,price):
    need_money = position * price
    return need_money

def cal_get_base_coin(price, quoteCoin):
    result = quoteCoin / price * (1 - 0.002)
    return float(as_num(result, 18))

def cal_get_quote_coin(price, baseCoin):
    result = baseCoin * price * (1 - 0.002)
    return float(as_num(result, 18))

def heart_beat():
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print(f"context['base_amount'] is {context['base_amount']} context['quote_amount'] is {context['quote_amount']}")
    try:
        handel_data()
    except BaseException as e:
        print(f"error {e}")
    finally:
        threading.Timer(60, heart_beat).start()

if __name__ == '__main__':
    # 初始化账户信息
    init_context()
    # 循环处理数据
    heart_beat()
