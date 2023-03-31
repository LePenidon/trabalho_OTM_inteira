import gurobipy as gp
import io
import sys
from funcoes import *
from gurobipy import GRB


def setParametrosGurobi(modelo, minutos):
    modelo.m.setParam("TimeLimit", minutos*60)
    modelo.m.setParam('OutputFlag', 0)

    modelo.m.update()
    return


def setVariaveis(modelo, dados):
    modelo.x = modelo.m.addVars(
        dados.n, vtype=GRB.BINARY, name="Cobrir")


def setFuncaoObjetivo(modelo, dados):
    modelo.m.setObjective(sum(dados.c[i]*modelo.x[i]
                          for i in range(dados.n)), GRB.MINIMIZE)


def setRestricoes(modelo, dados):

    for i in range(dados.m):
        modelo.m.addConstr(sum(dados.a[i, j]*modelo.x[j]
                               for j in range(dados.n)) >= 1)


def printSolucaoValores(modelo, instancia):
    print("\n\nInstância: " + str(instancia))

    if (modelo.m.status == 3):
        print("Solução Infactível")
    else:
        print("Existe solução")

    try:
        print("\nValor da solução ótima: " + str(round(modelo.m.objVal)))
    except:
        print("\nValor da solução ótima: - ")

    try:
        print("Lower Bound: " + str(round(modelo.m.objBound)))
    except:
        print("Lower Bound: - ")

    try:
        print("Nodes: " + str(round(modelo.m.NodeCount)))
    except:
        print("Nodes: - ")

    try:
        print("Tempo: " + str(round(modelo.m.Runtime)) + " segundos" +
              " = " + str(round(modelo.m.Runtime)/60) + " minutos\n")
    except:
        print("Tempo: - \n")

    return


def printSolucao(modelo, dados):
    output = ""

    try:
        solfile = io.open("solucao.txt", "w+")

        for j in range(dados.n):
            output += str(modelo.x[j].X)
            output += " "

        solfile.write(output)
        print(output)

    except:
        print("\nErro ao imprimir solucao")

    return
