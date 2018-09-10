from app.base.envBase import EnvBase

class DataReaderBase(EnvBase):
    def __init__(self, ticker, fromdate=None, todate=None):
        self.ticker = ticker
        self.fromdate = fromdate
        self.todate = todate

        self.env.readers[self.ticker] = self
        self.env.fromdate = fromdate
        self.env.todate = todate

    def load(self, fromdate=None, todate=None):
        raise NotImplementedError

    def get_bar(self):
        raise NotImplementedError
