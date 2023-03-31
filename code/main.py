from funcoes import *
from modelo import *
from dados import *

instancia = int(sys.argv[1])
minutos_totais = 60

modelo = Modelo()
dados = Dados()

setParametrosGurobi(modelo, minutos_totais)
setVariaveis(modelo, dados)
setFuncaoObjetivo(modelo, dados)
setRestricoes(modelo, dados)

modelo.m.optimize()

printSolucao(modelo, dados, instancia)
