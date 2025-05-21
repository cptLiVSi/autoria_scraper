from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DB = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")

DB_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
ENGINE = create_engine(DB_URI)