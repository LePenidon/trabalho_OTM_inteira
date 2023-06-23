# importando a biblioteca utilizada
import numpy as np
from itertools import chain


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

        merged_lines = []
        current_line = []

        for line in leitura:
            if index_linha_atual == 1:
                index_linha_atual += 1
                continue

            if len(line) == 1 and line[0] < self.m:
                # Adiciona a linha atual com o valor isolado
                merged_lines.append(line+current_line)
                current_line = []  # Reseta a linha atual

            else:
                # Acrescenta a linha atual com a linha quebrada
                current_line.append(line)
                index_linha_atual += 1

        custos = []
        valores = []

        custos.append(merged_lines[0])

        colunas = []
        colunas.append(custos[0][0])
        merged_lines.pop(0)
        custos[0].pop(0)

        for i in merged_lines:
            colunas.append(i[0])
            i.pop(0)

        colunas.pop(-1)

        custos = list(chain.from_iterable(custos))
        custos = list(chain.from_iterable(custos))

        for i in merged_lines:
            valores_aux = [
                numero for sublista in i for numero in sublista]
            valores.append(valores_aux)

        self.c = custos

        linha_matriz = 0

        for i in valores:
            for coluna in i:
                self.a[linha_matriz][coluna-1] = 1

            linha_matriz += 1
