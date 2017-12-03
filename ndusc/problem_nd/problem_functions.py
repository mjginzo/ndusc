# -*- coding: utf-8 -*-
"""Functionalities for Model class."""

# packages
import pyomo.environ as pyenv
import logging as log

# package modules
import ndusc.problem_nd.format_sol as format_sol


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
    opt = pyenv.SolverFactory(solver)

    # Create a model instance and optimize
    solver_results = opt.solve(problem)

    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    log.info('Status: ' + status)
    if status == 'optimal':
        results = format_sol.get_solution(problem, solver_results, duals)
        return solver_results, results
    else:
        raise ValueError('Infeasible Problem.')
# --------------------------------------------------------------------------- #
