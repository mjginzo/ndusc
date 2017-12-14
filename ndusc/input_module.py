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
        return data_tree
    # ----------------------------------------------------------------------- #

    # load_data ---------------------------------------------------------------
    def load_data(self):
        """Get data."""
        with open(self.path_data, "r") as data_file:
            data = yaml.load(data_file)
        return data
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
