from sqlalchemy.orm import sessionmaker
from repository.engine import engine
from data_model.model import tables, get_table_info
from messaging import run_message_consumers

Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    # table_name = "studios"
    # get_table_info(tables[table_name], copy_to_clipboard=True)
    run_message_consumers() # Message publisher should be already running
    session = Session()

