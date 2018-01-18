# -*- coding: utf-8 -*-
"""Nested decomposition module."""
# Python packages
import logging as _log

# Package modules
import ndusc.problem.problem as _problem
import ndusc.logger.logger as _logger
import ndusc.queues_nodes.queues as _queues
import ndusc.nd.executions_vars as _execution
from timeit import default_timer as timer

# nd --------------------------------------------------------------------------
def nd(tree, config, problem_type='continuous', L=None):
    """Nested decomposition algorithm.

    Args:
        tree (:obj:`ndusc.tree.tree.Tree`): tree information.
        config (:obj:`configure`): configuration struct.
        problem_type (:obj:`str`, opt): problem type. Options:
            ``'continuous'``, ``'binary'``. Defaults to ``'continuous'``.
        L (:obj:`float`): lower bound for the binary problem.

    Return:
        :obj:`dict`: solution.

    Example:
        >>> from ndusc.examples import input_module
        >>> from ndusc.nd import nested_decomposition
        >>> import ndusc.nd.configuration as _config
        >>> data = input_module.input_module_example()
        >>> tree_dic = data.load_tree()
        >>> data_dic = data.load_data()
        >>> config = _config.Configuration();
        >>> problem_type = 'continuous'
        >>> L=None
        >>> tree = nested_decomposition(tree_dic, data_dic, config.solver)
    """
    # INICIO METODO
    #
    _log.info("STARTING ND ALGORTITHM")

    exec_vars = _execution.Execution_vars(problem_type)

    # Seleccionar la lista inicial de nodos a visitar ---------
    # nodes_id = tree.get_nodes_info(stage=stage, keys='id')
    nodes_id = [1, 2, 3, 1, 2, 3, 1]
    # ---------------------------------------------------------

    first_stage_node = tree.first_stage_node_id()
    last_stage_nodes = tree.last_stage_nodes_id()

    stopcontion = 0
    while (stopcontion == 0):

        #nodes_id = _queues.return_by_levels(tree)

        for node_id in nodes_id:
            # --------------------
            # Iteration information
            # --------------------
            if node_id in first_stage_node:
                exec_vars.iters = exec_vars.iters+1
                time = timer() - exec_vars.start

                _log.info("================================================")
                _log.info("* ITERATION: " + str(exec_vars.iters) + " | TIME: "
                          + str(time) + " s")
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
                    tree.add_cuts(node_id, exec_vars.bin_cuts, L)

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

            solution = problem.solve_node(config.solver, get_duals)
            exec_vars.evals = exec_vars.evals + 1
            # --------------------
            # Update node solution
            # --------------------
            _log.info("\t* Update node solution")
            _logger.vars_format(solution['variables'])
            node.update_solution(solution)

#            import pdb; pdb.set_trace()

            _log.info('')

            #nodes_id = _queues.method1()
            stopcontion = check_stopping_criteria(config, exec_vars)
            if (stopcontion != 0):
                break

    return tree
# --------------------------------------------------------------------------- #

# nd --------------------------------------------------------------------------
def check_stopping_criteria(config, exec_vars):
    """Check if the algorithm fulfilled with any stopping criteria option

    Args:
        stop (int): counter to identify the stop cause.
        config (:obj:`configure`): configuration struct.
    Return:
    :obj:`int`: stopcontion.
    """

    stopcontion = 0
    time = timer() - exec_vars.start

    if time >= config.time:
        stopcontion = 1
        _log.info("================================================")
        _log.info("* STOP METHOD: Maximum execution time achieved  ")
        _log.info("================================================")
    elif exec_vars.iters >= config.iters:
        stopcontion = 2
        _log.info("================================================")
        _log.info("* STOP METHOD: Maximum iteration method achieved")
        _log.info("================================================")
    elif exec_vars.evals >= config.evals:
        stopcontion = 3
        _log.info("================================================")
        _log.info("* STOP METHOD: Maximum number of evaluations")
        _log.info("================================================")

    return stopcontion
# --------------------------------------------------------------------------- #
