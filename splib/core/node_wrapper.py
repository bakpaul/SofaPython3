from functools import wraps

# The two classes are not merged because one could want to use a PrefabMethod
# (enabling to pass dictionary fixing params) without wanting to use a full PrefabSimulation
class PrefabNode(object):
    def __init__(self,_node):
        self.node = _node

    def addChild(self,*args, **kwargs):
        child = self.node.addChild(*args,**kwargs)
        return PrefabNode(child)

    def __getattr__(self, item):
        return getattr(self.node,item)

class NodeWrapper(object):
    def __init__(self,_node):
        self.node = _node

    def addObject(self,*args, **kwargs):
        parameters = {}
        # Expand any parameter that has been set by the user in a custom dictionary
        # and having the same key as the component name
        if "name" in kwargs:
            parameters["name"] = kwargs["name"]
            if kwargs["name"] in kwargs:
                if isinstance(kwargs[kwargs["name"]], dict):
                    parameters = {**parameters, **kwargs[kwargs["name"]]}
        # Add all the parameters from kwargs that are not dictionary
        for param in kwargs:
            if param in parameters:
                if not(param == "name"):
                    print("[warning] You are redefining the parameter "+ param + " of object "  + str(args[0]))
            elif not(isinstance(kwargs[param], dict)):
                parameters = {**parameters,param:kwargs[param]}

        return self.node.addObject(*args,**parameters)

    def __getattr__(self, item):
        return getattr(self.node,item)



def PrefabSimulation(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if len(args)>1:
            return method(PrefabNode(args[0]),*args[1:],**kwargs)
        else:
            return method(PrefabNode(args[0]),**kwargs)
    return wrapper
def PrefabMethod(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if len(args)>1:
            return method(NodeWrapper(args[0]),*args[1:],**kwargs)
        else:
            return method(NodeWrapper(args[0]),**kwargs)
    return wrapper
