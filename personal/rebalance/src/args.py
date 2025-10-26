import argparse


<<<<<<< HEAD
def parse_arguments() -> any:
=======
def parse_arguments() -> dict:
>>>>>>> 018a7ae2f2f378fb4ba5a056cf3451f6676604f4
    """
    명령줄에서 금액 아규먼트를 파싱합니다.
    
    Returns:
        int: 입력된 총 투자 금액
        
    Raises:
        ValueError: 금액이 양수가 아닌 경우
    """
    parser = argparse.ArgumentParser(description="포트폴리오 비중 조절을 위한 매수/매도 수량 계산")
    parser.add_argument("--amount", type=int, required=True, help="총 투자 금액 (원)")
<<<<<<< HEAD
    parser.add_argument("--file", required=True, help="포트폴리오 파일 이름")
=======
    parser.add_argument("--file", required=True, help="포트폴리오 구성 json 파일명")
>>>>>>> 018a7ae2f2f378fb4ba5a056cf3451f6676604f4
    args = parser.parse_args()

    # if args.amount < 0:
    #     raise ValueError("금액은 양수여야 합니다.")
    
<<<<<<< HEAD
    if len(args.file) == 0:
        raise ValueError("포트폴리오 파일을 지정해야 합니다..")
    
    return args
=======
    if len(args.file) < 5:
        raise ValueError("파일 이름이 잘못되었습니다.")
    
    return vars(args)
>>>>>>> 018a7ae2f2f378fb4ba5a056cf3451f6676604f4
