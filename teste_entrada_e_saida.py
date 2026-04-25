from grafo_entrada_e_saida import Grafo_Entrada_Saida

if __name__ == "__main__":
    entrada = "Entrada.txt"
    saida = "Saida.txt"

    g = Grafo_Entrada_Saida.carregar_grafo(entrada)

    print("Grafo carregado:")
    print(g)

    Grafo_Entrada_Saida.salvar(g, saida)
    
    print("Arquivo de saída gerado com sucesso!")