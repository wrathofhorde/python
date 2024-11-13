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
