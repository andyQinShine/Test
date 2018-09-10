from app.web import HuobiServices
from app.data.data_reader_base import DataReaderBase

class HuobiReader(DataReaderBase):
    def __init__(self, ticker, fromdate=None, todate=None):
        super().__init__(ticker, fromdate, todate)

    def load(self, fromdate=None, todate=None):
        if fromdate is None:
            fromdate = self.fromdate
        if todate is None:
            todate = self.todate
