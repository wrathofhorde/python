from icecream import ic
from datetime import datetime, timedelta


class days:
    def __init__(self):
        self.today = datetime.today()
        self.today = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
        self.yesterday = self.today - timedelta(days=1)
        self.startday = self.today - timedelta(days=365)
        self.endday = self.yesterday
    def tostring(self, day):
        return day.strftime("%Y-%m-%d")


if __name__ == "__main__":
    d = days()
    ic(d.startday)
    ic(d.endday)
