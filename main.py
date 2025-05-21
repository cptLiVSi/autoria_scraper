import logging
import pandas as pd

import db
from get_car_cards_urls import get_car_cards_urls
from parse_car_page import parse_car_page


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def main():
    processed_urls = set()
    page = 0
    while True:
        page += 1
        url = f'https://auto.ria.com/car/used/?page={page}'
        logger.info(f"Loading list of cars from page {page}")
        try:
            car_cards_urls_on_page = get_car_cards_urls(url, headers=HEADERS)
            if not car_cards_urls_on_page:
                break
        except Exception as e:
            logger.error(f"Failed to get car card URLs from page {page}: {e}")
            continue

        cars_to_process = car_cards_urls_on_page - processed_urls
        processed_urls.update(cars_to_process)


        logger.info(f"{len(cars_to_process)} cards to parse")
        if len(car_cards_urls_on_page) > len(cars_to_process):
            logger.info(f"{len(car_cards_urls_on_page) - len(cars_to_process)} already in db")

        page_result = []

        for car_url in cars_to_process:
            try:
                result = parse_car_page(car_url, HEADERS)
            except Exception as e:
                logger.error(f"Error parsing {car_url}: {e}, {e.__class__}")
                continue
            page_result.append(result)
        if page_result:
            df = pd.DataFrame(page_result)
            df.to_sql('autoria_cars', db.config.ENGINE, if_exists='append', index=False)
            logger.info(f"Saved {len(df)} cards")


if __name__ == '__main__':
    db.backup_db()
    db.setup_db()
    main()