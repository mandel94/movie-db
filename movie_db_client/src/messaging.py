import pika
import json
import sys
import os


def get_settings():
    with open("../settings/settings.json", mode="r") as f:
        # settings = json.load(settings_file)["crawling"]["messaging"]
        settings = json.load(f)["crawling"]["messaging"]
    return settings


def create_rabbitmq_connection(host, port, username, password):
    try:
        credentials = pika.PlainCredentials(username, password)
        connection_params = pika.ConnectionParameters(
            host=host, port=port, virtual_host="/", credentials=credentials
        )
        connection = pika.BlockingConnection(connection_params)
        return connection
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        raise



class RabbitMQAPI:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self, host, port, username, password):
        self.connection = create_rabbitmq_connection(host, port, username, password)

    def create_channel(self):
        if not self.connection:
            raise Exception("Connection not found on object")
        self.channel = self.connection.channel()
        return self

    def subscribe_to_queue(self, queue, callback):
        if not self.channel:
            print("Channel not found on object")
            self.create_channel()
            print("Channel created")
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        print(f"Subscribed to queue {queue}")
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
    

   
