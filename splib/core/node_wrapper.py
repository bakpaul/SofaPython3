
class NodeWrapper(object):
    def __init__(self,_node):
        self.node = _node

    def addObject(self,*args, **kwargs):
        parameters = {}
        if "name" in kwargs:
            if kwargs["name"] in kwargs:
                if isinstance(kwargs[kwargs["name"]], dict):
                    parameters = kwargs[kwargs["name"]]
        self.node.addObject(*args,**parameters)

    def __getattr__(self, item):
        return getattr(self.node,item)



def PrefabMethod(method):
    def wrapper(*args, **kwargs):
        method(NodeWrapper(args[0]),**kwargs)
    return wrapper()
