# -*- coding: utf-8 -*-
"""Functionalities for Model class."""

# packages
import importlib.util as _importu
import pyomo.environ as _pyenv
import logging as _log

# package modules
import ndusc.problem.format_sol as _format_sol
import ndusc.problem.extrem_directions as _ex_dir
import ndusc.problem.integer_utils as _int_u
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
def solve(problem, solver='gurobi', relaxed=False):
    """Solve.

    Solve a given problem.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of pyomo.
        solver (:obj:`str`, opt): solver name. The disered solver must be in
            the path. Defaults to ``'gurobi'``.
        relaxed (:obj:`bool`, opt): if ``True`` solve problem relaxation.
            Defaults to ``False``.

    Return:
        :obj:`tuple`: problem and solver results information.
    """
    # Create a solver
    opt = _pyenv.SolverFactory(solver)

    # Relax problem
    if relaxed:
        int_vars = _int_u.get_integer_vars(problem)
        _int_u.change_vars_domain(problem, int_vars, 'RealSet')

    # Create a model instance and optimize
    solver_results = opt.solve(problem)

    # Ask for dual information
    if relaxed:
        if not hasattr(problem, 'dual'):
            problem.del_component('dual')
        problem.dual = _pyenv.Suffix(direction=_pyenv.Suffix.IMPORT)

    # Create a model instance and optimize
    solver_results = opt.solve(problem)

    # Unrelax problem
    if relaxed:
        _int_u.change_vars_domain(problem, int_vars, 'IntegerSet')

    return problem, solver_results
# --------------------------------------------------------------------------- #


# solve_node ------------------------------------------------------------------
def solve_node(problem, solver='gurobi',
               info=['variables', 'objective', 'solver_info', 'duals']):
    """Solve a node problem.

    Solve a node of the nested decomposition algorithm.

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
    # Solve the problem
    problem, solver_results = problem.solve(solver, relaxed=False)

    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    results = {'status': status}

    _log.debug('\t\t* Status of the node problem: ' + status)
    if status == 'optimal':
        return _format_sol.get_sol_info(results, problem, solver_results,
                                        solver, info)
    else:
        info = ['solver_info', 'duals']
        _ex_dir.get_extr_direction_dual_problem(problem)
        problem, solver_results = problem.solve(solver, relaxed=True)
        new_status = str(solver_results['Solver'][0]['Termination condition'])
        if new_status == 'optimal':
            return _format_sol.get_sol_info(problem, solver_results, solver,
                                            info)
        else:
            _error.infeasible_problem("'extreme directions'")
# --------------------------------------------------------------------------- #


# problem_type ----------------------------------------------------------------
def problem_type(problem):
    """Get problem type.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
            pyomo.
    Return:
        :obj:`str`: more restricted problem type.
    """
    prob_type = 'continuous'
    for v in problem.component_objects(_pyenv.Var, active=True):
        for i in getattr(problem, str(v)):
                if hasattr(v[i], 'domain_type'):
                    if str(v[i].domain_type) == "IntegerSet":
                        prob_type = 'integer'
                elif hasattr(v[i], 'domain'):
                    if str(v[i].domain) in ["Integer", "Binary"]:
                        prob_type = 'integer'
    return prob_type
# --------------------------------------------------------------------------- #
