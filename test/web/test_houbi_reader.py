import arrow
import unittest
from app.data.huobi_reader import HuobiReader as hbReader

class testHoubiReader(unittest.TestCase):
    def testArrow(self):
        date = arrow.get('2018-09-12 00:00:00')
        print(date)
        print(date.format('YYYYMMDD'))
    
    def testLoad(self):
        reader = hbReader(ticker='eosbtc', fromdate='2018-08-01', todate='2018-09-01')
        feeds = reader.get_bar()
        feeds.next()
        print(feeds.current_ohlc)



