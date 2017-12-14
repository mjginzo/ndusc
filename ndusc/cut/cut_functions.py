# -*- coding: utf-8 -*-
"""Functions to compute new cuts in the nested decomposition method.

Todo: Create cut functions.
Todo: Could be tree methods?
"""


# compute_cuts ----------------------------------------------------------------
def compute_cuts(tree, node):
    """Compute new cuts parameters.

    Given the successor nodes, computes the needed cuts parameters.

    Args:
        node (:obj:`int` or `str`): node id.
        tree (:obj:`Tree`): tree.
    """
    tree = compute_feas_cuts(tree)
    tree = compute_feas_cuts(tree)

    return tree
# --------------------------------------------------------------------------- #


# compute_feas_cuts -----------------------------------------------------------
def compute_feas_cuts(tree, node):
    """Compute feasibility cuts parameters.

    Args:
        node (:obj:`int` or `str`): node id.
        tree (:obj:`Tree`): tree.
    """
    return tree
# --------------------------------------------------------------------------- #


# compute_opt_cuts ------------------------------------------------------------
def compute_opt_cuts(tree, node):
    """Compute optimality cuts parameters.

    Args:
        node (:obj:`int` or `str`): node id.
        tree (:obj:`Tree`): tree.
    """
    return tree
# --------------------------------------------------------------------------- #
