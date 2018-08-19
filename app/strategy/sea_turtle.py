from app.base.base_strategy import StrategyBase

class SeaTurtle(StrategyBase):
    def __init__(self, base, quote):
        super().__init__(base,quote)
