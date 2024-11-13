head = 0
tail = 0
size = 5
real_size = size + 1
queue = [-1 for _ in range(real_size)]

print(queue)


def is_queue_empty():
    global head, tail

    return head == tail


def is_queue_full():
    global head, tail

    return (tail + 1) % real_size == head


def enqueue(val):
    global head, tail

    if is_queue_full():
        print(f"fail to enqueue:{val} Queue Full")
        return False

    queue[tail] = val
    tail += 1
    tail %= real_size


def dequeue():
    global head, tail

    if is_queue_empty():
        print("Queue empty")
        return None

    ret = queue[head]
    head += 1
    head %= real_size

    return ret


def queue_print():
    print("*" * 40)
    print(f"head:{head}, tail:{tail}")
    print(queue)
    print("*" * 40)


if __name__ == "__main__":
    for i in range(6):
        enqueue(i)

    queue_print()

    for _ in range(3):
        print(f"deque: {dequeue()}")
    for i in range(10, 15):
        enqueue(i)

    queue_print()
