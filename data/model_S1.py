"""
First stage model of the stochastic problem from the thesis of Lee.
"""
#
# Imports
#


def model_S1(model, data):
    """."""
    import pyomo.environ as pyenv
    #
    # Model
    #

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

    def Obj_rule(self):
        """."""
        return sum(model.P[i]*model.Z[i] for i in model.Resources)

    model.Obj = pyenv.Objective(rule=Obj_rule, sense=pyenv.minimize)
