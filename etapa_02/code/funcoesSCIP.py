# importando as bibliotecas utilizadas
import io
import sys
import time
from ortools.linear_solver import pywraplp
import dados
import modelo

# =======================================================================
#                               SCIP


# Definição do solver e parâmetros
def setParametrosSCIP(modelo, tempo):
    # Definição de tempo limite em minutos que o solver SCIP irá executar
    modelo.m.SetTimeLimit(tempo*60*1000)

    return


# Criando variáveis binárias de decisão (com tamanho entre 0 e dados.n-1)
def setVariaveisSCIP(modelo: modelo.ModeloSCIP, dados: dados.Dados):
    modelo.x = [modelo.m.BoolVar(f'x[{i}]') for i in range(dados.n)]


# Criando a função objetivo do problema de cobertura (somatório da multiplicação dos custos pelas variáveis de decisão)
def setFuncaoObjetivoSCIP(modelo: modelo.ModeloSCIP, dados: dados.Dados):
    modelo.m.Minimize(sum(dados.c[j]*modelo.x[j]
                      for j in range(dados.n)))


# Definindo as restrições do modelo (somatório da multiplicação entre as variáveis de decisão e a variável a_{i,j})
def setRestricoesSCIP(modelo: modelo.ModeloSCIP, dados: dados.Dados):
    for i in range(dados.m):
        # Restrição >= 1
        constraint = modelo.m.Constraint(
            1, modelo.m.infinity())
        for j in range(dados.n):
            constraint.SetCoefficient(modelo.x[j], dados.a[i][j])


# Imprimindo a solução ótima, o tempo de execução, os nós explorados e o lower bound
def printSolucaoValoresSCIP(modelo: modelo.ModeloSCIP, status, instancia, tempo):
    print("\n\nSCIP -> Instância: " + str(instancia))

    print("Status:", status)

    try:
        print("\nValor da solução ótima: " +
              str(round(modelo.m.Objective().Value())))
    except:
        print("\nValor da solução ótima: - ")

    try:
        print("Lower Bound: " + str(round(modelo.m.Objective().BestBound())))
    except:
        print("Lower Bound: - ")

    try:
        print("Nodes: " + str(round(modelo.m.nodes())))
    except:
        print("Nodes: - ")

    try:
        print("Tempo: " + str(round(tempo)) + " segundos" +
              " = " + str(round(tempo)/60) + " minutos\n")
    except:
        print("Tempo: - \n")

    return


# Imprimindo a solução do problema no arquivo solucao.txt
def printSolucaoSCIP(modelo: modelo.ModeloSCIP, status, dados: dados.Dados):
    output = ""

    solfile = io.open("solucao_SCIP.txt", "w+")

    for j in range(dados.n):
        output += "x[" + str(j+1) + "]: "
        output += str(modelo.x[j].solution_value())
        output += "\n"

    solfile.write(output)

    return


# Função responsável por resolver o problema de otimização (utiliza a função objetivo, as restrições, as variáveis e os parâmetros criados)
def resolverSCIP(modelo_SCIP: modelo.ModeloSCIP, dados: dados.Dados, minutos_totais, instancia):
    setParametrosSCIP(modelo_SCIP, minutos_totais)
    setVariaveisSCIP(modelo_SCIP, dados)
    setFuncaoObjetivoSCIP(modelo_SCIP, dados)
    setRestricoesSCIP(modelo_SCIP, dados)

    inicio_tempo = time.time()
    status = modelo_SCIP.m.Solve()
    fim_tempo = time.time()

    printSolucaoValoresSCIP(modelo_SCIP, status, instancia,
                            fim_tempo-inicio_tempo)

    printSolucaoSCIP(modelo_SCIP, status, dados)
