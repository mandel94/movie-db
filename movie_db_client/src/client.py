from sqlalchemy.orm import sessionmaker
from repository.engine import engine
from data_model.model import tables, get_table_info
from sqlalchemy import Table


Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    table_name = "studios"
    get_table_info(tables[table_name], copy_to_clipboard=True)
    session = Session()

