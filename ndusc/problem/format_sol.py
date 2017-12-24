# -*- coding: utf-8 -*-
"""Format pyomo problem solution."""

# Packages
import pyomo.environ as _pyenv
import logging as _log

# Package modules
import ndusc.error.error as _error


# get_sol_info ----------------------------------------------------------------
def get_sol_info(results, problem, solver_results, solver,
                 info=['variables', 'objective', 'solver_info',
                       'duals']
                 ):
    """Get solution.

    Get solution of pyomo concrete model.

    Args:
        results (:obj:`dict`): initialization of the results dictionary.
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.
        solver_results (:obj:`dict`): solver result.
        solver (:obj:`str`): solver name.
        info (:obj:`list`, opt): list strings with desired information to
            return. Options: ``'variables'``, ``'objective'``,
            ``'solver_info'``, ``'duals'``. Defaults to
            ``['variables', 'objective', 'solver_info', 'duals']``.

    Return:
        :obj:`dict`: solution.
    """
    # Get objective function value
    if 'objective' in info:
        results['objective'] = get_objective_info(problem)

    # Get variables value
    if 'variables' in info:
        results['variables'] = get_variables_info(problem)

    # Get solver information
    if 'solver_info' in info:
        results['solver'] = get_solver_info(solver_results)

    # Get duals
    if 'duals' in info:
        results['constraints'] = get_duals_info(problem, solver='gurobi')

    return results
# --------------------------------------------------------------------------- #


# get_variables_info ----------------------------------------------------------
def get_variables_info(problem):
    """Get variables information.

    Args:
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.

    Return:
        :obj:`dict`: variables information.
    """
    results = {}
    for v in problem.component_objects(_pyenv.Var, active=True):
        results[v.getname()] = {}
        varobject = getattr(problem, str(v))
        for index in varobject:
            results[v.getname()][index] = varobject[index].value

    return results
# --------------------------------------------------------------------------- #


# get_objective_info ----------------------------------------------------------
def get_objective_info(problem):
    """Get objective function information.

    Args:
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.

    Return:
        :obj:`dict`: objective information.
    """
    results = {}
    for o in problem.component_objects(_pyenv.Objective, active=True):
        o_name = o.getname()
        results[o_name] = {}
        oobject = getattr(problem, str(o))
        for index in oobject:
            results[o_name]['value'] = oobject[index]()

    return results
# --------------------------------------------------------------------------- #


# get_solver_info -------------------------------------------------------------
def get_solver_info(solver_results):
    """Get solver information.

    Args:
        solver_results (:obj:`dict`): solver result.

    Return:
        :obj:`dict`: solver information.
    """
    return solver_results['Solver'][0]
# --------------------------------------------------------------------------- #


# get_constraints_info --------------------------------------------------------
def get_constraints_info(problem, get_duals):
    """Get constraints information.

    Args:
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.
        get_duals (:obj:`bool`): ``True`` to return dual information.

    Return:
        :obj:`dict`: constraints information.
    """
    # Store dual variables
    results = {}
    for c in problem.component_objects(_pyenv.Constraint, active=True):
        results[c.getname()] = {}
        cobject = getattr(problem, str(c))
        for index in cobject:
            if get_duals:
                results[c.getname()][index] = {'dual':
                                               problem.dual[cobject[index]]}
    return results
# --------------------------------------------------------------------------- #


# get_duals_info --------------------------------------------------------------
def get_duals_info(problem, solver='gurobi'):
    """Get duals.

    Get duals from the relaxed problem.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        solver (:obj:`str`, opt): solver name. The disered solver must be in
            the path. Defaults to ``'gurobi'``.

    Return:
        :obj:`dict`: results information.
    """
    # If no dual information solve the relaxed problem
    if not hasattr(problem, 'dual'):
        problem, solver_results = problem.solve(solver, relaxed=True)

    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    _log.debug('\t\t* Status of the relaxed problem: ' + status)

    if status == 'optimal':
        get_duals = True
        return get_constraints_info(problem, get_duals)
    else:
        _error.infeasible_problem("'relaxed'")
# --------------------------------------------------------------------------- #
