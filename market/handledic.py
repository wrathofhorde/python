import os
import pickle
from icecream import ic

filename = "average_prices.dat"

def write(data, name = None):
  name = filename if name is None else name
  
  with open(name, "wb") as file:
    pickle.dump(data, file)

def read(name = None):
  name = filename if name is None else name

  if os.path.isfile(name):
    with open(name, "rb") as file:
      data = pickle.load(file)
      return data
  else:
    return {}

if __name__ == "__main__":
  prices = {
    '2024-08-06': [83273000.0, 3716000.0, 802.6],
    '2024-08-07': [83273000.0, 3716000.0, 802.6],
    '2024-08-08': [83273000.0, 3716000.0, 802.6],
    '2024-08-09': [83273000.0, 3716000.0, 802.6],
    '2024-08-10': [83273000.0, 3716000.0, 802.6],
    '2024-08-11': [83273000.0, 3716000.0, 802.6],
    '2024-08-12': [83273000.0, 3716000.0, 802.6],
    '2024-08-13': [83273000.0, 3716000.0, 802.6],
    '2024-08-14': [83273000.0, 3716000.0, 802.6]
  }

  write(prices)
  data = read()
  ic(data)
  ic(data['2024-08-06'])
  for k, v in data.items():
    v.insert(0, k)
    ic(v)  # ['2024-08-06', 83273000.0, 3716000.0, 802.6]