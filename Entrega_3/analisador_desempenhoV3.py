import gc
import heapq
import os
import time
from typing import Dict, List, Optional

try:
    import psutil
except ImportError:
    psutil = None

from grafoV3 import Grafo
from grafo_entrada_e_saidaV3 import Grafo_Entrada_Saida

INF = float("inf")

# Configurações
REPETICOES = 1


class AnalisadorDesempenho:

    @staticmethod
    def medir_memoria_mb():
        if psutil is None:
            return 0.0

        processo = psutil.Process(os.getpid())
        return processo.memory_info().rss / (1024 * 1024)


    @staticmethod
    def preparar_grafo(grafo):

        nos = grafo.get_nodes()
        adj = grafo.adj_list

        possui_negativo = any(
            peso < 0
            for vizinhos in adj.values()
            for _, peso in vizinhos
        )

        arestas = sum(len(vizinhos) for vizinhos in adj.values())

        if not grafo.directed:
            arestas //= 2

        return nos, adj, possui_negativo, arestas


    @staticmethod
    def medir_tempo_medio_bellman(grafo, origem, repeticoes=REPETICOES):

        tempos = []

        for _ in range(repeticoes):

            inicio = time.perf_counter()
            grafo.bellman_ford(origem)
            fim = time.perf_counter()

            tempos.append(fim - inicio)

        return sum(tempos) / len(tempos)


    @staticmethod
    def medir_tempo_medio_dijkstra(grafo, origem, repeticoes=REPETICOES):

        tempos = []

        for _ in range(repeticoes):

            inicio = time.perf_counter()
            grafo.dijkstra(origem)
            fim = time.perf_counter()

            tempos.append(fim - inicio)

        return sum(tempos) / len(tempos)


    @staticmethod
    def inverter_grafo(grafo):

        invertido = Grafo(directed=True)

        for no in grafo.get_nodes():
            invertido.add_node(no)

        for origem in grafo.get_nodes():

            for destino, peso in grafo.get_neighbors(origem):

                invertido.add_edge(destino, origem, peso)

        return invertido


    @staticmethod
    def reconstruir_caminho(parent, origem, destino):

        if destino not in parent:
            return []

        caminho = []
        visitados = set()

        atual = destino

        while atual is not None:

            if atual in visitados:
                # ciclo encontrado
                print(f"Ciclo detectado na reconstrução do caminho em {atual}")
                return []

            visitados.add(atual)

            caminho.append(atual)

            if atual == origem:
                break

            atual = parent.get(atual)

        caminho.reverse()

        if caminho and caminho[0] == origem:
            return caminho

        return []


    @staticmethod
    def formatar_distancia(valor):

        if valor == INF:
            return "Infinito"

        return f"{valor:.6f}".rstrip("0").rstrip(".")


    @staticmethod
    def formatar_caminho(caminho):

        if not caminho:
            return "Não alcançável"

        return " -> ".join(caminho)


    @staticmethod
    def escrever_resultados_bellman(
            arquivo,
            distancias,
            pais,
            ciclo_negativo,
            destino="100"
    ):

        arquivo.write("\n===== BELLMAN-FORD =====\n\n")

        arquivo.write(f"Possui ciclo negativo: {ciclo_negativo}\n\n")

        arquivo.write("Origem\tDistância\tCaminho\n")

        for origem in ["10", "20", "30"]:

            caminho = AnalisadorDesempenho.reconstruir_caminho(
                pais,
                destino,
                origem
            )

            arquivo.write(
                f"{origem}\t"
                f"{AnalisadorDesempenho.formatar_distancia(distancias.get(origem, INF))}\t"
                f"{AnalisadorDesempenho.formatar_caminho(caminho)}\n"
            )


    @staticmethod
    def escrever_resultados_dijkstra(
            arquivo,
            distancias,
            pais,
            destino="100"
    ):

        arquivo.write("\n===== DIJKSTRA =====\n\n")

        arquivo.write("Origem\tDistância\tCaminho\n")

        for origem in ["10", "20", "30"]:

            caminho = AnalisadorDesempenho.reconstruir_caminho(
                pais,
                destino,
                origem
            )

            arquivo.write(
                f"{origem}\t"
                f"{AnalisadorDesempenho.formatar_distancia(distancias.get(origem, INF))}\t"
                f"{AnalisadorDesempenho.formatar_caminho(caminho)}\n"
            )

    @staticmethod
    def processar_grafo(caminho_arquivo, caminho_saida):

        print(f"Processando: {os.path.basename(caminho_arquivo)}")

        gc.collect()

        memoria_antes = AnalisadorDesempenho.medir_memoria_mb()

        # Carrega o grafo direcionado
        grafo = Grafo_Entrada_Saida.carregar_grafo(
            caminho_arquivo,
            directed=True
        )

        memoria_depois = AnalisadorDesempenho.medir_memoria_mb()

        memoria_usada = memoria_depois - memoria_antes

        vertices, adj, possui_negativo, arestas = \
            AnalisadorDesempenho.preparar_grafo(grafo)

        # Grafo invertido para calcular distâncias até o vértice 100
        invertido = AnalisadorDesempenho.inverter_grafo(grafo)

        tempo_bellman = \
            AnalisadorDesempenho.medir_tempo_medio_bellman(
                invertido,
                "100"
            )

        dist_bellman, pais_bellman, ciclo_negativo = \
            invertido.bellman_ford("100")
        
        print(f"{os.path.basename(caminho_arquivo)} -> ciclo negativo: {ciclo_negativo}")

        with open(caminho_saida, "w", encoding="utf-8") as arq:

            arq.write("=" * 60 + "\n")
            arq.write("RELATÓRIO - BELLMAN-FORD\n")
            arq.write("=" * 60 + "\n\n")

            arq.write(f"Arquivo: {os.path.basename(caminho_arquivo)}\n")
            arq.write(f"Vértices: {len(vertices)}\n")
            arq.write(f"Arestas: {arestas}\n")
            arq.write(f"Pesos negativos: {possui_negativo}\n")
            arq.write(f"Ciclo negativo: {ciclo_negativo}\n")
            arq.write(f"Memória utilizada: {memoria_usada:.2f} MB\n")
            arq.write(f"Tempo médio Bellman-Ford (2 execuções): "
                      f"{tempo_bellman:.6f} s\n")

            AnalisadorDesempenho.escrever_resultados_bellman(
                arq,
                dist_bellman,
                pais_bellman,
                ciclo_negativo,
                destino="100"
            )

            # Comparação com Dijkstra somente se não houver pesos negativos
            if not possui_negativo:

                tempo_dijkstra = \
                    AnalisadorDesempenho.medir_tempo_medio_dijkstra(
                        invertido,
                        "100"
                    )

                dist_dijkstra, pais_dijkstra = invertido.dijkstra("100")


                arq.write("\n")
                arq.write("=" * 60 + "\n")
                arq.write("COMPARAÇÃO COM DIJKSTRA\n")
                arq.write("=" * 60 + "\n")

                arq.write(
                    f"\nTempo médio Dijkstra (2 execuções): "
                    f"{tempo_dijkstra:.6f} s\n"
                )

                AnalisadorDesempenho.escrever_resultados_dijkstra(
                    arq,
                    dist_dijkstra,
                    pais_dijkstra,
                    destino="100"
                )

        print(f"Relatório salvo em: {caminho_saida}")


def main():

    pasta_entrada = "grafos"
    pasta_saida = "resultados"

    os.makedirs(pasta_saida, exist_ok=True)

    arquivos = [a for a in os.listdir(pasta_entrada) if a.endswith(".txt")]
    total = len(arquivos)

    for i, arquivo in enumerate(arquivos, start=1):

        print(f"[{i}/{total}] Processando {arquivo}...")

        entrada = os.path.join(pasta_entrada, arquivo)

        saida = os.path.join(
            pasta_saida,
            arquivo.replace(".txt", "_resultado.txt")
        )

        AnalisadorDesempenho.processar_grafo(
            entrada,
            saida
        )

        print(f"[{i}/{total}] Concluído!\n")

if __name__ == "__main__":
    main()