def count_character(str, dic):
    str = str.lower()

    for char in str:
        if char.isalpha():
            dic[char] += 1


def create_counter():
    counts = dict()  # 빈 딕셔너리 생성
    for i in range(ord("a"), ord("z") + 1):  # ascii code가 아닌 unicode
        counts[chr(i)] = 0

    return counts


if __name__ == "__main__":
    dic = create_counter()

    with open("str.txt", "r") as text:
        for line in text:
            count_character(line, dic)

    print(dic)
