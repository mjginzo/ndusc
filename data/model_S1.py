#  _________________________________________________________________________
#
#  Example: stochastic problem from the thesis of Lee.
#  First stage model.
#  _________________________________________________________________________

#
# Imports
#

from pyomo.environ import *

def model_S1(data):
    #
    # Model
    #

    model = ConcreteModel()

    #
    # Sets
    #

    model.Resources = Set(initialize=data['sets']['Resources'])

    #
    # Parameters
    #

    model.P = Param(model.Resources, 
                    initialize=data['params']['P'], 
                    within=PositiveReals)

    #
    # Variables
    #

    model.Z = Var(model.Resources, within=Binary)

    #
    # Objective
    #

    def Obj_rule(model):
        return  + sum(model.P[i]*model.Z[i] for i in model.Resources)
    
    model.Obj = Objective(rule=Obj_rule, sense=minimize)
    
    return model

