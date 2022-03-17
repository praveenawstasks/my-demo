from util.util import today_date
import unittest
from datetime import date

class UtilTest(unittest.TestCase):
    def test_today_date(self):
        today = date.today()
        test_date = today.strftime("%Y-%m-%d")
        assert test_date == today_date()
        
if __name__ == '__main__':
    unittest.main()