# -*- coding: utf-8 -*-
"""Nested decomposition module."""

# Package modules
import ndusc.tree.tree as _tree
import ndusc.problem.problem as _problem


# nested_decomposition --------------------------------------------------------
def nested_decomposition(tree_dic, data_dic, solver='gurobi'):
    """Nested decomposition algorithm.

    Args:
        tree_dic (:obj:`dict`): tree with node information.
        data_dic (:obj:`dict`): general data.
        solver (:obj:`str`, opt): solver name. Defaults to ``'gurobi'``.

    Return:
        :obj:`dict`: solution.

    Example:
        >>> from ndusc.examples import input_module
        >>> from ndusc.nd import nested_decomposition
        >>> data = input_module.input_module_example()
        >>> tree_dic = data.load_tree()
        >>> data_dic = data.load_data()
        >>> solver = 'gurobi'
        >>> tree = nested_decomposition(tree_dic, data_dic, solver)
    """
    # INICIO METODO
    #
    verbosity = 1
    if (verbosity):
        print("\nINFO: STARTING ND ALGORTITHM\n")

    iteration = 1
    tree = _tree.Tree(tree_dic, data_dic)
    stage = tree.get_first_stage()

    first_stage_node = tree.first_stage_node_id()
    last_stage_nodes = tree.last_stage_nodes_id()

    stopcontion = False

    while not stopcontion:
        nodes_id = tree.get_nodes_info(stage=stage, keys='id')

        if (verbosity):
            print("* ITERATION: ", iteration)
            print("  * CURRENT STAGE: ", stage)
            print("  * NUMBER OF NODES IN THE LEVEL: ", len(nodes_id))
            print("")

        nodes_id = [1, 2, 3, 1]

        for node_id in nodes_id:
            # --------------------
            # Add new cuts to the node
            # --------------------
            if node_id not in last_stage_nodes:
                if tree.have_next_nodes_eq_sol(node_id):
                    if (verbosity):
                        print("    * CREATING CUTS")
                    print("        * Get duals")
                    tree.add_cuts(node_id)
                    # cuts.create_cuts(modeldata.get_model_data(), node)

            # --------------------
            # Loading node
            # --------------------
            if (verbosity):
                print("    * LOADING NODE ID", node_id)
            problem_info = tree.get_node_problem_info(node_id)
            problem = _problem.Problem()
            problem.load_from_file(**problem_info)

            # --------------------
            # Fix previous node variables value
            # --------------------
            if node_id not in first_stage_node:
                # Get previous node variables
                variables = tree.get_previous_node_vars(node_id)
                problem.fix_vars(variables)

            # --------------------
            # Solving node
            # --------------------
            if (verbosity):
                print("    * EXECUTING PROBLEM")

            if node_id in first_stage_node:
                get_duals = False
            else:
                print("        * GET DUALS")
                get_duals = True

            solution = problem.solve(solver, get_duals)
            # --------------------
            # Update node solution
            # --------------------
            if (verbosity):
                print("    * UPDATE NODE SOLUTION")
            tree.update_solution(node_id, solution)

        iteration = iteration+1
        stage = stage + 1
        stopcontion = True

    return tree
# --------------------------------------------------------------------------- #
