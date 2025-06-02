from icecream import ic
from db import CoinPriceDb
from utils import strtodate
from datetime import datetime, timedelta

class Days:
    def __init__(self, sqlite: CoinPriceDb):
        self.today = datetime.today()
        self.today = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
        self.yesterday = self.today - timedelta(days=1)
        self.oneyearago = self.yesterday - timedelta(days=365)
        self.last_update_date = self.get_last_update_day(sqlite)
    
    def get_last_update_day(self, sqlite: CoinPriceDb) -> datetime:
        self.last_update_date = strtodate(sqlite.select_last_update_major_coins())
        ic(self.last_update_date)

        oneday = timedelta(days = 1)
        self.recent_start_day = self.last_update_date + oneday
        self.recent_end_day = self.yesterday
        
        ic(self.recent_start_day)
        ic(self.recent_end_day)
        ic(self.last_update_date)
        ic(self.oneyearago)


if __name__ == "__main__":
    ic.enable()
    d = Days()
    ic(d.startday)
    ic(d.endday)
