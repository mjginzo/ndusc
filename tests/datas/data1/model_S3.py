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
    m.prod = environ.Param(initialize=data['params']['prod'])
    m.cost = environ.Param(initialize=data['params']['cost'])
    m.high_cost = environ.Param(initialize=data['params']['high_cost'])
    m.store_cost = environ.Param(initialize=data['params']['store_cost'])
    m.demand = environ.Param(initialize=data['params']['demand'])

    # Variables
    m.x = environ.Var(m.current_stage, within=environ.PositiveReals)
    m.w = environ.Var(m.current_stage, within=environ.PositiveReals)
    m.y = environ.Var(m.stages, within=environ.PositiveReals)

    # ------------
    # Objective
    # ------------

    def Obj_rule(m):
        return m.cost*m.x[3] + m.high_cost*m.w[3] + m.store_cost*m.y[3]

    m.Obj = environ.Objective(rule=Obj_rule, sense=environ.minimize)

    # ------------
    # Constraints
    # ------------

    # low production
    def low_prod_rule(m):
        return m.x[3] <= m.prod

    m.low_prod = environ.Constraint(rule=low_prod_rule)

    # total demand
    def total_demand_rule(m):
        return m.x[3] + m.w[3] + m.y[2] - m.y[3] == m.demand

    m.total_demand = environ.Constraint(rule=total_demand_rule)
# --------------------------------------------------------------------------- #
