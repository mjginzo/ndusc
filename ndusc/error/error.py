# -*- coding: utf-8 -*-
"""Module with error messages."""


# -----------------------
# Nested Decomposition
# -----------------------

# parameter_problem_type ------------------------------------------------------
def parameter_problem_type(problem_type):
    """Error message when unknown problem_type parameter."""
    raise ValueError(("Unknown problem_type parameter: {}."
                     "\nAllowed options: 'continuous' or 'binary'."
                      ).format(problem_type))


# -----------------------
# Trees
# -----------------------

# no_root_node ----------------------------------------------------------------
def no_root_node():
    """Error message when no nodes with prev_id == None."""
    raise ValueError("No root node.")
# --------------------------------------------------------------------------- #


# multiple_root_node ----------------------------------------------------------
def multiple_root_node():
    """Error message when multiple root nodes."""
    raise ValueError("Multiple root nodes.")
# --------------------------------------------------------------------------- #


# mutiple_parents -------------------------------------------------------------
def mutiple_parents(id):
    """Error message when a node has multiple parents."""
    raise ValueError("Node '{}' has multiple parents.".format(id))
# --------------------------------------------------------------------------- #


# mutiple_ids -----------------------------------------------------------------
def mutiple_ids(id):
    """Error message when node id is duplicated."""
    raise ValueError("Node '{}' is duplicated.".format(id))
# --------------------------------------------------------------------------- #


# no_node_id ------------------------------------------------------------------
def no_node_id(id):
    """Error message when no node id."""
    raise ValueError("No node '{}' id.".format(id))
# --------------------------------------------------------------------------- #


# -----------------------
# Node
# -----------------------

# no_solved -------------------------------------------------------------------
def no_solved(id):
    """Error message when node is not solved."""
    raise ValueError("Node '{}' id is not solved.".format(id))
# --------------------------------------------------------------------------- #


# no_solution -----------------------------------------------------------------
def no_solution(id):
    """Error message when node has not a solution."""
    raise ValueError("Node '{}' id has not a solution.".format(id))
# --------------------------------------------------------------------------- #


# -----------------------
# Problem
# -----------------------

# funtion_not_found -----------------------------------------------------------
def funtion_not_found(filename, function):
    """Error message when function not found."""
    raise AttributeError("Filename {} has no function '{}'.".format(filename,
                                                                    function))
# --------------------------------------------------------------------------- #


# file_not_found --------------------------------------------------------------
def file_not_found(filename):
    """Error message when file not found."""
    raise IOError("File '{}' not found.".format(filename))
# --------------------------------------------------------------------------- #


# infeasible_problem ----------------------------------------------------------
def infeasible_problem(problem_info=None):
    """Error message when the problem is infeasible."""
    if problem_info:
        raise ValueError('Infeasible {} problem.'.format(problem_info))
    else:
        raise ValueError('Infeasible problem.')
# --------------------------------------------------------------------------- #
