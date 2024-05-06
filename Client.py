import pika
import random
import threading
import time

# Client configuration
HIGH_PRIORITY_QUEUE = 'high_priority'
LOW_PRIORITY_QUEUE = 'low_priority'


class Client:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.response = None

    def on_response(self, ch, method, properties, body):
        self.response = body.decode()

    def send_task(self, priority, execution_time, resource_cost):
        queue = HIGH_PRIORITY_QUEUE if priority == 'high' else LOW_PRIORITY_QUEUE
        message = f"{execution_time} {resource_cost}"
        self.response = None

        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue
            )
        )

        print(f"Sent task to {queue} queue: {message}")

        while self.response is None:
            self.connection.process_data_events()

        print(f"Received: {self.response}")

        if self.response == 'Insufficient Resources':
            print("Não devia acontecer nunca ta")
            return False
        return True

