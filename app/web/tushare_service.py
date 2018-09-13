from app.web.Keys import *
import tushare
import arrow

class TushareService:
    def __init__(self):
        tushare.set_token(TUSHARE_TOKEN)

    def getPro(self):
        return tushare.pro_api()

    def formate_date(self, str_date):
        date = arrow.get(str_date)
        return date.format('YYYYMMDD')

    def getCoinbar(self, exchange='huobi',symbol=None, freq='daily', start_date=None, end_date=None):
        pro = self.getPro()
        start_date = self.formate_date(start_date)
        end_date = self.formate_date(end_date)
        df = pro.query('coinbar', exchange=exchange, symbol=symbol, freq=freq, start_date=start_date, end_date=end_date)
        return df


date1 = '2018-08-01'
tushareService = TushareService()
print(tushareService.formate_date(date1))

df = tushareService.getCoinbar(symbol='btcusdt', start_date='2018-08-01',end_date='2018-09-01')
print(df)
print(len(df))
