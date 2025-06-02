import closingprice

from icecream import ic
from duration import Days
from db import CoinPriceDb
from utils import datetostr
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

ic.disable()
class calc:
    def __init__(self, sqlite: CoinPriceDb):
        self.field_names = None
        self.days = Days(sqlite)
        self.sqlite: CoinPriceDb = sqlite

    def get_closingprice(self):
        recent_start_day = self.days.recent_start_day
        recent_end_day = self.days.recent_end_day

        recent_prices = []
        oneday = timedelta(days = 1)

        while recent_start_day <= recent_end_day:
            day : str = datetostr(recent_start_day)
            [btc, eth, xrp] = closingprice.get(day)
            btc = int(btc)
            eth = int(eth)
            xrp = int(xrp)
            price = [day, btc, eth, xrp]
            recent_prices.append(price)
            recent_start_day += oneday

        ic(recent_prices)
        self.sqlite.insert_major_coin_prices(recent_prices)
        self.startday = self.days.oneyearago
        self.endday = self.days.yesterday

        # save in tuple
        (
            self.date, self.btc, self.eth, self.xrp
            ) = self.sqlite.select_major_coins_data(self.startday, self.endday)
        # save in tuple   
        (
            self.min_btc, self.max_btc, self.avg_btc,
            self.min_eth, self.max_eth, self.avg_eth,
            self.min_xrp, self.max_xrp, self.avg_xrp,
            ) = self.sqlite.select_major_coins_min_max_avg(self.startday, self.endday)


if __name__ == "__main__":
    ic.enable()
    s = CoinPriceDb("prices.db")
    s.create_major_coins_table()

    c = calc(s)
    c.get_closingprice()
    # print(c.get_xticks(1))