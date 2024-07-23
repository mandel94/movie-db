import pika
import json
import sys
import os


def get_settings():
    with open("../settings/settings.json", mode="r") as f:
        # settings = json.load(settings_file)["crawling"]["messaging"]
        settings = json.load(f)["crawling"]["messaging"]
    return settings

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def connect_to_crawling_queue():
    settings = get_settings()
    # Connect to the crawling queue 
    rabbitmq_host = settings["RABBITMQ_HOST"]
    rabbitmq_queue = settings["RABBITMQ_QUEUE"]

    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(
        queue=rabbitmq_queue
    )  # It's a good practice to repeat declaring the queue in both programs.
    channel.basic_consume(
        queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True
    )
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def run_message_consumers():
    try:
        connect_to_crawling_queue()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


