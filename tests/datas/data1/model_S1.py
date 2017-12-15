# -*- coding: utf-8 -*-
"""Example 1 taken from page 270 of the book: Birge & Louveaux (2011).

Introduction to Stochastic Programming.
"""

# Python packages
from pyomo import environ


# model_S1 --------------------------------------------------------------------
def model_S1(m, data):
    """First stage model."""
    # ------------
    # Definitions
    # ------------

    # Sets
    m.current_stage = environ.Set(initialize=[1])

    # Parameters
    m.prod = environ.Param(initialize=data['params']['prod'])
    m.cost = environ.Param(initialize=data['params']['cost'])
    m.high_cost = environ.Param(initialize=data['params']['high_cost'])
    m.store_cost = environ.Param(initialize=data['params']['store_cost'])
    m.demand = environ.Param(initialize=data['params']['demand'])

    # Variables
    m.x = environ.Var(m.current_stage, within=environ.PositiveReals)
    m.w = environ.Var(m.current_stage, within=environ.PositiveReals)
    m.y = environ.Var(m.current_stage, within=environ.PositiveReals)

    # ------------
    # Objective
    # ------------

    def Obj_rule(m):
        return m.cost*m.x[1] + m.high_cost*m.w[1] + m.store_cost*m.y[1]

    m.Obj = environ.Objective(rule=Obj_rule, sense=environ.minimize)

    # ------------
    # Constraints
    # ------------

    # lower production
    def low_prod_rule(m):
        return m.x[1] <= m.prod

    m.low_prod = environ.Constraint(rule=low_prod_rule)

    # total demand
    def total_demand_rule(m):
        return m.x[1] + m.w[1] - m.y[1] == m.demand

    m.total_demand = environ.Constraint(rule=total_demand_rule)
# --------------------------------------------------------------------------- #
