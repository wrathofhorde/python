from icecream import ic

def factorial(num):
    if num == 1:
        return 1
    
    return num * factorial(num - 1)

def fibo(num):
    if num == 1: return 0
    if num == 2: return 1

    return fibo(num - 1) + fibo(num - 2)

if __name__ == "__main__":
    ic(factorial(1))
    ic(factorial(2))
    ic(factorial(3))
    ic(factorial(4))
    ic(factorial(9))

    for i in range(1, 15):
        ic(fibo(i))