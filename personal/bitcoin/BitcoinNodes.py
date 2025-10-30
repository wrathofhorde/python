import time
import requests
import matplotlib.pyplot as plt

# 100페이지까지만 조회한다. 이 사이트는 최근 60일까지 데이터를 제공함.
nPage = 20

if nPage > 100:
  print("요청 페이지가 너무 많아 시간이 오래 걸립니다.")
else:
  t= []
  n= []

for page in range(1, nPage):
  # 페이지당 100개씩 요청한다. (Max= 100)
  url = 'https://bitnodes.io/api/v1/snapshots/?limit=100&page=' + str (page)
  resp = requests.get(url = url)
  # print(resp)
  data = resp.json()
  # print(data)
  print("page %d loaded." % page)

  for i in range(len(data['results'])):
    ts = time.gmtime(data['results'][i]['timestamp'])
    t.append (time.strftime("%Y-%m-%d %H:%M:%S", ts))
    n.append(data['results'][i]['total_nodes'])
  
t = t[::-1]
n = n[::-1]

# 최근 노드수의 변화를 확인한다
plt.figure(figsize = (8, 6))
plt.plot(n, color = 'red', linewidth = 0.7)
plt.title( 'Bitcoin Nodes\n' + t[0] + '~' + t[-1])
plt.grid(color = 'green', alpha = 0.2)
plt.show()
