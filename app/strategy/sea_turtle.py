from app.base.base_strategy import StrategyBase
from app.base.constants import Period
from app.base.bar_reader import BarReader
import pandas as pd
import numpy as numpy
from app.base import util

class SeaTurtle(StrategyBase):
    def __init__(self, base, quote = 'btc'):
        super().__init__(base, quote)

    def init_system(self, short_in_date=14, long_in_date=55, short_out_date=10, long_out_date=20, period = "60min"):
        # 系统1入市的trailing date
        self.short_in_date = short_in_date
        # 系统2入市的trailing date
        self.long_in_date = long_in_date
        # 系统1 exiting market trailing date
        self.short_out_date = short_out_date
        # 系统2 exiting market trailing date
        self.long_out_date = long_out_date
        # 获取bar的粒度
        self.period = period
        # 系统标志
        self.sys1 = True
        # 加仓次数
        self.add_times = 0
        # 交易手续费
        self.fee = 0.002

    def handel_data(self):
        bar_size = self.short_in_date
        if self.sys1 == False:
            bar_size = self.long_in_date

        self.T = bar_size
        barReader = BarReader(self)
        # 获取市场最新数据
        market_data = barReader.read_bar(size=bar_size)
        # 获取市场最新价格
        price = barReader.read_current_price()
        # 获取ATR
        atr = barReader.calc_data_atr()

        in_out_flage = self.in_out(market_data, price)

        # 入场
        if in_out_flage == 1:
            # 还没有入场
            if self.add_times == 0:
                print(f"产生突破信号，进入市场，突破价格是:{price}")


    def in_out(self, market_data, price):
        dataFrame = pd.DataFrame(market_data)
        T = self.T

        high = dataFrame['high'].iloc[-T:]
        # 这里是T/2唐奇安下沿，在向下突破T/2唐奇安下沿卖出而不是在向下突破T唐奇安下沿卖出，这是为了及时止损
        low = dataFrame['low'].iloc[-int(T / 2):]

        up = numpy.max(high)
        down = numpy.min(low)

        print("当前价格为: " + str(price) + " , 唐奇安上轨为: " + str(up) + ", 唐奇安下轨为: " + str(down))
        print(f"当前的价格为{price}, 唐奇安上轨为:{up}, 下轨为:{down}")

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

    def buy_market(self,price, atr):
        # 计算per_unit
        unit = self.cal_unit_by_atr(atr)
        if unit > 0:
            # 计算购买unit 所需要的money
            need_money = unit * self.price
            print(f'购买的unit 是{unit} 需要的money 是{need_money} ')
            value = min(need_money, self.init_quote_amount)
            print(f'实际需要的money数量是{value}')

            print(f"下单金额为 {value} 元")
            baseCoin = self.cal_get_base_coin(price, value)
            self.init_base_amount = self.init_base_amount + baseCoin
            self.init_quote_amount = self.init_quote_amount - value

            print(f"能够得到的baseCoin is {baseCoin} ")
            print(f"self.init_base_amount is {self.init_base_amount} self.init_quote_amount is {self.init_quote_amount}")
        else:
            print(f'账户余额不足，购买的unit 0, 不产生订单信息 ')

    def cal_unit_by_atr(self, atr):
        money = self.init_base_amount
        position = (money * 0.01) / atr
        position = util.as_num(position,self.amount_precision)
        return float(position)

    def cal_get_base_coin(self,price, quoteCoin):
        result = quoteCoin / price * (1 - self.fee)
        return float(util.as_num(result, 18))

    def cal_get_quote_coin(self,price, baseCoin):
        result = baseCoin * price * (1 - self.fee)
        return float(util.as_num(result, 18))