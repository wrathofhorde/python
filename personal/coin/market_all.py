import requests
from icecream import ic

def get_market_all():
    url = "https://api.bithumb.com/v1/market/all?isDetails=false"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    # print(response.status_code)      # 상태 코드 출력 (200, 404 등)
    # print(response.text)             # 응답 본문 (str)
    # print(response.headers)          # 응답 헤더 (dict-like 객체)
    data = response.json()            # JSON 응답을 파싱해서 dict로 반환
    # 딕셔너리 구조 확인
    ic(data[0])
    # ic| data[0]: {'english_name': 'Bitcoin', 'korean_name': '비트코인', 'market': 'KRW-BTC'}

if __name__ == "__main__":
    get_market_all()