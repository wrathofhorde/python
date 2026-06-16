from icecream import ic
from ArrayList import ArrayList

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_point(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")

    def comp(self, p):
        if self.x == p.x and self.y == p.y:
            return 0
        elif self.x == p.x:
            return 1
        elif self.y == p.y:
            return 2
        else:
            return -1

if __name__ == "__main__":
    list = ArrayList()

    list.insert(Point(2, 1))
    list.insert(Point(2, 2))
    list.insert(Point(3, 1))
    list.insert(Point(3, 2))

    ic(list.count())

    p = [0]

    if list.first(p):
        p[0].show()

        while list.next(p):
            p[0].show()

    print("================================")
    p2 = Point(2, 0)

    if list.first(p):
        if p[0].comp(p2) == 1:
            p[0].show()
            list.remove()

        while list.next(p):
            if p[0].comp(p2) == 1:
                p[0].show()
                list.remove()

    ic(list.count())


