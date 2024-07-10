import datetime
from typing import Any
from exceptions import handle_error
import os

LOGS_FOLDER = 'logs/'
WIKI_CLIENT_LOGS_PATH = LOGS_FOLDER + 'wiki_client.log'
WIKI_CLIENT_ERROR_LOGS_PATH = LOGS_FOLDER + 'wiki_client_errors.log'
OTHER_LOGS_PATH = 'logs/other.log'





def write_time(func):
    """Decorator to write the time of the function call to a file"""
    def decorator(file: Any, *args, **kwargs):
        with open(file, mode='a') as f:
            f.write(f"Time: {datetime.datetime.now()}\n")
        return func(file, *args, **kwargs)
    return decorator

@write_time
def write_to_file(file: Any, message: str) -> None:
    # Get absolute path of the file
    abs_path = file.name
    # Write to the file

# TODO Debug --> Why the following functions are not writing to the file? 
def write_to_wiki_client_logs(message: str) -> None:
    # Get absolute path of the file
    with open(os.path.abspath(WIKI_CLIENT_LOGS_PATH), mode='a') as f:
        f.write(message)

def write_to_wiki_client_error_logs(message: str) -> None:
    with open(os.path.abspath(WIKI_CLIENT_ERROR_LOGS_PATH), mode='a') as f:
        f.write(message)