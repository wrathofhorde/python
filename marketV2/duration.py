from icecream import ic
from datetime import datetime, timedelta


class days:
    def __init__(self):
        self.today = datetime.today()
        self.today = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
        # 어제
        self.yesterday = self.today - timedelta(days=1)
        # 이달의 1일
        self.firstday = self.today.replace(day=1)
        # 직전달 마지막 날
        self.endday = self.firstday - timedelta(days=1)
        # 일년전 1일
        self.startday = datetime(
            self.firstday.year - 1, self.firstday.month, self.firstday.day
        )

    def tostring(self, day):
        return day.strftime("%Y-%m-%d")


if __name__ == "__main__":
    d = days()
    ic(d.today)
    ic(d.tostring(d.yesterday))
    ic(d.tostring(d.firstday))
    ic(d.startday)
    ic(d.endday)
