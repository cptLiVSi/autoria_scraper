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
START_URL = 'https://auto.ria.com/car/used/?page=1'

DB_URI = f'postgresql://{user}:{password}@{host}:{port}/{db}'
engine = create_engine(DB_URI)

def setup_db():
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS autoria_cars"))
        conn.execute(text("""
            CREATE TABLE autoria_cars (
                url TEXT PRIMARY KEY,
                title TEXT,
                price_usd INTEGER,
                odometer INTEGER,
                username TEXT,
                phone_number TEXT,
                image_url TEXT,
                images_count INTEGER,
                car_number TEXT,
                car_vin TEXT,
                datetime_found TIMESTAMPTZ
            );
        """))
    logger.info("Database table 'autoria_cars' created (old table dropped)")


def insert_ignore_duplicates(df, engine, table_name):
    if df.empty:
        return

    conn = engine.raw_connection()
    try:
        with conn.cursor() as cur:
            cols = list(df.columns)
            values = [tuple(x) for x in df.to_numpy()]
            insert_sql = f"""
                INSERT INTO {table_name} ({', '.join(cols)})
                VALUES %s
                ON CONFLICT (url) DO NOTHING
            """
            execute_values(cur, insert_sql, values)
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting data into '{table_name}': {e}")
    finally:
        conn.close()


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
    for page in range(1,3):

        url = f'https://auto.ria.com/car/used/?page={page}'
        logger.info(f"Loading list of cars from page {page}")
        try:
            car_cards_urls_on_page = get_car_cards_urls(url, headers=HEADERS)
        except Exception as e:
            logger.error(f"Failed to get car card URLs from page {page}: {e}")
            continue
        logger.info(f"{len(car_cards_urls_on_page)} cards to parse")

        page_result = []

        for car_url in car_cards_urls_on_page:
            logger.info(f"Parsing {car_url}")
            try:
                result = parse_car_page(car_url, HEADERS)
            except Exception as e:
                logger.error(f"Error parsing {car_url}: {e}")
                continue
            page_result.append(result)
        if page_result:
            df = pd.DataFrame(page_result)
            insert_ignore_duplicates(df, engine, 'autoria_cars')
            logger.info(f"Saved {len(df)} cards")


if __name__ == '__main__':
    backup_db()
    setup_db()
    main()