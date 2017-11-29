import jmespath
from ndusc import node

class Tree(object):

    def __init__(self, data_tree):
        self.nodes = [node.Node(n) for n in data_tree['nodes']]
        self.stages = sorted(list(set(jmespath.search("[*].stage",
                                                      self.nodes))))

    def return_stage_nodes(self, stageid):
        return jmespath.search("[?stage==`{}`]".format(stageid),
                               self.nodes)

    def return_previous_node(self, previd):
        """Retrun previous node id.

        Todo:
            Exception unique parent node
        """
        return jmespath.search("[?id==`{}`].prev_id".format(previd),
                                self.nodes)
