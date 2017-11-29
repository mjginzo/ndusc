

class Node(dict):

#def __init__(self, node):
    def __init__(self,*arg,**kw):
        super(Node,self).__init__(*arg, **kw)
#        self = node
