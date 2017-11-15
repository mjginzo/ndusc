#  _________________________________________________________________________
#
#  Example: stochastic problem from the thesis of Lee.
#  Second stage model.
#  _________________________________________________________________________

#
# Imports
#

from pyomo.environ import *


def model_S2(data):
    #
    # Model
    #

    model = ConcreteModel()

    #
    # Sets
    #

    model.Resources = Set(initialize=data['sets']['Resources'])

    model.NumPer = Param(initialize=data['params']['NumPer'], within=Integers)

    def Periods_rule(model):
        return set(range(1, model.NumPer()+1))

    model.Periods = Set(initialize=Periods_rule)

    #
    # Parameters
    #

    model.C = Param(model.Resources, initialize=data['params']['C'], within=PositiveReals)

    model.A = Param(model.Resources, initialize=data['params']['A'], within=PositiveReals)

    model.PR = Param(model.Resources, initialize=data['params']['PR'], within=PositiveReals)

    model.H = Param(model.Periods, initialize=data['params']['H'], within=PositiveReals)

    model.NVC = Param(model.Periods, initialize=data['params']['NVC'], within=PositiveReals)

    model.SP = Param(model.Periods, initialize=data['params']['SP'], within=PositiveReals)

    def PER_init(model, p):
        if p == 1:
            return model.SP[p]
        else:
            return model.SP[p]-model.SP[p-1]

    model.PER = Param(model.Periods, initialize=PER_init, within=PositiveReals)

    def M_init(model):
        return max(model.SP)

    model.M = Param(initialize=M_init ,within=PositiveReals)

    model.Z = Param(model.Resources, initialize=data['params']['Z'])

    #
    # Variables
    #

    model.D = Var(model.Resources, model.Periods, within=Binary)

    model.Y = Var(model.Periods, within=Binary, doc='1 if the wildfire is not content')

    #
    # Objective
    #

    def Obj_rule(model):
        return sum(model.C[i]*model.H[j]*model.D[i,j]
                    for i in model.Resources for j in model.Periods) \
                + model.NVC[1] + sum(model.NVC[j]*model.Y[j-1]
                    for j in model.Periods if j > 1)\
                + model.Y[model.NumPer]
    model.Obj = Objective(rule=Obj_rule, sense=minimize)

    #
    # Constraints
    #

    def end_contention_rule(model):
        return sum((model.H[j]-model.A[i])*model.PR[i]*model.D[i,j] 
                    for i in model.Resources for j in model.Periods) \
                >= \
                model.PER[1] \
                + sum(model.PER[j]*model.Y[j-1] for j in model.Periods if j > 1)

    model.end_contention = Constraint(rule=end_contention_rule)

    def selection_rule(model, i):
        return sum(model.D[i,j] for j in model.Periods) <= model.Z[i]

    model.selection = Constraint(model.Resources, rule=selection_rule)

    def contention_rule(model, j):
        if j > 1:
            return model.SP[j]*model.Y[j-1] \
            -sum((model.H[j]-model.A[i])*model.PR[i]*model.D[i,j] 
                    for i in model.Resources) \
                <= model.M*model.Y[j]
        else:
            return model.SP[j] \
            -sum((model.H[j]-model.A[i])*model.PR[i]*model.D[i,j] 
                    for i in model.Resources) \
                <= model.M*model.Y[j]

    model.contention = Constraint(model.Periods, rule=contention_rule)
    return model