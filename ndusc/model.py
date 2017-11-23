from pyomo.environ import *

import logging as log

import format_sol

def load(file, function, data):
    execfile(file)
    return eval("{}(data)".format(function))


def solve(problem, solver='gurobi', duals=True):
    """
    """
    # Create a solver
    opt = SolverFactory(solver)
    
    # Get duals
    problem.dual = Suffix(direction=Suffix.IMPORT)
    
    # Create a model instance and optimize
    solver_results = opt.solve(problem)
    
    # Obtain results
    status = str(solver_results['Solver'][0]['Termination condition'])
    log.info('Status: ' + status)
    if status == 'optimal':
        results = format_sol.get_solution(problem, solver_results, duals)
    elif status == 'infeasible':
        results = None
    else:
        results = None
    
    return solver_results, results