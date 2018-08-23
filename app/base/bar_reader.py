from app.base.environment import Enviroment
from app.base.base_strategy import StrategyBase
from app.web import HuobiServices as huobi
import pandas as pd
import talib

class BarReader(Enviroment):

    def __init__(self, strategy = StrategyBase):
        self.strategy = strategy

    # 获取当前市场数据
    def read_bar(self, size = 20):
        # 获取市场最新的bar
        market_data = huobi.get_kline(self.strategy.symbol, period = self.strategy.period, size = size)
        market_data = market_data['data']
        self.strategy.market_data = market_data
        return market_data

    # 获取最新价格
    def read_current_price(self):
        price = float(huobi.get_current_price(self.strategy.symbol))
        self.strategy.price = price
        return price

    # 计算market data 的 ATR
    def calc_data_atr(self):
        market_data = self.strategy.market_data
        dataFrame = pd.DataFrame(market_data)
        size = len(market_data)

        # 按照时间顺序，由前到后排列
        high_price = dataFrame['high'].iloc[::-1]
        low_price = dataFrame['low'].iloc[::-1]
        close_price = dataFrame['close'].iloc[::-1]

        atr_array = talib.ATR(high_price, low_price, close_price, size - 1)
        atr = atr_array[0]
        atr = self.as_num(atr,self.strategy.price_precision)
        # atr = float(atr)
        self.strategy.ATR = atr
        return atr

    def as_num(self, x, precision):
        format_str = "{:." + str(precision) + "f}"
        r_y = format_str.format(float(x))
        return r_y