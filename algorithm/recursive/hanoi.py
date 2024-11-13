def hanoi(n, start, by, end):
    if n == 1:
        print(f"원반 1을 {start}에서 {end}로 이동")
    else:
        hanoi(n - 1, start, end, by)
        print(f"원반 {n}을 {start}에서 {end}로 이동")
        hanoi(n - 1, by, start, end)


hanoi(2, "A", "B", "C")
print("*" * 20)
hanoi(3, "A", "B", "C")
