import logging
import subprocess
import os
import pandas as pd
from datetime import datetime as dt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from psycopg2.extras import execute_values

from get_car_cards_urls import get_car_cards_urls
from parse_car_page import parse_car_page


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


load_dotenv()

db = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

HEADERS = {'User-Agent': 'Mozilla/5.0'}

DB_URI = f'postgresql://{user}:{password}@{host}:{port}/{db}'
engine = create_engine(DB_URI)


def setup_db():
    folder = os.getcwd()
    print(folder)
    with open('/app/sql_query_create_table.txt', 'r') as f:
        crate_table_query = f.read()
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS autoria_cars"))
        conn.execute(text(crate_table_query))


def backup_db():
    backup_dir = "/app/dumps"
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = dt.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"backup-{timestamp}.dump")

    cmd = [
        "pg_dump",
        "-U", user,
        "-h", host,
        "-p", port,
        "-d", db,
        "-F", "c",
        "-f", backup_file
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    try:
        subprocess.run(cmd, env=env, check=True)
        logger.info(f"Backup saved to {backup_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed: {e}")


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
            df.to_sql('autoria_cars', engine, if_exists='append', index=False)
            logger.info(f"Saved {len(df)} cards")


if __name__ == '__main__':
    backup_db()
    setup_db()
    main()