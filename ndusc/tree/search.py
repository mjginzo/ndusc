# -*- coding: utf-8 -*-
"""Search functions module."""

# Python packages
import jmespath as _jmp

# Package modules
from ndusc.node import node as _node


# _jmp_expr -------------------------------------------------------------------
def _jmp_expr(key, val):
    """Format jmespath expression.

    Args:
        key (:obj:`str`): key value.
        val (:obj:`int` or :obj:`float` :obj:`str`): value.

    Return:
        :obj:`str`: expression.
    """
    if val is None:
        return "{}=={}".format(key, val)
    elif isinstance(key, (int, float, str)):
        return "{}==`{}`".format(key, val)
    else:
        raise ValueError("Unkown info[key] type.")
# --------------------------------------------------------------------------- #


# get_nodes -------------------------------------------------------------------
def get_nodes(nodes, info=None):
    """Get nodes.

    Args:
        nodes (:obj:`list`): list of nodes.
        info (:obj:`dict`): dictionary to search nodes with the desired key
            values. If None, all nodes.

    Return:
        :obj:`list`: list of nodes.

    Example:
        >>> from ndusc.tree import search
        >>> from ndusc.examples.tree import tree_example
        >>> tree = tree_example()
        >>> nodes = tree.get_nodes()
        >>> search.get_nodes(nodes, {'id': [1, 2], 'stage': 2})
            [{'id': 2,
            'model': {'file': 'data/model_S2.py', 'function': 'model_S2'},
            'params': [{'demand': 1}],
            'prev_id': 1,
            'probability': 0.5,
            'set': None,
            'stage': 2}]
    """
    if not info:
        return nodes
    elif isinstance(info, dict):
        expr = "[?"
        or_expr = " || "
        and_expr = " && "
        first = True
        for k in info.keys():
            if first is False:
                expr += and_expr
            if isinstance(info[k], list):
                val_list = [_jmp_expr(k, v) for v in info[k]]
                expr += "(" + or_expr.join(val_list) + ")"
                first = False
            else:
                expr += _jmp_expr(k, info[k])
                first = False
        expr += "]"
        new_nodes = _jmp.search(expr, nodes)
        return [_node.Node(n) for n in new_nodes]
    else:
        raise TypeError("Info type must be dict.")
# --------------------------------------------------------------------------- #


# get_key_values --------------------------------------------------------------
def get_key_values(nodes, keys=None):
    """Get nodes.

    Args:
        nodes (:obj:`list`): list of nodes.
        keys (:obj:`list`): key names. If None, all keys.

    Return:
        :obj:`list`: list of nodes info.

    Example:
        >>> from ndusc.tree import search
        >>> from ndusc.examples.tree import tree_example
        >>> tree = tree_example()
        >>> nodes = tree.get_nodes()
        >>> search.get_key_values(nodes, keys='stage')
            [1, 2, 2, 3, 3, 3, 3]
    """
    if keys is None:
        return nodes
    elif isinstance(keys, str):
        expr = '[*].{}'.format(keys)
        return _jmp.search(expr, nodes)
    elif isinstance(keys, list):
        expr = "[*].{"
        expr += ", ".join(['{k}: {k}'.format(k=k) for k in keys])
        expr += "}"
        return _jmp.search(expr, nodes)
    else:
        raise TypeError("Keys type must be list.")
# --------------------------------------------------------------------------- #
