# -*- coding: utf-8 -*-
"""Example 2 taken from the Thesis of Lee."""

# Python packages
from pyomo import environ


# model_S2 --------------------------------------------------------------------
def model_S2(m, data):
    """Second stage model."""
    # ------------
    # Definitions
    # ------------

    # Sets
    m.prev_stage = environ.Set(initialize=[1])
    m.current_stage = environ.Set(initialize=[2])
    m.Resources = environ.Set(initialize=data['sets']['Resources'])
    m.Periods = environ.Set(initialize=data['sets']['Periods'])

    # Parameters
    m.C = environ.Param(m.Resources,
                        initialize=data['params']['C'],
                        within=environ.PositiveReals)
    m.A = environ.Param(m.Resources,
                        initialize=data['params']['A'],
                        within=environ.PositiveReals)
    m.PR = environ.Param(m.Resources, initialize=data['params']['PR'],
                         within=environ.PositiveReals)
    m.H = environ.Param(m.Periods,
                        initialize=data['params']['H'],
                        within=environ.PositiveReals)
    m.NVC = environ.Param(m.current_stage, m.Periods,
                          initialize=data['params']['NVC'],
                          within=environ.PositiveReals)
    m.SP = environ.Param(m.current_stage, m.Periods,
                         initialize=data['params']['SP'],
                         within=environ.PositiveReals)

    def PER_init(m, s, p):
        """Perimeter initialization."""
        if p == 1:
            return m.SP[s, p]
        else:
            return m.SP[s, p]-m.SP[s, p-1]
    m.PER = environ.Param(m.current_stage, m.Periods, initialize=PER_init,
                          within=environ.PositiveReals)

    def M_init(model):
        return max([model.SP[s, p]
                    for s in m.current_stage for p in m.Periods])
    m.M = environ.Param(initialize=M_init, within=environ.PositiveReals)

    # Variables
    m.Z = environ.Var(m.prev_stage, m.Resources, within=environ.Binary)
    m.D = environ.Var(m.current_stage, m.Resources, m.Periods,
                      within=environ.Binary)
    m.Y = environ.Var(m.current_stage, m.Periods, within=environ.Binary,
                      doc='1 if the wildfire is not content')

    # ------------
    # Objective
    # ------------

    def Obj_rule(m, s):
        return sum(m.C[i]*m.H[j]*m.D[s, i, j]
                   for i in m.Resources for j in m.Periods) \
                + m.NVC[s, 1] + sum(m.NVC[s, j]*m.Y[s, j-1]
                                    for j in m.Periods if j > 1)\
                + m.Y[s, max(m.Periods)]
    m.Obj = environ.Objective(m.current_stage, rule=Obj_rule,
                              sense=environ.minimize)

    # ------------
    # Constraints
    # ------------

    # end contention
    def end_contention_rule(m, s):
        return sum((m.H[j]-m.A[i])*m.PR[i]*m.D[s, i, j]
                   for i in m.Resources for j in m.Periods) \
                >= \
                m.PER[s, 1] + sum(m.PER[s, j]*m.Y[s, j-1]
                                  for j in m.Periods if j > 1)

    m.end_contention = environ.Constraint(m.current_stage,
                                          rule=end_contention_rule)

    # aircraft selection
    def selection_rule(m, s, i):
        return sum(m.D[s, i, j] for j in m.Periods) <= m.Z[s-1, i]
    m.selection = environ.Constraint(m.current_stage, m.Resources,
                                     rule=selection_rule)

    # contention
    def contention_rule(m, s, j):
        if j > 1:
            return m.SP[s, j]*m.Y[s, j-1] -\
                   sum((m.H[j]-m.A[i])*m.PR[i]*m.D[s, i, j]
                       for i in m.Resources) <= m.M*m.Y[s, j]
        else:
            return m.SP[s, j] \
                   - sum((m.H[j]-m.A[i])*m.PR[i]*m.D[s, i, j]
                         for i in m.Resources) \
                   <= m.M*m.Y[s, j]

    m.contention = environ.Constraint(m.current_stage, m.Periods,
                                      rule=contention_rule)
# --------------------------------------------------------------------------- #
