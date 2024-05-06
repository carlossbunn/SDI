import pika
import threading
import time
import random

HIGH_PRIORITY_QUEUE = 'high_priority'
LOW_PRIORITY_QUEUE = 'low_priority'

class Server:
    def __init__(self):
        self.tasks_data = []
        self.resources = random.choice([100, 200])
        self.connection = None
        self.channels = {}
        self.empty_queue = [False, False]

    def process_task(self, ch, method, properties, body):
        start_task_process = time.time()
        
        execution_time, resource_cost = map(int, body.decode().split())
        print(f"Processing task {threading.get_ident()}: Execution Time: {execution_time}s, Resource Cost: {resource_cost}")

        if self.resources >= resource_cost:
            self.resources -= resource_cost
            print(f"Resources remaining: {self.resources}")
            time.sleep(execution_time)
            message = 'Task Completed'
        else:
            while not self.resources >= resource_cost:
                print('Waiting for resources...')
                continue            
            print(f"Resources remaining: {self.resources}")
            time.sleep(execution_time) 
            message = 'Task Completed'

        ch.basic_ack(delivery_tag=method.delivery_tag)

        if properties.reply_to:
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=message
            )
        self.resources += resource_cost
        
        end_task_process = time.time()
        self.tasks_data.append([execution_time , resource_cost, start_task_process, end_task_process])

    def is_priority_queue_empty(self):
        return self.empty_queue[0]

    def is_secondary_queue_empty(self):
        return self.empty_queue[1]

    def consume_priority_queue(self):
        try:
            while True:
                if self.connection is None or self.connection.is_closed:
                    self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

                channel = self.connection.channel()
                channel.queue_declare(queue=HIGH_PRIORITY_QUEUE)

                channel.basic_consume(queue=HIGH_PRIORITY_QUEUE, on_message_callback=self.process_task)
                self.channels[HIGH_PRIORITY_QUEUE] = channel
                print(f"Thread {threading.current_thread().name} consuming tasks from {HIGH_PRIORITY_QUEUE}...")
                channel.start_consuming()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
        finally:
            print("Priority queue empty. Stopping server.")
            self.connection.close()  # Fecha a conexão com o RabbitMQ

    def consume_secondary_queue(self):
        try:
            while True:
                if self.connection is None or self.connection.is_closed:
                    self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

                channel = self.connection.channel()
                
                channel.queue_declare(queue=LOW_PRIORITY_QUEUE)

                channel.basic_consume(queue=LOW_PRIORITY_QUEUE, on_message_callback=self.process_task)
                self.channels[LOW_PRIORITY_QUEUE] = channel
                print(f"Thread {threading.current_thread().name} consuming tasks from {LOW_PRIORITY_QUEUE}...")
                channel.start_consuming()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
        finally:
            print("Secondary queue empty. Stopping server.")
            self.connection.close()

    def is_priority_queue_empty(self):
        return self.empty_queue[0]

    def is_secondary_queue_empty(self):
        return self.empty_queue[1]


    def start(self):
        high_priority_thread = threading.Thread(target=self.consume_priority_queue)
        secondary_thread = threading.Thread(target=self.consume_secondary_queue)
        
        high_priority_thread.start()
        secondary_thread.start()

        print(f"Server {threading.get_ident()} started...")

        high_priority_thread.join()
        secondary_thread.join()

    def get_task_data(self):
        return self.tasks_data
