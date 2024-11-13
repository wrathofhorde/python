import parse
import requests
from icecream import ic

# ic.disable()

def scrap(url):
  res = requests.get(url, headers={"User-Agent" : 
                                    '''
                                      Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
                                      AppleWebKit/537.36 (KHTML, like Gecko) 
                                      Chrome/128.0.0.0 Safari/537.36
                                    '''})
  
  if res.status_code != 200:
    ic(res.status_code)
    ic(res.content.decode('utf-8'))
    return ""
  
  ic(res.text)
  return res.text

if __name__ == "__main__":
  url = "https://www.lazyfoo.net/SDL_tutorials/"
  html = scrap(url)

  balance = parse.get_final(html)
  print(balance)