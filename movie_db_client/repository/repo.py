from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def delete(self, data):
        pass


class MovieRepository(Repository):
    def __init__(self, db):
        self.db = db # connection to db

    def create(self, data):
        self.db.create(data)

    def read(self, data):
        return self.db.read(data)

    def update(self, data):
        self.db.update(data)

    def delete(self, data):
        self.db.delete(data)