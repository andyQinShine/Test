from app.base.envBase import EnvBase
from app.web import HuobiServices as huobi

class StrategyBase(EnvBase):
    def __init__(self, base, quote):
        self.env.base = base
        self.env.quote = quote
        self.symbol = base + ''+ quote



    def initialize(self):
        self.init_coin()

    def init_coin(self):
        precision_data = huobi.get_symbol_precision(self.env.base, self.env.quote)
        print(precision_data)
        self.env.price_precision = precision_data['price-precision']
        self.env.amount_precision = precision_data['amount-precision']

