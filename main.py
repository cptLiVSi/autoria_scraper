import db
from scraper.run_scraper import run_scraper


if __name__ == '__main__':
    db.backup_db()
    db.setup_db()
    run_scraper()