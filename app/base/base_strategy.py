from app.base.envBase import EnvBase
from app.web import HuobiServices as huobi
from itertools import count

class StrategyBase(EnvBase):
    strategy_counter = count(1)
    def __init__(self, base, quote):
        self.name = f'{self.__class__.__name__}_{next(self.strategy_counter)}'
        self.env.strategies.update(self.name, self)
        self.base = base
        self.quote = quote
        self.symbol = base + ''+ quote

        # 初始化交币种精度
        self.init_coin()
        # 初始化账户币种数量
        self.init_account_amount()

    def init_coin(self):
        precision_data = huobi.get_symbol_precision(self.base, self.quote)
        # 价格精度
        self.price_precision = int(precision_data['price-precision'])
        # 数量精度
        self.amount_precision = int(precision_data['amount-precision'])

    def init_account_amount(self):
        # 获取账户base amount
        self.init_base_amount = float(huobi.get_symbol_balance(self.base))
        # 获取账户 quote amount
        self.init_quote_amount = float(huobi.get_symbol_balance(self.quote))