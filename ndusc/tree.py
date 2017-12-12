import jmespath
from ndusc.node import Node
from ndusc.model import StocasticModel
from pyomo.environ import *


class Tree(object):
    """

    """
    def __init__(self, data_tree, data_values):
        self.__nodes = [Node(n) for n in data_tree['nodes']]
        self.__stages = sorted(list(set(jmespath.search("[*].stage",
                                                        self.__nodes))))
        self.__data_values = data_values

    def get_data_values(self):
        return self.__data_values


    def get_stages(self):
        return self.__stages


    def get_nodes(self):
        return self.__nodes


    def return_stage_nodes(self, stageid):
        list_nodes = []
        nodes_dic = jmespath.search("[?stage==`{}`]".format(stageid),
                                    self.__nodes)
        for node_dic in nodes_dic:
            node_object = Node(node_dic)
            list_nodes.append(node_object)
        return list_nodes

    def get_stage_id(self, id):
        return jmespath.search("[?id==`{}`].stage".format(id), self.__nodes)


    def get_first_stage(self):
        return jmespath.search("[?id==`{}`].stage".format(id), self.__nodes)


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


    def return_previous_node(self, previd):
        """Retrun previous node id.

        Todo:
            Exception unique parent node
        """
        return jmespath.search("[?id==`{}`].prev_id".format(previd),
                               self.__nodes)


    @staticmethod
    def return_node_id(node_dic):
        return node_dic.get("id")
