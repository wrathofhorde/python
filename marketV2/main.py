import tkinter as tk
from tkinter import ttk
from db import CoinPriceDb;
from calculation import calc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_chart(root, prices):
	for idx in range(len(prices.btc)):
		prices.btc[idx] = int(prices.btc[idx])
		prices.eth[idx] = int(prices.eth[idx])
		prices.xrp[idx] = int(prices.xrp[idx])

	xticks = prices.get_xticks(3)
	xtick_labels = []
	for tick in xticks:
		xtick_labels.append(tick.strftime("%Y-%m"))

	fig = plt.Figure(figsize=(15, 4), linewidth=1)
	ax = fig.add_subplot(131)
	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.get_tk_widget().pack(side=tk.TOP)

	ax.grid(True)
	ax.plot(prices.days, prices.btc, label="BTC", color="blue", linewidth=1)
	ax.set_title("BTC")
	ax.set_xticks(ticks=xticks, labels=xtick_labels)

	ax = fig.add_subplot(132)
	canvas = FigureCanvasTkAgg(fig, master=root)
	ax.grid(True)
	ax.plot(prices.days, prices.eth, label="ETH", color="green", linewidth=1)
	ax.set_title("ETH")
	ax.set_xticks(ticks=xticks, labels=xtick_labels)

	ax = fig.add_subplot(133)
	canvas = FigureCanvasTkAgg(fig, master=root)
	ax.grid(True)
	ax.plot(prices.days, prices.xrp, label="XRP", color="magenta", linewidth=1)
	ax.set_title("XRP")
	ax.set_xticks(ticks=xticks, labels=xtick_labels)


def draw_table(root, prices):
	column_title = prices.field_names
	column_width = [100, 100, 100, 100, 200]
	column_anchor = ["center", "center", "center", "center", "e"]

	tree = ttk.Treeview(root, columns=column_title, show="headings", height=10)
	for idx in range(len(column_title)):
		tree.heading(column_title[idx], text=column_title[idx])
		tree.column(
			column_title[idx], width=column_width[idx], anchor=column_anchor[idx]
		)

	data = [prices.avg_btc, prices.avg_eth, prices.avg_xrp]
	for item in data:
		tree.insert("", "end", values=item)

	tree.pack(side="left")



sqlite = CoinPriceDb("prices.db")
# 테이블이 이미 있으면, 테이블을 새로 생성하지 않음
sqlite.create_major_coins_table()

root = tk.Tk()
root.title("주요 자산 일년 가격 차트")
root.geometry("1400x400")
root.resizable(False, False)

prices = calc()
prices.get_closingprice()

draw_chart(root, prices)
# draw_table(root, prices)

root.mainloop()
