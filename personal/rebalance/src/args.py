import argparse


def parse_arguments() -> int:
    """
    명령줄에서 금액 아규먼트를 파싱합니다.
    
    Returns:
        int: 입력된 총 투자 금액
        
    Raises:
        ValueError: 금액이 양수가 아닌 경우
    """
    parser = argparse.ArgumentParser(description="포트폴리오 비중 조절을 위한 매수/매도 수량 계산")
    parser.add_argument("--amount", type=int, required=True, help="총 투자 금액 (원)")
    args = parser.parse_args()
    
    if args.amount < 0:
        raise ValueError("금액은 양수여야 합니다.")
    
    return args.amount
