def print_contacts(contacts):
    for person in contacts:
        print(person)  # dict 그대로 출력


def new_contact():
    name = input("연착처 이름 입력: ")
    phone = input("휴대폰 번호 입력: ")

    return {"name": name, "phone": phone}


def find_person(contacts):
    name = input("검색할 이름 입력: ")

    for person in contacts:
        # print(person) # dict에서 키값을 사용하여 검색
        if person["name"] == name:
            return f"{person['name']}: {person['phone']}"

    return f"{name}을 찾을 수 없습니다."


def main():
    contacts = []
    print("**********************")
    print("*      CONTACTS      *")
    print("*1.Print contacts    *")
    print("*2.New contact       *")
    print("*3.Find in contacts  *")
    print("*0.EXIT              *")
    print("**********************")

    while True:
        menu = input("Select menu(0~4): ")
        match menu:
            case "1":
                print_contacts(contacts)
            case "2":
                person = new_contact()
                contacts.append(person)
            case "3":
                result = find_person(contacts)
                print(result)
            case "4":
                break
            case _:
                print("[ERROR]Invalid Menu")


if __name__ == "__main__":
    main()
