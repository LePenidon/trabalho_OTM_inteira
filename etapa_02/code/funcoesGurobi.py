# importando as bibliotecas utilizadas
import io
import sys
from gurobipy import GRB
import time


# =======================================================================
#                               GUROBI

# Definição do solver e parâmetros
def setParametrosGurobi(modelo, minutos):
    modelo.m.setParam("TimeLimit", minutos*60)
    modelo.m.setParam('OutputFlag', 0)

    modelo.m.update()
    return


# Criando variáveis binárias de decisão (com tamanho entre 0 e dados.n-1)
def setVariaveisGurobi(modelo, dados):
    modelo.x = modelo.m.addVars(
        dados.n, vtype=GRB.BINARY, name="Cobrir")


# Criando a função objetivo do problema de cobertura (somatório da multiplicação dos custos pelas variáveis de decisão)
def setFuncaoObjetivoGurobi(modelo, dados):
    modelo.m.setObjective(sum(dados.c[j]*modelo.x[j]
                          for j in range(dados.n)), GRB.MINIMIZE)


# Definindo as restrições do modelo (somatório da multiplicação entre as variáveis de decisão e a variável a_{i,j})
def setRestricoesGurobi(modelo, dados):

    for i in range(dados.m):
        modelo.m.addConstr(sum(dados.a[i][j]*modelo.x[j]
                               for j in range(dados.n)) >= 1)


# Imprimindo a solução ótima, o tempo de execução, os nós explorados e o lower bound
def printSolucaoValoresGurobi(modelo, instancia, tempo):
    print("\n\nGUROBI -> Instância: " + str(instancia))

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


# Imprimindo a solução do problema no arquivo solucao.txt
def printSolucaoGurobi(modelo, dados):
    output = ""

    try:
        solfile = io.open("solucao_gurobi.txt", "w+")

        for j in range(dados.n):
            output += "x[" + str(j+1) + "]: "
            output += str(modelo.x[j].X)
            output += "\n"

        solfile.write(output)

    except:
        output = "Erro ao imprimir solucao"
        print(output)
        solfile = io.open("solucao_gurobi.txt", "w+")
        solfile.write(output)

    return


# Função responsável por resolver o problema de otimização (utiliza a função objetivo, as restrições, as variáveis e os parâmetros criados)
def resolverGurobi(modelo_GP, dados, minutos_totais, instancia):
    setParametrosGurobi(modelo_GP, minutos_totais)
    setVariaveisGurobi(modelo_GP, dados)
    setFuncaoObjetivoGurobi(modelo_GP, dados)
    setRestricoesGurobi(modelo_GP, dados)

    inicio_tempo = time.time()
    modelo_GP.m.optimize()
    fim_tempo = time.time()

    printSolucaoValoresGurobi(modelo_GP, instancia, fim_tempo-inicio_tempo)

    printSolucaoGurobi(modelo_GP, dados)
