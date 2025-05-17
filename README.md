# AutoRia Scraper

This project collects used car listings from [auto.ria.com](https://auto.ria.com/) and stores them in a PostgreSQL database. It is designed for daily automated scraping, with Docker-based deployment and backup functionality.

## Features

- Stores listings in PostgreSQL.
- Avoiding duplicates with `ON CONFLICT DO UPDATE`.
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


## Usage

### Note:
During startup, you might see errors like:

```
scraper_7 Error   pull access denied for autoria_scraper, repository does not exist or may require 'docker login'
```
These appear because Docker first tries to pull the image from Docker Hub but it doesn’t exist there.
This is normal since the image is built locally by Docker Compose.

### 1. Build and start the application

```bash
docker compose up
```

### 2. Run for test purposes

Uncomment line 8 in .env and line 115 in main.py
```bash
docker compose up
```