# -*- coding: utf-8 -*-
"""Format pyomo problem solution."""

# Packages
import pyomo.environ as pyenv
import logging as log


# get_solution ----------------------------------------------------------------
def get_solution(problem, solver_results, duals, solver):
    """Get solution.

    Get solution of pyomo concrete model.

    Args:
        problem (:obj:`ndusc.problem.problem.Problem`): mathematical problem.
        solver_results (:obj:`dict`): solver result.
        duals
        solver

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
        results['constraints'] = get_constraints(problem, duals, solver)

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
def get_constraints(problem, duals, solver):
    """Get constraints information.

    Args:
        problem ():

    Return:
        :obj:`dict`:
    """
    # fix_integer_vars --------------------------------------------------------
    def fix_integer_vars(problem, fix=True):
        """Fix or unfix integer variables.

        Args:
            problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
                pyomo.
            fix (:obj:`str`, opt): if ``True`` fix integer variables. Defaults
                to ``True``.
        """
        #integer = ['Binary', 'Integer']
        for v in problem.component_objects(pyenv.Var, active=True):
            vobject = getattr(problem, str(v))
            for i in vobject:
                if str(v[i].domain_type) in "IntegerSet":
                    v[i].fixed = fix
        problem.preprocess()
    # ----------------------------------------------------------------------- #

    # change_vars_domain ------------------------------------------------------
    def change_vars_domain(problem, vars, new_domain):
        """Relax or unrelax integer variables.

        Args:
            problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
                pyomo.
            vars (:obj:`list`): list of variables of pyomo to change domain.
            new_domain (:obj:`str`): domain to change desired variables.
                Options: ``'RealSet'`` or ``'IntegerSet'``.
        """
        if new_domain == 'RealSet':
            domain_type = pyenv.RealSet
        elif new_domain == 'IntegerSet':
            domain_type = pyenv.IntegerSet
        else:
            raise NameError("""Unknown domain_type = {}.
                            Allowed options: "RealSet" or "IntegerSet"
                            """.format(domain_type))
        import pdb; pdb.set_trace()
        for v in vars:
            v.domain_type = domain_type
        problem.preprocess()
    # ----------------------------------------------------------------------- #

    # integer_vars ------------------------------------------------------
    def integer_vars(problem):
        """Return integer variables.

        Args:
            problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
                pyomo.
        Return:
            :obj:`list`: list of variables of pyomo.

        Todo: check all runs ok.
        """
        import pdb; pdb.set_trace()
        vars = []
        for v in problem.component_objects(pyenv.Var, active=True):
            for i in getattr(problem, str(v)):
                    if hasattr(v[i], 'domain_type'):
                        if str(v[i].domain_type) == "IntegerSet":
                            vars = vars + [v[i]]
                    elif hasattr(v[i], 'domain'):
                        if str(v[i].domain) in ["Integer", "Binary"]:
                            vars = vars + [v[i]]
        return vars
    # ----------------------------------------------------------------------- #

    # Get duals (of the relaxed problem)
    if duals:
        vars = integer_vars(problem)
        change_vars_domain(problem, vars, new_domain)
        if not hasattr(problem, 'dual'):
            log.info('Removing dual attribute')
            problem.del_component('dual')
        problem.dual = pyenv.Suffix(direction=pyenv.Suffix.IMPORT)
        opt = pyenv.SolverFactory(solver)
        solver_results = opt.solve(problem)
        change_vars_domain(problem, vars, domain_type)

    # Solve proble to get dual variables
    #
    #

    # Store dual variables
    results = {}
    for c in problem.component_objects(pyenv.Constraint, active=True):
        results[c.getname()] = {}
        cobject = getattr(problem, str(c))
        for index in cobject:
            results[c.getname()][index] = {'dual': problem.dual[cobject[index]]}

    # Unfix integer variables

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
