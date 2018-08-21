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

    def test_init(self):
        self.assertGreater(self.seal.amount_precision, 0)
        self.assertGreater(self.seal.price_precision, 0)
        self.assertGreater(self.seal.init_base_amount, 0)
        self.assertGreater(self.seal.init_quote_amount, 0)

    def test_getMarketData(self):
        self.seal.init_system(period=Period.DAY_1.value)
        reader = BarReader()
        reader.read_bar(strage=self.seal, size=21)
        self.assertIsNotNone(self.seal.market_data)
        print(self.seal.market_data)

if __name__ == "__main__":
    unittest.main()