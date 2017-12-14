# -*- coding: utf-8 -*-
"""Input_module examples module."""

# Package modules
from ndusc.input_module import Input_module


# input_module_example ----------------------------------------------------------------
def input_module_example(test_example='1'):
    """Load tree of the test examples folder.

    Args:
        test_example (:obj:`str`): number of the test.

    Return:
        :obj:`ndusc.tree.tree.Tree`: tree.
    """
    folder = "tests/datas/data{}".format(test_example)
    data = Input_module(folder + '/data.yaml', folder + '/tree.yaml')
    return data
# --------------------------------------------------------------------------- #
