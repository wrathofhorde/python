import duration
import handledic
import handlecsv
import closingprice
from icecream import ic
from prettytable import PrettyTable
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

# ic.disable()
class calc:
	def __init__(self):
		self.btc = []
		self.eth = []
		self.xrp = []
		self.days = []
		self.xticks = []
		self.avg_btc = None
		self.avg_eth = None
		self.avg_xrp = None
		self.field_names = None

	def closingprice(self):
		pass

	def get_closingprice(self):
		days = duration.days()
		prices = handledic.read()
		today = days.today
		startday = days.startday
		endday = days.endday
		diff = today - startday

		self.startday = startday
		self.endday = endday

		for offset in range(diff.days):
			day = days.tostring(startday + timedelta(days=offset))
			value = prices.get(day)

			if value is None or len(value) != 3:
				list = closingprice.get(day)
				prices[day] = list
				print(f"{day}: {list}")
			else:
				print(f"{day}: {prices[day]}")

		self.prices = prices
		handledic.write(prices)

		csvlist = []
		btc = eth = xrp = 0
		diff = endday - startday
		sum_of_days = diff.days + 1

		for offset in range(sum_of_days):
			day = days.tostring(startday + timedelta(days=offset))
			value = prices.get(day)
			btc += value[0]
			eth += value[1]
			xrp += value[2]
			value.insert(0, day)
			csvlist.append(value)

			self.days.append(datetime.strptime(value[0], "%Y-%m-%d"))
			self.btc.append(value[1])
			self.eth.append(value[2])
			self.xrp.append(value[3])

		btc /= sum_of_days
		eth /= sum_of_days
		xrp /= sum_of_days
		btc = format(int(round(btc, 0)), ",d")
		eth = format(int(round(eth, 0)), ",d")
		xrp = format(int(round(xrp, 0)), ",d")

		csvlist.append(["average", btc, eth, xrp])

		str_startday = days.tostring(startday)
		str_endday = days.tostring(endday)

		handlecsv.write(csvlist, f"{str_startday}-{str_endday}.csv")

		str_type = "Type"
		str_from = "From"
		str_to = "To"
		str_days = "Days"
		str_price = "Price"

		self.field_names = [str_type, str_from, str_to, str_days, str_price]
		self.avg_btc = ["BTC", str_startday, str_endday, sum_of_days, btc]
		self.avg_eth = ["ETH", str_startday, str_endday, sum_of_days, eth]
		self.avg_xrp = ["XRP", str_startday, str_endday, sum_of_days, xrp]

		table = PrettyTable()
		table.field_names = self.field_names
		table.add_rows([self.avg_btc, self.avg_eth, self.avg_xrp])
		table.align[str_price] = "r"

		print()
		print(table)
		print()
		# input("Press any key to close....")

	def get_xticks(self, durations):
		ticks = []
		for months in range(0, 13, durations):
			ticks.append(self.startday + relativedelta(months=months))
		
		return ticks

if __name__ == "__main__":
	c = calc()
	c.get_closingprice()
	ic(c.get_xticks(3))