import csv
import shlex
from typing import List, Optional, Tuple

from grafoV3 import Grafo


class Grafo_Entrada_Saida:
    """
    Entrada e saída adaptada para a versão V2 da biblioteca de grafos.

    Formatos aceitos para arestas ponderadas:
    1) u v peso
       Ex.: 1 2 0.1
    2) u;v;peso
       Ex.: Edsger W. Dijkstra;Alan M. Turing;0.25
    3) u,v,peso
    4) u<TAB>v<TAB>peso
    5) "u com espaço" "v com espaço" peso

    A primeira linha pode conter o número de vértices. Quando isso ocorre,
    os vértices numéricos de 1 até N são criados antes da leitura das arestas.
    Mesmo assim, vértices com nomes textuais encontrados nas arestas também
    são adicionados automaticamente pelo método add_edge da classe Grafo.
    """

    @staticmethod
    def _linha_vazia_ou_comentario(linha: str) -> bool:
        linha = linha.strip()
        return not linha or linha.startswith("#") or linha.startswith("//")

    @staticmethod
    def _parse_aresta(linha: str) -> Optional[Tuple[str, str, float]]:
        linha = linha.strip()
        if Grafo_Entrada_Saida._linha_vazia_ou_comentario(linha):
            return None

        # Preferência para separadores que preservam nomes com espaço.
        for delimitador in [";", ",", "\t"]:
            if delimitador in linha:
                partes = [p.strip() for p in linha.split(delimitador)]
                if len(partes) >= 3:
                    u = partes[0]
                    v = partes[1]
                    peso = float(partes[2])
                    return u, v, peso

        # Suporta aspas: "Edsger W. Dijkstra" "Alan M. Turing" 0.5
        partes = shlex.split(linha)
        if len(partes) < 3:
            raise ValueError(f"Linha de aresta inválida: {linha}")

        u = partes[0]
        peso = float(partes[-1])

        if len(partes) == 3:
            v = partes[1]
        else:
            # Fallback para casos sem aspas. Para nomes com espaço, prefira ;, vírgula, tab ou aspas.
            v = " ".join(partes[1:-1])

        return u, v, peso

    @staticmethod
    def carregar_grafo(caminho, directed=False):
        g = Grafo(directed=directed)

        with open(caminho, 'r') as f:
            linhas = f.readlines()

        num_vertices = int(linhas[0].strip())

        # criação dos vértices
        for i in range(1, num_vertices + 1):
            g.add_node(str(i))

        # adição das arestas
        for linha in linhas[1:]:

            if not linha.strip():
                continue

            u, v, w = linha.strip().split()
            g.add_edge(u, v, float(w))

        return g

    @staticmethod
    def analisar(g):
        graus = [len(g.get_neighbors(n)) for n in g.get_nodes()]
        if not graus:
            return {
                "vertices": 0,
                "arestas": 0,
                "grau_min": 0,
                "grau_max": 0,
                "grau_medio": 0,
                "mediana": 0,
            }

        n = len(graus)
        num_arestas = sum(graus) if g.directed else sum(graus) // 2
        grau_min = min(graus)
        grau_max = max(graus)
        grau_medio = sum(graus) / n

        graus_ord = sorted(graus)
        if n % 2 == 0:
            mediana = (graus_ord[n // 2 - 1] + graus_ord[n // 2]) / 2
        else:
            mediana = graus_ord[n // 2]

        return {
            "vertices": n,
            "arestas": num_arestas,
            "grau_min": grau_min,
            "grau_max": grau_max,
            "grau_medio": grau_medio,
            "mediana": mediana,
        }

    @staticmethod
    def componentes_conexas(g):
        visitados = set()
        componentes = []

        for node in sorted(g.get_nodes(), key=str):
            if node not in visitados:
                parent, _ = g.bfs(node)
                comp = sorted(parent.keys(), key=str)
                visitados.update(comp)
                componentes.append({"tamanho": len(comp), "vertices": comp})

        componentes.sort(key=lambda c: c["tamanho"], reverse=True)
        return componentes

    @staticmethod
    def salvar(g, caminho_saida):
        stats = Grafo_Entrada_Saida.analisar(g)
        comps = Grafo_Entrada_Saida.componentes_conexas(g)

        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(f"Número de vértices: {stats['vertices']}\n")
            f.write(f"Número de arestas: {stats['arestas']}\n")
            f.write(f"Grau mínimo: {stats['grau_min']}\n")
            f.write(f"Grau máximo: {stats['grau_max']}\n")
            f.write(f"Grau médio: {stats['grau_medio']:.2f}\n")
            f.write(f"Mediana dos graus: {stats['mediana']}\n\n")

            f.write(f"Componentes conexas: {len(comps)}\n")
            for i, comp in enumerate(comps, 1):
                f.write(f"Componente {i}: tamanho = {comp['tamanho']}, vértices = {comp['vertices']}\n")
