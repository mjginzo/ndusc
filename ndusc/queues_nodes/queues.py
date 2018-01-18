# -*- coding: utf-8 -*-
"""Module with different queues rules to determine node list to execute."""
import time

def return_by_levels(tree):
    """Nested decomposition algorithm.

    Args:
        tree (:obj:`ndusc.tree.tree.Tree`): tree information.

    """

    nodes_id = []
    first_stage_node = tree.first_stage_node_id()
    last_stage_nodes = tree.last_stage_nodes_id()

    stop = 0
    sense = 0
    nodes = first_stage_node

    while (stop == 0):
        next_node = []
        print("nodes_id")
        print(nodes_id)
        print("nodes")
        print(nodes)
        for n_id in nodes:
            if (sense == 0):
                nodes_id.append(n_id)
                next_node1 = tree.get_next_nodes_id(n_id)
            elif (sense == 1):
                next_node1 = []
                if (tree.get_previous_node_id(n_id) is not None):
                    next_node1.append(tree.get_previous_node_id(n_id))
            elif (n_id in last_stage_nodes):
                next_node1 = []
            # Append the next node ids to next_node LIST
            for next_id in next_node1:
                if (next_id not in next_node):
                    next_node.append(next_id)


        print("NEXT_NODE")
        print(next_node)
        print(len(next_node))

        # if there are not sons' nodes, the algorithm reach to the floor of the
        # tree, and the sense of the search need to be changed.
        if (len(next_node) == 0) and (sense == 0):
            sense = 1
            next_node = nodes
        elif (len(next_node) > 0) and (sense == 1):
            print("ENTRA")
            for n_id in next_node:
                nodes_id.append(n_id)
        elif (len(next_node) == 0) and (sense == 1):
            print("STOP")
            stop = 1

        print("SENSE")
        print(sense)

        nodes = next_node
        time.sleep(1)

    return nodes_id
