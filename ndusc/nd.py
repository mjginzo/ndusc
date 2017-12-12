from ndusc.tree import Tree
from ndust.problem_nd.problem import Problem

def nested_decomposition(tree_dic, data_dic):
    # INICIO METODO
    #
    verbosity = 1
    if (verbosity):
        print("\nINFO: STARTING ND ALGORTITHM\n")

    iteration = 1
    tree_nc = Tree(tree_dic, data_dic)
    current_stage = tree_nc.get_first_stage()
    stopcontion = False

    while not stopcontion:
        current_stage_nodes_id = tree_nc.get_stage_nodes_id(current_stage)

        if (verbosity):
            print("* ITERATION: ", iteration)
            print("  * CURRENT STAGE: ", current_stage)
            print("  * NUMBER OF NODES IN THE LEVEL: ",
                  len(current_stage_nodes_id))
            print("  * CONTENT: ", current_stage_nodes_id)
            print("")

        for nodeid in current_stage_nodes_id:
            if (verbosity):
                print("    * SOLVING NODE ID", nodeid)
            problem_data = tree_nc.get_problem_data_by_idnode(nodeid)
            if (verbosity):
                print("    * CREATING MODEL: ", problem_data)
            problem = Problem()
            problem.load_from_file(**problem_data)
            import pdb; pdb.set_trace()

            if (verbosity):
                print("    * CREATING PROBLEM: ", problem)
            if (verbosity):
                print("    * CREATING CUTS")
            # cuts.create_cuts(modeldata.get_model_data(), node)
            if (verbosity):
                print("    * EXECUTING NLP SOLVER:")
            # sresults, presults = modeldata.solve(problem, 'gurobi', False)
            print("ACABA")
        iteration = iteration+1
        next_stage = next_stage + 1
        current_stage = tree_nc.get_stage_id(next_stage)
        stopcontion = True

    output = 1
    return output
