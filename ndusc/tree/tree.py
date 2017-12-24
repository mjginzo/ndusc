# -*- coding: utf-8 -*-
"""Tree class module."""

# Python package
import jmespath as _jmp

# Package modules
import ndusc.node.node as _node
import ndusc.tree.search as _search
import ndusc.tree.utilities as _utilities
import ndusc.error.error as _error
import ndusc.problem.problem as _problem
import ndusc.cut.cut as _cut


# Tree ------------------------------------------------------------------------
class Tree(object):
    """Tree class."""

    # __init__ ----------------------------------------------------------------
    def __init__(self, tree_dic, data_dic):
        """Initialization.

        Args:
            tree_dic (:obj:`dict`): tree with node information.
            data_dic (:obj:`dict`): general data.

        Example:
            >>> from ndusc.examples import input_module
            >>> from ndusc.tree.tree import Tree
            >>> data = input_module.input_module_example()
            >>> tree = Tree(data.load_tree(), data.load_data())
        """
        self.__nodes = [_node.Node(n) for n in tree_dic['nodes']]
        self.__stages = sorted(list(set(_jmp.search("[*].stage",
                                        self.__nodes))))
        self.__general_data = data_dic
        self._add_constraints_info()
    # ----------------------------------------------------------------------- #

    # ================
    # GENERAL DATA INFO
    # ================

    # general_data ------------------------------------------------------------
    def general_data(self):
        """Get general_data.

        Return:
            :obj:`dict`: general data.
        """
        return self.__general_data
    # ----------------------------------------------------------------------- #

    # ================
    # STAGES INFO
    # ================

    # stages --------------------------------------------------------------
    def stages(self):
        """Get stages attribute.

        Return:
            :obj:`list`: stages ids.
        """
        return self.__stages
    # ----------------------------------------------------------------------- #

    # get_first_stage ------------------------------------------------------- #
    def get_first_stage(self):
        """Get first stage."""
        s = self.get_nodes_info(prev_id=None, keys='stage')
        if len(s) == 1:
            return s[0]
        elif len(s) > 1:
            _error.multiple_root_node()
        else:
            _error.no_root_node()
    # ----------------------------------------------------------------------- #

    # get_last_stage ------------------------------------------------------- #
    def get_last_stage(self):
        """Get last stage."""
        prev_node = self.get_nodes_id()[-1]
        while prev_node:
            new_node = self.get_next_nodes_id(prev_node)
            if new_node:
                prev_node = new_node
            else:
                return self.get_nodes_info(id=prev_node, keys='stage')
    # ----------------------------------------------------------------------- #

    # ================
    # NODES INFO
    # ================

    # nodes -------------------------------------------------------------------
    def nodes(self):
        """Get nodes.

        Return:
            :obj:`dict`: general data.
        """
        return self.__nodes
    # ----------------------------------------------------------------------- #

    # get_nodes ---------------------------------------------------------------
    def get_nodes(self, **args):
        """Get nodes.

        Args:
            **args: keys and values to search nodes.

        Return:
            :obj:`list`: list of nodes.

        Example:
            >>> tree.get_nodes(id=[1, 2], stage=2)
                [{'id': 2,
                'model': {'file': 'data/model_S2.py', 'function': 'model_S2'},
                'params': [{'demand': 1}],
                'prev_id': 1,
                'probability': 0.5,
                'set': None,
                'stage': 2}]
        """
        return _search.get_nodes(self.nodes(), args)
    # ----------------------------------------------------------------------- #

    # get_nodes_info -------------------------------------------------------- #
    def get_nodes_info(self, keys=None, **args):
        """Get nodes.

        Args:
            keys (:obj:`list`): list of keys.
            **args: keys and values to search nodes.

        Return:
            :obj:`list`: nodes information.

        Example:
            >>> tree.get_nodes_info(keys='stage', id=2)
                [2]
        """
        nodes = self.get_nodes(**args)
        return _search.get_key_values(nodes, keys)
    # ----------------------------------------------------------------------- #

    # Specific functions
    # ================

    # get_nodes_id -------------------------------------------------- #
    def get_nodes_id(self):
        """Return nodes id.

        Return:
            :obj:`list`: list of nodes id.
        """
        return self.get_nodes_info(keys='id')
    # ----------------------------------------------------------------------- #

    # get_previous_node_id ----------------------------------------------------
    def get_previous_node_id(self, id):
        """Return previous node id.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`str` or :obj:`int`: previous node id.
        """
        if self.exist_node(id):
            n = self.get_nodes_info(id=id, keys='prev_id')
            if len(n) == 1:
                return n[0]
            if len(n) == 0:
                return None
            else:
                _error.mutiple_parents(id)
        else:
            _error.no_node_id(id)
    # ----------------------------------------------------------------------- #

    # get_previous_node_vars --------------------------------------------------
    def get_previous_node_vars(self, id):
        """Return previous node id.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`str` or :obj:`int`: previous node id.
        """
        prev_id = self.get_previous_node_id(id)
        return self.get_node_variables_info(prev_id)
    # ----------------------------------------------------------------------- #

    # get_next_nodes_id -------------------------------------------------------
    def get_next_nodes_id(self, id):
        """Return next node id.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`str` or :obj:`int`: next node id.
        """
        if self.exist_node(id):
            return self.get_nodes_info(prev_id=id, keys='id')
        else:
            _error.no_node_id(id)
    # ----------------------------------------------------------------------- #

    # get_node ----------------------------------------------------------------
    def get_node(self, id, copy=True):
        """Retrun node object.

        Args:
            id (:obj:`str` or :obj:`int`): node id.
            copy (:obj:`bool`, opt): If ``True`` return a copy of the node
                object.

        Return:
            :obj:`ndusc.node.node.Node`: node.
        """
        if copy is True:
            n = self.get_nodes(id=id)
        else:
            n = [node for node in self.__nodes if node['id'] == id]
        if len(n) == 1:
            return n[0]
        if len(n) == 0:
            _error.no_node_id(id)
        else:
            _error.mutiple_ids(id)
    # ----------------------------------------------------------------------- #

    # exist_node --------------------------------------------------------------
    def exist_node(self, id):
        """Check if node exists.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`bool`: ``True`` if node id exists.
        """
        n = self.get_nodes(id=id)
        if len(n) == 1:
            return True
        if len(n) == 0:
            return False
        else:
            _error.mutiple_ids(id)
    # ----------------------------------------------------------------------- #

    # first_stage_node_id -----------------------------------------------------
    def first_stage_node_id(self):
        """Return list of first stage nodes id.

        Return:
            :obj:`list`: list of nodes id.
        """
        first_stage = self.get_first_stage()
        nodes = self.get_nodes_info(keys='id', stage=first_stage)
        if len(nodes) == 1:
            return nodes
        elif len(nodes) > 1:
            _error.multiple_root_node()
        else:
            _error.no_root_node()
    # ----------------------------------------------------------------------- #

    # last_stage_nodes_id -----------------------------------------------------
    def last_stage_nodes_id(self):
        """Return list of last stage nodes id.

        Return:
            :obj:`list`: list of nodes id.
        """
        last_stage = self.get_last_stage()
        return self.get_nodes_info(keys='id', stage=last_stage)
    # ----------------------------------------------------------------------- #

    # ================
    # PROBLEM INFO
    # ================

    # get_share_vars ----------------------------------------------------------
    def get_share_vars(self, id):
        """Get data information from the node.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`dict`: problem data.
        """
        id_vars_info = self.get_node_variables_info(id)
        id_vars = {v: [i for i in id_vars_info[v].keys()]
                   for v in id_vars_info.keys()}

        for v in list(id_vars):
            for i in id_vars[v]:
                for n in self.get_next_nodes_id(id):
                    n_vars = self.get_node_variables_info(n)
                    if v not in list(n_vars):
                        id_vars.pop(v, None)
                        break
                    else:
                        if i not in list(n_vars[v]):
                            id_vars[v].remove(i)
                            break

        return {v: id_vars[v] for v in id_vars.keys() if len(id_vars[v]) > 0}
    # ----------------------------------------------------------------------- #

    # get_node_data -----------------------------------------------------------
    def get_node_data(self, id):
        """Get data information from the node.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`dict`: problem data.
        """
        return _utilities.join_data(self.general_data(),
                                    self.get_node(id=id),
                                    ['params', 'sets'])
    # ----------------------------------------------------------------------- #

    # get_node_problem_info ---------------------------------------------------
    def get_node_problem_info(self, id):
        """Get problem information from the node.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`dict`: problem information.
        """
        problem_info = self.get_nodes_info(id=id, keys=['model'])
        if len(problem_info) == 1:
            problem_info = problem_info[0]['model']
            problem_info['data'] = self.get_node_data(id)
            return problem_info
        elif len(problem_info) == 0:
            _error.no_node_id(id)
        else:
            _error.mutiple_ids(id)
    # ----------------------------------------------------------------------- #

    # get_constraints_info ----------------------------------------------------
    def get_constraints_info(self, ids):
        """Get constraints information of nodes ids.

        Args:
            ids (:obj:`list`): list of nodes ids.

        Return:
            :obj:`dict`: constraints information.
        """
        return {i: self._get_node_constraints_info(i) for i in ids}
    # ----------------------------------------------------------------------- #

    # _get_node_constraints_info ----------------------------------------------
    def _get_node_constraints_info(self, id):
        """Get constraints information.

        Args:
            id (:obj:`list`): nodes id.

        Return:
            :obj:`dict`: constraints information.
        """
        return self.get_node(id=id)['problem_info']
    # ----------------------------------------------------------------------- #

    # _add_constraints_info ---------------------------------------------------
    def _add_constraints_info(self):
        """Add constrains information for each node.

        Return:
            :obj:`dict`: problem data.
        """
        for node in self.get_nodes():
            prob_info = self.get_node_problem_info(node['id'])
            problem = _problem.Problem()
            problem.load_from_file(**prob_info)
            node['problem_info'] = {'A': problem.get_constrain_coeffs(),
                                    'rhs': problem.get_rhs()}
    # ----------------------------------------------------------------------- #

    # ================
    # CUTS INFO
    # ================

    # add_cuts ----------------------------------------------------------------
    def add_cuts(self, id, bin_cuts=False, L=0.0):
        """Add new cuts to node id if problems where solved.

        Args:
            id (:obj:`str` or :obj:`int`): node id.
            bin_cuts (:obj:`bool`, opt): ``True`` if binary cuts are desired.
            L (:obj:`float`, opt): lower bound for the expected value. It may
                obtained by solving the relaxed integer problem. Defaults to
                ``0.0``.
        """
        # Node
        node = self.get_node(id=id, copy=False)

        # Cuts intialization
        if 'cuts' not in node.keys():
            node['cuts'] = _cut.Cut()

        # Next nodes ids
        next_nodes = self.get_next_nodes_id(id)

        # Get infeasible nodes
        infeas_nodes = self.get_infeasible_nodes_id(next_nodes)

        # Necessary cuts information
        vars = self.get_share_vars(id)

        # Continuous cuts (always)

        # Optimality cuts
        if len(infeas_nodes) == 0:
            dual = self.get_duals_info(next_nodes)
            cons = self.get_constraints_info(next_nodes)
            probs = {n: self.get_node(n)['probability']
                     for n in next_nodes}
            node['cuts'].add_opt(vars, dual, cons, probs)

        # Feasible cuts
        else:
            dual = self.get_duals_info(next_nodes)
            cons = self.get_constraints_info(next_nodes)
            node['cuts'].add_feas(vars, dual, cons)

        # Binary cuts
        if bin_cuts:
            # Take variable values
            vars_val = node['solution']['variables']

            # Optimality cuts
            if len(infeas_nodes) == 0:
                # Compute EV
                values = _jmp.search('[*].solution.objective.*.*[][]',
                                     self.get_nodes(id=next_nodes))
                probs = _jmp.search('[*].probability',
                                    self.get_nodes(id=next_nodes))
                EV = sum([values[i]*probs[i]/sum(probs)
                          for i in range(len(probs))])

                #  Se calcula anteriormente, ha de ser un parametro de entrada
                #  para el algoritmo (nested distance binaries)

                node['cuts'].add_bin_opt(vars, vars_val, EV, L)

            # Feasible cuts
            else:
                node['cuts'].add_bin_feas(vars, vars_val)
    # ----------------------------------------------------------------------- #

    # get_cuts ----------------------------------------------------------------
    def get_cuts(self, id):
        """Get cuts of the node.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`ndusc.cut.cut.Cut`: cuts information.
        """
        node = self.get_node(id=id, copy=False)

        if 'cuts' not in node.keys():
            return None
        else:
            return node['cuts']
    # ----------------------------------------------------------------------- #

    # ================
    # SOLUTION INFO
    # ================

    # get_infeasible_nodes_id -------------------------------------------------
    def get_infeasible_nodes_id(self, ids=None):
        """Get the id of the infeasibles nodes.

        Args:
            ids (:obj:list): list of nodes ids. If None all nodes are consider.
                Defaults to None.
        """
        if ids is None:
            ids = self.get_nodes_id()

        return [n for n in ids if self.is_infeasible_node(n)]
    # ----------------------------------------------------------------------- #

    # is_infeasible_node ------------------------------------------------------
    def is_infeasible_node(self, id):
        """Check if node has a infeasible solution.

        Args:
            id (:obj:`int` or :obj:`str`): node id.

        Return:
            :obj:`bool`: ``True`` if node is infeasible.
        """
        try:
            sol = self.get_node(id)['solution']
            return sol['status'] != 'optimal'
        except KeyError:
            raise _error.node_not_solved
    # ----------------------------------------------------------------------- #

    # update_solution ---------------------------------------------------------
    def update_solution(self, id, solution):
        """Update node solution.

        Args:
            id (:obj:`str` or :obj:`int`): node id.
            solution (:obj:`dict`): solution information.
        """
        node = self.get_node(id=id, copy=False)
        node['solution'] = solution
    # ----------------------------------------------------------------------- #

    # get_node_variables_info -------------------------------------------------
    def get_node_variables_info(self, id):
        """Get variable information of node.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`dict`: variables information.
        """
        try:
            return self.get_node(id=id)['solution']['variables']
        except KeyError:
            return None
    # ----------------------------------------------------------------------- #

    # get_duals_info ----------------------------------------------------------
    def get_duals_info(self, ids):
        """Get nodes dual information.

        Args:
            ids (:obj:`str` or :obj:`int`): list of nodes ids.

        Return:
            :obj:`dict`: dual information.
        """
        return {i: self._get_node_duals_info(i) for i in ids}
    # ----------------------------------------------------------------------- #

    # _get_node_duals_info ----------------------------------------------------
    def _get_node_duals_info(self, id):
        """Get node dual information.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`dict`: dual information.
        """
        try:
            cons = self.get_node(id=id)['solution']['constraints']
            return {c: {i: cons[c][i]['dual']} for c in cons for i in cons[c]}
        except KeyError:
            return None
    # ----------------------------------------------------------------------- #

    # has_next_nodes_eq_sol ---------------------------------------------------
    def have_next_nodes_eq_sol(self, id):
        """Check if next nodes have the same solution as id node.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`bool`: true if the variable solution is the same.
        """
        id_vars = self.get_node_variables_info(id)
        if id_vars is not None:
            equal = []
            for n_id in self.get_next_nodes_id(id):

                # If no solution return False ---
                n_vars = self.get_node_variables_info(n_id)
                if n_vars is None:
                    return False
                # ------------------------------------

                for k in id_vars.keys():
                    if k in n_vars.keys():
                        for i in id_vars[k].keys():
                            if i in n_vars[k].keys():
                                equal += [id_vars[k][i] == n_vars[k][i]]
            return all(equal)
        else:
            return False
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
