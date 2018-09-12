from app.web.Keys import *
import tushare
import  arrow

tushare.set_token(TUSHARE_TOKEN)
print(tushare.__version__)

def getPro():
    return tushare.pro_api()

def formate_date(str_date):
    date = arrow(str_date)
    return date.format('YYYYMMDD')

def getCoinbar(exchange='huobi',symbol=None, freq='daily', start_date=None, end_date=None):
    pro = getPro()
    start_date = formate_date(start_date)
    end_date = formate_date(start_date)
    df = pro.query('coinbar', exchange=exchange, symbol=symbol, freq=freq, start_date=start_date, end_date=end_date)
    return df

