from icecream import ic
from db import CoinPriceDb
from datetime import datetime, timedelta

from utils import datetostr, strtodate

dateformat: str = "%Y-%m-%d"

class Days:
	def __init__(self, sqlite: CoinPriceDb):
		self.today = datetime.today()
		self.today = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
		# 어제
		self.yesterday = self.today - timedelta(days=1)
		# 이달의 1일
		self.firstday = self.today.replace(day=1)
		# 직전달 마지막 날
		self.endday = self.firstday - timedelta(days=1)
		# 일년전 1일
		self.startday = datetime(
			self.firstday.year - 1, self.firstday.month, self.firstday.day
		)
		self.get_last_update_day(sqlite)

	def get_last_update_day(self, sqlite: CoinPriceDb) -> None:
		last_update_date = strtodate(sqlite.select_last_update_major_coins())
		oneday = timedelta(days = 1)
		self.recent_start_day = last_update_date + oneday
		self.recent_end_day = self.yesterday


if __name__ == "__main__":
	ic.enable()
	s = CoinPriceDb("prices.db")
	d = Days(s)

	ic(d.today)
	ic(d.last_update_date)
	ic(datetostr(d.yesterday))
	ic(datetostr(d.firstday))
	ic(d.startday)
	ic(d.endday)
