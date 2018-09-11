from app.web.Keys import *
import tushare

tushare.set_token(TRADE_URL)
print(tushare.__version__)
