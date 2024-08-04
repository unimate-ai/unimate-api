import pytz
from datetime import datetime

def get_datetime_now_melb():
    TIMEZONE_MELB = pytz.timezone(zone='Australia/Melbourne')
    return datetime.now(tz=TIMEZONE_MELB)