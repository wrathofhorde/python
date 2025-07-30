import numpy as np
from icecream import ic
from pathlib import Path

from src.args import *
from src.portfolio import *
from src.json_handler import *


def main():
    input_file: str = "owns.json"
    output_file: str = "rebal.json"
    input_path = Path(input_file)
    output_path = Path(output_file)

    total_amount = parse_arguments()
    portfolio_data = read_json_file(input_path)
    portfolio = portfolio_data["portfolio"]
    
    # 현재 비중 계산: (value * quantity) / 총 가치
    values = [item["value"] * item["quantity"] for item in portfolio]
    current_total_value = sum(values)
    current_weights = np.array([value / current_total_value for value in values])
    
    # 목표 비중 계산: ratio / 총 ratio
    ratios = [item["ratio"] for item in portfolio]
    total_ratio = sum(ratios)
    target_weights = np.array([ratio / total_ratio for ratio in ratios])
    
    # 자산 정보
    assets = [item["asset"] for item in portfolio]
    prices = [item["value"] for item in portfolio]
    
    # 리밸런싱 실행
    total_amount += current_total_value
    print(f"총투자금액: {total_amount}원")
    adjustments = rebalance_portfolio(current_weights, target_weights, total_amount, prices, assets)
    
    # 결과 저장
    portfolio_data["adjustments"] = adjustments
    write_json_file(output_path, portfolio_data)
    print(f"조정 결과가 {output_file}에 저장되었습니다.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"오류 발생: {e}")
