from splib.core.node_wrapper import ChildWrapper
from splib.prefabs.simulated_object import SimulatedObject
from splib.prefabs.non_simulated_object import NonSimulatedObject
from functools import wraps

class RootWrapper(ChildWrapper):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addSimulatedObject(self,name,*args,**kwargs):
        child = self.node.addChild(name)
        ## We need to wrap the child passed to the prefab object to enforce the mechanism of "addChild"
        return SimulatedObject(RootWrapper(child),*args,**kwargs)

    def addNonSimulatedObject(self,name,*args,**kwargs):
        child = self.node.addChild(name)
        ## We need to wrap the child passed to the prefab object to enforce the mechanism of "addChild"
        return NonSimulatedObject(RootWrapper(child),*args,**kwargs)

    def __setattr__(self, key, value):
        if(not(key=="node") and ("node" in self.__dict__)):
            self.__dict__["node"].__setattr__(key,value)
        else:
            self.__dict__[key] = value

def PrefabSimulation(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if len(args)>1:
            return method(RootWrapper(args[0]),*args[1:],**kwargs)
        else:
            return method(RootWrapper(args[0]),**kwargs)
    return wrapper

