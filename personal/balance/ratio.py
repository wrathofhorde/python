import sys
import json
import keys
from operator import itemgetter
import matplotlib.pyplot as plot

PRECISION = 2

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 ratio.py json_file")
    exit(0)

jsonfile = sys.argv[1]

with open(jsonfile) as s:
  stocks = json.load(s)

total_balance = 0

for s in stocks:
  s[keys.TOTAL_PRICE] = s[keys.QUANTITY] * s[keys.UNIT_PRICE]
  total_balance += s[keys.TOTAL_PRICE]

stocks = sorted(stocks, key=itemgetter(keys.TOTAL_PRICE), reverse=True)

ratio = []
labels = []

for s in stocks:
  labels.append(s[keys.NAME])
  s[keys.RATIO] = round(100 * s[keys.TOTAL_PRICE] / total_balance, PRECISION)
  ratio.append(s[keys.RATIO])

with open("ratio_out.json", 'w', encoding="utf-8") as w:
  json.dump(stocks, w, ensure_ascii = False, indent = 2)
  
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
plot.rc("font", size=12)
plot.pie(ratio, labels=labels, autopct="%.1f%%", wedgeprops=wedgeprops, startangle=90, counterclock=False)
plot.show()
