from typing import Any


LOGS_FOLDER = 'logs/'
SPIDERS_LOGS_FILE = '../' + LOGS_FOLDER + 'spiders_logs.log'
SPIDERS_ERROR_LOGS_FILE = '../' + LOGS_FOLDER + 'spiders_error_logs.log'


spider_logs_file = open(SPIDERS_LOGS_FILE, 'w')
spider_error_logs_file = open(SPIDERS_ERROR_LOGS_FILE, 'w')


def write_on_file(file: Any, message: str) -> None:
    with file as f:
        f.write(message)


