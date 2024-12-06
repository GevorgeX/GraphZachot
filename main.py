import enum
import json
import networkx as nx
import matplotlib.pyplot as plt

class COLOR(enum.Enum):
    RED = 1
    BLUE = 2
    WHITE = 3

class GraphList:
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
        self.adjacency_list[node2].append(node1)

    def display(self):
        for node, neighbors in self.adjacency_list.items():
            print(f"{node}: {', '.join(map(str, neighbors))}")

def create_graph(vertices, edges):
    graph = GraphList()
    for vertex in vertices:
        graph.add_node(vertex)
    for edge in edges:
        node1, node2 = edge
        graph.add_edge(node1, node2)
    return graph

def colored_graph(graph):
    colors = dict([(i , COLOR.WHITE) for i in vertices])
    colors[vertices[0]] = COLOR.BLUE

    for key , value in graph.adjacency_list.items():
        for childs in value:
            if colors[childs] == COLOR.WHITE:
                if colors[key] == COLOR.RED:
                    colors[childs] = COLOR.BLUE
                else:
                    colors[childs] = COLOR.RED
            
            elif colors[childs] == colors[key]:
                return (False, colors)
            
    return (True, colors)

def draw_bitpart(vertices, edges, colors):
    G = nx.Graph()
    G.add_nodes_from(vertices)

    pos = {}
    leftside = [v for v in vertices if colors[v] == COLOR.RED ]
    rightside = [v for v in vertices if colors[v] == COLOR.BLUE ]

    for i, v in enumerate(leftside):
        pos[v] = (1,i)
    for i, v in enumerate(rightside):
        pos[v] = (0,i)

    for e in edges:
        G.add_edge(*tuple(e))
    nx.draw(G , 
            with_labels = True, 
            pos = pos,
            node_color = "red",
            node_size = 1000)
    plt.savefig("filename.png")


if __name__ == "__main__":
    with open('myjson.json', 'r') as f:
        file = json.load(f)
    edges = file["E"]
    vertices = file["V"]
    graph = create_graph(vertices, edges)

    isBin,colors  = colored_graph(graph)

    if isBin:
        draw_bitpart(vertices, edges, colors)
    else:
        # TODO
        pass