from datetime import datetime

from matplotlib.dates import relativedelta

dbname: str = "market.sq3"
dateformat: str = "%Y-%m-%d"

def add_comma(number):
	return format(int(round(number, 0)), ",d")

def datetostr(date: datetime, format: str = dateformat, /) -> str:
    return date.strftime(format)

def strtodate(date: str, format: str = dateformat, /) -> str:
    return datetime.strptime(date, format)

def get_xticks(startday:datetime, duration: int = 12, tickunit: int = 3, /):
	ticks = []
    # 1년 기준으로 12개월 후 포함을 위해 duration + 1
	for months in range(0, duration + 1, tickunit):
		ticks.append(startday + relativedelta(months=months))
	
	return ticks