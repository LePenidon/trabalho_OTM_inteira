# importando as bibliotecas utilizadas
from funcoesGurobi import *
from funcoesSCIP import *
from modelo import *
from dados import *

# definindo qual arquivo de instancia será utilizado
instancia = int(sys.argv[1])
minutos_totais = 1  # definindo tempo total de execução do problema

# criando objetos que serão utilizados nas funções resovlerGurobi e resolverCBC
modelo_GP = ModeloGurobi()
# modelo_SCIP = ModeloSCIP()
dados = Dados(instancia)

# =======================================================================
#                               GUROBI

# chamando a função resolverGurobi
# ela utiliza os objetos modelo_GP, dados, o tempo máximo de execução do problema e a instância utilizada

resolverGurobi(modelo_GP, dados, minutos_totais, instancia)

# =======================================================================
#                               SCIP

# chamando a função resolverSCIP
# ela utiliza os objetos modelo_SCIP, dados, o tempo máximo de execução do problema e a instância utilizada

# resolverSCIP(modelo_SCIP, dados, minutos_totais, instancia)
