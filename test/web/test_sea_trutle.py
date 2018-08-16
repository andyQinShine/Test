import unittest
from app.strategy.sea_turtle import SeaTurtle


class TestSeaTurtle(unittest.TestCase):

    def test_init(self):
        sea1 = SeaTurtle('btc', 'eos')
        sea1.initialize()
        print(sea1.env.amount_precision)
        print(sea1.env.price_precision)



if __name__ == "__main__":
    unittest.main()