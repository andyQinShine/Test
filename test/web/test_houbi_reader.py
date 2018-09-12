import arrow
import unittest

class testHoubiReader(unittest.TestCase):
    def testArrow(self):
        date = arrow.get('2018-09-12 00:00:00')
        print(date)
        print(date.format('YYYYMMDD'))


