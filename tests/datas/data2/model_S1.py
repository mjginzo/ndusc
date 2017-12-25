# -*- coding: utf-8 -*-
"""Example 2 taken from the Thesis of Lee."""

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
    m.Resources = environ.Set(initialize=data['sets']['Resources'])

    # Parameters
    m.P = environ.Param(m.Resources,
                        initialize=data['params']['P'],
                        within=environ.PositiveReals)

    # Variables
    m.Z = environ.Var(m.current_stage, m.Resources, within=environ.Binary)

    # ------------
    # Objective
    # ------------

    def Obj_rule(m, s):
        return sum(m.P[i]*m.Z[s, i] for i in m.Resources)

    m.Obj = environ.Objective(m.current_stage, rule=Obj_rule,
                              sense=environ.minimize)
# --------------------------------------------------------------------------- #
