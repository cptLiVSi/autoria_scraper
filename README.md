# AutoRia Scraper

This project collects used car listings from [auto.ria.com](https://auto.ria.com/) and stores them in a PostgreSQL database. It is designed for daily automated scraping, with Docker-based deployment and backup functionality.

## Features

- Stores listings in PostgreSQL.
- Avoiding duplicates.
- Performs automatic daily database backups.
- Runs via Docker Compose.
- Logging for all scraping and parsing activities.

## Project Structure

```
.
├── db/
│   ├── __init__.py
│   ├── backup_db.py            # Dumps the database to /app/dumps
│   ├── config.py               # Loads env vars and configures SQLAlchemy
│   ├── models.py               # SQLAlchemy ORM model
│   └── setup_db.py             # Creates tables using ORM
│
├── scraper/
│   ├── __init__.py
│   ├── get_car_cards_urls.py   # Gets car listing URLs from index pages
│   ├── parse_car_page.py       # Parses detailed car data from each URL
│   └── run_scraper.py          # Main scraping logic
│
├── dumps/                      # PostgreSQL backup files (dump format)
├── logs/                       # Log files (scraping, cron)
├── .env                        # Environment variables
├── Dockerfile                  # Image for the scraper container
├── docker-compose.yml          # Services: scraper and PostgreSQL
├── main.py                     # Entry point: runs backup, setup, scraper
└── requirements.txt            # Python dependencies

```



## Build and start the application

```bash
docker compose up
```