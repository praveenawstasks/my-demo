
from datetime import date
def today_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")
