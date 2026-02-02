import pandas as pd
import sys
import os
from decimal import Decimal
from datetime import timedelta

def process_transaction_data(file_path):
    # 1. 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"오류: 파일을 찾을 수 없습니다. ({file_path})")
        return

    # 2. 데이터 읽기 및 기본 전처리
    df = pd.read_csv(file_path, dtype=str)
    
    # 시간 변환 및 KST 날짜 생성
    df['DateTime (UTC)'] = pd.to_datetime(df['DateTime (UTC)'])
    df['KST_Date'] = (df['DateTime (UTC)'] + timedelta(hours=9)).dt.date
    
    # TxnFee(POL)를 Decimal로 변환 (소수점 정밀도 유지)
    df['TxnFee(POL)'] = df['TxnFee(POL)'].apply(
        lambda x: Decimal(str(x)) if pd.notnull(x) and str(x).strip() != "" else Decimal('0')
    )
    
    # 3. 전체 데이터에 대한 날짜별 합계
    overall_daily = df.groupby('KST_Date')['TxnFee(POL)'].sum().reset_index()
    overall_daily.rename(columns={'TxnFee(POL)': 'Total_Fee(POL)'}, inplace=True)
    
    # 4. Method가 0x60606040인 행만 필터링하여 날짜별 합계
    method_val = '0x60606040'
    method_df = df[df['Method'].str.strip() == method_val].copy()
    
    if not method_df.empty:
        method_daily = method_df.groupby('KST_Date')['TxnFee(POL)'].sum().reset_index()
        method_daily.rename(columns={'TxnFee(POL)': f'Method_{method_val}_Fee(POL)'}, inplace=True)
        # 두 결과 병합
        combined_result = pd.merge(overall_daily, method_daily, on='KST_Date', how='left').fillna(Decimal('0'))
    else:
        combined_result = overall_daily
        combined_result[f'Method_{method_val}_Fee(POL)'] = Decimal('0')
    
    # 결과 출력
    print(f"\n[ 분석 파일: {file_path} ]")
    print("=" * 60)
    print(combined_result.to_string(index=False))
    print("=" * 60)

if __name__ == "__main__":
    # 실행 시 매개변수(파일명)가 있는지 확인
    if len(sys.argv) < 2:
        print("사용법: python script_name.py <파일명.csv>")
        print("예시: python script_name.py 1.csv")
    else:
        target_file = sys.argv[1]
        process_transaction_data(target_file)