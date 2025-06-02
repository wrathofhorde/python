from datetime import datetime

from matplotlib.dates import relativedelta

dateformat: str = "%Y-%m-%d"

def datetostr(date: datetime, format: str = dateformat, /) -> str:
    return date.strftime(format)

def strtodate(date: str, format: str = dateformat, /) -> str:
    return datetime.strptime(date, format)

def get_xticks(startday:datetime, durations: int, /):
	ticks = []
	for months in range(0, 13, durations):
		ticks.append(startday + relativedelta(months))
	
	return ticks