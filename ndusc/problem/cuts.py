# -*- coding: utf-8 -*-
"""Module to create feasibility and optimality cuts.

Todo: Create cut functions for LP problems and MILP problems.
"""

# Packages
import pyomo.environ as _pyenv


# create_feas_cuts ------------------------------------------------------------
def create_feas_cuts(problem, feas_cuts):
    """Create feasibility cuts.

    Args:
        problem (:obj:`ndusc.`): mathematical optimization problem.
        feas_cuts (:obj:`ndusc.cuts.Cuts`): feasibility cuts of the current
            node.

    Todo: ¿What happends when a variable has not index?
    """
    # Sets
    problem._Cuts_Feas = _pyenv.Set(initialize=[i for i in feas_cuts.keys()])

    # Constraints
    def _feas_cuts_rule(problem, l):
        return sum([feas_cuts[l]['A'][v][i] *
                    getattr(problem, v)[i]
                    for v in feas_cuts[l]['A'].keys()
                    if v != 'Aux_Obj'
                    for i in feas_cuts[l]['A'][v].keys()
                    ]) >= feas_cuts[l]['rhs']

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
    """
    # Sets
    problem._Cuts_Opt = _pyenv.Set(initialize=[i for i in opt_cuts.keys()])

    # Variables
    problem.Aux_Obj = _pyenv.Var()

    # Objective
    for o in problem.component_objects(_pyenv.Objective, active=True):
        if o.active:
            expression = sum([o.rule(problem, s)
                              for s in problem.current_stage])+problem.Aux_Obj
            problem._Obj = _pyenv.Objective(expr=expression)
            o.deactivate()

    # Constraints
    def _opt_cuts_rule(problem, l):
        return sum([opt_cuts[l]['A'][v][i] *
                    getattr(problem, v)[i]
                    for v in opt_cuts[l]['A'].keys()
                    if v != 'Aux_Obj'
                    for i in opt_cuts[l]['A'][v].keys()
                    ]) + problem.Aux_Obj >= opt_cuts[l]['rhs']

    problem._opt_cuts = _pyenv.Constraint(problem._Cuts_Opt,
                                          rule=_opt_cuts_rule)
# --------------------------------------------------------------------------- #


# create_bin_feas_cuts --------------------------------------------------------
def create_bin_feas_cuts(problem, bin_feas_cuts):
    """Create binary feasibility cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        bin_feas_cuts (:obj:`dict`): cuts information.

    Todo: Check if current optimality constraints exists.
    """
    # Sets
    set_bin_feas_cuts = [i for i in bin_feas_cuts.keys()]
    problem._Cuts_Bin_Feas = _pyenv.Set(initialize=set_bin_feas_cuts)

    # Constraints
    def _bin_feas_cuts_rule(problem, l):
        return sum([bin_feas_cuts[l]['A'][v][i] *
                    getattr(problem, v)[i]
                    for v in bin_feas_cuts[l]['A'].keys()
                    if v != 'Aux_Obj'
                    for i in bin_feas_cuts[l]['A'][v].keys()
                    ]) >= bin_feas_cuts[l]['rhs']

    problem._bin_feas_cuts = _pyenv.Constraint(problem._Cuts_Bin_Feas,
                                               rule=_bin_feas_cuts_rule)
# --------------------------------------------------------------------------- #


# create_bin_opt_cuts ---------------------------------------------------------
def create_bin_opt_cuts(problem, bin_opt_cuts):
    """Create optimality integer cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        bin_opt_cuts (:obj:`dict`): binary optimality cuts of the current node.

    Todo: Check if current optimality constraints exists.
    """
    # Sets
    set_bin_opt_cuts = [i for i in bin_opt_cuts.keys()]
    problem._Cuts_Bin_Opt = _pyenv.Set(initialize=set_bin_opt_cuts)

    # Constraints
    def _bin_opt_cuts_rule(problem, l):
        return sum([bin_opt_cuts[l]['A'][v][i] *
                    getattr(problem, v)[i]
                    for v in bin_opt_cuts[l]['A'].keys()
                    if v != 'Aux_Obj'
                    for i in bin_opt_cuts[l]['A'][v].keys()
                    ]) + problem.Aux_Obj >= bin_opt_cuts[l]['rhs']

    problem._bin_opt_cuts = _pyenv.Constraint(problem._Cuts_Bin_Opt,
                                              rule=_bin_opt_cuts_rule)
# --------------------------------------------------------------------------- #
