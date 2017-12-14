# -*- coding: utf-8 -*-
"""Functionalities for Model class."""

# packages
import pyomo.environ as _pyenv
import logging as _log

# package modules
from ndusc.problem import format_sol as _format_sol
from ndusc.problem import integer_utils as _integer_utils


# load_from_file --------------------------------------------------------------
def load_from_file(problem, file, function, data):
    """Load ConcreteModel from file.

    Load ConcreteModel from a function defined in a file and initialize the
    model with data information.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        file (:obj:`str`): model filename.
        function (:obj:`str`): model function name.
        data (:obj:`dict`): dictionary with model data information.
    """
    with open(file, 'r') as model_file:
        exec(model_file.read())
    eval("{}(problem, data)".format(function))
# --------------------------------------------------------------------------- #


# solve -----------------------------------------------------------------------
def solve(problem, solver='gurobi', duals=True):
    """Solve.

    Solve a given problem.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        solver (:obj:`str`, opt): solver name. The disered solver must be in
            the path. Defaults to ``'gurobi'``.
        duals (:obj:`bool`, opt): if ``True`` return dual information. Defaults
            to ``True``.

    Return:
        :obj:`dict`: results information.
    """
    # Create a solver
    opt = _pyenv.SolverFactory(solver)

    if duals:
        int_vars = _integer_utils.get_integer_vars(problem)
        if len(int_vars) == 0:
            if not hasattr(problem, 'dual'):
                problem.del_component('dual')
            problem.dual = _pyenv.Suffix(direction=_pyenv.Suffix.IMPORT)
        else:
            raise ValueError('Integer problem has not dual information.')

    # Create a model instance and optimize
    solver_results = opt.solve(problem)

    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    _log.info('Status: ' + status)
    if status == 'optimal':
        results = _format_sol.get_solution(problem, solver_results,
                                           duals, solver)
        return solver_results, results
    else:
        raise ValueError('Infeasible Problem.')
# --------------------------------------------------------------------------- #
