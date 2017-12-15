# -*- coding: utf-8 -*-
"""Format pyomo problem solution."""

# Packages
import pyomo.environ as _pyenv


# get_solution ----------------------------------------------------------------
def get_solution(problem, solver_results, get_duals, solver):
    """Get solution.

    Get solution of pyomo concrete model.

    Args:
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.
        solver_results (:obj:`dict`): solver result.
        get_duals (:obj:`bool`): ``True`` to return dual information.
        solver (:obj:`str`): solver name.

    Return:
        :obj:`dict`: solution.
    """
    # Results
    results = {}

    # Get objective function value
    results['objective'] = get_objective(problem)

    # Get variables value
    results['variables'] = get_variables(problem)

    # Get constraints
    if get_duals:
        relaxed_problem =
        results['constraints'] = get_constraints(problem, get_duals, solver)

    # Get solver information
    results['solver'] = get_solver_info(solver_results)

    return results
# --------------------------------------------------------------------------- #


# get_variables ---------------------------------------------------------------
def get_variables(problem):
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


# get_constraints -------------------------------------------------------------
def get_constraints(problem, get_duals):
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


# get_relaxed_problem_sol -----------------------------------------------------
def get_relaxed_problem_sol(problem, solver='gurobi'):
    """Get duals.

    Get duals from the relaxed problem.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        solver (:obj:`str`, opt): solver name. The disered solver must be in
            the path. Defaults to ``'gurobi'``.

    Return:
        :obj:`dict`: results information.
    """
    # Create a solver
    opt = _pyenv.SolverFactory(solver)

    # Relax problem
    int_vars = _integer_utils.get_integer_vars(problem)
    _integer_utils.change_vars_domain(problem, int_vars, 'RealSet')

    # Ask for dual information
    problem.dual = _pyenv.Suffix(direction=_pyenv.Suffix.IMPORT)

    # Create a model instance and optimize
    solver_results = opt.solve(problem)

    # Unrelax problem
    _integer_utils.change_vars_domain(problem, int_vars, 'IntegerSet')

    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    _log.debug('Status of the relaxed problem: ' + status)
    if status == 'optimal':
        results = _format_sol.get_solution(problem, solver_results,
                                           duals, solver)
        return results
    else:
        raise ValueError('Infeasible Problem.')
# --------------------------------------------------------------------------- #


# get_objective ---------------------------------------------------------------
def get_objective(problem):
    """Get objective function information.

    Args:
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.

    Return:
        :obj:`dict`: objective information.
    """
    results = {}
    for o in problem.component_objects(_pyenv.Objective, active=True):
        results[o.getname()] = {}
        oobject = getattr(problem, str(o))
        results[o.getname()]['value'] = oobject()

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
