import gurobipy as gp
import pulp as pu


class ModeloGurobi():

    m = gp.Model("Cobertura")

    x = 0


class ModeloCBC():
    m = pu.LpProblem("Cobertura", pu.LpMinimize)
    x = 0
