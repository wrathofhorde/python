from bs4 import BeautifulSoup
from icecream import ic

# ic.disable()

def get_final(contents):
  html = BeautifulSoup(contents, "html.parser")
  trs = html.find_all(name="tr")

  strFinalBalance = "Final Balance"

  for tr in trs:
    tds = tr.findChildren("td", recursive=False)
    ic(len(tds))
    ic(tds)

    if len(tds) > 1 and tds[0].getText() == strFinalBalance:
      texts = tds[1].getText().split()
      ic(texts)
      ic(texts[0])

      if '.' in texts[0]:
        return texts[0]

  return "none"

if __name__ == "__main__":
  with open('1.html') as file:
    contents = file.read()
  # contents = ""
  balance = get_final(contents=contents)
  print(balance)