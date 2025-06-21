import requests
from icecream import ic
from datetime import datetime

def get_ticker(markets : str = "KRW-BTC"):
    url = f"https://api.bithumb.com/v1/ticker?markets={markets}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    json = response.json()[0]
    ic(json['market'])
    ic(json['trade_date_kst'])
    ic(json['trade_time_kst'])
    ic(json['trade_timestamp'])
    ic(json['trade_price'])
    ic(json['timestamp'])

    trade_dt = datetime.fromtimestamp(int(json['timestamp']) / 1000)
    ic(trade_dt)

    kst_str = f"{json['trade_date_kst']} {json['trade_time_kst']}"
    kst_dt = datetime.strptime(kst_str, "%Y%m%d %H%M%S")
    ic(kst_dt)

if __name__ == "__main__":
    get_ticker()

# {
#     'acc_trade_price': 37013337349.27563,
#     'acc_trade_price_24h': 75979337540.7154,
#     'acc_trade_volume': 257.06558063,
#     'acc_trade_volume_24h': 524.69221463,
#     'change': 'FALL',
#     'change_price': 297000,
#     'change_rate': 0.0021,
#     'high_price': 145116000,
#     'highest_52_week_date': '2025-01-21',
#     'highest_52_week_price': 163460000,
#     'low_price': 143024000,
#     'lowest_52_week_date': '2024-08-06',
#     'lowest_52_week_price': 71573000,
#     'market': 'KRW-BTC',
#     'opening_price': 144254000,
#     'prev_closing_price': 144247000,
#     'signed_change_price': -297000,
#     'signed_change_rate': -0.0021,
#     'timestamp': 1750480141644,
#     'trade_date': '20250621',
#     'trade_date_kst': '20250621',
#     'trade_price': 143950000,
#     'trade_time': '042855',
#     'trade_time_kst': '132855',
#     'trade_timestamp': 1750512535651,
#     'trade_volume': 0.00054356
# }
