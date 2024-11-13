scores = []

while True:
    print("1: 성적입력")
    print("2: 성적계산")
    print("3: 종료")

    user_input = input("메뉴 선택 (1 ~ 3): ")

    match user_input:
        case "1":
            input_scores = input("성적입력:")
            input_scores = input_scores.split()
            for score in input_scores:
                scores.append(int(score))
            print(scores)
        case "2":
            size_scores = len(scores)
            if size_scores != 0:
                scores.sort()
                min_value = scores[0]
                max_value = scores[-1]

                if size_scores % 2 == 0:
                    pass
                else:
                    pass
            else:
                print("성적을 입력하시오")
        case "3":
            break
        case _:
            pass
