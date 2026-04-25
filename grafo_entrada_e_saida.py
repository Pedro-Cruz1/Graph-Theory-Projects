from grafo import Grafo

class Grafo_Entrada_Saida:

    def carregar_grafo(caminho):
        g = Grafo(directed=False)
    
        with open(caminho, 'r') as f:
            linhas = f.readlines()

        num_vertices = int(linhas[0].strip())

        #criação de vértices
        for i in range(1, num_vertices + 1):
            g.add_node(str(i))

        #adição de arestas
        for linha in linhas[1:]:
            u, v = linha.strip().split()
            g.add_edge(u,v)

        return g
    

    def analisar(g):
        graus = [len(g.get_neighbors(n)) for n in g.get_nodes()]

        n = len(graus)
        num_arestas = sum(graus) // 2

        grau_min = min(graus)
        grau_max = max(graus)
        grau_medio = sum(graus) / n

        graus_ord = sorted(graus)
        if n % 2 == 0:
            mediana = (graus_ord[n//2 - 1] + graus_ord[n//2]) / 2
        else:
            mediana = graus_ord[n//2]

        return{
            "vertices": n,
            "arestas": num_arestas,
            "grau_min": grau_min,
            "grau_max": grau_max,
            "grau_medio": grau_medio,
            "mediana": mediana 
        }
    
    def componentes_conexas(g):
        visitados = set()
        componentes = []

        for node in g.get_nodes():
            if node not in visitados:
                comp = g.bfs(node)
                componentes.append(comp)
                visitados.update(comp)

        return componentes
    
    def salvar(g, caminho_saida):

        stats = Grafo_Entrada_Saida.analisar(g)
        comps = Grafo_Entrada_Saida.componentes_conexas(g)

        with open(caminho_saida, 'w') as f:
            f.write(f"Número de vértices: {stats['vertices']}\n")
            f.write(f"Número de arestas: {stats['arestas']}\n")
            f.write(f"Grau mínimo: {stats['grau_min']}\n")
            f.write(f"Grau máximo: {stats['grau_max']}\n")
            f.write(f"Grau médio: {stats['grau_medio']:.2f}\n")
            f.write(f"Mediana dos graus: {stats['mediana']}\n\n")

            f.write(f"Componentes conexas: {len(comps)}\n")
            for i, comp in enumerate(comps, 1):
                f.write(f"Componente {i}: {comp}\n")