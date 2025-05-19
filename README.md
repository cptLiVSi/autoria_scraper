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
├── Dockerfile                 # Image for the scraper app
├── docker-compose.yml         # Defines services: scraper and PostgreSQL
├── .env                       # Environment variables
├── main.py                    # Entry point: orchestrates scraping and saving
├── get_car_cards_urls.py      # Gets car card URLs from listing pages
├── parse_car_page.py          # Parses individual car detail pages
├── dumps/                     # Directory for database backups
├── logs/                      # Directory for log files
└── requirements.txt           # Python dependencies
```



## Build and start the application

```bash
docker compose up
```