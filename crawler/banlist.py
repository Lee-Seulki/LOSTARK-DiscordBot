import requests
from bs4 import BeautifulSoup

def get_banlist(name):

    INVEN_URL = "https://www.inven.co.kr/board/lostark/5355?query=list&p=1&sterm=&name=subject&keyword="

    response = requests.get(INVEN_URL + name)
    soup = BeautifulSoup(response.text, 'html.parser')

    board_list = soup.find("div", class_="board-list")
    data = board_list.find_all("td", class_="tit")

    ban_list = []

    for d in data[1:]:
        # 카테고리: a>span의 text
        # 제목: a에서 span을 제외한 텍스트
        tits = d.find_all("a", class_="subject-link")
        category = d.find_all("span", class_="category")
        for cate, tit in zip(category, tits):
            c = cate.get_text(strip=True)
            t = tit.text
            t = t.replace(c, '').lstrip().rstrip()

            link = tit["href"]

            ban_list.append([c, t, link])

    return ban_list