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


def search_contacts(name, contact):
    for idx in range(len(contact)):
        if name == contact[idx]:
            print(f"연락처 색인 {idx}에 {contact[idx]} 이름 있음")
            return True

    print(f"{name} 찾지 못함")
    return False


if __name__ == "__main__":
    user_input = input("연락처 검색할 이름 입력: ")

    if search_contacts(user_input, contact):
        print(f"{user_input} found")
    else:
        print(f"{user_input} NOT FOUND")
