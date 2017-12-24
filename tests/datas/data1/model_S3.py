# -*- coding: utf-8 -*-
"""Example 1 taken from page 270 of the book: Birge & Louveaux (2011).

Introduction to Stochastic Programming.
"""

# Python packages
from pyomo import environ


# model_S3 --------------------------------------------------------------------
def model_S3(m, data):
    """Third stage model."""
    # ------------
    # Definitions
    # ------------

    # Sets
    m.stages = environ.Set(initialize=[2, 3])
    m.current_stage = environ.Set(initialize=[3])

    # Parameters
    m.prod = environ.Param(m.current_stage, initialize=data['params']['prod'])
    m.cost = environ.Param(m.current_stage, initialize=data['params']['cost'])
    m.high_cost = environ.Param(m.current_stage,
                                initialize=data['params']['high_cost'])
    m.store_cost = environ.Param(m.current_stage,
                                 initialize=data['params']['store_cost'])
    m.demand = environ.Param(m.current_stage,
                             initialize=data['params']['demand'])

    # Variables
    m.x = environ.Var(m.current_stage, within=environ.PositiveReals)
    m.w = environ.Var(m.current_stage, within=environ.PositiveReals)
    m.y = environ.Var(m.stages, within=environ.PositiveReals)

    # ------------
    # Objective
    # ------------

    def Obj_rule(m, s):
        return m.cost[s]*m.x[s] +\
               m.high_cost[s]*m.w[s] +\
               m.store_cost[s]*m.y[s]

    m.Obj = environ.Objective(m.current_stage, rule=Obj_rule,
                              sense=environ.minimize)

    # ------------
    # Constraints
    # ------------

    # low production
    def low_prod_rule(m, s):
        return m.x[s] <= m.prod[s]

    m.low_prod = environ.Constraint(m.current_stage, rule=low_prod_rule)

    # total demand
    def total_demand_rule(m, s):
        return m.x[s] + m.w[s] + m.y[s-1] - m.y[s] == m.demand[s]

    m.total_demand = environ.Constraint(m.current_stage,
                                        rule=total_demand_rule)
# --------------------------------------------------------------------------- #
