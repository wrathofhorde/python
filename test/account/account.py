import csv
import pandas
from icecream import ic
from datetime import datetime
from data_entry import get_date, get_category, get_amount, get_description


class CSV:
    FILE_NAME = "account_book.csv"  # class variable
    DATE = "date"
    AMOUNT = "amount"
    CATEGORY = "category"
    DESC = "description"
    DATE_FORMAT = "%Y-%m-%d"
    COLUMN_NAMES = [DATE, AMOUNT, CATEGORY, DESC]

    @classmethod  # decorator
    def init_csv(cls):
        try:
            pandas.read_csv(cls.FILE_NAME)
        except FileNotFoundError:
            df = pandas.DataFrame(columns=cls.COLUMN_NAMES)
            df.to_csv(cls.FILE_NAME, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, desc):
        new_entry = {
            cls.DATE: date,
            cls.AMOUNT: amount,
            cls.CATEGORY: category,
            cls.DESC: desc,
        }

        with open(
            cls.FILE_NAME, "a", encoding="utf-8-sig", newline=""
        ) as csvfile:  # context manager
            csv_writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMN_NAMES)
            csv_writer.writerow(new_entry)

        print("새 항목을 추가하였습니다.")

    @classmethod
    def get_transactions(cls, start_day, end_day):
        df = pandas.read_csv(CSV.FILE_NAME)
        ic(df)
        ic(type(df[cls.DATE]))
        df[cls.DATE] = pandas.to_datetime(df[cls.DATE], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_day, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_day, cls.DATE_FORMAT)
        print(df[cls.DATE] >= start_date)
        print(df[cls.DATE] <= end_date)

        mask = (start_date <= df[cls.DATE]) & (df[cls.DATE] <= end_date)
        ic(mask)
        filtered_df = df.loc[mask]
        ic(filtered_df)
        if filtered_df.empty:
            print("주어진 날짜에 해당하는 거래가 없습니다.")
        else:
            print(f"{start_day} ~ {end_day} 거래 출력")
            # 출력할 내용을 문자열로 변경하고 인덱스 생략
            print(filtered_df.to_string(index=False))
            ic(filtered_df[filtered_df[cls.CATEGORY] == "수입"])
            ic(filtered_df[filtered_df[cls.CATEGORY] == "수입"][cls.AMOUNT
            ])
            total_income = filtered_df[filtered_df[cls.CATEGORY] == "수입"][
                cls.AMOUNT
            ].sum()
            total_expense = filtered_df[filtered_df[cls.CATEGORY] == "지출"][
                cls.AMOUNT
            ].sum()

            print("\n요약")
            print(f"총수입: {total_income}, 총지출: {total_expense}")
            print(f"저축 가능금액: {total_income - total_expense}")

        return filtered_df


def add_entry():
    CSV.init_csv()

    date = get_date(
        "'2024-01-01' 형식으로 날짜을 입력하시오. 오늘 날짜를 입력하려면 'Enter'을 입력하시오: ",
        True,
    )
    amount = get_amount()
    category = get_category()
    desc = get_description()

    CSV.add_entry(date, amount, category, desc)


def main():
    while True:
        print("\n1. 새 항목 추가")
        print("2. 지난 항목 및 날짜별 거래 보기")
        print("3. 종료")
        user_input = input("메뉴 선택(1 ~ 3): ")

        match user_input:
            case "1":
                add_entry()
            case "2":
                start_day = get_date("검색 시작 날짜를 입력하세요 (yyyy-mm-dd): ")
                end_day = get_date("검색 종료 날짜를 입력하세요 (yyyy-mm-dd): ")
                df = CSV.get_transactions(start_day, end_day)
            case "3":
                break
            case _:
                pass


if __name__ == "__main__":
    main()
