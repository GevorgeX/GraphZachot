import enum
import pickle
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class COLOR(enum.Enum):
    RED = 1
    BLUE = 2
    WHITE = 3

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adjacency_list:
            self.add_node(node1)
        if node2 not in self.adjacency_list:
            self.add_node(node2)
        self.adjacency_list[node1].append(node2)
        self.adjacency_list[node2].append(node1)  # Для неориентированного графа

    def display(self):
        for node, neighbors in self.adjacency_list.items():
            print(f"{node}: {', '.join(map(str, neighbors))}")



def create_graph(vertices, edges):
    graph = Graph()
    for vertex in vertices:
        graph.add_node(vertex)
    for edge in edges:
        node1, node2 = edge
        graph.add_edge(node1, node2)
    return graph



with open('myjson.json', 'r') as f:
    file1 = json.load(f)

edges = file1["E"]

vertices = file1["V"]

graph = create_graph(vertices, edges)

colors = dict([(i , COLOR.WHITE) for i in vertices])

colors[vertices[0]] = COLOR.BLUE

# for key , value in graph.adjacency_list:
#     if colors[key]

# g = nx.Graph()
#
# for v in vertices:
#     g.add_node(v)
#
# for e in edges:
#     g.add_edge(*tuple(e))
#
#
#
#
# nx.draw(g , with_labels=True)
# plt.savefig("filename.png")


