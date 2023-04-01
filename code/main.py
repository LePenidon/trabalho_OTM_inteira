from funcoesGurobi import *
from funcoesCBC import *
from modelo import *
from dados import *
import time

instancia = int(sys.argv[1])
minutos_totais = 60

modelo_GP = ModeloGurobi()
modelo_CBC = ModeloCBC()
dados = Dados(instancia)

# =======================================================================
#                               GUROBI

setParametrosGurobi(modelo_GP, minutos_totais)
setVariaveisGurobi(modelo_GP, dados)
setFuncaoObjetivoGurobi(modelo_GP, dados)
setRestricoesGurobi(modelo_GP, dados)

inicio_tempo = time.time()
modelo_GP.m.optimize()
fim_tempo = time.time()

printSolucaoValoresGurobi(modelo_GP, instancia, inicio_tempo-fim_tempo)

printSolucaoGurobi(modelo_GP, dados)

# =======================================================================
#                               CBC

# solver = setParametrosCBC(minutos_totais)
# setVariaveisCBC(modelo_CBC, dados)
# setFuncaoObjetivoCBC(modelo_CBC, dados)
# setRestricoesCBC(modelo_CBC, dados)

# inicio_tempo = time.time()
# status = modelo_CBC.m.solve(solver)
# fim_tempo = time.time()

# printSolucaoValoresCBC(modelo_CBC, status, instancia, inicio_tempo-fim_tempo)

# printSolucaoCBC(modelo_CBC, dados)
