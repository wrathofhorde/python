import time
import closingprice

from icecream import ic
from db import CoinPriceDb
from utils import datetostr, strtodate
from datetime import datetime, timedelta

def gethistory()->None:
    sqlite = CoinPriceDb("history.sq3")
    sqlite.create_major_coins_table()

    lastupdate = sqlite.select_last_update_major_coins()
    ic(lastupdate)
    lastupdate = lastupdate if lastupdate else "2020-12-31"

    oneday: timedelta = timedelta(days=1)
    startday: datetime = strtodate(lastupdate) + oneday
    today = datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    count = 0
    prices = []

    while startday < today:
        day: str = datetostr(startday)
        [btc, eth, xrp] = closingprice.get(day=day)
        btc = int(btc)
        eth = int(eth)
        xrp = int(xrp)
        price = [day, btc, eth, xrp]
        prices.append(price)
        count += 1
        startday += oneday
        print(f'{day} done')
        time.sleep(1)

    sqlite.insert_major_coin_prices(prices)

    sqlite.close()

if __name__ == "__main__":
    ic.enable()
    gethistory()