from pyomo.environ import *

# get_solution -----------------------------------------------------------------
def get_solution(problem, solver_results, duals):
    """
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
# ---------------------------------------------------------------------------- #


# get_variables ----------------------------------------------------------------
def get_variables(problem):
    """
    """
    results = {}
    for v in problem.component_objects(Var, active=True):
        results[v.getname()] = {}
        varobject = getattr(problem, str(v))
        for index in varobject:
            results[v.getname()][index] = varobject[index].value
    
    return results
# ---------------------------------------------------------------------------- #

# get_constraints --------------------------------------------------------------
def get_constraints(problem):
    """
    """
    results = {}
    for c in problem.component_objects(Constraint, active=True):
        results[c.getname()] = {}
        cobject = getattr(problem, str(c))
        for index in cbject:
            results[c.getname()][index]['dual'] = problem.dual[cobject[index]]
    
    return results
# ---------------------------------------------------------------------------- #

# get_constraints --------------------------------------------------------------
def get_constraints(problem):
    """
    """
    results = {}
    for c in problem.component_objects(Constraint, active=True):
        results[c.getname()] = {}
        cobject = getattr(problem, str(c))
        for index in cbject:
            results[c.getname()][index]['dual'] = problem.dual[cobject[index]]
    
    return results
# ---------------------------------------------------------------------------- #

# get_objective ----------------------------------------------------------------
def get_objective(problem):
    """
    """
    results = {}
    for o in problem.component_objects(Objective, active=True):
        results[o.getname()] = {}
        oobject = getattr(problem, str(o))
        results[o.getname()]['value'] = oobject()
    
    return results
# ---------------------------------------------------------------------------- #

# get_solver_info ---------------------------------------------------------
def get_solver_info(solver_results):
    """
    """
    return solver_results['Solver'][0]
# ---------------------------------------------------------------------------- #