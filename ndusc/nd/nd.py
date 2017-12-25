# -*- coding: utf-8 -*-
"""Nested decomposition module."""
# Python packages
import logging as _log

# Package modules
import ndusc.tree.tree as _tree
import ndusc.problem.problem as _problem
import ndusc.error.error as _error
import ndusc.logger.logger as _logger


# nested_decomposition --------------------------------------------------------
def nested_decomposition(tree_dic, data_dic,
                         solver='gurobi', problem_type='continuous', L=None):
    """Nested decomposition algorithm.

    Args:
        tree_dic (:obj:`dict`): tree with node information.
        data_dic (:obj:`dict`): general data.
        solver (:obj:`str`, opt): solver name. Defaults to ``'gurobi'``.
        problem_type (:obj:`str`, opt): problem type. Options:
            ``'continuous'``, ``'binary'``. Defaults to ``'continuous'``.
        L (:obj:`float`): lower bound for the binary problem.

    Return:
        :obj:`dict`: solution.

    Example:
        >>> from ndusc.examples import input_module
        >>> from ndusc.nd import nested_decomposition
        >>> data = input_module.input_module_example()
        >>> tree_dic = data.load_tree()
        >>> data_dic = data.load_data()
        >>> solver = 'gurobi'
        >>> problem_type = 'continuous'
        >>> L=None
        >>> tree = nested_decomposition(tree_dic, data_dic, solver)
    """
    # INICIO METODO
    #
    _log.info("\nINFO: STARTING ND ALGORTITHM\n")
    iteration, tree, bin_cuts, L, LB, UB = params_init(tree_dic, data_dic, L,
                                                       problem_type)

    # Seleccionar la lista inicial de nodos a visitar ---------
    # nodes_id = tree.get_nodes_info(stage=stage, keys='id')
    nodes_id = [1, 2, 3, 1, 2, 3, 1]
    # ---------------------------------------------------------

    first_stage_node = tree.first_stage_node_id()
    last_stage_nodes = tree.last_stage_nodes_id()

    stopcontion = False

    while not stopcontion:

        for node_id in nodes_id:
            # --------------------
            # Iteration information
            # --------------------
            if node_id in first_stage_node:
                iteration = iteration+1
                _log.info("================================================")
                _log.info("* ITERATION: " + str(iteration))
                _log.info("================================================")
                _log.info('')
            # --------------------
            # Node information
            # --------------------
            _log.info("* NODE ID: " + str(node_id))

            # --------------------
            # Add new cuts to the node
            # --------------------
            if node_id not in last_stage_nodes:
                if tree.have_next_nodes_eq_sol(node_id):
                    _log.info("\t* Creating cuts")
                    tree.add_cuts(node_id, bin_cuts, L)

            # --------------------
            # Loading node
            # --------------------
            _log.info("\t* Loading problem")
            problem_info = tree.get_node_problem_info(node_id)
            problem = _problem.Problem()
            problem.load_from_file(**problem_info)

            # --------------------
            # Fix previous node variables value
            # --------------------
            if node_id not in first_stage_node:
                _log.info("\t* Fixing vars")
                # Get previous node variables
                variables = tree.get_previous_node_vars(node_id)
                problem.fix_vars(variables)

            # --------------------
            # Add cuts
            # --------------------
            node = tree.get_node(node_id, copy=False)
            cuts = node.get_cuts()
            if cuts is not None:
                problem.create_cuts(cuts)

            # --------------------
            # Solve node
            # --------------------
            _log.info("\t* Executing problem")

            if node_id in first_stage_node:
                get_duals = False
            else:
                _log.debug("\t\t* Get duals")
                get_duals = True

            solution = problem.solve_node(solver, get_duals)

            # --------------------
            # Update node solution
            # --------------------
            _log.info("\t* Update node solution")
            _logger.vars_format(solution['variables'])
            node.update_solution(solution)
            _log.info('')
        stopcontion = True

    return tree
# --------------------------------------------------------------------------- #


# params_init -----------------------------------------------------------------
def params_init(tree_dic, data_dic, L, problem_type):
    """Parameter initializtion."""
    if problem_type == 'continuous':
        bin_cuts = False
    elif problem_type == 'binary':
        if L is None:
            L = 0.0
        bin_cuts = True
    else:
        _error.parameter_problem_type()

    LB = -float('inf')
    UB = -float('inf')

    iteration = 0
    tree = _tree.Tree(tree_dic, data_dic)
    return iteration, tree, bin_cuts, L, LB, UB
# --------------------------------------------------------------------------- #
