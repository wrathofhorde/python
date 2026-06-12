from icecream import ic

def BSearch(arr, target):
    lhs = 0
    rhs = len(arr) - 1

    while lhs <= rhs:
        mid = (lhs + rhs) // 2

        if target == arr[mid]:
            return mid
        else:
            if target < arr[mid]:
                rhs = mid - 1
            else:
                lhs = mid + 1
    
    return -1

if __name__ == "__main__":
    arr = [-7, -4, -1, 1, 3, 4, 8, 9, 11]

    idx = BSearch(arr, 3)
    ic(idx, arr[idx]) if idx >= 0 else ic(idx)

    idx = BSearch(arr, -5)
    ic(idx, arr[idx]) if idx >= 0 else ic(idx)
