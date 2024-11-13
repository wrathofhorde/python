import sys
import json
from pokemon import get_pokemon_info

pokemon = ""

if len(sys.argv) != 2:
    print("포켓몬 이름이 빠져있습니다.")
    exit(0)

pokemon = sys.argv[1]
print(f"검색할 포켓몬의 이름은 {pokemon}입니다.")

try:
    info = get_pokemon_info(pokemon)

    if info:
        print(f"아이디: {info['id']}", end=", ")
        print(f"이름: {info['name']}")
        print(f"크기: {info['height']}", end=" / ")
        print(f"무게: {info['weight']}")

        filename = f"{pokemon}.json"

        with open(filename, "w") as json_file:
            json.dump(info, json_file)

        print(f"{filename}이 생성되었습니다.")
    else:
        print(f"{pokemon}은(는) 존재하지 않습니다.")
except Exception as e:  # 예외 출력
    print(e)
