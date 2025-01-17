from functools import wraps
from splib.core.utils import defaultValueType
# The two classes are not merged because one could want to use a PrefabMethod
# (enabling to pass dictionary fixing params) without wanting to use a full PrefabSimulation


class BasePrefab(object):

    def __init__(self,node):
        self.node = node

    def __getattr__(self, item):
        return getattr(self.node,item)


class ObjectWrapper(BasePrefab):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addObject(self,*args, **kwargs):
        # TODO: add warnings when kwargs are nonsense
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
                    print("[warning] You are redefining the parameter '"+ param + "' of object "  + str(args[0]))
            elif not(isinstance(kwargs[param], dict)) and not(isinstance(kwargs[param],defaultValueType)):
                parameters = {**parameters,param:kwargs[param]}

        return self.node.addObject(*args,**parameters)




class ChildWrapper(ObjectWrapper):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    # This method enforces that the object that is created by the addChild method keeps the prefab type
    def addChild(self,*args, **kwargs):
        child = self.node.addChild(*args,**kwargs)
        returnObject =  self.__new__(type(self))
        returnObject.__init__(child)
        return returnObject




def PrefabMethod(method):
    @wraps(method)
    def wrapper(*args, **kwargs):

        node = args[0]
        #We don't want to wrap an object that is already wrapped
        if( not isinstance(node,ObjectWrapper) ):
            node = ObjectWrapper(node)
        else:
            print("Not wrapping this node as it is already wrapped in " + str(type(node)))

        if len(args)>1:
            return method(node,*args[1:],**kwargs)
        else:
            return method(node,**kwargs)
    return wrapper
