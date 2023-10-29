from datetime import timedelta, datetime
from random import randint


def random_date(days_back: int, days_forward: int) -> datetime:
    today = datetime.now()
    dt_min_month = (today - timedelta(days=days_back))
    dt_max_month = (today + timedelta(days=days_forward))
    random_month = randint(dt_min_month.month, dt_max_month.month)
    random_year = randint(1970, today.year)
    next_month = random_month+1 if random_month <= 12 else 1
    months_days = (datetime(random_year, next_month, day=1) - datetime(random_year, random_month, day=1)).days
    random_day = randint(1, months_days)

    return datetime(random_year, random_month, random_day)
#end