import time
import requests
from icecream import ic

ic.disable()

def get(day):
  date = day + "T15:00:00"
  trade_prices = []
  markets = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
  headers = {"accept": "application/json"}
  url = "https://api.upbit.com/v1/candles/minutes/1?market=%s&to=%s"

  for market in markets:
    time.sleep(1)
    ic(url % (market, date))
    res = requests.get(url % (market, date), headers=headers)

    if res.status_code == 200:
      data = (res.json())[0]
      ic(data)
      trade_prices.append(data['trade_price'])
    else:
      ic(res)

  return trade_prices

if __name__ == "__main__":
    print(get("2024-08-14"))
