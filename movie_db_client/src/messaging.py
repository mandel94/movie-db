import pika
import os
import sys


def callback(ch, method, properties, body):
    print(f"Received: {body}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue="hello_world")
    channel.basic_consume(queue="hello_world", on_message_callback=callback, auto_ack=True)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
            print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
