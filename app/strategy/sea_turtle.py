from app.base.base_strategy import StrategyBase
from app.base.constants import Period
from app.base.bar_reader import BarReader

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

    def handel_data(self):
        bar_size = self.short_in_date
        if self.sys1 == False:
            bar_size = self.long_in_date

        barReader = BarReader(self)
        # 获取市场最新数据
        market_data = barReader.read_bar(size=bar_size)
        # 获取市场最新价格
        price = barReader.read_current_price()
        # 获取ATR
        atr = barReader.calc_data_atr()


