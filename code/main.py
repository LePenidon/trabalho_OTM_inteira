from funcoesGurobi import *
from funcoesCBC import *
from modelo import *
from dados import *

instancia = int(sys.argv[1])
minutos_totais = 60

modelo_GP = ModeloGurobi()
modelo_CBC = ModeloCBC()
dados = Dados(instancia)

# =======================================================================
#                               GUROBI

resolverGurobi(modelo_GP, dados, minutos_totais, instancia)

# =======================================================================
#                               CBC

# resolverCBC(modelo_CBC, dados, minutos_totais, instancia)
