import jmespath
from ndusc.node import Node
import ndusc.utilities as utilities

class Tree(object):
    """

    """
    def __init__(self, data_tree, data_values):
        self.__nodes = [Node(n) for n in data_tree['nodes']]
        self.__stages = sorted(list(set(jmespath.search("[*].stage",
                                                        self.__nodes))))
        self.__data_values = data_values


    def get_stages(self):
        return self.__stages


    def get_nodes(self):
        return self.__nodes


    def get_stage_nodes(self, stageid):

        nodes_dic = jmespath.search("[?stage==`{}`]".format(stageid),
                                    self.__nodes)
        return [Node(node_dic) for node_dic in nodes_dic]

    def get_stage_nodes_id(self, stageid):
        return jmespath.search("[?stage==`{}`].id".format(stageid),
                                        self.__nodes)

    def get_stage_id(self, id):
        return jmespath.search("[?id==`{}`].stage".format(id), self.__nodes)


    def get_first_stage(self):
        s = jmespath.search("[?prev_id==None].stage".format(id), self.__nodes)
        if len(s) == 1:
            return s[0]
        else:
            raise ValueError("More than one node in the first stage.")


    def update_tree(tree, main_data, new_data, key):
        """Update main_data[key] with information of new_data[key].

        """

        data = dict(main_data)

        if key in new_data.keys():
            if new_data[key]:
                if key in data.keys():
                    data[key].update(new_data[key])
                else:
                    data[key] = new_data[key]

        return data


    def get_previous_node(self, previd):
        """Retrun previous node id.

        Todo:
            Exception unique parent node
        """
        return jmespath.search("[?id==`{}`].prev_id".format(previd),
                               self.__nodes)


    # get_data_by_idnode ------------------------------------------------------
    def get_data_by_idnode(self, idnode):
        """Get data information from the node.

        Args:
            idnode (:obj:`str` or :obj:`int`): node id.
        """
        return utilities.update_data(self.__data_values,
                                     self.get_node_id(idnode),
                                     ['params', 'sets'])
    # ----------------------------------------------------------------------- #

    # get_problem_data_by_idnode ----------------------------------------------
    def get_problem_data_by_idnode(self, idnode):
        """Get data information from the node.

        Args:
            idnode (:obj:`str` or :obj:`int`): node id.
        """
        node = self.get_node_id(idnode)
        return {'data': utilities.update_data(self.__data_values,
                                              node,
                                              ['params', 'sets']),
                'file': node.get_file(),
                'function': node.get_function()
                }
    # ----------------------------------------------------------------------- #


    def get_node_id(self, idnode):
        """."""
        node = jmespath.search("[?id == `{}`]".format(idnode),
                               self.__nodes)
        if len(node) == 1:
            return Node(node[0])
        else:
            raise ValueError("Duplicated node id.")
