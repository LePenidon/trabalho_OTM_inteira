from funcoes import *
from modelo import *
from dados import *
import numpy as np


instancia = int(sys.argv[1])
minutos_totais = 60

modelo = Modelo()
dados = Dados(instancia)

setParametrosGurobi(modelo, minutos_totais)
setVariaveis(modelo, dados)
setFuncaoObjetivo(modelo, dados)
setRestricoes(modelo, dados)

modelo.m.optimize()

printSolucaoValores(modelo, instancia)
printSolucao(modelo, dados)
