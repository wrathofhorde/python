import time
import requests

from typing import Any
from icecream import ic
from datetime import datetime

ic.disable()

def get(day: datetime) -> list[Any]:
	date = day + "T15:00:00"
	trade_prices = []
	markets = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
	headers = {"accept": "application/json"}
	url = "https://api.upbit.com/v1/candles/minutes/1?market=%s&to=%s"

	for market in markets:
		time.sleep(0.5)
		ic(url % (market, date))
		res = requests.get(url % (market, date), headers=headers)

		if res.status_code == 200:
			data = (res.json())[0]
			ic(data)
			trade_prices.append(data['trade_price'])
		else:
			ic(res)
			return []

	return trade_prices

if __name__ == "__main__":
	print(get("2024-08-14"))
