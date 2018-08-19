import unittest
from app.strategy.sea_turtle import SeaTurtle


class TestSeaTurtle(unittest.TestCase):

    def test_init(self):
        sea1 = SeaTurtle('eos','btc')
        self.assertGreater(sea1.amount_precision, 0)
        self.assertGreater(sea1.price_precision, 0)
        self.assertGreater(sea1.init_base_amount, 0)
        self.assertGreater(sea1.init_quote_amount, 0)



if __name__ == "__main__":
    unittest.main()