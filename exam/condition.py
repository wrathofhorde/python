user_input = input("숫자를 입력하세요: ")

number = int(user_input)

if number % 2 == 0:
    print(f"사용자가 입력한 수 {number}는(은) 짝수")
else:
    print(f"사용자가 입력한 수 {number}는(은) 홀수")
