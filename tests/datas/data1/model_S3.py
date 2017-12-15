#  _________________________________________________________________________
#
#  Example: stochastic problem from the thesis of Lee.
#  First stage model.
#  _________________________________________________________________________

#
# Imports
#

from pyomo.environ import *

def model_S3(m, data):
    #
    # Sets
    #

    #
    # Parameters
    #

    m.prod = Param(initialize=data['params']['prod'])
    m.cost = Param(initialize=data['params']['cost'])
    m.high_cost = Param(initialize=data['params']['high_cost'])
    m.store_cost = Param(initialize=data['params']['store_cost'])
    m.demand = Param(initialize=data['params']['demand'])

    m.y_prev = Param(initialize=data['params']['y'])
    #
    # Variables
    #

    m.x = Var(within=PositiveReals)
    m.w = Var(within=PositiveReals)
    m.y = Var(within=PositiveReals)

    #
    # Objective
    #

    def Obj_rule(m):
        return  m.cost * m.x + m.high_cost * m.w + m.store_cost * m.y

    m.Obj = Objective(rule=Obj_rule, sense=minimize)

    #
    # Constraints
    #

    def prod_rule(m):
        return m.x <= m.prod

    m.low_prod = Constraint(rule=prod_rule)

    def demand_rule(m):
        return m.x + m.w + m.y_prev - m.y == m.demand

    m.total_demand = Constraint(rule=demand_rule)
