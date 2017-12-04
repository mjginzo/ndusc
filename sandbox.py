#
# Imports
#

import yaml
import jmespath
from pyomo.environ import *

# Own modules
from ndusc import cuts
from ndusc import input_module
from ndusc.nd import nested_decomposition
from ndusc import node


input_data = input_module.Input_module("data/data.yaml", "data/tree.yaml")
tree_nc = input_data.load_tree()
data_nc = input_data.load_data()

output = nested_decomposition(tree_nc, data_nc)
