from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os

load_dotenv()


url_object = URL.create(
    "postgresql",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    database="movie_db"
    )

engine = create_engine(url_object)