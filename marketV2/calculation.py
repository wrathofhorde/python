import handlecsv
import closingprice
from typing import Any
from icecream import ic
from duration import Days
from db import CoinPriceDb
from prettytable import PrettyTable
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from utils import dbname, add_comma, strtodate, datetostr

class Calc:
	def __init__(self, sqlite: CoinPriceDb):
		self.xticks = []
		self.sqlite = sqlite
		self.field_names = None

	@property
	def startday(self):
		return self.days.startday
	
	@property
	def endday(self):
		return self.days.endday

	def closingprice(self):
		days = Days(self.sqlite)
		self.days = days
		
		recent_start_day: datetime = days.recent_start_day
		recent_end_day: datetime = days.recent_end_day		
		oneday: timedelta = timedelta(days=1)
		recent_prices:list[Any] = []

		while recent_start_day <= recent_end_day:
			day: str = strtodate(recent_start_day)
			[btc, eth, xrp] = closingprice.get(day)
			recent_prices.append(
				[day, int(round(btc)), int(round(eth)), int(round(xrp))]
			) 
			recent_start_day += oneday

		self.sqlite.insert_major_coin_prices(recent_prices)

		str_startday = datetostr(days.startday)
		str_endday = datetostr(days.endday)

		(
            min_btc, max_btc, avg_btc,
            min_eth, max_eth, avg_eth,
            min_xrp, max_xrp, avg_xrp,
            ) = self.sqlite.select_major_coins_min_max_avg(str_startday, str_endday)
		
		csvlist = self.sqlite.select_major_coins_prices(str_startday, str_endday)

		for price in csvlist:
			price[1] = add_comma(price[1])
			price[2] = add_comma(price[2])
			price[3] = add_comma(price[3])

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
			str_min, str_max, str_avg, 
		]
		row_btc = [
			"BTC", 
			str_startday, str_endday, sum_of_days, 
			add_comma(min_btc), add_comma(max_btc), add_comma(avg_btc),
		]
		row_eth = [
			"ETH", 
			str_startday, str_endday, sum_of_days, 
			add_comma(min_eth), add_comma(max_eth), add_comma(avg_eth),
		]
		row_xrp = [
			"XRP", 
			str_startday, str_endday, sum_of_days, 
			add_comma(min_xrp), add_comma(max_xrp), add_comma(avg_xrp),
		]

		firstday = datetostr(self.days.endday + oneday)
		lastday = datetostr(self.days.yesterday)
		recent = self.sqlite.select_major_coins_prices(firstday, lastday)

		# csv 파일에 저장되지 않은 최근 값 화면 출력
		for price in recent:
			print(price)
		
		table = PrettyTable()
		table.field_names = field_names
		table.add_rows([row_btc, row_eth, row_xrp])
		table.align[str_avg] = "r"
		table.align[str_min] = "r"
		table.align[str_max] = "r"

		print()
		print(table)
		print()


if __name__ == "__main__":
	ic.enable()
	s = CoinPriceDb(db_name=dbname)
	c = Calc(s)
	c.closingprice()
	ic(c.get_xticks(3))