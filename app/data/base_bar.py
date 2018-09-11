from app.base.envBase import EnvBase
class BaseBar(EnvBase):

    def __init__(self, reader):
        self._iter_data = reader.load()
        self.current_ohlc = None
        self.next_ohlc = next(self._iter_data)
        self.ticker = reader.ticker
    def next(self):
        self.current_ohlc, self.next_ohlc = self.next_ohlc, next(self._iter_data)

    @property
    def cur_price(self):
        return self.close

    @property
    def date(self):
        return self.current_ohlc['date']

    @property
    def open(self):
        return self.current_ohlc['open']

    @property
    def high(self):
        return self.current_ohlc['high']

    @property
    def low(self):
        return self.current_ohlc['low']

    @property
    def close(self):
        return self.current_ohlc['close']

    @property
    def volume(self):
        return self.current_ohlc['volume']