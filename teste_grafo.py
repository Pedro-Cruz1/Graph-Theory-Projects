# teste_grafo.py

from grafo import Grafo  # ajuste o nome do arquivo se necessário

g = Grafo(directed=False)

# Adicionando nós
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

# Adicionando arestas
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")

# Teste de impressão
print("Lista de adjacência:")
print(g)

# Teste BFS
print("BFS a partir de A:")
print(g.bfs("A"))

# Teste DFS
print("DFS a partir de A:")
print(g.dfs("A"))

# Teste Dijkstra (sem peso → assume peso 1)
print("Dijkstra a partir de A:")
print(g.dijkstra("A"))

# Teste menor caminho
print("Menor caminho de A até D:")
print(g.shortest_path("A", "D"))

# Teste matriz de adjacência
print("Matriz de adjacência:")
matrix = g.to_adj_matrix()
for row in matrix:
    print(row)

# Teste remoção de aresta
g.remove_edge("A", "B")
print("Após remover aresta A-B:")
print(g)

# Teste remoção de nó
g.remove_node("C")
print("Após remover nó C:")
print(g)