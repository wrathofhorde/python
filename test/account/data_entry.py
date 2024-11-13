from datetime import datetime


def get_date(prompt, allow_default=False):
    date_format = "%Y-%m-%d"
    input_date = input(prompt)

    if allow_default and not input_date:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(input_date, date_format)
        return valid_date.strftime(date_format)
    except:
        print("날짜 형식이 잘못되었습니다. 2000-01-23 과 같은 형식으로 입력하시오")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = int(input("금액을 입력하시오: "))

        if amount <= 0:
            raise ValueError("금액은 0보다 큰 값이어야 합니다.")

        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    except Exception as e:
        print(e)
        return get_amount()


def get_category():
    category = {"I": "수입", "E": "지출"}
    user_input = input("수입('I') / 지출('E') 항목 선택하시오: ").upper()
    if user_input in category:
        return category[user_input]

    print("잘못된 항목입력입니다.")
    return get_category()


def get_description():
    return input("상세 내역을 입력하세요(선택사항): ")


if __name__ == "__main__":
    print(
        get_date(
            "'2024-01-01' 형식으로 날짜을 입력하시오. 오늘 날짜를 입력하려면 'Enter'을 입력하시오:",
            True,
        )
    )
    print(get_amount())
    print(get_category())
    print(get_description())
