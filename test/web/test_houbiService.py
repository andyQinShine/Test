import unittest
from app.web import HuobiServices as houbi

class TestHoubiService(unittest.TestCase):
    symbol = "eosbtc"
    period = "5min"

    def test_get_kinLine(self):
        data = houbi.get_kline(self.symbol,self.period)
        print(data)
        self.assertIsNotNone(data)
        self.assertEqual(data['status'], 'ok')

    def test_get_accounts(self):
        data = houbi.get_accounts()
        print(data)
        self.assertIsNotNone(data)




if __name__ == "__main__":
    unittest.main()