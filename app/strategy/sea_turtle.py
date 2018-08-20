from app.base.base_strategy import StrategyBase

class SeaTurtle(StrategyBase):
    def __init__(self, base):
        super().__init__(base)

    def init_system(self, short_in_date=14, long_in_date=55, short_out_date=10, long_out_date=20, initial_cash=100000,
                    comm=1, comm_pct=None, margin_rate=0.1):
        # 系统1入市的trailing date
        self.short_in_date = short_in_date
        # 系统2入市的trailing date
        self.long_in_date = long_in_date
        # 系统1 exiting market trailing date
        self.short_out_date = short_out_date
        # 系统2 exiting market trailing date
        self.long_out_date = long_out_date