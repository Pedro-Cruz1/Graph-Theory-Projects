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
print("\nLista de adjacência:")
print(g)

# Teste BFS
print("\nBFS a partir de A:")
print(g.bfs("A"))

# Teste DFS
print("\nDFS a partir de A:")
print(g.dfs("A"))

# Teste Dijkstra (sem peso → assume peso 1)
print("\nDijkstra a partir de A:")
print(g.dijkstra("A"))

# Teste menor caminho
print("\nMenor caminho de A até D:")
print(g.shortest_path("A", "D"))

# Teste matriz de adjacência
print("\nMatriz de adjacência:")
matrix = g.to_adj_matrix()
for row in matrix:
    print(row)

#Teste vetor de adjacência
print("\nVetor de adjacência:")
v = g.to_adj_vector()
print(v)

# Teste remoção de aresta
g.remove_edge("A", "B")
print("\nApós remover aresta A-B:")
print(g)

# Teste remoção de nó
g.remove_node("C")
print("\nApós remover nó C:")
print(g)