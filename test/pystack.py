top = 0
size = 5
stack = [-1 for _ in range(size)]


def stack_push(val):
    global top

    if top >= len(stack):
        print(f"Stack Full, {val} rejected")
        return False

    stack[top] = val
    top += 1  # stack pointer를 다음으로 이동
    return True


def stack_pop():
    global top

    if top <= 0:
        print("Stack Empty")
        return None

    top -= 1
    return stack[top]


def is_stack_empty():
    global top

    return top == 0


def stack_size():
    global top

    return top


def stack_peek():
    global top

    if top == 0:
        return None

    return stack[top - 1]


def stack_print():
    print("*" * 40)
    print(f"top:{top}", end=", ")
    print(stack)
    print("*" * 40)


if __name__ == "__main__":
    stack_push(10)
    for i in range(5):
        stack_push(i)

    stack_print()
    print(f"peek: {stack_peek()}")
    print(f"pop: {stack_pop()}")
    print(f"pop: {stack_pop()}")
    print(f"size: {stack_size()}")

    for _ in range(5):
        print(f"pop: {stack_pop()}")
