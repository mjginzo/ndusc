import yaml


class Input_module():

    def __init__(self, path_data, path_tree, format="yaml"):
        self.path_data = path_data
        self.path_tree = path_tree
        self.format = format

    def load_tree(self):
        with open(self.path_tree, "r") as tree_file:
            data_tree = yaml.load(tree_file)
        return data_tree

    def load_data(self):
        with open(self.path_data, "r") as data_file:
            data = yaml.load(data_file)
        return data
