# -*- coding: utf-8 -*-
"""Nested decomposition module."""

# Package modules
from ndusc.tree.tree import Tree
from ndusc.problem.problem import Problem


# nested_decomposition --------------------------------------------------------
def nested_decomposition(tree_dic, data_dic):
    """Nested decomposition algorithm.

    Args:
        tree_dic (:obj:`dict`): tree with node information.
        data_dic (:obj:`dict`): general data.

    Return:
        :obj:`dict`: solution.
    """
    # INICIO METODO
    #
    verbosity = 1
    if (verbosity):
        print("\nINFO: STARTING ND ALGORTITHM\n")

    iteration = 1
    tree_nc = Tree(tree_dic, data_dic)
    stage = tree_nc.get_first_stage()
    stopcontion = False

    while not stopcontion:
        nodes_id = tree_nc.get_nodes_info(stage=stage, keys='id')

        if (verbosity):
            print("* ITERATION: ", iteration)
            print("  * CURRENT STAGE: ", stage)
            print("  * NUMBER OF NODES IN THE LEVEL: ", len(nodes_id))
            print("")

        for node_id in nodes_id:
            # --------------------
            # Create cuts
            # --------------------
            if (verbosity):
                print("    * CREATING CUTS")
            # cuts.create_cuts(modeldata.get_model_data(), node)

            # --------------------
            # Loading node
            # --------------------
            if (verbosity):
                print("    * LOADING NODE ID", node_id)
            problem_info = tree_nc.get_node_problem_info(node_id)
            problem = Problem()
            problem.load_from_file(**problem_info)

            # --------------------
            # Solving node
            # --------------------
            if (verbosity):
                print("    * EXECUTING PROBLEM")
            # sresults, presults = modeldata.solve(problem, 'gurobi', False)

        iteration = iteration+1
        stage = stage + 1
        stopcontion = True

    output = 1
    return output
# --------------------------------------------------------------------------- #
