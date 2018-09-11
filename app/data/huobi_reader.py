from app.web import HuobiServices
from app.data.data_reader_base import DataReaderBase
from app.data.base_bar import BaseBar
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
