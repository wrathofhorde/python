import handledic
from db import Sqlite
from icecream import ic


def main():
  sqlite = Sqlite("prices.db")
  sqlite.execute('''
      CREATE TABLE IF NOT EXISTS major_coins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        btc INTEGER,
        eth INTEGER,
        xrp INTEGER
      );
  ''')

  prices = handledic.read()

  params = []
  for date, coins in prices.items():
     t = (date, int(coins[0]), int(coins[1]), int(coins[2]))
     params.append(t)

  ic(params)

  insert_cursor = sqlite.excutemany(
      "INSERT INTO major_coins (date, btc, eth, xrp) VALUES (?, ?, ?, ?);",
      params
  )

  rows = sqlite.execute("SELECT date, btc, eth, xrp FROM major_coins;").fetchall()
  count = sqlite.count("major_coins")

  ic(insert_cursor.lastrowid)
  ic(len(prices))
  ic(count)

  sqlite.close()

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


if __name__ == "__main__":
    main()
