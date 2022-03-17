from datetime import date

SOURCE_BUCKET = 'praveen-demo-bucket1'

def today_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")
