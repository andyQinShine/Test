from app.web import HuobiServices
from app.data.data_reader_base import DataReaderBase
from app.data.base_bar import BaseBar
from app.web.tushare_service import TushareService

import arrow

class HuobiReader(DataReaderBase):
    def __init__(self, ticker, fromdate=None, todate=None):
        super().__init__(ticker, fromdate, todate)

    def get_bar(self):
        return BaseBar(self)

    def load(self, fromdate=None, todate=None):
        if fromdate is None:
            fromdate = self.fromdate
        if todate is None:
            todate = self.todate

        ts = TushareService()
        df = ts.getCoinbar(symbol=self.ticker, start_date=fromdate, end_date=todate)
        final_data = []

        for i in range(0, len(df)):
            ohlc = df.iloc[i]
            print(ohlc['date'])
            print(ohlc['open'])
            # if todate:
                # if arrow.get(ohlc['date']) >= arrow.get(todate):
                #     break

            if arrow.get(ohlc['date']) >= arrow.get(fromdate):
                ohlc['open'] = float(ohlc['open'])
                ohlc['high'] = float(ohlc['high'])
                ohlc['low'] = float(ohlc['low'])
                ohlc['close'] = float(ohlc['close'])
                ohlc['volume'] = float(ohlc['vol'])

                final_data.append(ohlc)
        final_generator = (i for i in final_data)
        del final_data

        return final_generator