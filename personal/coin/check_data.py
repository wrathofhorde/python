import sqlite3
from datetime import datetime, timedelta

def check_data_completeness(start_date="2021-01-01", end_date="2025-06-18"):
    """2021-01-01부터 2025-06-18까지 데이터가 모두 저장되었는지 확인"""
    # 날짜 범위 계산
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    total_days = (end_dt - start_dt).days + 1
    
    # 데이터베이스 연결
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    
    # 저장된 날짜 조회
    cursor.execute("SELECT date FROM btc_daily WHERE date BETWEEN ? AND ? ORDER BY date", (start_date, end_date))
    saved_dates = {row[0] for row in cursor.fetchall()}
    conn.close()
    
    # 예상 날짜 생성
    expected_dates = { (start_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(total_days) }
    
    # 누락된 날짜 확인
    missing_dates = expected_dates - saved_dates
    
    # 결과 출력
    print(f"확인 범위: {start_date} ~ {end_date} ({total_days}일)")
    print(f"저장된 데이터: {len(saved_dates)}일")
    
    if not missing_dates:
        print("모든 날짜의 데이터가 저장되어 있습니다.")
    else:
        print(f"누락된 날짜 ({len(missing_dates)}일):")
        for date in sorted(missing_dates):
            print(date)
    
    # 완전성 요약
    completeness = (len(saved_dates) / total_days) * 100
    print(f"\n데이터 완전성: {completeness:.2f}% ({len(saved_dates)}/{total_days}일)")

def main():
    check_data_completeness()

if __name__ == "__main__":
    main()