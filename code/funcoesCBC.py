# importando as bibliotecas utilizadas
import io
import sys
from pulp import *
import time


# =======================================================================
#                               CBC

# Definição do solver e parâmetros
def setParametrosCBC(tempo):
    # Definição de tempo limite em minutos que o solver CBC irá executar
    solver = PULP_CBC_CMD(msg=False, timeLimit=tempo*60)

    return solver

# Criando variáveis binárias de decisão (com tamanho entre 0 e dados.n-1)


def setVariaveisCBC(modelo, dados):
    modelo.x = LpVariable.dicts(
        "Cobrir", range(dados.n), 0, 1, cat='Binary')


# Criando a função objetivo do problema de cobertura (somatório da multiplicação dos custos pelas variáveis de decisão)
def setFuncaoObjetivoCBC(modelo, dados):
    modelo.m += lpSum(dados.c[j]*modelo.x[j]
                      for j in range(dados.n))


# Definindo as restrições do modelo (somatório da multiplicação entre as variáveis de decisão e a variável a_{i,j})
def setRestricoesCBC(modelo, dados):
    for i in range(dados.m):
        modelo.m += lpSum(dados.a[i, j]*modelo.x[j]
                          for j in range(dados.n)) >= 1


# Imprimindo a solução ótima, o tempo de execução, os nós explorados e o lower bound
def printSolucaoValoresCBC(modelo, status, instancia, tempo):
    print("\n\nCBC -> Instância: " + str(instancia))

    print("Status:", LpStatus[status])

    try:
        print("\nValor da solução ótima: " +
              str(round(value(modelo.m.objective))))
    except:
        print("\nValor da solução ótima: - ")

    try:
        print("Lower Bound: " + str(round(modelo.m.objective.LB)))
    except:
        print("Lower Bound: - ")

    try:
        print("Nodes: " + str(round(modelo.m.getNumNodes())))
    except:
        print("Nodes: - ")

    try:
        print("Tempo: " + str(round(tempo)) + " segundos" +
              " = " + str(round(tempo)/60) + " minutos\n")
    except:
        print("Tempo: - \n")

    return


# Imprimindo a solução do problema no arquivo solucao.txt
def printSolucaoCBC(modelo, status, dados):
    output = ""

    if (LpStatus[status] == 'Infeasible'):
        output += "Erro ao imprimir solucao"
        print(output)

        solfile = io.open("solucao_CBC.txt", "w+")
        solfile.write(output)
        return

    try:
        solfile = io.open("solucao_CBC.txt", "w+")

        for j in range(dados.n):
            output += "x[" + str(j+1) + "]: "
            output += str(value(modelo.x[j]))
            output += "\n"

        solfile.write(output)

    except:
        output += "Erro ao imprimir solucao"
        print(output)
        solfile = io.open("solucao_CBC.txt", "w+")
        solfile.write(output)
        print("\nErro ao imprimir solucao")

    return


# Função responsável por resolver o problema de otimização (utiliza a função objetivo, as restrições, as variáveis e os parâmetros criados)
def resolverCBC(modelo_CBC, dados, minutos_totais, instancia):
    solver = setParametrosCBC(minutos_totais)
    setVariaveisCBC(modelo_CBC, dados)
    setFuncaoObjetivoCBC(modelo_CBC, dados)
    setRestricoesCBC(modelo_CBC, dados)

    inicio_tempo = time.time()
    status = modelo_CBC.m.solve(solver)
    fim_tempo = time.time()

    printSolucaoValoresCBC(modelo_CBC, status, instancia,
                           fim_tempo-inicio_tempo)

    printSolucaoCBC(modelo_CBC, status, dados)
