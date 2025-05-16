import requests
from bs4 import BeautifulSoup

def get_car_cards_urls(url, headers):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    car_cards = soup.select('section.ticket-item')

    car_cards_urls = []

    for card in car_cards:
        url = card.select_one('a.address')['href']
        if "newauto" not in url:
            car_cards_urls.append(url)

    return car_cards_urls