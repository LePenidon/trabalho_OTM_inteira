import io
import sys
from pulp import *


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
    print("\n\nInstância: " + str(instancia))

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


def printSolucaoCBC(modelo, dados):
    output = ""

    try:
        solfile = io.open("solucao.txt", "w+")

        for j in range(dados.n):
            output += str(value(modelo.x[j]))
            output += "\n"

        solfile.write(output)

    except:
        print("\nErro ao imprimir solucao")

    return
