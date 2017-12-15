# -*- coding: utf-8 -*-
"""Module to create feasibility and optimality cuts.

Todo: Create cut functions for LP problems and MILP problems.
"""

# Packages
import pyomo.environ as _pyenv


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
    problem._Cuts_Feas = _pyenv.Set(initialize=feas_cuts['sets']['id'])
    problem._Vars = _pyenv.Set(initialize=feas_cuts['sets']['vars'])

    # Parameters
    problem._D = _pyenv.Param(problem._Cuts_Feas, problem._Vars,
                              initialize=feas_cuts['params']['D'],
                              mutable=True)
    problem._d = _pyenv.Param(problem._Cuts_Feas,
                              initialize=feas_cuts['params']['d'],
                              mutable=True)

    # Constraints
    def _feas_cuts_rule(problem, l):
        return sum([problem._D[l, (str(v), i)] *
                    getattr(problem, str(v))[i]
                    for v in problem.component_objects(_pyenv.Var, active=True)
                    if str(v) != 'Aux_Obj'
                    for i in v.index_set()
                    ]) >= problem._d[l]

    problem._feas_cuts = _pyenv.Constraint(problem._Cuts_Feas,
                                           rule=_feas_cuts_rule)
# --------------------------------------------------------------------------- #


# create_opt_cuts -------------------------------------------------------------
def create_opt_cuts(problem, opt_cuts):
    """Create optimality cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        cuts (:obj:`dict`): optimality cuts of the current node.

    Todo: Check if current optimality constraints exists.
    """
    # Sets
    problem._Cuts_Opt = _pyenv.Set(initialize=opt_cuts['sets']['cuts'])

    # Variables
    problem.Aux_Obj = _pyenv.Var()

    # Objective
    for o in problem.component_objects(_pyenv.Objective, active=True):
        if o.active:
            problem._Obj = _pyenv.Objective(rule=o.rule+problem.Aux_Obj)
            o.deactivate()

    # Constraints
    def _opt_cuts_rule(problem, l):
        return sum([opt_cuts['params']['E'][l][str(v)][i] *
                    getattr(problem, str(v))[i]
                    for v in problem.component_objects(_pyenv.Var, active=True)
                    if str(v) != 'Aux_Obj'
                    for i in v.index_set()
                    ]) + problem.Aux_Obj >= opt_cuts['params']['e'][l]

    problem._opt_cuts = _pyenv.Constraint(problem._Cuts_Opt,
                                          rule=_opt_cuts_rule)
# --------------------------------------------------------------------------- #


# create_feas_int_cuts --------------------------------------------------------
def create_feas_int_cuts(problem, opt_cuts):
    """Create feasibility integer cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        cuts (:obj:`dict`): optimality cuts of the current node.

    Todo: Check if current optimality constraints exists.
    """
    # Sets
    problem._Cuts_Opt = _pyenv.Set(initialize=opt_cuts['sets']['cuts'])

    # Variables
    problem.Aux_Obj = _pyenv.Var()

    # Objective
    for o in problem.component_objects(_pyenv.Objective, active=True):
        if o.active:
            problem._Obj = _pyenv.Objective(rule=o.rule+problem.Aux_Obj)
            o.deactivate()

    # Constraints
    def _opt_cuts_rule(problem, l):
        return sum([opt_cuts['params']['E'][l][str(v)][i] *
                    getattr(problem, str(v))[i]
                    for v in problem.component_objects(_pyenv.Var, active=True)
                    if str(v) != 'Aux_Obj'
                    for i in v.index_set()
                    ]) >= opt_cuts['params']['e'][l]

    problem._opt_cuts = _pyenv.Constraint(problem._Cuts_Opt,
                                          rule=_opt_cuts_rule)
# --------------------------------------------------------------------------- #


# create_opt_int_cuts ---------------------------------------------------------
def create_opt_int_cuts(problem, opt_cuts):
    """Create optimality integer cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        cuts (:obj:`dict`): optimality cuts of the current node.

    Todo: Check if current optimality constraints exists.
    """
    # Sets
    problem._Cuts_Opt = _pyenv.Set(initialize=opt_cuts['sets']['cuts'])

    # Variables
    problem.Aux_Obj = _pyenv.Var()

    # Objective
    for o in problem.component_objects(_pyenv.Objective, active=True):
        if o.active:
            problem._Obj = _pyenv.Objective(rule=o.rule+problem.Aux_Obj)
            o.deactivate()

    # Constraints
    def _opt_cuts_rule(problem, l):
        return sum([opt_cuts['params']['E'][l][str(v)][i] *
                    getattr(problem, str(v))[i]
                    for v in problem.component_objects(_pyenv.Var, active=True)
                    if str(v) != 'Aux_Obj'
                    for i in v.index_set()
                    ]) >= opt_cuts['params']['e'][l]

    problem._opt_cuts = _pyenv.Constraint(problem._Cuts_Opt,
                                          rule=_opt_cuts_rule)
# --------------------------------------------------------------------------- #
