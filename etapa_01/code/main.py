# importando as bibliotecas utilizadas
from funcoesGurobi import *
from funcoesCBC import *
from modelo import *
from dados import *

# definindo qual arquivo de instancia será utilizado
instancia = int(sys.argv[1])
minutos_totais = 60  # definindo tempo total de execução do problema

# criando objetos que serão utilizados nas funções resovlerGurobi e resolverCBC
modelo_GP = ModeloGurobi()
modelo_CBC = ModeloCBC()
dados = Dados(instancia)

# =======================================================================
#                               GUROBI

# chamando a função resolverGurobi
# ela utiliza os objetos modelo_GP, dados, o tempo máximo de execução do problema e a instância utilizada

resolverGurobi(modelo_GP, dados, minutos_totais, instancia)

# =======================================================================
#                               CBC

# chamando a função resolverCBC
# ela utiliza os objetos modelo_CBC, dados, o tempo máximo de execução do problema e a instância utilizada

resolverCBC(modelo_CBC, dados, minutos_totais, instancia)
