class MyStack2:
    def __init__(self, size):
        self.size = size
        self.stack = []

    def __str__(self):
        return f"size: {self.size}, stack: {self.stack}"

    def push(self, data):
        if self.size <= len(self.stack):
            print("stack full")
            return

        self.stack.append(data)

    def pop(self):
        if len(self.stack) == 0:
            print("stack empty")
            return

        data = self.stack[-1]  # 마지막 요소의 인덱스는 -1로 사용 가능
        del self.stack[-1]

        return data


if __name__ == "__main__":
    s1 = MyStack2(3)
    s1.push(1)
    s1.push(3)
    s1.push(5)

    s2 = MyStack2(2)
    s2.push(2)
    s2.push(4)
    s2.push(5)

    print(s1)
    print(s2)

    s1.pop()
    s1.pop()
    s1.pop()

    s2.pop()
    s2.pop()
    s2.pop()

    arr = [1, 3, 5]

    arr.append(7)
    arr.append(5)
    print(arr)

    del arr[1]
    print(arr)

    arr = [1, 3, 5]
    arr.insert(1, 7)
    arr.insert(-1, 7)
    print(arr)

    arr.remove(7)
    print(arr)
    arr.remove(arr[0])
    print(arr)
