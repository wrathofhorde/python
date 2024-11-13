import requests
from icecream import ic

COUNTRY_CODE = "countryCode"

url = "http://ip-api.com/json/"
ip = "222.108.230.146"

res = requests.get(url + ip)

if res.status_code == 200:
    data = res.json()
    ic(data)
    if data[COUNTRY_CODE].lower() == "kr":
        print("한국")
    else:
        print("다른 나라")
else:
    print(f"{ip} request failure")
