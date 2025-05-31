import handledic
from icecream import ic
from db import CoinPriceDb


def main():
  sqlite = CoinPriceDb("prices.db")
  sqlite.create_major_coins_table()

  prices = handledic.read()

  params = []
  for date, coins in prices.items():
     t = (date, int(coins[0]), int(coins[1]), int(coins[2]))
     params.append(t)

  ic(params)

  insert_cursor = sqlite.insert_major_coin_prices(params)

  rows = sqlite.fetchall("SELECT date, btc, eth, xrp FROM major_coins;")
  count = sqlite.count()

  ic(insert_cursor.lastrowid)
  ic(len(prices))
  ic(count)

  for row in rows:
     date = row["date"]
     coins = prices[date]
     [btc, eth, xrp] = coins
     if row['btc'] != int(btc):
        ic(f"{date} btc error")
     if row['eth'] != int(eth):
        ic(f"{date} eth error")
     if row['xrp'] != int(xrp):
        ic(f"{date} xrp error")

  ic("값 비교 완료")
  
  start_date = "2025-05-14"
  end_date = "2025-05-30"

  ic(sqlite.select_major_coins_prices(start_date, end_date))
  ic(sqlite.select_last_update_major_coins())
  ic(sqlite.select_prices_at("2025-04-21"))
  ic(sqlite.select_prices_at("2021-04-21"))
  

  sqlite.close()


if __name__ == "__main__":
    main()
