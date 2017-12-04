from ndusc.tree import Tree
from ndusc.model import StocasticModel
from ndusc import cuts


def nested_decomposition(tree_dic, data_dic):
    # INICIO METODO
    #
    verbosity = 1
    if (verbosity):
        print("\nINFO: STARTING ND ALGORTITHM\n")

    iteration = 1
    tree_nc = Tree(tree_dic, data_dic)
    next_stage = 0
    current_stage = tree_nc.get_stage_id(next_stage)
    stopcontion = False

    while not stopcontion:
        current_stage_nodes = tree_nc.return_stage_nodes(current_stage)
        current_data_values = tree_nc.get_data_values()

        if (verbosity):
            print("* ITERATION: ", iteration)
            print("  * CURRENT STAGE: ", current_stage)
            print("  * NUMBER OF NODES IN THE LEVEL: ", len(current_stage_nodes))
            print("  * CONTENT: ", current_stage_nodes)
            print("")

        for node in current_stage_nodes:
            if (verbosity):
                print("    * SOLVING NODE ID", tree_nc.return_node_id(node))
            modeldata = StocasticModel(
                        node.charge_node_in_data(node,
                                                 current_data_values))
            if (verbosity):
                print("    * CREATING MODEL: ", modeldata.get_model_data())
            problem = modeldata.load(node)
            if (verbosity):
                print("    * CREATING PROBLEM: ", problem)
            if (verbosity):
                print("    * CREATING CUTS")
            cuts.create_cuts(modeldata.get_model_data(), node)
            if (verbosity):
                print("    * EXECUTING NLP SOLVER:")
            sresults, presults = modeldata.solve(problem, 'gurobi', False)
            print("ACABA")
        iteration = iteration+1
        next_stage = next_stage + 1
        current_stage = tree_nc.get_stage_id(next_stage)
        stopcontion = True

    output = 1
    return output
