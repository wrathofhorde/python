import sys
import json
import keys
from icecream import ic
from operator import itemgetter
import matplotlib.pyplot as plot

PRECISION = 2

def printUsageAndExit():
  print('Usage: python3 balance.py deposit_amount json_file')
  print('Example: python3 balance.py 100000 owns.json')
  exit(0)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    printUsageAndExit()

try:
  deposit = int(sys.argv[1])
except:
  printUsageAndExit()

json_file = sys.argv[2]

print("*******************************************")
print(f"입금금액: {format(deposit, ',')}, json file: {json_file}")

with open(json_file) as s:
  stocks = json.load(s)

sum = 0
total_ratio = 0

for s in stocks:
  total_ratio += s[keys.RATIO]

for s in stocks:
  s[keys.TOTAL_PRICE] = s[keys.UNIT_PRICE] * s[keys.QUANTITY]
  s[keys.TARGET_RATIO] = s[keys.RATIO] / total_ratio
  sum += s[keys.TOTAL_PRICE]

sum += deposit

for s in stocks:
  s[keys.CURRENT_RATIO] = s[keys.TOTAL_PRICE] / sum
  s[keys.PERCENT_POINT] = s[keys.TARGET_RATIO] - s[keys.CURRENT_RATIO]

stocks = sorted(stocks, key = itemgetter(keys.PERCENT_POINT), reverse = True)

balance = deposit

for s in stocks:
  buy = 0
  unit_price = s[keys.UNIT_PRICE]
  total_price = s[keys.TOTAL_PRICE]
  target_ratio = s[keys.TARGET_RATIO]
  current_ratio = s[keys.CURRENT_RATIO]

  while current_ratio < target_ratio and balance > unit_price:
    buy += 1
    balance -= unit_price
    total_price += unit_price
    current_ratio = total_price / sum

  s[keys.BUY] = buy

for s in stocks:
  total_after_buy = s[keys.TOTAL_PRICE] + s[keys.UNIT_PRICE] * s[keys.BUY]
  s[keys.RATIO_AFTER_BUY] = round(total_after_buy / sum, PRECISION)
  s[keys.TARGET_RATIO] = round(s[keys.TARGET_RATIO] * 100, PRECISION)
  s[keys.CURRENT_RATIO] = round(s[keys.CURRENT_RATIO] * 100, PRECISION)
  s[keys.PERCENT_POINT] = round(s[keys.PERCENT_POINT] * 100, PRECISION)
  s[keys.RATIO_AFTER_BUY] = round(s[keys.RATIO_AFTER_BUY] * 100, PRECISION)
  j = json.dumps(s, indent = 2, ensure_ascii = False)
  print(j)

with open("out.json", 'w', encoding="utf-8") as w:
  json.dump(stocks, w, ensure_ascii = False, indent = 2)

print(f"잔액: {balance}")

ratio = []
labels = []

for s in stocks:
  ratio.append(s[keys.RATIO_AFTER_BUY])
  labels.append(f"{s[keys.NAME]} ({s[keys.BUY]})")

wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
plot.rc("font", size=16)
plot.pie(ratio, labels=labels, autopct="%.1f%%", wedgeprops=wedgeprops, startangle=90, counterclock=False)
plot.show()
