import requests
from icecream import ic

def get_orderbook():
    url = "https://api.bithumb.com/v1/orderbook?markets=KRW-BTC"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    json = response.json()
    ic(json)

if __name__ == "__main__":
    get_orderbook()
