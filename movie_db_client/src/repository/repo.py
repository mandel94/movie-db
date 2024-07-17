from abc import ABC, abstractmethod
from ..data_model.model import tables
from sqlalchemy import insert, select, update, delete


class Repository:

    def __init__(self, session) -> None:
        self.session = session

    def create(self, table_name: str, data: dict) -> None:
        with self.session.begin() as transaction:
            self.session.execute(insert(tables[table_name]).values(data))
            
    def read(self, table_name: str, column: str, value) -> None:
        # At the end of the context below, assuming no exceptions were raised, 
        # any pending objects will be flushed to the database and the database 
        # transaction will be committed. If an exception was raised within the 
        # above block, then the transaction would be rolled back 
        # --> SEE https://docs.sqlalchemy.org/en/20/orm/session_transaction.html 
        with self.session.begin():
            self.session.execute(select(tables[table_name]).where(column == value))

    def update(self, table_name: str, column: str, value, data: dict) -> None:
        with self.session.begin():
            self.session.execute(
                update(tables[table_name]).where(column == value).values(data)
            )

    def delete(self, table_name: str, column: str, value) -> None:
        with self.session.begin():
            self.session.execute(delete(tables[table_name]).where(column == value))
