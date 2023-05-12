# importando as bibliotecas utilizadas
import gurobipy as gp
import pulp as pu
import scip


# definição da classe ModeloGurobi
class ModeloGurobi():
    # objeto do tipo gp.Model (modelo matemático do problema)
    m = gp.Model("Cobertura")

    # posteriormente este atributo será preenchido com as variáveis de decisão do problema
    x = 0


# definição da classe ModeloSCIP
class ModeloSCIP():
    scip_inst = scip.SCIP()

    # objeto do tipo pu.LpProblem (modelo matemático do problema)
    m = pu.LpProblem("Cobertura", pu.LpMinimize)

    # posteriormente este atributo será preenchido com as variáveis de decisão do problema
    x = 0
