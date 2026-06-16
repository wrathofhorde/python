from icecream import ic

def hanoi(num, frm, by, to):
    if num == 1:
        print(f"원반 {num}을 {frm}에서 {to}로 이동")
        return
    else:
        hanoi(num - 1, frm, to, by)
        print(f"원반 {num}을 {frm}에서 {to}로 이동")
        hanoi(num - 1, by, frm, to)


if __name__ == "__main__":
    hanoi(3, 'A', 'B', 'C')
    print("==============================")
    hanoi(5, 'A', 'B', 'C')
    print("==============================")
