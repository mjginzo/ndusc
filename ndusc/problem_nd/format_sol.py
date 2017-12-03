# -*- coding: utf-8 -*-
"""Format pyomo problem solution."""

# Packages
import pyomo.environ as pyenv


# get_solution ----------------------------------------------------------------
def get_solution(problem, solver_results, duals):
    """Get solution.

    Get solution of pyomo concrete model.

    Args:
        problem ()
        solver_results
        duals

    Return:
        :obj:`dict`:
    """
    # Results
    results = {}

    # Get objective function value
    results['objective'] = get_objective(problem)

    # Get variables value
    results['variables'] = get_variables(problem)

    # Get constraints
    if duals:
        results['constraints'] = get_constraints(problem)

    # Get solver information
    results['solver'] = get_solver_info(solver_results)

    return results
# --------------------------------------------------------------------------- #


# get_variables ---------------------------------------------------------------
def get_variables(problem):
    """Get variables information.

    Args:
        problem ():

    Return:
        :obj:`dict`:
    """
    results = {}
    for v in problem.component_objects(pyenv.Var, active=True):
        results[v.getname()] = {}
        varobject = getattr(problem, str(v))
        for index in varobject:
            results[v.getname()][index] = varobject[index].value

    return results
# --------------------------------------------------------------------------- #


# get_constraints -------------------------------------------------------------
def get_constraints(problem):
    """Get constraints information.

    Args:
        problem ():

    Return:
        :obj:`dict`:
    """
    results = {}
    for c in problem.component_objects(pyenv.Constraint, active=True):
        results[c.getname()] = {}
        cobject = getattr(problem, str(c))
        for index in cobject:
            print(str(c)+'_'+str(index))
            results[c.getname()][index]['dual'] = problem.dual.get(cobject[index])

    return results
# --------------------------------------------------------------------------- #


# get_objective ---------------------------------------------------------------
def get_objective(problem):
    """Get objective function information.

    Args:
        problem ():

    Return:
        :obj:`dict`:
    """
    results = {}
    for o in problem.component_objects(pyenv.Objective, active=True):
        results[o.getname()] = {}
        oobject = getattr(problem, str(o))
        results[o.getname()]['value'] = oobject()

    return results
# --------------------------------------------------------------------------- #


# get_solver_info -------------------------------------------------------------
def get_solver_info(solver_results):
    """Get solver information.

    Args:
        solver_results ():

    Return:
        :obj:`dict`:
    """
    return solver_results['Solver'][0]
# --------------------------------------------------------------------------- #
