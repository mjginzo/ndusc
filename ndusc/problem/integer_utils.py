# -*- coding: utf-8 -*-
"""Module with pyomo utilities to work with MIP.

Todo: Check functions.
"""

# Python packages
import pyomo.environ as _pyenv


# relax -----------------------------------------------------------------------
def relax(problem):
    """Relax the integer variables.

    Change domain of all integer variables to the Real set insted of Integer
    set.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
            pyomo.
    """
    integer_vars = get_integer_vars(problem)
    change_vars_domain(problem, integer_vars, 'RealSet')
# --------------------------------------------------------------------------- #


# change_vars_domain ----------------------------------------------------------
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
        domain_type = _pyenv.RealSet
    elif new_domain == 'IntegerSet':
        domain_type = _pyenv.IntegerSet
    else:
        raise NameError("""Unknown domain_type = {}.
                        Allowed options: "RealSet" or "IntegerSet"
                        """.format(domain_type))
    for v in vars:
        v.domain_type = domain_type
    problem.preprocess()
# --------------------------------------------------------------------------- #


# get_integer_vars ------------------------------------------------------------
def get_integer_vars(problem):
    """Get integer variables.

    Args:
        problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
            pyomo.
    Return:
        :obj:`list`: list of variables of pyomo.

    Todo: check all runs ok.
    """
    integer_vars = []
    for v in problem.component_objects(_pyenv.Var, active=True):
        for i in getattr(problem, str(v)):
                if hasattr(v[i], 'domain_type'):
                    if str(v[i].domain_type) == "IntegerSet":
                        integer_vars = integer_vars + [v[i]]
                elif hasattr(v[i], 'domain'):
                    if str(v[i].domain) in ["Integer", "Binary"]:
                        integer_vars = integer_vars + [v[i]]
    return integer_vars
# --------------------------------------------------------------------------- #
