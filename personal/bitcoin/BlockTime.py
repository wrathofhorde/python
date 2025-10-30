import time
import requests
import numpy as np
import pandas as pd
from icecream import ic
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta


now_utc = datetime.now(timezone.utc).date()
today_utc_midnight = datetime(now_utc.year, now_utc.month, now_utc.day, tzinfo=timezone.utc)
time_in_milliseconds = int(today_utc_midnight.timestamp() * 1000)


url: str = f"https://blockchain.info/blocks/{time_in_milliseconds}?format=json"
resp = requests.get(url=url)
ic(resp)

header = []
block = resp.json()

for n in range(len(block)):
    bhash = block[n]['hash']
    btime = block[n]['time']
    bheight = block[n]["height"]
    header.append([bheight, btime, bhash])

ic(header)

df = pd.DataFrame(header, columns=["height", "time", "hash"])
sdf = df.sort_values("time")
sdf = sdf.reset_index()
print(f"총 {len(df)}개 블록 헤더를 읽어 왔습니다.")

mtime = sdf['time'].diff().values
mtime = mtime[np.logical_not(np.isnan(mtime))]
print(f"평균 Mining time = {np.mean(mtime)}")
print(f"표준편차 = {np.std(mtime)}")