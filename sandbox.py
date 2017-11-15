%load_ext autoreload
%autoreload 2

#
# Imports
#

import yaml
import jmespath
from pyomo.environ import *

# Own modules
from nested_decomposition import utilities
from nested_decomposition import model
from nested_decomposition import cuts

#
# Load data
#

with open('data/data.yaml', 'r') as data_file:
    data = yaml.load(data_file)

#
# Load tree
#

with open('data/tree.yaml', 'r') as tree_file:
    tree = yaml.load(tree_file)

#
# Iterate over al nodes of each stage
#

stages = sorted(list(set(jmespath.search("nodes[*].stage", tree))))

# dir = 1 # if 1 forward if -1 backward

# - while optimality conditions are not met
# while 

# - for stage in stages:

# FIRST STAGE
stage = stages[0]

stage_nodes = jmespath.search("nodes[?stage==`{}`]".format(stage), tree)

# -- for node in stage_nodes:

node = stage_nodes[0]

# Get node data
model_data = utilities.node_data(node, data)

# Create the problem
problem = model.load(node['model']['file'],
                    node['model']['function'], 
                    model_data)


cuts.create_cuts(model, node)

# Solve the problem
solver_results, problem_results = model.solve(problem, 'gurobi', duals=False)

# update tree with new results
node.update(problem_results)

# SECOND STAGE
stage = stages[1]
stage_nodes = jmespath.search("nodes[?stage==`{}`]".format(stage), tree)

# -- for node in stage_nodes:

node = stage_nodes[0]

# update data with 
model_data = utilities.node_data(node, data)

prev_id = node['prev_id']

prev_vars = jmespath.search("nodes[?id==`{}`].variables".format(prev_id), tree)

# <------------
# Load solution of the previous node
if len(prev_vars) == 1:
    prev_vars = prev_vars[0]
else:
    print "Error more than one parent"

model_data['params'].update(prev_vars)
# <------------

problem = model.load(node['model']['file'],
                    node['model']['function'], 
                    model_data)

solver_results, problem_results = model.solve(problem, 'gurobi', duals=False)




#
# Load Second Model
#
#
#model1 = model_S1(data, node)
#
#
#cuts = {
#            'sets':{
#                'Cuts_Opt':[],
#                'Cuts_Feas':[],
#            },
#            'params':{
#                'D':{},
#                'd':{},
#                'E':{},
#                'e':{}
#            }
#        }
#
#
## 
## Create a solver
##
#
#opt = SolverFactory('gurobi')
#
### Create a model instance and optimize
#instance_S1 = model_S1.create_instance()
#results_S1 = opt.solve(instance_S1)
#instance_S1.load(results_S1)
#print results_S1
#
## Iterate to eliminate the previously found solution
#results = {'variables':{}}
#for v in instance_S1.active_components(Var):
#    results['variables'][v.getname()] = {}
#    varobject = getattr(instance_S1, str(v))
#    for index in varobject:
#        results['variables'][v.getname()][index] = varobject[index].value
#

