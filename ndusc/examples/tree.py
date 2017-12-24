# -*- coding: utf-8 -*-
"""Tree examples module."""

# Package modules
from ndusc.input.input_module import Input_module
from ndusc.tree.tree import Tree


# tree_example ----------------------------------------------------------------
def tree_example(test_example='1'):
    """Load tree of the test examples folder.

    Args:
        test_example (:obj:`str`): number of the test.

    Return:
        :obj:`ndusc.tree.tree.Tree`: tree.
    """
    folder = "tests/datas/data{}".format(test_example)
    data = Input_module(folder + '/data.yaml', folder + '/tree.yaml')
    return Tree(data.load_tree(), data.load_data())
# --------------------------------------------------------------------------- #
