import os
import csv
from icecream import ic

filename = "average_prices.csv"

def write(prices, name = None):
  name = filename if name is None else name

  with open(name, 'w') as file:
    writer = csv.writer(file)
    writer.writerows(prices)


def read(name = None):
  list = []
  name = filename if name is None else name

  if os.path.isfile(name):
    with open(name, "r") as file:
      data = csv.reader(file)
      for row in data:
        list.append(row)
    
  return list

if __name__ == "__main__":
  prices = [
    ['2024-08-06', 83273000.0, 3716000.0, 802.6],
    ['2024-08-07', 83273000.0, 3716000.0, 802.6],
    ['2024-08-08', 83273000.0, 3716000.0, 802.6],
    ['2024-08-09', 83273000.0, 3716000.0, 802.6],
    ['2024-08-10', 83273000.0, 3716000.0, 802.6],
    ['2024-08-11', 83273000.0, 3716000.0, 802.6],
    ['2024-08-12', 83273000.0, 3716000.0, 802.6],
    ['2024-08-13', 83273000.0, 3716000.0, 802.6],
    ['2024-08-14', 83273000.0, 3716000.0, 802.6]
  ]

  write(prices)
  list = read()
  ic(list)
