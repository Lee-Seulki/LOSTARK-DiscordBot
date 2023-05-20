import requests
from bs4 import BeautifulSoup

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