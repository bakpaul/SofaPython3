from core.node_wrapper import ChildWrapper
from prefabs.simulated_object import SimulatedObject
from prefabs.non_simulated_object import NonSimulatedObject
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



def PrefabSimulation(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if len(args)>1:
            return method(RootWrapper(args[0]),*args[1:],**kwargs)
        else:
            return method(RootWrapper(args[0]),**kwargs)
    return wrapper

