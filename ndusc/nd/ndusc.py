# -*- coding: utf-8 -*-
"""Nested decomposition with usc utilities module."""
# Python packages
import logging as _log

# Package modules
import ndusc.tree.tree as _tree
import ndusc.nd.nd as _nd
import ndusc.error.error as _error


# ndusc -----------------------------------------------------------------------
def ndusc(tree_dic, data_dic, config):
    """Nested decomposition algorithm with usc utilities.

    Args:
        tree_dic (:obj:`dict`): tree with node information.
        data_dic (:obj:`dict`): general data.
        config (:obj:`Configure`): configuration file

    Return:
        :obj:`dict`: solution.

    Example:
        >>> import ndusc.examples.input_module as im
        >>> import ndusc.nd.ndusc as ndusc
        >>> import ndusc.nd.configuration as _config
        >>> data = im.input_module_example()
        >>> tree_dic = data.load_tree()
        >>> data_dic = data.load_data()
        >>> config = _config.Configure()
        >>> tree = ndusc.ndusc(tree_dic, data_dic, config)
    """
    # Get tree
    tree = _tree.Tree(tree_dic, data_dic)

    problem_type = tree.problem_type()

    if problem_type == 'continuous':
        return _nd.nd(tree, config, problem_type=problem_type)
    else:
        _log.info('SOLVE RELAXATION')
        cont_tree = _nd.nd(tree, config, problem_type='continuous')
        L = cont_tree.ev()
        _log.info('SOLVE BINARY PROBLEM')
        return _nd.nd(tree, config, problem_type=problem_type, L=L)
# --------------------------------------------------------------------------- #
