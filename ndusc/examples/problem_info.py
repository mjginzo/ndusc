# -*- coding: utf-8 -*-
"""Tree examples module."""

# Package modules
from ndusc import examples


# problem_info_example --------------------------------------------------------
def problem_info_example(test_example='1', node_id=1):
    """Load problem information of the test examples folder.

    Args:
        test_example (:obj:`str`): number of the test.

    Return:
        :obj:`dict`: problem information.
    """
    tree = examples.tree.tree_example(test_example='1')
    return tree.get_node_problem_info(node_id)
# --------------------------------------------------------------------------- #
