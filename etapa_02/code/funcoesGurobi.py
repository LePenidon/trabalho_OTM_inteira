# importando as bibliotecas utilizadas
import io
import sys
from gurobipy import GRB
import time
import dados
import modelo


# =======================================================================
#                               GUROBI

# Definição do solver e parâmetros
def setParametrosGurobi(modelo: modelo.ModeloGurobi, minutos):
    modelo.m.setParam("TimeLimit", minutos*60)
    modelo.m.setParam('OutputFlag', 0)

    modelo.m.setParam('Presolve', 0)

    # modelo.m.setParam("Sifting", 2)
    # modelo.m.setParam("Disconnected", 2)

    # https://www.gurobi.com/documentation/9.5/refman/sifting.html#parameter:Sifting
    # https://www.gurobi.com/documentation/9.5/refman/disconnected.html#parameter:Disconnected
    # https://www.gurobi.com/documentation/9.5/refman/covercuts.html#parameter:CoverCuts

    modelo.m.update()
    return


# Criando variáveis binárias de decisão (com tamanho entre 0 e dados.n-1)
def setVariaveisGurobi(modelo: modelo.ModeloGurobi, dados: dados.Dados):
    modelo.x = modelo.m.addVars(
        dados.n, vtype=GRB.BINARY, name="Cobrir")


# Criando a função objetivo do problema de cobertura (somatório da multiplicação dos custos pelas variáveis de decisão)
def setFuncaoObjetivoGurobi(modelo: modelo.ModeloGurobi, dados: dados.Dados):
    modelo.m.setObjective(sum(dados.c[j]*modelo.x[j]
                          for j in range(dados.n)), GRB.MINIMIZE)


# Definindo as restrições do modelo (somatório da multiplicação entre as variáveis de decisão e a variável a_{i,j})
def setRestricoesGurobi(modelo: modelo.ModeloGurobi, dados: dados.Dados):

    for i in range(dados.m):
        modelo.m.addConstr(sum(dados.a[i][j]*modelo.x[j]
                               for j in range(dados.n)) >= 1)


# Imprimindo a solução ótima, o tempo de execução, os nós explorados e o lower bound
def printSolucaoValoresGurobi(modelo: modelo.ModeloGurobi, instancia, tempo):
    output = ""

    solfile = io.open("resultados/"+str(instancia) + "/" +
                      "output_gurobi.txt", "w+")

    output += "GUROBI -> Instancia: " + str(instancia) + "\n"

    if (modelo.m.status == 3):
        output += "Solucao Infactivel" + "\n"
    else:
        output += "Existe solucao" + "\n"

    try:
        output += "\nValor da solucao otima: " + \
            str(round(modelo.m.objVal)) + "\n"
    except:
        output += "\nValor da solucao otima: - " + "\n"

    try:
        output += "Limitante Dual: " + str(round(modelo.m.objBound)) + "\n"
    except:
        output += "Limitante Dual: - " + "\n"
    try:
        dual = modelo.m.objBound
        sol = modelo.m.objVal
        GAP = (sol-dual)/sol*100

        output += "GAP: " + str(round(GAP)) + "%\n"
    except:
        output += "GAP: - " + "\n"
    try:
        output += "Nos: " + str(round(modelo.m.NodeCount)) + "\n"
    except:
        output += "Nos: - " + "\n"

    try:
        output += "Tempo: " + \
            str(round(tempo)) + " segundos" + " = " + \
            str(round(tempo/60)) + " minutos\n"
    except:
        output += "Tempo: - \n"

    solfile.write(output)

    return


# Imprimindo a solução do problema no arquivo solucao.txt
def printSolucaoGurobi(modelo: modelo.ModeloGurobi, dados: dados.Dados, instancia):
    output = ""

    try:
        solfile = io.open("resultados/"+str(instancia) +
                          "/" + "solucao_gurobi.txt", "w+")

        for j in range(dados.n):
            output += "x[" + str(j+1) + "]: "
            output += str(modelo.x[j].X)
            output += "\n"

        solfile.write(output)

    except:
        output = "Erro ao imprimir solucao"
        print(output)
        solfile = io.open("resultados/"+str(instancia) +
                          "/" + "solucao_gurobi.txt", "w+")

        solfile.write(output)

    return


# Função responsável por resolver o problema de otimização (utiliza a função objetivo, as restrições, as variáveis e os parâmetros criados)
def resolverGurobi(modelo_GP: modelo.ModeloGurobi, dados: dados.Dados, minutos_totais, instancia):
    setParametrosGurobi(modelo_GP, minutos_totais)
    setVariaveisGurobi(modelo_GP, dados)
    setFuncaoObjetivoGurobi(modelo_GP, dados)
    setRestricoesGurobi(modelo_GP, dados)

    inicio_tempo = time.time()
    modelo_GP.m.optimize()
    fim_tempo = time.time()

    printSolucaoValoresGurobi(modelo_GP, instancia, fim_tempo-inicio_tempo)

    printSolucaoGurobi(modelo_GP, dados, instancia)
