import db
import os
from dotenv import load_dotenv
from scraper.run_scraper import run_scraper


load_dotenv()

start_page = int(os.getenv("SCRAPER_START_PAGE", False))
end_page = int(os.getenv("SCRAPER_END_PAGE", False))

# Entry point: runs backup, DB setup, then starts the scraper
if __name__ == '__main__':
    do_backup = os.getenv("SCRAPER_DO_BACKUP", "false").lower() == "true"
    if do_backup:
        db.backup_db()  # Run backup before updating DB only on scraper 1
    db.setup_db()    # Сreate the autoria_cars table (if not exists)
    run_scraper(start_page, end_page)  # for parallelized scraping in several containers