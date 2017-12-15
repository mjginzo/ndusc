# -*- coding: utf-8 -*-
"""Tree class module."""

# Python package
import jmespath as _jmp

# Package modules
import ndusc.node.node as _node
import ndusc.tree.search as _search
import ndusc.utilities as _utilities
import ndusc.error.error as _error


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
        else:
            _error.multiple_root_node()
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

    # get_previous_node_id -------------------------------------------------- #
    def get_previous_node_id(self, id):
        """Retrun previous node id.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`ndusc.node.node.Node`: previous node.
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

    # get_node ----------------------------------------------------------------
    def get_node(self, id):
        """Retrun node object.

        Args:
            id (:obj:`str` or :obj:`int`): node id.

        Return:
            :obj:`ndusc.node.node.Node`: node.
        """
        n = self.get_nodes(id=id)
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

    # ================
    # PROBLEM INFO
    # ================

    # get_node_data ------------------------------------------------------
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
# --------------------------------------------------------------------------- #
