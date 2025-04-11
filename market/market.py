import pandas as pd
import tkinter as tk
import seaborn as sns
from calculation import calc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

prices = calc()
prices.get_closingprice()

for idx in range(len(prices.btc)):
    prices.btc[idx] =int(prices.btc[idx])
    prices.eth[idx] =int(prices.eth[idx])
    prices.xrp[idx] =int(prices.xrp[idx])

# root = tk.Tk()
# root.title("일년 평균")
# root.geometry("600x500")

plt.plot(prices.days, prices.btc, label='BTC', color='blue', linewidth=1)

xticks = [
    prices.days[0],
    prices.days[0] + relativedelta(month=3),
    prices.days[0] + relativedelta(month=6),
    prices.days[0] + relativedelta(month=9),
]

print(prices.days[0])
print(prices.days[0] + relativedelta(month=3))

ax = plt.gca()
ax.set_xticks(xticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))  # 연도-월 형식

# plt.title("Bitcoin", fontsize=14)
# plt.xlabel("X 축", fontsize=12)
# plt.ylabel("Y 축", fontsize=12)
# plt.grid(True)  # 격자선 추가

plt.show()
