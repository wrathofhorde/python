contact = [
    "john",
    "michael",
    "kelly",
    "ryan",
    "marco",
    "jason",
    "lily",
    "lisa",
    "bella",
    "teo",
    "peter",
]


def binary_search(target, arr):
    lhs = 0
    rhs = len(arr) - 1
    mid = (lhs + rhs) // 2  # 홀수인 경우, 중간값이 .5로 계산되기 때문에

    while True:
        if lhs > rhs:
            print(f"{target} 찾지 못함")
            return False
        elif arr[mid] < target:
            lhs = mid + 1
            mid = (lhs + rhs) // 2
        elif arr[mid] > target:
            rhs = mid - 1
            mid = (lhs + rhs) // 2
        else:
            print(f"인덱스 {mid}에서 {target} 찾음")
            return True


if __name__ == "__main__":
    binary_search("kelly", contact)
    binary_search("jane", contact)

    contact.sort()
    binary_search("kelly", contact)
    binary_search("jane", contact)
