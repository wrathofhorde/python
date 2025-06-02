import handlecsv
import closingprice
from typing import Any
from icecream import ic
from duration import Days
from db import CoinPriceDb
from prettytable import PrettyTable
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

def add_comma(number):
	return format(int(round(number, 0)), ",d")

class Calc:
	def __init__(self, sqlite: CoinPriceDb):
		self.btc = []
		self.eth = []
		self.xrp = []
		self.date = []
		self.xticks = []
		self.sqlite = sqlite
		self.field_names = None


	def closingprice(self):
		days = Days(self.sqlite)
		self.days = days
		
		recent_start_day: datetime = days.recent_start_day
		recent_end_day: datetime = days.recent_end_day		
		oneday: timedelta = timedelta(days=1)
		recent_prices:list[Any] = []

		while recent_start_day <= recent_end_day:
			day: str = days.tostring(recent_start_day)
			[btc, eth, xrp] = closingprice.get(day)
			recent_prices.append(
				[day, int(round(btc)), int(round(eth)), int(round(xrp))]
			) 
			recent_start_day += oneday

		self.sqlite.insert_major_coin_prices(recent_prices)

		str_startday = days.tostring(days.startday)
		str_endday = days.tostring(days.endday)

		(
            min_btc, max_btc, avg_btc,
            min_eth, max_eth, avg_eth,
            min_xrp, max_xrp, avg_xrp,
            ) = self.sqlite.select_major_coins_min_max_avg(str_startday, str_endday)
		
		csvlist = self.sqlite.select_major_coins_prices(str_startday, str_endday)

		csvlist.append(
			["average", add_comma(avg_btc), add_comma(avg_eth), add_comma(avg_xrp)]
		)
		csvlist.append(
			["lowest", add_comma(min_btc), add_comma(min_eth), add_comma(min_xrp)]
		)
		csvlist.append(
			["highest", add_comma(max_btc), add_comma(max_eth), add_comma(max_xrp)]
		)

		str_type = "종류"
		str_from = "시작일"
		str_to = "종료일"
		str_days = "일수"
		str_avg = "평균가격"
		str_min = "최저가"
		str_max = "최고가"

		handlecsv.write(csvlist, f"{str_startday}-{str_endday}.csv")
		sum_of_days = (days.endday - days.startday).days + 1

		field_names = [
			str_type, 
			str_from, str_to, str_days, 
			str_avg, str_min, str_max
		]
		row_btc = [
			"BTC", 
			str_startday, str_endday, sum_of_days, 
			add_comma(avg_btc), add_comma(min_btc), add_comma(max_btc)
		]
		row_eth = [
			"ETH", 
			str_startday, str_endday, sum_of_days, 
			add_comma(avg_eth), add_comma(min_eth), add_comma(max_eth)
		]
		row_xrp = [
			"XRP", 
			str_startday, str_endday, sum_of_days, 
			add_comma(avg_xrp), add_comma(min_xrp), add_comma(max_xrp)
		]

		firstday = self.days.tostring(self.days.endday + oneday)
		lastday = self.days.tostring(self.days.yesterday)
		recent = self.sqlite.select_major_coins_prices(firstday, lastday)

		table = PrettyTable()
		table.field_names = field_names
		table.add_rows([row_btc, row_eth, row_xrp])
		table.align[str_avg] = "r"
		table.align[str_min] = "r"
		table.align[str_max] = "r"

		print()
		print(table)
		print()

		(self.date, self.btc, self.eth, self.xrp) = self.sqlite.select_major_coins_data(str_startday, str_endday)

	def get_xticks(self, durations):
		ticks = []
		for months in range(0, 13, durations):
			ticks.append(self.days.startday + relativedelta(months=months))
		
		return ticks

if __name__ == "__main__":
	ic.enable()
	s = CoinPriceDb("prices.db")
	c = Calc(s)
	c.closingprice()
	ic(c.get_xticks(3))