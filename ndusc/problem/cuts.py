# -*- coding: utf-8 -*-
"""Module to create feasibility and optimality cuts."""

# Packages
import pyomo.environ as pyenv


# update_cuts -----------------------------------------------------------------
# def update_cuts(model, node):
#    """Update feasibility and optimality cuts.
#
#    Args:
#        node (:obj:`ndusc.node.Node`): tree node.
#    """
#
#    if 'feas' in node['cuts'].keys():
#        log.info('\t- feasibility cuts')
#        create_feas_cuts(model, node['cuts']['feas'])
#    if 'opt' in node['cuts'].keys():
#        log.info('\t- optimality cuts')
#        create_opt_cuts(model, node['cuts']['opt'])
# --------------------------------------------------------------------------- #


# create_feas_cuts ------------------------------------------------------------
def create_feas_cuts(problem, feas_cuts):
    """Create feasibility cuts.

    Args:
        problem (:obj:`ndusc.`): mathematical optimization problem.
        feas_cuts (:obj:`ndusc.cuts.Cuts`): cuts of the current node.

    Todo: ¿What happends when a variable has not index?
    """
    # Sets
    problem._Cuts_Feas = pyenv.Set(initialize=feas_cuts['sets']['id'])
    problem._Vars = pyenv.Set(initialize=feas_cuts['sets']['vars'])

    # Parameters
    problem._D = pyenv.Param(problem._Cuts_Feas, problem._Vars,
                             initialize=feas_cuts['params']['D'],
                             mutable=True)
    problem._d = pyenv.Param(problem._Cuts_Feas,
                             initialize=feas_cuts['params']['d'],
                             mutable=True)

    # Constraints
    def _feas_cuts_rule(problem, l):
        return sum([problem._D[l, (str(v), i)] *
                    getattr(problem, str(v))[i]
                    for v in problem.component_objects(pyenv.Var, active=True)
                    if str(v) != 'Aux_Obj'
                    for i in v.index_set()
                    ]) >= problem._d[l]

    problem._feas_cuts = pyenv.Constraint(problem._Cuts_Feas,
                                          rule=_feas_cuts_rule)
# --------------------------------------------------------------------------- #


# update_feas_cuts ------------------------------------------------------------
def update_feas_cuts(problem, feas_cuts):
    """Update feasibility cuts.

    Args:
        problem (:obj:`ndusc.`): mathematical optimization problem.
        feas_cuts (:obj:`ndusc.cuts.Cuts`): cuts of the current node.
    """
    new_id = feas_cuts['sets']['id'][0]

    # Sets
    problem._Cuts_Feas.add(new_id)

    # Parameters
    for v in feas_cuts['sets']['vars']:
        new_index = (new_id, v[0], v[1])
        new_value = feas_cuts['params']['D'][(new_id, v[0], v[1])]
        problem._D[new_index] = new_value

    problem._d[new_id] = feas_cuts['params']['d'][new_id]

    # Constraints
    problem._feas_cuts.reconstruct()
# --------------------------------------------------------------------------- #


# create_opt_cuts -------------------------------------------------------------
def create_opt_cuts(problem, opt_cuts):
    """Create feasibility cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        cuts (:obj:`dict`): optimality cuts of the current node.

    Todo: Check if current optimality constraints exists.
    """
    # Sets
    problem._Cuts_Opt = pyenv.Set(initialize=opt_cuts['sets']['cuts'])

    # Variables
    problem.Aux_Obj = pyenv.Var()

    # Objective
    for o in problem.component_objects(pyenv.Objective, active=True):
        if o.active:
            problem._Obj = pyenv.Objective(rule=o.rule+problem.Aux_Obj)
            o.deactivate()

    # Constraints
    def _opt_cuts_rule(problem, l):
        return sum([opt_cuts['params']['E'][l][str(v)][i] *
                    getattr(problem, str(v))[i]
                    for v in problem.component_objects(pyenv.Var, active=True)
                    if str(v) != 'Aux_Obj'
                    for i in v.index_set()
                    ]) >= opt_cuts['params']['e'][l]

    problem._opt_cuts = pyenv.Constraint(problem._Cuts_Opt,
                                         rule=_opt_cuts_rule)
# --------------------------------------------------------------------------- #
