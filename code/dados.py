# importando a biblioteca utilizada
import numpy as np

# classe criada par ler os dados fornecidos pelo toy problem


class Dados():
    arquivo = "instancias/"
    c = 0
    a = 0
    m = 0
    n = 0

    # construtor
    def __init__(self, instancia) -> None:
        self.instancia = str(instancia)
        self.arquivo += self.instancia + ".txt"

        # le arquivo
        with open(self.arquivo, 'r') as f:
            leitura = [[int(num) for num in linha.split(' ')] for linha in f]

        self.a = np.zeros(leitura[0])
        self.m = leitura[0][0]
        self.n = leitura[0][1]

        index_linha_atual = 1
        linha_matriz = 0

        for i in leitura:
            if (index_linha_atual == 1):
                index_linha_atual += 1
                continue

            if (index_linha_atual == 2):
                self.c = i
                index_linha_atual += 1
                continue

            if (index_linha_atual % 2 != 0):

                index_linha_atual += 1

                continue

            for j in i:
                self.a[linha_matriz, j-1] = 1

            linha_matriz += 1
            index_linha_atual += 1
