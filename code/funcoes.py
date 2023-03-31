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
    modelo.s = modelo.m.addVars(
        dados.N, vtype=GRB.CONTINUOUS, lb=0, name="Secoes")


def setFuncaoObjetivo(modelo, dados):
    modelo.m.setObjective(sum(modelo.s[i]
                          for i in range(dados.N)), GRB.MAXIMIZE)


def setRestricoes(modelo, dados):
    modelo.m.addConstr(sum(modelo.s[i]*dados.a[i]
                       for i in range(dados.N)) <= dados.e)

    modelo.m.addConstr(
        sum(modelo.s[i]*dados.S for i in range(dados.N)) <= dados.d)

    modelo.m.addConstr(sum(modelo.s[i]*dados.b[i]
                       for i in range(dados.N)) <= dados.c)


def printSolucao(modelo, dados, instancia):
    print("\n\t\tInstância:", instancia)
    print("\n")
    print("Valor da solução ótima:\t" + str(modelo.m.ObjVal))

    for i in range(dados.N):
        if (i == 0):
            print("\n Seçoes de Natacao: " + str(modelo.s[i].x))
        elif (i == 1):
            print("Secoes de Ciclismo: " + str(modelo.s[i].x))
