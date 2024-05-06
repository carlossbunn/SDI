import threading
from Server import Server
from Client import Client
import random
import time
from Graph import Graph

NUMBER_OF_SERVERS = 1
NUMBER_OF_TASKS = 5 #tasks enviadas por servidor
NUMBER_OF_CLIENTS = 10

servers = []

def test_server(n_server):
    for i in range(n_server):
        servers.append(Server())
        threading.Thread(target=servers[i].start).start()

def client_test():
    client = Client()
    print(f'Start client {threading.get_ident()}')
    for i in range(NUMBER_OF_TASKS):  
        execution_time = random.randint(1, 20)  
        resource_cost = random.randint(1, 10)   
        priority = 'high' if random.choice([True, False]) else 'low'

        if not client.send_task(priority, execution_time, resource_cost):
            print(f"{threading.get_ident()} - Stopping task generation: server out of resources")
            break


def test_client(number_of_clients,):
    for i in range(number_of_clients):
        threading.Thread(target=client_test).start()


server_thread = threading.Thread(target=test_server, args=(NUMBER_OF_SERVERS,))
client_thread = threading.Thread(target=test_client, args=(NUMBER_OF_CLIENTS,))

client_thread.start()
time.sleep(1)
server_thread.start()

client_thread.join()
server_thread.join()

print("All queues empty. Stopping servers.")

def build_graph(n_servers):
    graphs = []
    for i in range(n_servers):
        graphs.append(Graph(i+1))
    return graphs

graphs = build_graph(len(servers))
while True:
    for i in range(len(servers)):
        graphs[i].update_data(servers[i].get_task_data())