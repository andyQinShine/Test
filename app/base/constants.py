from enum import Enum

class COIN(Enum):
    BTC = 'btc'
    EOS = 'eos'
    USDT = 'usdt'

class Period(Enum):
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    MIN_60 = "60min"
    DAY_1 = "1day"
    MONTH_1 = "1mon"
    WEEK_1 = "1week"
    YEAR_1 = "1year"