"""Module to compute extreme directions of the dual problem."""
# Python packages
import pyomo.environ as _pyenv


# get_extr_direction_dual_problem ---------------------------------------------
def get_extr_direction_dual_problem(problem):
    """Create optimality cuts.

    Args:
        problem (:obj:`ndusc.problem.Problem`): mathematical optimization
            problem.
        cuts (:obj:`dict`): optimality cuts of the current node.
    """
    # Add slack variables
    problem._v_plus = _pyenv.Var(within=_pyenv.PositiveReals)
    problem._v_minus = _pyenv.Var(within=_pyenv.PositiveReals)

    # Convert to cone
    for c in problem.component_objects(_pyenv.Constraint, active=True):
        cobject = getattr(problem, str(c))
        for i in cobject:
            constr = cobject[i]
            if constr.lower is not None:
                constr._body = constr.body + problem._v_plus
                constr._lower = 0
            if constr.upper:
                constr._body = constr.body - problem._v_minus
                constr._upper = 0
            constr._equality = True

    # Objective
    for o in problem.component_objects(_pyenv.Objective, active=True):
        if o.active:
            o.deactivate()

    problem._Extr_Dir_Obj = _pyenv.Objective(expr=problem._v_plus +
                                             problem._v_minus)
# --------------------------------------------------------------------------- #
