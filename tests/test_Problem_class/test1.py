"""Test Problem class."""

import ndusc
import yaml

# Input
data_yaml_file = "../../data/data.yaml"

model_file = "../../data/model_S1.py"
model_function = "model_S1"
with open(data_yaml_file, "r") as data_file:
    data = yaml.load(data_file)

# Initialization
problem_nd = ndusc.Problem()

# Load data
problem_nd.load_from_file(model_file, model_function, data)

# Solve problem
#problem_nd.solve()

# Cuts
cuts = ndusc.Cuts()
cuts['feas'] = {1: {'D': {'Z': {
                                'Dozer': 1,
                                'Tractor': 2,
                                'Grupo_I': 3,
                                'Grupo_II': 4,
                                'Maquina_I': 5,
                                'Maquina_II': 6,
                                'Maquina_III': 7
                                }
                          },
                    'd': 10
                    },
                2: {'D': {'Z': {
                                'Dozer': 8,
                                'Tractor': 9,
                                'Grupo_I': 10,
                                'Grupo_II': 11,
                                'Maquina_I': 12,
                                'Maquina_II': 13,
                                'Maquina_III': 14
                                }
                          },
                    'd': 10
                    }
                }

new_cut = cuts.get_cut('feas', 1)

problem_nd.create_feas_cuts(new_cut)

new_cut = cuts.get_cut('feas', 2)

problem_nd.create_feas_cuts(new_cut)

problem_nd.solve(duals=True)

problem_nd._feas_cuts.pprint()
