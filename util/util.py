# import pytz import timezone
# def current_est_date():
#     utc = timezone('UTC')
#     now = utc.localize(datetime.utcnow())
#     la = timezone('America/New_York')
#     local_est_time = now.astimezone(la)
#     return local_est_time.date()
from datetime import date
def today_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")
