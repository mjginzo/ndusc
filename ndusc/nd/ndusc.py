# -*- coding: utf-8 -*-
"""Nested decomposition with usc utilities module."""
# Python packages
import logging as _log

# Package modules
import ndusc.tree.tree as _tree
import ndusc.nd.nd as _nd
import ndusc.error.error as _error


# ndusc -----------------------------------------------------------------------
def ndusc(tree_dic, data_dic, solver='gurobi'):
    """Nested decomposition algorithm with usc utilities.

    Args:
        tree_dic (:obj:`dict`): tree with node information.
        data_dic (:obj:`dict`): general data.
        solver (:obj:`str`, opt): solver name. Defaults to ``'gurobi'``.

    Return:
        :obj:`dict`: solution.

    Example:
        >>> import ndusc.examples.input_module as im
        >>> import ndusc.nd.ndusc as ndusc
        >>> data = im.input_module_example()
        >>> tree_dic = data.load_tree()
        >>> data_dic = data.load_data()
        >>> solver = 'gurobi'
        >>> tree = ndusc.ndusc(tree_dic, data_dic, solver)
    """
    # Get tree
    tree = _tree.Tree(tree_dic, data_dic)

    problem_type = tree.problem_type()

    if problem_type == 'continuous':
        return _nd.nd(tree, solver='gurobi', problem_type=problem_type)
    else:
        _log.info('SOLVE RELAXATION')
        cont_tree = _nd.nd(tree, solver='gurobi', problem_type='continuous')
        L = cont_tree.ev()
        _log.info('SOLVE BINARY PROBLEM')
        return _nd.nd(tree, solver='gurobi', problem_type=problem_type, L=L)
# --------------------------------------------------------------------------- #
