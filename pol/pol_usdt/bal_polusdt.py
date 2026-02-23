import pandas as pd
from decimal import Decimal, getcontext
import sys
import os

def analyze(file_path, current_balance_str, target_addr):
    getcontext().prec = 50
    
    if not os.path.exists(file_path):
        print(f"Error: 파일을 찾을 수 없습니다 -> {file_path}")
        return

    # 1. 데이터 로드
    df = pd.read_csv(file_path)
    
    # 컬럼명 대응
    time_col = 'DateTime (UTC+9)' if 'DateTime (UTC+9)' in df.columns else 'DateTime (UTC)'
    df = df.rename(columns={time_col: 'DateTime (Local)'})
    
    # 2. 전처리
    target_addr = target_addr.lower()
    df['DateTime (Local)'] = pd.to_datetime(df['DateTime (Local)'])
    df['Quantity'] = df['Quantity'].apply(lambda x: Decimal(str(x).replace(',', '')))
    df['From'] = df['From'].str.lower()
    df['To'] = df['To'].str.lower()
    df['Date'] = df['DateTime (Local)'].dt.date

    # 3. 입금/출금 구분 컬럼 생성
    # 입금: To가 대상 주소인 경우, 출금: From이 대상 주소인 경우
    df['Inflow'] = df.apply(lambda row: row['Quantity'] if row['To'] == target_addr else Decimal('0'), axis=1)
    df['Outflow'] = df.apply(lambda row: row['Quantity'] if row['From'] == target_addr else Decimal('0'), axis=1)

    # 4. 역산 계산 (Balance 추적을 위해 최신순 정렬)
    df_sorted = df.sort_values(by='DateTime (Local)', ascending=False).reset_index(drop=True)
    balances = []
    temp_balance = Decimal(current_balance_str)

    for _, row in df_sorted.iterrows():
        balances.append(temp_balance)
        if row['To'] == target_addr:
            temp_balance -= row['Quantity']
        elif row['From'] == target_addr:
            temp_balance += row['Quantity']

    df_sorted['Balance'] = balances

    # 5. 일별 데이터 집계 (입금 합계, 출금 합계, 마지막 잔고)
    # 입출금은 합산(sum), 잔고는 해당 날짜의 첫 번째 행(first)
    daily_summary = df_sorted.groupby('Date').agg({
        'Inflow': 'sum',
        'Outflow': 'sum',
        'Balance': 'first',
        'DateTime (Local)': 'max' # 확인용
    }).sort_index()

    # 소수점 6자리 정리
    for col in ['Inflow', 'Outflow', 'Balance']:
        daily_summary[col] = daily_summary[col].apply(lambda x: x.quantize(Decimal('0.000000')))

    # 6. CSV 저장
    output_name = f"final_summary_{os.path.basename(file_path)}"
    daily_summary.to_csv(output_name, encoding='utf-8-sig')
    
    print(f"\n✅ 분석 완료!")
    print(f"결과 저장: {output_name}\n")
    print(daily_summary[['Inflow', 'Outflow', 'Balance']])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: bal_polusdt.exe <file_path> <current_balance>")
    else:
        analyze(sys.argv[1], sys.argv[2], '0xc8f7787d062a91a5367dde72b35eeb5da807102d')