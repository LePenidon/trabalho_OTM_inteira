import io
import sys
from gurobipy import GRB

# =======================================================================
#                               GUROBI


def setParametrosGurobi(modelo, minutos):
    modelo.m.setParam("TimeLimit", minutos*60)
    modelo.m.setParam('OutputFlag', 0)

    modelo.m.update()
    return


def setVariaveisGurobi(modelo, dados):
    modelo.x = modelo.m.addVars(
        dados.n, vtype=GRB.BINARY, name="Cobrir")


def setFuncaoObjetivoGurobi(modelo, dados):
    modelo.m.setObjective(sum(dados.c[j]*modelo.x[j]
                          for j in range(dados.n)), GRB.MINIMIZE)


def setRestricoesGurobi(modelo, dados):

    for i in range(dados.m):
        modelo.m.addConstr(sum(dados.a[i, j]*modelo.x[j]
                               for j in range(dados.n)) >= 1)


def printSolucaoValoresGurobi(modelo, instancia, tempo):
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
        print("Tempo: " + str(round(tempo)) + " segundos" +
              " = " + str(round(tempo)/60) + " minutos\n")
    except:
        print("Tempo: - \n")

    return


def printSolucaoGurobi(modelo, dados):
    output = ""

    try:
        solfile = io.open("solucao.txt", "w+")

        for j in range(dados.n):
            output += str(modelo.x[j].X)
            output += "\n"

        solfile.write(output)
        print(output)

    except:
        print("\nErro ao imprimir solucao")

    return
