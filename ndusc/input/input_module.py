# -*- coding: utf-8 -*-
"""Input_module."""

# Python package
import yaml


# Input_module ----------------------------------------------------------------
class Input_module():
    """Input_module class."""

    # __init__ ----------------------------------------------------------------
    def __init__(self, path_data, path_tree, format="yaml"):
        """Initialization."""
        self.path_data = path_data
        self.path_tree = path_tree
        self.format = format
    # ----------------------------------------------------------------------- #

    # load_tree ---------------------------------------------------------------
    def load_tree(self):
        """Get tree."""
        with open(self.path_tree, "r") as tree_file:
            data_tree = yaml.load(tree_file)

        for node in data_tree['nodes']:
            if isinstance(node, dict):
                if 'params' in node.keys():
                    if isinstance(node['params'], dict):
                        for p, vs in node['params'].items():
                            node['params'][p] = format_param(vs)
        return data_tree
    # ----------------------------------------------------------------------- #

    # load_data ---------------------------------------------------------------
    def load_data(self):
        """Get data."""
        with open(self.path_data, "r") as data_file:
            data = yaml.load(data_file)

        if 'params' in data.keys():
            if isinstance(data['params'], dict):
                for p, vs in data['params'].items():
                    data['params'][p] = format_param(vs)

        return data
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #


# format_param ---------------------------------------------------------------
def format_param(param):
    """Put param indices in correct way.

    Args:
        param (:obj:`dict`): parameter information.

    Return:
        :obj:`dict`: parameter information with format.

    Example:
        >>> import ndusc.input.input_module as _ip
        >>> param = {2: {1: 10, 2: 20}, 3: {1: 30}}
        >>> _ip.format_param(param)
            {(2, 1): 10, (2, 2): 20, (3, 1): 30}
    """
    if isinstance(param, dict):
        return {k: v for k, v in format_dict(param)}
    else:
        return param
# --------------------------------------------------------------------------- #


# format_dict ---------------------------------------------------------------
def format_dict(param, pre=None):
    """Put param indices in correct way.

    Args:
        param (:obj:`dict`): parameter information.

    Return:
        :obj:`dict`: parameter information with format.

    Example:
        >>> import ndusc.input.input_module as _ip
        >>> param = {2: {1: 10, 2: 20}, 3: {1: 30}}
        >>> {k: v for k, v in _ip.format_dict(param)}
            {(2, 1): 10, (2, 2): 20, (3, 1): 30}
    """
    pre = pre[:] if pre else []
    if isinstance(param, dict):
        for k, v in param.items():
            if isinstance(v, dict):
                for d in format_dict(v, pre + [k]):
                    yield d
            else:
                index = pre + [k]
                if len(index) == 1:
                    yield [index[0], v]
                elif len(index) > 1:
                    yield [tuple(index), v]

    else:
        return param
# --------------------------------------------------------------------------- #
