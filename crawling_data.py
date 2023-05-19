import requests
from bs4 import BeautifulSoup

def get_character_info(character_name):
    LOSTARK_URL = 'https://lostark.game.onstove.com/Profile/Character/'
    response = requests.get(LOSTARK_URL + character_name)

    soup = BeautifulSoup(response.text, 'html.parser')

    info = soup.find_all("div", class_="profile-info")
    server = soup.find("span", class_="profile-character-info__server").text

    img_element = soup.find("img", class_="profile-character-info__img")

    character_info = {}

    character_info['server'] = server
    thumnail = img_element['src']
    character_info['thumnail'] = thumnail    

    def extract_info(class_name):
        if class_name == 'game-info__wisdom':
            # 영지는 두세번째 요소를 가져와야함
            element = info[0].find("div", class_=class_name)
            spans = element.find_all("span")
            if spans:
                wisdom = spans[1].text + ' ' + spans[2].text
                character_info[class_name] = wisdom
        else:
            # 영지가 아닌경우는 span 두번째 요소만
            element = info[0].find("div", class_=class_name)
            if element:
                spans = element.find_all("span")

                if len(spans) > 1 :
                    item = spans[1]
                    character_info[class_name] = item.text

                else:
                    character_info[class_name] = element.text

    # 원정대레벨
    extract_info("level-info__expedition")
    # 전투 레벨
    extract_info("level-info__item")
    # 장착 아이템레벨
    extract_info("level-info2__expedition")
    # 달성 아이템 레벨
    extract_info("level-info2__item")
    # 칭호
    extract_info("game-info__title")
    # 길드
    extract_info("game-info__guild")
    # PVP
    extract_info("level-info__pvp")
    # 영지
    extract_info("game-info__wisdom")

    # 각인 효과
    engraves = soup.find("div", class_="profile-ability-engrave")

    if engraves:
        spans = engraves.find_all("span")
        character_info["engraves"] = [span.text for span in spans]

    return character_info

def get_marishop_item():
    MARI_URL = 'https://lostark.game.onstove.com/Shop#mari'

    response = requests.get(MARI_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = []

    div_elements = soup.find_all('div', id='lui-tab1-2')
    list_items = div_elements[0].find_all('ul', class_='list-items')[0]

    names = list_items.find_all('span', class_='item-name')
    prices = list_items.find_all('span', class_='amount')

    for price, name in zip(prices, names):
        items.append('💎' + price.text + ' ' + name.text)
    
    return items

get_marishop_item()