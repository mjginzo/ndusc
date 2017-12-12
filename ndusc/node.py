

class Node(dict):

    def __init__(self,*arg,**kw):
        super(Node, self).__init__(*arg, **kw)

    def get_file(self):
        return self['model']['file']

    def get_function(self):
        return self['model']['function']
