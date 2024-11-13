import csv
import pandas
from datetime import datetime


class CSV:
    FILE_NAME = "account_book.csv"  # class variable
    DATE = "date"
    AMOUNT = "amount"
    CATEGORY = "category"
    DESC = "description"
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


if __name__ == "__main__":
    print(CSV.FILE_NAME)  # 인스턴스 생성없이, CSV() 없이 접근할 수 있음
    CSV.init_csv()
    CSV.add_entry("2024-10-10", 100, "수입", "월급")
    CSV.add_entry("2024-10-10", 10, "지출", "저녁 식사")
