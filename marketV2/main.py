import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import ttk
from db import CoinPriceDb;
from calculation import Calc
from datetime import datetime
from utils import datetostr, dbname, get_xticks
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_chart(root, startday: datetime, endday: datetime, sqlite: CoinPriceDb):
	(date, btc, eth, xrp) = sqlite.select_major_coins_data(startday, endday)
	xticks = get_xticks(startday)
	xtick_labels = []
	
	for tick in xticks:
		xtick_labels.append(datetostr(tick, "%Y-%m"))

	fig = plt.Figure(figsize=(15, 4), linewidth=1)
	ax = fig.add_subplot(131)
	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.get_tk_widget().pack(side=tk.TOP)

	ax.grid(True)
	ax.plot(date, btc, label="BTC", color="blue", linewidth=1)
	ax.set_title("BTC")
	ax.set_xticks(ticks=xticks, labels=xtick_labels)

	ax = fig.add_subplot(132)
	canvas = FigureCanvasTkAgg(fig, master=root)
	ax.grid(True)
	ax.plot(date, eth, label="ETH", color="green", linewidth=1)
	ax.set_title("ETH")
	ax.set_xticks(ticks=xticks, labels=xtick_labels)

	ax = fig.add_subplot(133)
	canvas = FigureCanvasTkAgg(fig, master=root)
	ax.grid(True)
	ax.plot(date, xrp, label="XRP", color="magenta", linewidth=1)
	ax.set_title("XRP")
	ax.set_xticks(ticks=xticks, labels=xtick_labels)


def draw_table(root, startday: datetime, endday: datetime, fieldnames: list[str]):
	column_title = fieldnames
	column_width = [100, 100, 100, 100, 200]
	column_anchor = ["center", "center", "center", "center", "e"]

	tree = ttk.Treeview(root, columns=column_title, show="headings", height=10)
	for idx in range(len(column_title)):
		tree.heading(column_title[idx], text=column_title[idx])
		tree.column(
			column_title[idx], width=column_width[idx], anchor=column_anchor[idx]
		)

	(
		min_btc, max_btc, avg_btc,
		min_eth, max_eth, avg_eth,
		min_xrp, max_xrp, avg_xrp,
		) = sqlite.select_major_coins_min_max_avg(startday, endday)
		

	data = [avg_btc, avg_eth, avg_xrp]
	for item in data:
		tree.insert("", "end", values=item)

	tree.pack(side="left")



sqlite = CoinPriceDb(db_name=dbname)
sqlite.create_tables_if_not_exists()

root = tk.Tk()
root.title("주요 자산 일년 가격 차트")
root.geometry("1400x400")
root.resizable(False, False)

calc = Calc(sqlite)
calc.closingprice()

draw_chart(root, calc.startday, calc.endday, sqlite)
# draw_table(root, calc.fieldnames)
sqlite.close()

root.mainloop()
