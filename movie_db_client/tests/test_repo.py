import pytest
from src.repository.engine import engine
from sqlalchemy import create_engine, URL
import os


@pytest.fixture(scope="module")
def db_url():
    url = URL.create(
        "postgresql",
        username="postgres",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5433", # Port of the test database
        database="test_db"
        )
    return url


@pytest.fixture(scope="module")
def engine(db_url):
    engine = create_engine(db_url)
    return engine
    


class TestEngine:
    def test_creation(self, engine):
        assert engine is not None
        assert str(type(engine)) == "<class 'sqlalchemy.engine.base.Engine'>"

    def test_connection(self, engine):
        connection = engine.connect()
        assert connection is not None
        connection.close()


# class TestRepository:



