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
        for child in value:
            if colors[child] == COLOR.WHITE:
                if colors[key] == COLOR.RED:
                    colors[child] = COLOR.BLUE
                else:
                    colors[child] = COLOR.RED
            
            elif colors[child] == colors[key]:
                return (False, (child, key))
    
    for i in vertices:
        if  colors[i] == COLOR.WHITE:
            colors[i] = COLOR.RED 

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
    plt.savefig(output_name)

def find_circle(grap , vert1 ,vert2):
    def dfs(node, target, visited, path):
        visited.add(node)
        path.append(node)
        for neighbor in grap[node]:
            if neighbor == target and len(path) > 2:
                path.append(neighbor)
                return True
            if neighbor not in visited:
                if dfs(neighbor, target, visited, path):
                    return True

        path.pop()
        return False

    # Find a cycle starting from v1 that contains v2
    for start in [vert1, vert2]:
        visited = set()
        path = []
        if dfs(start, start, visited, path) and vert1 in path and vert2 in path:
            return path[1:]

    return None

def draw_graph_with_circle(vertices, edges, circle):
    G = nx.Graph()
    G.add_nodes_from(vertices)

    for e in edges:
        G.add_edge(*tuple(e))

    color_map = ["red" if i in circle else "blue" for i in vertices ]
    pos = nx.spring_layout(G)

    nx.draw(G , 
            with_labels = True, 
            pos=pos,
            node_color = color_map,

            node_size = 400)
    plt.savefig(output_name)

if __name__ == "__main__":
    file_name = input("Get file name(json): ")
    with open(file_name, 'r') as f:
        file = json.load(f)
    edges = file["E"]
    vertices = file["V"]
    graph = create_graph(vertices, edges)

    
    output_name = input("Output png name: ")
    isBin,res  = colored_graph(graph)
    if isBin:
        print("Yes your graph is bitpart")
        draw_bitpart(vertices, edges, res)
    else:
        print(f"No your graph is not bitpart")
        circle = find_circle(graph.adjacency_list , res[0] ,res[1])
        draw_graph_with_circle(vertices, edges, circle)
