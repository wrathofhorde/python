import pandas as pd
import tkinter as tk
from calculation import calc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_chart(root, label, days, prices, xticks, xtick_labels, color):
    fig = plt.Figure(figsize=(5, 4), linewidth=1)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.LEFT)

    ax.grid(True)
    ax.plot(days, prices, label=label, color=color, linewidth=1)
    ax.set_title(label)
    ax.set_xticks(ticks=xticks, labels=xtick_labels)


prices = calc()
prices.get_closingprice()

for idx in range(len(prices.btc)):
    prices.btc[idx] =int(prices.btc[idx])
    prices.eth[idx] =int(prices.eth[idx])
    prices.xrp[idx] =int(prices.xrp[idx])

root = tk.Tk()
root.title("일년 평균")
root.geometry("1600x600")

xticks = prices.get_xticks(3)
xtick_labels = []
for tick in xticks:
    xtick_labels.append(tick.strftime("%Y-%m"))

draw_chart(root=root, 
           label="BTC", 
           days=prices.days, 
           prices=prices.btc, 
           xticks=xticks, 
           xtick_labels=xtick_labels, 
           color="blue")
draw_chart(root=root, 
           label="ETH", 
           days=prices.days, 
           prices=prices.eth, 
           xticks=xticks, 
           xtick_labels=xtick_labels, 
           color="red")
draw_chart(root=root, 
           label="XRP", 
           days=prices.days, 
           prices=prices.xrp, 
           xticks=xticks, 
           xtick_labels=xtick_labels, 
           color="green")

root.mainloop()