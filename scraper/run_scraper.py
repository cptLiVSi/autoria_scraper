import logging
from sqlalchemy.orm import Session
from db.models import AutoriaCar

import db
from .get_car_cards_urls import get_car_cards_urls
from .parse_car_page import parse_car_page


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def run_scraper():
    processed_urls = set()
    page = 0
    car_cards_urls_on_page = True  #  value to enter the loop for the 1st time
    while car_cards_urls_on_page:
        page += 1
        url = f'https://auto.ria.com/car/used/?page={page}'
        logger.info(f"Loading list of cars from page {page}")
        try:
            car_cards_urls_on_page = get_car_cards_urls(url, headers=HEADERS)
        except Exception as e:
            logger.error(f"Failed to get car card URLs from page {page}: {e}")
            continue
        if car_cards_urls_on_page:
            cars_to_process = car_cards_urls_on_page - processed_urls
            processed_urls.update(cars_to_process)

            logger.info(f"{len(cars_to_process)} cards to parse")
            if len(car_cards_urls_on_page) > len(cars_to_process):
                logger.info(f"{len(car_cards_urls_on_page) - len(cars_to_process)} already in db")

            page_result = process_cars_on_page(cars_to_process)
            if page_result:
                save_to_db(page_result)
    logger.info("Scraping completed")


def process_cars_on_page(cars_to_process):
    page_result = []
    for car_url in cars_to_process:
        try:
            result = parse_car_page(car_url, HEADERS)
        except Exception as e:
            logger.error(f"Error parsing {car_url}: {e}, {e.__class__}")
            continue
        page_result.append(result)
    return page_result


def save_to_db(page_result):
    with Session(db.config.ENGINE) as session:
        for item in page_result:
            car = AutoriaCar(**item)
            session.merge(car)
        session.commit()
    logger.info(f"Saved {len(page_result)} cards")