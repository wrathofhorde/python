import random
from icecream import ic


def select_lotto_numbers():
    lis = list()

    for _ in range(6):
        lis.append(random.randrange(1, 46))

    lis.sort()
    return lis


def select_numbers():
    lst = list()
    numbers = [i for i in range(1, 46)]

    for _ in range(6):
        # ic(len(numbers))
        index = random.randrange(0, len(numbers))
        lst.append(numbers[index])
        del numbers[index]

    lst.sort()
    return lst


if __name__ == "__main__":
    try_count = []

    for _ in range(10):
        try_count.append(select_lotto_numbers())

    ic(try_count)

    try_count = []

    for _ in range(10):
        try_count.append(select_numbers())

    ic(try_count)
