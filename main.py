import db
from scraper.run_scraper import run_scraper


# Entry point: runs backup, DB setup, then starts the scraper
if __name__ == '__main__':
    db.backup_db() # Run backup before updating DB
    db.setup_db()  # Сreate the autoria_cars table (if not exists)
    run_scraper()