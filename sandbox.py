%load_ext autoreload
%autoreload 2
#
# Imports
#


# Own modules
from ndusc import input_module
from ndusc import nd


input_data = input_module.Input_module("data/data.yaml", "data/tree.yaml")
tree_dic = input_data.load_tree()
data_dic = input_data.load_data()
solver = 'gurobi'

output = nd.nested_decomposition(tree_dic, data_dic, solver)
