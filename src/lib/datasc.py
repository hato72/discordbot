import requests
from bs4 import BeautifulSoup


# url = "https://www.ikaclo.jp/3/weapons/"
# res = requests.get(url)
# soup = BeautifulSoup(res.text, 'html.parser')
# weapons = []
# for weapon in soup.select('tr.weapons__item td.-name a.inner'):
#     weapons.append(weapon.text.replace('\n          ',''))
# print(weapons)



def weaponlist(): #スプラトゥーン3の武器一覧をhttps://www.ikaclo.jp/3/weapons/ から取得
    url = "https://www.ikaclo.jp/3/weapons/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    weapons = []
    for weapon in soup.select('tr.weapons__item td.-name a.inner'):
        weapons.append(weapon.text.replace('\n          ',''))
    return weapons

