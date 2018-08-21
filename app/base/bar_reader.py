from app.base.environment import Enviroment
from app.base.base_strategy import StrategyBase
from app.web import HuobiServices as huobi

class BarReader(Enviroment):

    def read_bar(self, strage = StrategyBase, size = 20):
        # 获取市场最新的bar
        market_data = huobi.get_kline(strage.symbol, period = strage.period, size = size)
        market_data = market_data['data']
        strage.market_data = market_data