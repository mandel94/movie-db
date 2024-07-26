from typing import Any
import pika
import logging
import json


LOGS_FOLDER = 'logs/'
SPIDERS_LOGS_FILE = '../' + LOGS_FOLDER + 'spiders_logs.log'
SPIDERS_ERROR_LOGS_FILE = '../' + LOGS_FOLDER + 'spiders_error_logs.log'


spider_logs_file = open(SPIDERS_LOGS_FILE, 'w')
spider_error_logs_file = open(SPIDERS_ERROR_LOGS_FILE, 'w')


# def write_on_file(file: Any, message: str) -> None:
#     with file as f:
#         f.write(message)


def _load_settings() -> None:
    try:
        with open("../settings/settings.json", mode="r") as f:
            settings = json.load(f)
            return settings["crawling"]["messaging"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load settings: {e}")
        raise e




def create_rabbitmq_connection(host, port, username, password):
    settings = _load_settings()
    try:
        credentials = pika.PlainCredentials(username, password)
        connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host='/',
            credentials=credentials
        )
        connection = pika.BlockingConnection(connection_params)
        return connection
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        raise

