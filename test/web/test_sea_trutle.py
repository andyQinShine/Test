import unittest
from app.strategy.sea_turtle import SeaTurtle
from app.base.constants import COIN
from app.base.constants import Period
from app.base.bar_reader import BarReader


class TestSeaTurtle(unittest.TestCase):

    seal = None

    @classmethod
    def setUp(self):
        self.seal = SeaTurtle(COIN.EOS.value,COIN.BTC.value)
        self.seal.init_system(period=Period.DAY_1.value)

    def test_init(self):
        self.assertGreater(self.seal.amount_precision, 0)
        self.assertGreater(self.seal.price_precision, 0)
        self.assertGreater(self.seal.init_base_amount, 0)
        self.assertGreater(self.seal.init_quote_amount, 0)

    def test_getMarketData(self):
        reader = BarReader(self.seal)
        reader.read_bar(size=21)
        self.assertIsNotNone(self.seal.market_data)
        print(self.seal.market_data)

    def test_getCurrent_price(self):
        reader = BarReader(self.seal)
        price = reader.read_current_price()
        print(price)
        print(self.seal.price)
        self.assertIsNotNone(price)

    def test_get_atr(self):
        reader = BarReader(self.seal)
        reader.read_bar(size=40)
        atr = reader.calc_data_atr()
        print(self.seal.ATR)
        self.assertIsNotNone(self.seal.ATR)

if __name__ == "__main__":
    unittest.main()