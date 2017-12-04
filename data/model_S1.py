#  _________________________________________________________________________
#
#  Example: stochastic problem from the thesis of Lee.
#  First stage model.
#  _________________________________________________________________________

#
# Imports
#
import pyomo.environ as pyenv


def model_S1(data):
    #
    # Model
    #

    model = pyenv.ConcreteModel()

    #
    # Sets
    #
    model.Resources = pyenv.Set(initialize=data['sets']['Resources'])

    #
    # Parameters
    #


    model.P = pyenv.Param(model.Resources,
                          initialize=data['params']['P'],
                          within=pyenv.PositiveReals)


    #
    # Variables
    #

    model.Z = pyenv.Var(model.Resources, within=pyenv.Binary)


    #
    # Objective
    #

    def Obj_rule(model):
        return  + sum(model.P[i]*model.Z[i] for i in model.Resources)

    model.Obj = pyenv.Objective(rule=Obj_rule, sense=pyenv.minimize)


    return model
