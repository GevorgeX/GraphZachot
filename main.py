import enum
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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

def find_circle(graph_dict):
    color = {}  # Хранит цвет вершины: 0 или 1
    parent = {}  # Хранит предков для восстановления пути

    for start in graph_dict:  # Проверяем каждую компоненту связности
        if start not in color:
            queue = deque([start])
            color[start] = 0  # Начинаем с цвета 0
            parent[start] = None  # У корневой вершины нет предка

            while queue:
                current = queue.popleft()

                for neighbor in graph_dict[current]:
                    if neighbor not in color:  # Если вершина ещё не окрашена
                        color[neighbor] = 1 - color[current]  # Красим в другой цвет
                        parent[neighbor] = current
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:  # Найден нечётный цикл
                        # Восстановим цикл
                        cycle = []
                        u, v = current, neighbor

                        # Идём назад от `u` и `v` до их общего предка
                        path_u, path_v = [], []
                        while u is not None:
                            path_u.append(u)
                            u = parent[u]
                        while v is not None:
                            path_v.append(v)
                            v = parent[v]

                        # Найдём их общий предок
                        path_u.reverse()
                        path_v.reverse()
                        i = 0
                        while i < len(path_u) and i < len(path_v) and path_u[i] == path_v[i]:
                            i += 1

                        # Формируем нечётный цикл
                        cycle.extend(path_u[i-1:][::-1])  # Часть пути u
                        cycle.extend(path_v[i:])  # Часть пути v
                        cycle.append(current)  # Добавляем текущее ребро
                        return cycle
    return None  # Нечётный цикл не найден


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
        circle = find_circle(graph.adjacency_list)
        draw_graph_with_circle(vertices, edges, circle)
