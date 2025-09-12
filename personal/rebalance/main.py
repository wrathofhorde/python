import numpy as np
from icecream import ic
from pathlib import Path

from src.args import *
from src.portfolio import *
from src.json_handler import *

ic.disable()

def main():
<<<<<<< HEAD
    args = parse_arguments()
    total_amount = args.amount
    input_path = Path(args.file)
    output_file: str = f"rebal_{args.file}"
    output_path = Path(output_file)
    portfolio_data = read_json_file(input_path)
=======

    args = parse_arguments()
    total_amount = args['amount']

    input_file: str = args['file']
    output_file: str = f"{input_file}_out.json"
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    portfolio_data = read_json_file(str(input_path))
>>>>>>> 018a7ae2f2f378fb4ba5a056cf3451f6676604f4
    portfolio = portfolio_data["portfolio"]
    ic(portfolio)
    
    # 현재 비중 계산: (value * quantity) / 총 가치
    values = [item["value"] * item["quantity"] for item in portfolio]
    current_total_value = sum(values)
    current_weights = [value / current_total_value for value in values]
    ic(current_total_value)
    ic(current_weights)
    print(f"현재 투자금액: {current_total_value}원")
    
    # 목표 비중 계산: ratio / 총 ratio
    ratios = [item["ratio"] for item in portfolio]
    total_ratio = sum(ratios)
    target_weights = np.array([ratio / total_ratio for ratio in ratios])
    
    # 자산 정보
    assets = [item["asset"] for item in portfolio]
    prices = [item["value"] for item in portfolio]
    quantities = [item["quantity"] for item in portfolio]
    
    # 리밸런싱 실행
    total_amount += current_total_value
    print(f"총투자금액: {total_amount}원")
    adjustments = rebalance(total_amount, list(target_weights), assets, prices, quantities)
    
    # 결과 저장
    results = {
        "rebalance": adjustments
    }
    write_json_file(str(output_path), results)
    print(f"조정 결과가 {output_file}에 저장되었습니다.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"오류 발생: {e}")
