import json
import requests
from icecream import ic

base_url = "https://pokeapi.co/api/v2"

ic.disable()

def get_pokemon_info(name):
  url = f"{base_url}/pokemon/{name}"
  ic(url)
  res = requests.get(url)
  ic(res)

  if res.status_code != 200:
    print(f"Error code: {res.status_code}")
    return {}
  
  data = res.json()
  ic(data)
  return data

if __name__ == "__main__":
  pokemon_name = "ditto"

  try:
    info = get_pokemon_info(pokemon_name)

    if info:
      print(f"ID: {info['id']}", end=", ")
      print(f"Name: {info['name']}")
      print(f"Height: {info['height']}", end=" / ")
      print(f"Weight: {info['weight']}")

      with open(f"{pokemon_name}.json", "w") as json_file:
        json.dump(info, json_file)
    else:
      print("NO DATA")
  except Exception as e: # 예외 출력
    print(e)

