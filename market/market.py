import duration
import handledic
import handlecsv
import closingprice
from datetime import timedelta
from prettytable import PrettyTable

days = duration.days()
prices = handledic.read()
today = days.today
firstday = days.firstday
startday = days.startday
endday = days.endday
diff = today - startday

for offset in range(diff.days):
    day = days.tostring(startday + timedelta(days=offset))
    value = prices.get(day)

    if value is None or len(value) != 3:
        list = closingprice.get(day)
        prices[day] = list
        print(f"{day}: {list}")
    else:
        print(f"{day} skipped")

handledic.write(prices)

csvlist = []
btc = eth = xrp = 0
diff = endday - startday
sum_of_days = diff.days + 1

for offset in range(sum_of_days):
    day = days.tostring(startday + timedelta(days=offset))
    value = prices.get(day)
    btc += value[0]
    eth += value[1]
    xrp += value[2]
    value.insert(0, day)
    csvlist.append(value)

btc /= sum_of_days
eth /= sum_of_days
xrp /= sum_of_days
btc = format(int(round(btc, 0)), ",d")
eth = format(int(round(eth, 0)), ",d")
xrp = format(int(round(xrp, 0)), ",d")

csvlist.append(["average", btc, eth, xrp])

str_startday = days.tostring(startday)
str_endday = days.tostring(endday)

handlecsv.write(csvlist, f"{str_startday}-{str_endday}.csv")


str_type = "Type"
str_from = "From"
str_to = "To"
str_days = "Days"
str_price = "Price"

table = PrettyTable()
table.field_names = [str_type, str_from, str_to, str_days, str_price]
table.add_rows([
    ["BTC", str_startday, str_endday, sum_of_days, btc],
    ["ETH", str_startday, str_endday, sum_of_days, eth],
    ["XRP", str_startday, str_endday, sum_of_days, xrp]
    ])

table.align[str_price] = "r"

print()
print(table)
print()
input("Press any key to close....")