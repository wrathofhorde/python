import fetch_data
import check_data
import calc_volatility
from datetime import datetime, timedelta

def main():
    print("=== 비트코인 데이터 수집 및 검증 시작 ===")

    # 1. 데이터 수집
    print("\n[데이터 수집]")
    fetch_data.main()  # fetch_data.py의 main() 호출

    # 2. 데이터 검증
    print("\n[데이터 검증]")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")  # 어제 날짜
    check_data.check_data_completeness(start_date="2021-01-01", end_date=end_date)

    # 3. 데이터 분석
    print('\n[데이터 분석]')
    calc_volatility.main()

    print("\n=== 작업 완료 ===")

if __name__ == "__main__":
    main()
