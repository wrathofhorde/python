import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_data_start_date():
    """데이터베이스에서 최초로 저장된 날짜를 가져오거나, 없으면 2021-01-01 반환"""
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(date) FROM btc_daily")
    result = cursor.fetchone()[0]
    conn.close()
    
    if result:
        return result
    return "2021-01-01"

def get_period_data(start_date, end_date,/):
    """데이터베이스에서 지정된 기간의 데이터를 조회"""
    conn = sqlite3.connect("btc_daily.sq3")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, high, low, close, open 
        FROM btc_daily 
        WHERE date BETWEEN ? AND ? 
        ORDER BY date
    """, (start_date, end_date))
    data = [{"date": row[0], "high": row[1], "low": row[2], "close": row[3], "open": row[4]} for row in cursor.fetchall()]
    conn.close()
    return data

def calc_volatility(start_date="2021-01-01", end_date="2025-06-18", days=3,/):
    """지정된 기간 동안 각 시작 날짜의 days일 간 변동율 계산"""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # 결과 리스트
    results = []
    
    current_dt = start_dt
    while current_dt <= end_dt:
        # 기간의 시작과 끝 날짜
        period_end_dt = current_dt + timedelta(days=days-1)
        if period_end_dt > end_dt:
            period_end_dt = end_dt
        
        # 데이터베이스에서 데이터 조회
        data = get_period_data(
            current_dt.strftime("%Y-%m-%d"),
            period_end_dt.strftime("%Y-%m-%d")
        )
        
        if len(data) < days and period_end_dt <= end_dt:
            print(f"{current_dt.strftime('%Y-%m-%d')}: 충분한 데이터 없음 ({len(data)}/{days}일)")
            current_dt += timedelta(days=1)
            continue
        
        # 최고가와 최저가 계산
        high_price = max(item["high"] for item in data)
        low_price = min(item["low"] for item in data)
        
        # 변동율 계산: (최고가 / 최저가 - 1) * 100
        volatility = (high_price / low_price - 1) * 100
        
        results.append((current_dt.strftime("%Y-%m-%d"), volatility))
        
        current_dt += timedelta(days=1)
    
    return results

def calc_daily_volatility(start_date="2021-01-01", end_date="2025-06-18",/):
    """각 날짜의 일별 최고가/최저가 변동율 계산"""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # 데이터베이스에서 데이터 조회
    data = get_period_data(start_date, end_date)
    
    # 결과 리스트
    results = []
    
    for item in data:
        item_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
        if start_dt <= item_date <= end_dt:
            # 일별 변동율 계산: (최고가 / 최저가 - 1) * 100
            volatility = (item["high"] / item["low"] - 1) * 100
            results.append((item["date"], volatility))
    
    if not data:
        print("데이터가 없습니다.")
    
    return results

def calc_open_to_high_low_volatility(start_date="2021-01-01", end_date="2025-06-18",/):
    """각 날짜의 시초가 대비 최고가/최저가 변동율 계산"""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # 데이터베이스에서 데이터 조회
    data = get_period_data(start_date, end_date)
    
    # 결과 리스트
    results = []
    
    for item in data:
        item_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
        if start_dt <= item_date <= end_dt:
            # 시초가 대비 최고가/최저가 변동율 계산
            open_price = item["open"]
            high_volatility = (item["high"] / open_price - 1) * 100 if open_price != 0 else 0
            low_volatility = (item["low"] / open_price - 1) * 100 if open_price != 0 else 0
            results.append((item["date"], high_volatility, low_volatility))
    
    if not data:
        print("데이터가 없습니다.")
    
    return results

def count_price_changes(start_date="2021-01-01", end_date="2025-06-18",/):
    """종가 기준 전날 대비 상승, 하락, 변동 없는 날의 일수 계산"""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # 데이터베이스에서 데이터 조회
    data = get_period_data(start_date, end_date)
    
    if len(data) < 2:
        print("비교를 위한 데이터가 부족합니다.")
        return {"up_days": 0, "down_days": 0, "no_change_days": 0, "total_days": 0}
    
    # 상승, 하락, 변동 없음 카운트
    up_days = 0
    down_days = 0
    no_change_days = 0
    
    # 첫 번째 날짜는 비교 대상 없으므로 제외
    for i in range(1, len(data)):
        current_date = datetime.strptime(data[i]["date"], "%Y-%m-%d").date()
        if start_dt <= current_date <= end_dt:
            current_close = data[i]["close"]
            prev_close = data[i-1]["close"]
            
            if current_close > prev_close:
                up_days += 1
            elif current_close < prev_close:
                down_days += 1
            else:
                no_change_days += 1
    
    total_days = up_days + down_days + no_change_days
    
    return {
        "up_days": up_days,
        "down_days": down_days,
        "no_change_days": no_change_days,
        "total_days": total_days
    }

def get_the_day_one_year_before(theday):
    return (theday - timedelta(days=364)).strftime("%Y-%m-%d")

def get_the_day_half_year_before(theday):
    return (theday - timedelta(weeks=26)).strftime("%Y-%m-%d")

def main():
    days = 3
    start_date = get_data_start_date()
    yesterday = datetime.now() - timedelta(days=1)
    end_date = yesterday.strftime("%Y-%m-%d")

    # 3일 간 변동율 계산
    results = calc_volatility(start_date, end_date, days)
    print(f"{start_date} ~ {end_date}, {days}일 간 변동율")
    # for date, volatility in results[:5]:
    #     print(f"{date}: {volatility:.2f}%")
    if results:
        avg_volatility = sum(vol for _, vol in results) / len(results)
        print(f"\t평균 변동율: {avg_volatility:.2f}%")
        print(f"\t총 {len(results)}개의 시작 날짜 처리됨")

    days = 3
    start_date = get_the_day_half_year_before(yesterday)
    results = calc_volatility(start_date, end_date, days)
    print(f"{start_date} ~ {end_date}, {days}일 간 변동율")
    # for date, volatility in results[:5]:
    #     print(f"{date}: {volatility:.2f}%")
    if results:
        avg_volatility = sum(vol for _, vol in results) / len(results)
        print(f"\t평균 변동율: {avg_volatility:.2f}%")
        print(f"\t총 {len(results)}개의 시작 날짜 처리됨")

    start_date = get_data_start_date()
    end_date = yesterday.strftime("%Y-%m-%d")
    # 일별 변동율 계산
    daily_results = calc_daily_volatility(start_date, end_date)
    print(f"{start_date} ~ {end_date}, 일별 변동율")
    # for date, volatility in daily_results[:5]:
    #     print(f"{date}: {volatility:.2f}%")
    if daily_results:
        avg_daily_volatility = sum(vol for _, vol in daily_results) / len(daily_results)
        print(f"\t평균 일별 변동율: {avg_daily_volatility:.2f}%")
        print(f"\t총 {len(daily_results)}개의 날짜 처리됨")

    start_date = get_the_day_half_year_before(yesterday)
    daily_results = calc_daily_volatility(start_date, end_date)
    print(f"{start_date} ~ {end_date}, 일별 변동율")
    # for date, volatility in daily_results[:5]:
    #     print(f"{date}: {volatility:.2f}%")
    if daily_results:
        avg_daily_volatility = sum(vol for _, vol in daily_results) / len(daily_results)
        print(f"\t평균 일별 변동율: {avg_daily_volatility:.2f}%")
        print(f"\t총 {len(daily_results)}개의 날짜 처리됨")

    # 시초가 대비 최고가/최저가 변동율 계산
    start_date = get_data_start_date()
    open_results = calc_open_to_high_low_volatility(start_date, end_date)
    print(f"{start_date} ~ {end_date}, 시초가 대비 최고가/최저가 변동율")
    for date, high_vol, low_vol in open_results[:5]:
        print(f"\t{date}: 최고가 변동율 {high_vol:.2f}%, 최저가 변동율 {low_vol:.2f}%")
    if open_results:
        avg_high_vol = sum(high_vol for _, high_vol, _ in open_results) / len(open_results)
        avg_low_vol = sum(low_vol for _, _, low_vol in open_results) / len(open_results)
        print(f"\t평균 최고가 변동율: {avg_high_vol:.2f}%")
        print(f"\t평균 최저가 변동율: {avg_low_vol:.2f}%")
        print(f"\t총 {len(open_results)}개의 날짜 처리됨")

    start_date = get_the_day_one_year_before(yesterday)
    open_results = calc_open_to_high_low_volatility(start_date, end_date)
    print(f"{start_date} ~ {end_date}, 시초가 대비 최고가/최저가 변동율")
    for date, high_vol, low_vol in open_results[:5]:
        print(f"\t{date}: 최고가 변동율 {high_vol:.2f}%, 최저가 변동율 {low_vol:.2f}%")
    if open_results:
        avg_high_vol = sum(high_vol for _, high_vol, _ in open_results) / len(open_results)
        avg_low_vol = sum(low_vol for _, _, low_vol in open_results) / len(open_results)
        print(f"\t평균 최고가 변동율: {avg_high_vol:.2f}%")
        print(f"\t평균 최저가 변동율: {avg_low_vol:.2f}%")
        print(f"\t총 {len(open_results)}개의 날짜 처리됨")

    # 종가 변화 일수 계산
    start_date = get_data_start_date()
    changes = count_price_changes(start_date, end_date)
    print(f"{start_date} ~ {end_date}, 종가 기준 전날 대비")
    print(f"\t상승한 날: {changes['up_days']}일")
    print(f"\t하락한 날: {changes['down_days']}일")
    print(f"\t변동 없는 날: {changes['no_change_days']}일")
    print(f"\t총 비교 날짜: {changes['total_days']}일 (첫 날 제외)")

    start_date = get_the_day_one_year_before(yesterday)
    changes = count_price_changes(start_date, end_date)
    print(f"{start_date} ~ {end_date}, 종가 기준 전날 대비")
    print(f"\t상승한 날: {changes['up_days']}일")
    print(f"\t하락한 날: {changes['down_days']}일")
    print(f"\t변동 없는 날: {changes['no_change_days']}일")
    print(f"\t총 비교 날짜: {changes['total_days']}일 (첫 날 제외)")


    start_date_half_year = get_the_day_half_year_before(yesterday)
    # start_date_half_year = get_the_day_one_year_before(yesterday)
    # start_date_half_year = get_data_start_date()
    open_results_half_year = calc_open_to_high_low_volatility(start_date_half_year, end_date)
    print(f"{start_date_half_year} ~ {end_date}, 시초가 대비 최고가/최저가 변동율 (6개월)")

    if open_results_half_year:
        dates = [item[0] for item in open_results_half_year]
        high_vols = [item[1] for item in open_results_half_year]
        low_vols = [item[2] for item in open_results_half_year]

        x = np.arange(len(dates))

        plt.figure(figsize=(15, 6)) # 차트 크기를 (15, 6)으로 변경
        plt.bar(x - 0.2, high_vols, width=0.4, label='High Price Volatility', color='red', align='center') # 레이블 변경
        plt.bar(x + 0.2, low_vols, width=0.4, label='Low Price Volatility', color='blue', align='center') # 레이블 변경

        plt.axhline(0, color='black', linewidth=0.8)

        # x축 월 단위 표시
        month_labels = [datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m") for d in dates]
        unique_months_indices = []
        last_month = None
        for i, month in enumerate(month_labels):
            if month != last_month:
                unique_months_indices.append(i)
                last_month = month

        plt.xticks([x[i] for i in unique_months_indices], [month_labels[i] for i in unique_months_indices], rotation=45, ha='right')
        plt.tick_params(axis='x', which='major', length=5) # 월 표시 눈금 길이

        plt.xlabel('Date') # '날짜' -> 'Date'
        plt.ylabel('Volatility (%)') # '변동율 (%)' -> 'Volatility (%)'
        plt.title(f'{start_date_half_year} ~ {end_date} Open vs High/Low Volatility') # 제목 변경
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show() # 차트를 창으로 보여주기
        # plt.savefig('open_to_high_low_volatility_6_months.png') # 파일 저장 주석 처리
        # plt.close() # 창을 닫지 않도록 주석 처리

if __name__ == "__main__":
    main()