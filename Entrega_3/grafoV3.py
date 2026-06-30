from collections import deque

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
            for to_node, weight in neighbors:
                    matrix[index[from_node]][index[to_node]] = weight

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
        for neighbors in self.adj_list.values():

            edge_to_remove = None

            for neighbor, weight in neighbors:
                if neighbor == node:
                    edge_to_remove = (neighbor, weight)
                    break

            if edge_to_remove:
                neighbors.remove(edge_to_remove)
        del self.adj_list[node]


    def add_edge(self, from_node, to_node, weight=1):   #adicionar aresta
        if from_node not in self.adj_list:
            self.add_node(from_node)

        if to_node not in self.adj_list:
            self.add_node(to_node)

        self.adj_list[from_node].add((to_node, weight))

        if not self.directed:
            self.adj_list[to_node].add((from_node, weight))


    def remove_edge(self, from_node, to_node):

        if from_node not in self.adj_list:
            raise ValueError("Aresta não existe")

        edge_to_remove = None

        for neighbor, weight in self.adj_list[from_node]:
            if neighbor == to_node:
                edge_to_remove = (neighbor, weight)
                break

        if edge_to_remove is None:
            raise ValueError("Aresta não existe")

        self.adj_list[from_node].remove(edge_to_remove)

        if not self.directed:

            reverse_edge = None

            for neighbor, weight in self.adj_list[to_node]:
                if neighbor == from_node:
                    reverse_edge = (neighbor, weight)
                    break

            if reverse_edge:
                self.adj_list[to_node].remove(reverse_edge)

    def get_neighbors(self, node):  #detectar vizinhos
        return self.adj_list.get(node, set())


    def has_node(self, node):   #detectar se há vértices
        return node in self.adj_list


    def has_edge(self, from_node, to_node):
        if from_node in self.adj_list:
            for neighbor, weight in self.adj_list[from_node]:
                if neighbor == to_node:
                    return True

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
        
        if start not in self.adj_list:
            raise ValueError("Vértice inicial não existe.")

        visited = set([start])
        queue = deque([start])

        parent = {start: None}
        level = {start: 0}

        while queue:
            node = queue.popleft()

            for neighbor, weight in self.get_neighbors(node):

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    level[neighbor] = level[node] + 1
                    queue.append(neighbor)

        return parent, level


    def dfs(self, start):

        if start not in self.adj_list:
            raise ValueError("Vértice inicial não existe.")

        visited = set([start])
        stack = [start]

        parent = {start: None}

        while stack:
            node = stack.pop()

            neighbors = sorted(self.get_neighbors(node), reverse=True)

            for neighbor, weight in neighbors:

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    stack.append(neighbor)

        return parent
    

    def dijkstra(self, start):  #busca usando dijkstra (com heap)
        
        if start not in self.adj_list:
            raise ValueError("Vértice inicial não existe.")

        import heapq

        # verifica se há pesos negativos
        for neighbors in self.adj_list.values():
            for neighbor, weight in neighbors:
                if weight < 0:
                    raise ValueError(
                        "A biblioteca ainda não implementa caminhos mínimos com pesos negativos"
                    )

        distances = {node: float('inf') for node in self.adj_list}
        parent = {node: None for node in self.adj_list}

        distances[start] = 0
        heap = [(0, start)]

        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_distance > distances[current_node]:
                continue
            neighbors = self.adj_list.get(current_node, set())
            for to, weight in neighbors:

                distance = current_distance + weight
                if distance < distances[to]:
                    distances[to] = distance
                    parent[to] = current_node

                    heapq.heappush(heap, (distance, to))

        return distances, parent

    def dijkstra_no_heap(self, start): #busca usando dijkstra (sem heap)

        # verifica pesos negativos
        for neighbors in self.adj_list.values():
            for neighbor, weight in neighbors:
                if weight < 0:
                    raise ValueError(
                        "A biblioteca ainda não implementa caminhos mínimos com pesos negativos"
                    )

        distances = {node: float('inf') for node in self.adj_list}

        distances[start] = 0

        visited = set()

        while len(visited) < len(self.adj_list):

            # encontra o vértice não visitado com menor distância
            current_node = None
            current_distance = float('inf')

            for node in self.adj_list:

                if node not in visited and distances[node] < current_distance:
                    current_distance = distances[node]
                    current_node = node

            # se não houver mais alcançáveis
            if current_node is None:
                break

            visited.add(current_node)

            # relaxamento das arestas
            for neighbor, weight in self.adj_list[current_node]:

                if neighbor not in visited:

                    distance = distances[current_node] + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance

        return distances

    def bellman_ford(self, start):      #Algoritmo de Bellman-Ford

        if start not in self.adj_list:
            raise ValueError("Vértice inicial não existe.")

       
        distances = {node: float('inf') for node in self.adj_list}
        parent = {node: None for node in self.adj_list}

        distances[start] = 0

        vertices = self.get_nodes()

    
        for i in range(len(vertices) - 1):

            if i % 1000 == 0:
                print(f"Bellman-Ford: iteração {i}/{len(vertices)-1}")

            updated = False

            for u in vertices:

                # Otimização: ignora vértices ainda inalcançáveis
                if distances[u] == float('inf'):
                    continue

                for v, weight in self.adj_list[u]:

                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        parent[v] = u
                        updated = True

            # Otimização 1: parada antecipada
            if not updated:
                print(f"Parada antecipada na iteração {i}")
                break

        # Verificação de ciclo negativo
        negative_cycle = False

        for u in vertices:

            if distances[u] == float('inf'):
                continue

            for v, weight in self.adj_list[u]:

                if distances[u] + weight < distances[v]:
                    negative_cycle = True
                    break

            if negative_cycle:
                break

        return distances, parent, negative_cycle


    def shortest_path(self, start, end):
        import heapq

        # verifica se há pesos negativos
        for neighbors in self.adj_list.values():
            for neighbor, weight in neighbors:
                if weight < 0:
                    raise ValueError(
                        "A biblioteca ainda não implementa caminhos mínimos com pesos negativos"
                    )

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
            for to, weight in neighbors:
                
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
        distances, _ = self.dijkstra(start)
        return distances.get(end, float('inf'))
    

    def diameter(self): #cálculo de diâmetro
        max_dist = 0

        for node in self.get_nodes():
            distances, _ = self.dijkstra(node)

            # remove infinitos (não alcançáveis)
            reachable = [
                d for d in distances.values()
                if d != float('inf')
            ]

            if reachable:
                current_max = max(reachable)
                max_dist = max(max_dist, current_max)

        return max_dist