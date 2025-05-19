import json
from icecream import ic


def read_json(filename = 'dns.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            multiple_dns = json.load(f)
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다: {filename}")
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류 발생 (파일 내용 확인 필요): {e}")
    except KeyError as e:
        print(f"딕셔너리 키 오류 발생: {e}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")

    return multiple_dns

def write_json(dict, filename = "out.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict, f, indent=4, ensure_ascii=False)
    except TypeError as e:
        print(f"오류: JSON으로 변환할 수 없는 데이터 타입이 있습니다. {e}")
    except IOError as e:
        print(f"오류: 파일을 쓰거나 읽는 중에 문제가 발생했습니다. {e}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")

if __name__ == "__main__":
    multiple_dns = read_json()
    ic(multiple_dns)
    dict = {
        "naver.com":["123.134.123.1", "123.134.123.2"],
        "daum.net": ["123.134.13.1", "123.134.122.1"],
        "aaa.com": []
    }
    write_json(dict)