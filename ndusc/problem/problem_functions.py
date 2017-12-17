# -*- coding: utf-8 -*-
"""Functionalities for Model class."""

# packages
import importlib.util as _importu
import pyomo.environ as _pyenv
import logging as _log

# package modules
from ndusc.problem import format_sol as _format_sol
import ndusc.error.error as _error


# fix_vars --------------------------------------------------------------------
def fix_vars(problem, vars_val):
    """Fix or unfix integer variables.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
            pyomo.
        vars_val (:obj:`dict`): dictionary with variables value
            information.
    """
    for v in vars_val.keys():
        if hasattr(problem, v):
            var = getattr(problem, v)
            for index in vars_val[v].keys():
                if index in var.keys():
                    variable = var[index]
                    variable.value = vars_val[v][index]
                    variable.fixed = True
    problem.preprocess()
# --------------------------------------------------------------------------- #


# get_vars --------------------------------------------------------------------
def get_var(problem, varname, index):
    """Get variables.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
            pyomo.
        var (:obj:`list`): variable name.
    Return:
        :obj:`pyomo.core.base.var._GeneralVarData`: pyomo variable.

    Todo: check all runs ok.
    """
    return getattr(problem, varname)[index]
# --------------------------------------------------------------------------- #


# load_from_file --------------------------------------------------------------
def load_from_file(problem, problem_file, function, data):
    """Load ConcreteModel from file.

    Load ConcreteModel from a function defined in a file and initialize the
    model with data information.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        problem_file (:obj:`str`): model filename.
        function (:obj:`str`): model function name.
        data (:obj:`dict`): dictionary with model data information.
    """
    spec = _importu.spec_from_file_location("problem", problem_file)
    if spec is not None:
        # Load module
        foo = _importu.module_from_spec(spec)
        spec.loader.exec_module(foo)

        # Load function
        try:
            problem_function = getattr(foo, function)
        except AttributeError:
            _error.function_not_found(problem_file, function)

        # Execute function
        problem_function(problem, data)

    else:
        _error.file_not_found(problem_file)
# --------------------------------------------------------------------------- #


# solve -----------------------------------------------------------------------
def solve(problem, solver='gurobi',
          info=['variables', 'objective', 'solver_info', 'duals']):
    """Solve.

    Solve a given problem.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        solver (:obj:`str`, opt): solver name. The disered solver must be in
            the path. Defaults to ``'gurobi'``.
        info (:obj:`list`, opt): list strings with desired information to
            return. Options: ``'variables'``, ``'objective'``,
            ``'solver_info'``, ``'duals'``. Defaults to
            ``['variables', 'objective', 'solver_info', 'duals']``.

    Return:
        :obj:`dict`: results information.
    """
    # Create a solver
    opt = _pyenv.SolverFactory(solver)

    # Create a model instance and optimize
    solver_results = opt.solve(problem)

    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    _log.info('Status: ' + status)
    if status == 'optimal':
        results = _format_sol.get_solution_info(problem, solver_results,
                                                solver, info)
        return results
    else:
        _error.infeasible_problem()
# --------------------------------------------------------------------------- #
