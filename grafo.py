# Criando a classe grafo e definindo seus métodos

class Grafo:

    def __init__(self, directed=False):
        self.directed = directed
        self.adj_list = dict()


    def __repr__(self): #representação usando a lista de adjacência
        graph_str =  ""
        for node, neighbors in self.adj_list.items():
            graph_str += f"{node} -> {neighbors}\n" 
        return graph_str


    def to_adj_matrix(self):    #representação usando matriz de adjacência
        nodes = self.get_nodes()
        index = {node: i for i, node in enumerate(nodes)}
        size = len(nodes)
        matrix = [[0 for _ in range(size)] for _ in range(size)]
        for from_node, neighbors in self.adj_list.items():
            for to_node in neighbors:
                if isinstance(to_node, tuple):
                    to, weight = to_node
                    matrix[index[from_node]][index[to]] = weight
                else:
                    matrix[index[from_node]][index[to_node]] = 1

        return matrix


    def to_adj_vector(self):
        vetor = []

        for node in self.get_nodes():
            vizinhos = list(self.get_neighbors(node))
            vetor.append([node, vizinhos])

        return vetor


    def add_node(self, node):   #adicionar vértice (ou nó)
        if node not in self.adj_list:
            self.adj_list[node] = set()
        else:
            raise ValueError("O vértice já existe")


    def remove_node(self, node):    #remover vértice
        if node not in self.adj_list:
            raise ValueError("O vértice não existe")
        
        for neighbors in self.adj_list.values():
            neighbors.discard(node)

        del self.adj_list[node]


    def add_edge(self, from_node, to_node, weight=None):    #adicionar aresta  
        if from_node not in self.adj_list:
            self.add_node(from_node)

        if to_node not in self.adj_list:
            self.add_node(to_node)

        if weight is None:
            self.adj_list[from_node].add(to_node)
            if not self.directed:
                self.adj_list[to_node].add(from_node)

        else:
            self.adj_list[from_node].add((to_node, weight))
            if not self.directed:
                self.adj_list[to_node].add((from_node, weight))


    def remove_edge(self, from_node, to_node):  #remover aresta
        if from_node in self.adj_list:
            if to_node in self.adj_list[from_node]:
                self.adj_list[from_node].remove(to_node)
            else:
                raise ValueError('Aresta não existe')
            
            if not self.directed:
                if from_node in self.adj_list[to_node]:
                    self.adj_list[to_node].remove(from_node)
        else:
            raise ValueError('Aresta não existe')

    def get_neighbors(self, node):  #detectar vizinhos
        return self.adj_list.get(node, set())


    def has_node(self, node):   #detectar se há vértices
        return node in self.adj_list


    def has_edge(self, from_node, to_node): #detectar arestas
        if from_node in self.adj_list:
            return to_node in self.adj_list[from_node]
        return False


    def get_nodes(self):    #detectar vértices e apresentar em lista
        return list(self.adj_list.keys())


    def get_edges(self):    #detectar arestas e apresentar em lista
        edges = []
        for from_node, neighbors in self.adj_list.items():
            for to_node in neighbors:
                edges.append((from_node, to_node))
        
        return edges


    def bfs(self, start):   #busca em largura
        visited = set()
        queue = [start]
        parent = {start: None}
        level = {start: 0}

        while queue:
            node = queue.pop(0)

            neighbors = self.get_neighbors(node)

            for neighbor in neighbors:
                if isinstance(neighbor, tuple):
                    neighbor = neighbor[0]

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    level[neighbor] = level[node] + 1
                    queue.append(neighbor)

        return parent, level


    def dfs(self, start):   #busca em profundidade
        visited = set()
        stack = [start]
        parent = {start: None}

        while stack:
            node = stack.pop()

            neighbors = self.get_neighbors(node)

            for neighbor in sorted(neighbors, reverse=True):
                if isinstance(neighbor, tuple):
                    neighbor = neighbor[0]

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    stack.append(neighbor)
                        
        return parent


    def dijkstra(self, start):  #busca usando dijkstra
        import heapq

        distances = {node: float('inf') for node in self.adj_list}
        distances[start] = 0
        heap = [(0, start)]

        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_distance > distances[current_node]:
                continue
            neighbors = self.adj_list.get(current_node, set())
            for neighbor in neighbors:
                if isinstance(neighbor, tuple):
                    to, weight = neighbor
                else:
                    to, weight = neighbor, 1
                distance = current_distance + weight
                if distance < distances[to]:
                    distances[to] = distance
                    heapq.heappush(heap, (distance, to))

        return distances


    def shortest_path(self, start, end):
        import heapq

        distances = {node: float('inf') for node in self.adj_list}
        previous = {node: None for node in self.adj_list}
        distances[start] = 0
        heap = [(0, start)]

        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_node == end:
                break
            if current_distance > distances[current_node]:
                continue
            neighbors = self.adj_list.get(current_node, set())
            for neighbor in neighbors:
                if isinstance(neighbor, tuple):
                    to, weight = neighbor
                else:
                    to, weight = neighbor, 1
                distance = current_distance + weight
                if distance < distances[to]:
                    distances[to] = distance
                    previous[to] = current_node
                    heapq.heappush(heap, (distance, to))
        
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous.get(node)
        path.reverse()
        if path[0] == start:
            return path
        return []
    

    def distance(self, start, end):   #cálculo de distância
        parent, level = self.bfs(start)
        return level.get(end, float('inf'))
    

    def diameter(self): #cálculo de diâmetro
        max_dist = 0

        for node in self.get_nodes():
            _, level = self.bfs(node)

            #maior distância alcançável a partir do nó
            if len(level) > 1: #ignora nós isolados
                current_max = max(level.values())
                max_dist = max(max_dist, current_max)
        
        return max_dist