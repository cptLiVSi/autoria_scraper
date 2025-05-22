import requests
from bs4 import BeautifulSoup
import logging


logger = logging.getLogger(__name__)

def get_car_cards_urls(page_url, headers):
    # Retry up to 3 times in case of connection errors
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            res = requests.get(page_url, headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            # Extract items with urls
            car_cards = soup.select('section.ticket-item')
            break
        except Exception as e:
            logger.error(f"Attempt {attempt} failed: {e}")
            if attempt == max_attempts:
                return []

    car_cards_urls = []

    for card in car_cards:
        # Extract links to car detail pages, skips new cars
        card_url = card.select_one('a.address')['href']
        if "newauto" not in card_url:
            car_cards_urls.append(card_url)

    if car_cards:
        continue_parsing = True
    else:
        continue_parsing = False
        # Save last page for manual inspection
        with open('app/last_page_content.html', 'w', encoding='utf-8') as f:
            f.write(res.text)

    return (continue_parsing, set(car_cards_urls))