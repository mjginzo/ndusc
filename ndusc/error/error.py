# -*- coding: utf-8 -*-
"""Module with error messages."""


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
def infeasible_problem():
    """Error message when the problem is infeasible."""
    raise ValueError('Infeasible problem.')
# --------------------------------------------------------------------------- #
