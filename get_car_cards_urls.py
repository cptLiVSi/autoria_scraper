import requests
from bs4 import BeautifulSoup
import logging


logger = logging.getLogger(__name__)

def get_car_cards_urls(url, headers):
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            car_cards = soup.select('section.ticket-item')
            break
        except Exception as e:
            logger.error(f"Attempt {attempt} failed: {e}")
            if attempt == max_attempts:
                return []

    car_cards_urls = []

    for card in car_cards:
        url = card.select_one('a.address')['href']
        if "newauto" not in url:
            car_cards_urls.append(url)

    return car_cards_urls