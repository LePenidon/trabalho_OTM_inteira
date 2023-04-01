import io
import sys
from pulp import *
import time


# =======================================================================
#                               CBC


def setParametrosCBC(tempo):
    # Definição de parâmetros de solver
    solver_parameters = {
        "msg": False,    # exibe mensagens de progresso
        "maxSeconds": tempo*60,
    }

    # Definição do solver
    solver = PULP_CBC_CMD(solver_parameters)

    return solver


def setVariaveisCBC(modelo, dados):
    modelo.x = LpVariable.dicts(
        "Cobrir", range(dados.n), 0, 1, cat='Binary')


def setFuncaoObjetivoCBC(modelo, dados):

    modelo.m += lpSum(dados.c[j]*modelo.x[j]
                      for j in range(dados.n))


def setRestricoesCBC(modelo, dados):

    for i in range(dados.m):
        modelo.m += lpSum(dados.a[i, j]*modelo.x[j]
                          for j in range(dados.n)) >= 1


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


def printSolucaoCBC(modelo, status, dados):
    output = ""

    if (LpStatus[status] == 'Infeasible'):
        output += "Erro ao imprimir solucao"
        print(output)
        solfile = io.open("solucao.txt", "w+")
        solfile.write(output)
        return

    try:
        solfile = io.open("solucao.txt", "w+")

        for j in range(dados.n):
            output += str(value(modelo.x[j]))
            output += "\n"

        solfile.write(output)

    except:
        output += "Erro ao imprimir solucao"
        print(output)
        solfile = io.open("solucao.txt", "w+")
        solfile.write(output)
        print("\nErro ao imprimir solucao")

    return


def resolverCBC(modelo_CBC, dados, minutos_totais, instancia):
    solver = setParametrosCBC(minutos_totais)
    setVariaveisCBC(modelo_CBC, dados)
    setFuncaoObjetivoCBC(modelo_CBC, dados)
    setRestricoesCBC(modelo_CBC, dados)

    inicio_tempo = time.time()
    status = modelo_CBC.m.solve(solver)
    fim_tempo = time.time()

    printSolucaoValoresCBC(modelo_CBC, status, instancia,
                           inicio_tempo-fim_tempo)

    printSolucaoCBC(modelo_CBC, status, dados)
