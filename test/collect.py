import json
from pokemon import get_pokemon_info

pokemon = "pikachu"

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
except Exception as e: # 예외 출력
  print(e)
