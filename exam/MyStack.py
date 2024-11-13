top = 0
stack = [-1 for _ in range(5)]


def stack_push(data):
    global top

    if len(stack) == top:
        print("스택이 가득 찼습니다.")
        return

    stack[top] = data
    top += 1


def stack_pop():
    global top

    if top == 0:
        print("스택이 비어 있습니다.")
        return

    top -= 1
    return stack[top]


if __name__ == "__main__":
    print(stack)

    stack_push(1)

    stack_push(2)

    stack_push(3)
    print(stack)

    data = stack_pop()
    print(f"pop:{data}")
    data = stack_pop()
    print(f"pop:{data}")
    data = stack_pop()
    print(f"pop:{data}")
    print(stack)


scores = [39, 492, 3304, 2930]
scores2 = {0: 89, 1: 492, 2: 3304, 4: 2940}
