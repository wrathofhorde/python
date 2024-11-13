def fibonacci(n):
    if n == 1:
        return 1
    if n == 0:
        return 0

    return fibonacci(n - 1) + fibonacci(n - 2)


for i in range(0, 11):
    print(fibonacci(i))
