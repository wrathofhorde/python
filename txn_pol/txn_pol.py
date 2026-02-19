import sys
import pandas as pd
from decimal import Decimal, getcontext

# 정밀도 설정 (블록체인 계산용 36자리)
getcontext().prec = 36

if len(sys.argv) < 3:
    print("사용법: python script.py <pol.csv> <sut_combined.csv>")
    sys.exit(1)

def to_decimal(val):
    if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
        return Decimal('0')
    return Decimal(str(val).replace(',', ''))

# 1. 데이터 읽기 (dtype=str로 부동소수점 오차 방지)
df_pol = pd.read_csv(sys.argv[1], dtype=str)
df_token = pd.read_csv(sys.argv[2], dtype=str)

my_address = '0xc8f7787d062a91a5367dde72b35eeb5da807102d'.lower()

# 날짜 전처리
df_pol['Date'] = pd.to_datetime(df_pol['DateTime (UTC+9)']).dt.date

# 2. 토큰 데이터 정리 (해시 하나에 여러 토큰이 있을 수 있으므로 그룹화하여 합산)
# 여기서는 USDT0와 SUT를 명확히 구분하여 미리 집계해둡니다.
token_summary = {}

for _, row in df_token.iterrows():
    tx_hash = row['Transaction Hash']
    symbol = str(row['TokenSymbol']).strip() # "USDT0" 또는 "SUT"
    val = to_decimal(row['TokenValue'])
    is_in = str(row['To']).lower() == my_address
    
    if tx_hash not in token_summary:
        token_summary[tx_hash] = []
    token_summary[tx_hash].append({'symbol': symbol, 'val': val, 'is_in': is_in})

def analyze_row(row):
    tx_hash = row['Transaction Hash']
    fee = to_decimal(row['TxnFee(POL)'])
    pol_in = to_decimal(row['Value_IN(POL)'])
    pol_out = to_decimal(row['Value_OUT(POL)'])
    
    res = {
        'POL_입금': Decimal('0'), 'POL_입금_수수료': Decimal('0'),
        'POL_출금': Decimal('0'), 'POL_출금_수수료': Decimal('0'),
        'SUT_입금': Decimal('0'), 'SUT_입금_수수료': Decimal('0'),
        'SUT_출금': Decimal('0'), 'SUT_출금_수수료': Decimal('0'),
        'USDT0_입금': Decimal('0'), 'USDT0_입금_수수료': Decimal('0'),
        'USDT0_출금': Decimal('0'), 'USDT0_출금_수수료': Decimal('0')
    }

    # CASE 1: 토큰 거래(SUT, USDT0)가 있는 경우
    if tx_hash in token_summary:
        for item in token_summary[tx_hash]:
            # 기호에 따라 prefix 결정 (SUT 또는 USDT0)
            prefix = 'SUT' if 'SUT' in item['symbol'].upper() else 'USDT0'
            direction = '입금' if item['is_in'] else '출금'
            
            res[f'{prefix}_{direction}'] += item['val']
            res[f'{prefix}_{direction}_수수료'] += fee # 해당 트랜잭션의 수수료 할당
            
    # CASE 2: 순수 POL 거래인 경우
    else:
        if pol_in > 0:
            res['POL_입금'], res['POL_입금_수수료'] = pol_in, fee
        elif pol_out > 0 or fee > 0:
            res['POL_출금'], res['POL_출금_수수료'] = pol_out, fee
            
    return pd.Series(res)

# 3. 분석 적용 및 날짜별 집계
analysis_results = df_pol.apply(analyze_row, axis=1)
final_report = pd.concat([df_pol['Date'], analysis_results], axis=1).groupby('Date').sum()

# 4. 결과 출력
print("--- 날짜별 POL / SUT / USDT0 통합 분석 보고서 ---")
print(final_report.to_string())

# CSV 저장 (필요시 주석 해제)
final_report.astype(float).to_csv('final_crypto_report.csv')