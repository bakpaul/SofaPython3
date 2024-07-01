from core.node_wrapper import ChildWrapper
from prefabs.simulated_object import SimulatedObject
from prefabs.non_mechanical_object import NonMechanicalObject
from functools import wraps

class RootWrapper(ChildWrapper):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addSimulatedObject(self,*args,**kwargs):
        child = self.node.addChild(*args,**kwargs)
        ## We need to wrap the child passed to the prefab object to enforce the mechanism of "addChild"
        return SimulatedObject(RootWrapper(child))

    def addNonMechanicalObject(self,*args,**kwargs):
        child = self.node.addChild(*args,**kwargs)
        ## We need to wrap the child passed to the prefab object to enforce the mechanism of "addChild"
        return NonMechanicalObject(RootWrapper(child))



def PrefabSimulation(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if len(args)>1:
            return method(RootWrapper(args[0]),*args[1:],**kwargs)
        else:
            return method(RootWrapper(args[0]),**kwargs)
    return wrapper

