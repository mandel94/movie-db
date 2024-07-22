from typing import Any
import pika


LOGS_FOLDER = 'logs/'
SPIDERS_LOGS_FILE = '../' + LOGS_FOLDER + 'spiders_logs.log'
SPIDERS_ERROR_LOGS_FILE = '../' + LOGS_FOLDER + 'spiders_error_logs.log'


spider_logs_file = open(SPIDERS_LOGS_FILE, 'w')
spider_error_logs_file = open(SPIDERS_ERROR_LOGS_FILE, 'w')


# def write_on_file(file: Any, message: str) -> None:
#     with file as f:
#         f.write(message)


def send_message(message: str, queue_name: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()
    # write_on_file(spider_logs_file, f"Sent message: {message}\n")
    print(f"Sent message: {message}\n")