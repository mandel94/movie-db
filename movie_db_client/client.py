from sqlalchemy.orm import sessionmaker
from repository.engine import engine
from data_model.model import Base



Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    session = Session()

