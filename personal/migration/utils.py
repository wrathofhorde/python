from datetime import datetime

dbname: str = "market.sq3"
dateformat: str = "%Y-%m-%d"

def add_comma(number):
	return format(int(round(number, 0)), ",d")

def datetostr(date: datetime, format: str = dateformat, /) -> str:
    return date.strftime(format)

def strtodate(date: str, format: str = dateformat, /) -> str:
    return datetime.strptime(date, format)

