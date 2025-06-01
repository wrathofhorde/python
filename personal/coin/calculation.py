import closingprice

from icecream import ic
from db import CoinPriceDb
from prettytable import PrettyTable
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

dateformat: str = "%Y-%m-%d"
class days:
    def __init__(self, sqlite: CoinPriceDb):
        self.today = datetime.today()
        self.today = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
        self.yesterday = self.today - timedelta(days=1)
        self.oneyearago = self.yesterday - timedelta(days=365)
        self.last_update_date = self.get_last_update_day(sqlite)

    def tostring(self, day:datetime) -> str:
        return day.strftime(dateformat)
    
    def get_last_update_day(self, sqlite: CoinPriceDb) -> datetime:
        self.last_update_date = datetime.strptime(
            sqlite.select_last_update_major_coins(), dateformat
            )
        ic(self.last_update_date)

        oneday = timedelta(days = 1)
        self.recent_start_day = self.last_update_date + oneday
        self.recent_end_day = self.yesterday
        ic.enable()
        ic(self.recent_start_day)
        ic(self.recent_end_day)
        ic(self.last_update_date)
        ic(self.oneyearago)

class calc:
    def __init__(self, sqlite: CoinPriceDb):
        self.btc = []
        self.eth = []
        self.xrp = []
        self.date = []
        self.xticks = []
        self.min_btc: int = 0
        self.max_btc: int = 0
        self.avg_btc: int = 0
        self.min_eth: int = 0
        self.max_eth: int = 0
        self.avg_eth: int = 0
        self.min_xrp: int = 0
        self.max_xrp: int = 0
        self.avg_xrp: int = 0
        self.sqlite: CoinPriceDb = sqlite
        self.field_names = None
        self.days = days(sqlite)

    def get_closingprice(self):
        recent_start_day = self.days.recent_start_day
        recent_end_day = self.days.recent_end_day

        recent_prices = []
        oneday = timedelta(days = 1)

        while recent_start_day <= recent_end_day:
            day : str = self.days.tostring(recent_start_day)
            [btc, eth, xrp] = closingprice.get(day)
            btc = int(btc)
            eth = int(eth)
            xrp = int(xrp)
            price = [day, btc, eth, xrp]
            recent_prices.append(price)
            recent_start_day += oneday

        ic(recent_prices)
        self.sqlite.insert_major_coin_prices(recent_prices)
        start_day = self.days.oneyearago
        end_day = self.days.yesterday

        # save in tuple
        (
            self.date, self.btc, self.eth, self.xrp
            ) = self.sqlite.select_major_coins_data(start_day, end_day)
        # save in tuple   
        (
            self.min_btc, self.max_btc, self.avg_btc,
            self.min_eth, self.max_eth, self.avg_eth,
            self.min_xrp, self.max_xrp, self.avg_xrp,
            ) = self.sqlite.select_major_coins_min_max_avg(start_day, end_day)

    def get_xticks(self, durations):
        ticks = []
        for months in range(0, 13, durations):
            ticks.append(self.startday + relativedelta(months=months))
        
        return ticks

if __name__ == "__main__":
    s = CoinPriceDb("prices.db")
    s.create_major_coins_table()

    c = calc(s)
    c.get_closingprice()
    # print(c.get_xticks(1))