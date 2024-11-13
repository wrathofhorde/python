def show_balance(balance):
    print(f">>> Your balance is {balance:.2f}")


def deposit():
    deposit = float(input("Enter an amount to be deposited: "))

    if deposit < 0:
        print(">>> [ERROR]Wrong amount value")
        return 0

    return deposit


def withdraw(balance):
    withdraw = float(input("Enter an amount to be withdrawed: "))

    if withdraw < 0:
        print(">>> [ERROR]Wrong withdraw value")
        return 0
    elif withdraw > balance:
        print(">>> [ERROR]Insufficient fund ")
        return 0
    else:
        return withdraw


def main():
    balance = 0
    is_running = True

    while is_running:
        print("Bank Program")
        print("1.Show Balance")
        print("2.Deposit")
        print("3.Withdraw")
        print("4.Exit")

        menu = input("Select menu(1~4): ")

        if menu == "1":
            show_balance(balance)
        elif menu == "2":
            balance += deposit()
            show_balance(balance)
        elif menu == "3":
            balance -= withdraw(balance)
            show_balance(balance)
        elif menu == "4":
            is_running = False
        else:
            print("Input Error")

    print("Exit...")


if __name__ == "__main__":
    main()
