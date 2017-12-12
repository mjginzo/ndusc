%load_ext autoreload
%autoreload 2
#
# Imports
#

import yaml
import jmespath
from pyomo.environ import *

# Own modules
from ndusc import utilities
from ndusc import model
from ndusc import cuts
from ndusc import input_module
from ndusc import tree
from ndusc import nd
from ndusc import node


input_data = input_module.Input_module("data/data.yaml","data/tree.yaml")
tree_nc = input_data.load_tree()
data_nc = input_data.load_data()

# QUITAR
tree1  = tree.Tree(tree_nc)

tree1.return_stage_nodes(1)
tree1.return_previous_node(1)

# END QUITAR


output = nested_decomposition(tree_nc, data_nc)
