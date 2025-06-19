import requests
import sqlite3
import time
from datetime import datetime, timedelta
import threading
import queue

def create_database():
    """SQLite 데이터베이스와 테이블을 생성"""
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS btc_daily (
            date TEXT PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            value REAL
        )
    """)
    conn.commit()
    conn.close()

def get_last_update_date():
    """데이터베이스에서 마지막 업데이트 날짜를 가져오거나, 없으면 2021-01-01 반환"""
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM btc_daily")
    result = cursor.fetchone()[0]
    conn.close()
    
    if result:
        return result
    return "2021-01-01"

def get_btc_daily_price(market="KRW-BTC", date=None, count=1):
    """업비트 API에서 일봉 데이터를 가져옴"""
    url = "https://api.upbit.com/v1/candles/days"
    params = {
        "market": market,
        "count": count
    }
    if date:
        params["to"] = f"{date} 23:59:59"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data and isinstance(data, list):
            return [{
                "date": item["candle_date_time_kst"].split("T")[0],  # YYYY-MM-DD만 저장
                "open": item["opening_price"],
                "high": item["high_price"],
                "low": item["low_price"],
                "close": item["trade_price"],
                "volume": item["candle_acc_trade_volume"],
                "value": item["candle_acc_trade_price"]
            } for item in data]
        return None
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return None

def save_to_sqlite(data, start_date="2021-01-01"):
    """데이터를 SQLite에 저장, start_date 이전 데이터 제외"""
    if not data:
        print("저장할 데이터가 없습니다.")
        return None
    
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    
    saved_count = 0
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    
    for item in data:
        item_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
        if item_date >= start_date_dt:
            cursor.execute("""
                INSERT OR REPLACE INTO btc_daily (date, open, high, low, close, volume, value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["date"],
                item["open"],
                item["high"],
                item["low"],
                item["close"],
                item["volume"],
                item["value"]
            ))
            saved_count += 1
    
    conn.commit()
    conn.close()
    
    if saved_count > 0:
        latest_date = max(item["date"] for item in data if datetime.strptime(item["date"], "%Y-%m-%d").date() >= start_date_dt)
        print(f"{saved_count}개의 데이터가 {latest_date}까지 저장되었습니다.")
        return latest_date
    else:
        print("저장된 데이터가 없습니다.")
        return None

def get_user_input(q):
    """사용자 입력을 별도 스레드에서 처리"""
    while True:
        try:
            user_input = input()
            q.put(user_input.lower())
        except EOFError:
            q.put("x")  # EOF 발생 시 중단
            break

def main():
    # 데이터베이스 초기화
    create_database()
    
    # 마지막 업데이트 날짜 가져오기
    last_date = get_last_update_date()
    start_date = (datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)).date()
    
    # 어제 날짜 계산 (2025-06-18)
    yesterday = (datetime.now() - timedelta(days=1)).date()
    
    if start_date > yesterday:
        print("이미 최신 데이터까지 저장되었습니다.")
        return
    
    # 사용자 입력을 위한 큐와 스레드 설정
    input_queue = queue.Queue()
    input_thread = threading.Thread(target=get_user_input, args=(input_queue,), daemon=True)
    input_thread.start()
    
    print(f"{start_date}부터 {yesterday}까지 데이터를 저장합니다. 'x' 입력 후 Enter로 중단 가능.")
    
    current_date = start_date
    step_days = 1  # 한 번에 1일치 데이터 조회
    
    while current_date <= yesterday:
        # 사용자 입력 확인
        try:
            user_input = input_queue.get_nowait()
            if user_input == 'x':
                print(f"\n'x' 입력으로 {current_date}에서 중단됨.")
                break
        except queue.Empty:
            pass
        
        # API로 데이터 조회
        data = get_btc_daily_price(date=current_date.strftime("%Y-%m-%d"), count=step_days)
        if not data:
            print(f"{current_date} 이후 데이터가 없습니다.")
            break
        
        # 데이터 저장 (2021-01-01 이전 제외)
        latest_saved_date = save_to_sqlite(data, start_date="2021-01-01")
        if not latest_saved_date:
            current_date += timedelta(days=1)
            continue
        
        # 다음 날짜로 이동
        current_date = datetime.strptime(latest_saved_date, "%Y-%m-%d").date() + timedelta(days=1)
        
        # API 요청 제한 방지
        time.sleep(0.5)
    
    # 저장된 데이터 샘플 출력
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM btc_daily ORDER BY date DESC LIMIT 5")
    results = cursor.fetchall()
    if results:
        print("\n최근 저장된 데이터 샘플:")
        for row in results:
            print(row)
    conn.close()

if __name__ == "__main__":
    main()
