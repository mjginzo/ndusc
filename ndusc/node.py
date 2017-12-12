

class Node(dict):

    def __init__(self,*arg,**kw):
        super(Node,self).__init__(*arg, **kw)

    @staticmethod
    def get_file_node(node):
        return node['model']['file']


    @staticmethod
    def get_file_function(node):
        return node['model']['function']


    @staticmethod
    def update_data(main_data, new_data, key):
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


    def charge_node_in_data(self, node, data):
        """Get data information from the node

        Args:
            node (:obj:`dict`): node information.
            data (:obj:`dict`): dictionary with problem data.
        """
        data = self.update_data(data, node, 'params')
        data = self.update_data(data, node, 'sets')
        return data
