import matplotlib.pyplot as plt
import numpy as np
import time

class Graph:
    def __init__(self, id):
        self.server_id = id
        self.fig, self.ax = plt.subplots()
        self.tasks = []
        self.fig.canvas.set_window_title(f'Server {id}')

    def update_data(self, tasks):
        self.tasks = tasks
        self.plot_gantt()

    def plot_gantt(self):
        self.ax.clear()
        time_points = []
        cost_points = []
        for task in self.tasks:
            start = task[2]
            end = task[3]
            resource_cost = task[1]
            time_points.append(start)
            cost_points.append(0)
            time_points.append(start)
            cost_points.append(resource_cost)
            time_points.append(end)
            cost_points.append(resource_cost)
            time_points.append(end)
            cost_points.append(0)
        
        self.ax.fill_between(time_points, cost_points, color='blue', alpha=0.3, linewidth=0)
        
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Task Cost')
        self.ax.set_title('Consumo do server por tempo')
        plt.pause(0.01)
