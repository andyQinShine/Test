from app.base.environment import Enviroment
from app.base.base_strategy import StrategyBase
from app.web import HuobiServices as huobi
import pandas as pa

class BarReader(Enviroment):

    def __init__(self, strage = StrategyBase):
        self.strage = strage

    # 获取最新的market bar 数据
    def read_bar(self, size = 20):
        # 获取市场最新的bar
        market_data = huobi.get_kline(self.strage.symbol, period = self.strage.period, size = size)
        market_data = market_data['data']
        self.strage.market_data = market_data

    # 获取当前的市场价格
    def read_current_price(self):
        price = float(huobi.get_current_price(self.strage.symbol))
        self.strage.price = price
        return price

    # 计算market data 的ATR
    def cal_atr(self):
        market_data = self.strage.market_data
        df = pa.DataFrame(market_data)
        size = len(market_data)

        # 将获取的数据倒叙排列
        high_price = df['high'].iloc[::-1]
        low_price = df['low'].iloc[::-1]
        close_price = df['close'].iloc[::-1]

        atr_array = talib.ATR(high_price, low_price, close_price, size - 1)
        atr = atr_array[0]
        atr = as_num(atr, int(context['price_precision']))
        context['ATR'] = float(atr)
        return float(atr)