from splib.core.node_wrapper import ChildWrapper
from splib.core.modeled_object import ModeledObject
from splib.prefabs.simulated_object import SimulatedObject
from splib.prefabs.non_simulated_object import NonSimulatedObject
from functools import wraps

class RootWrapper(ModeledObject):
    def __init__(self,node,*args,**kwargs):
        super().__init__('Temp')
        self.m_node = node
        self._args = args
        self._kwargs = kwargs


    def addObject(self,*args, **kwargs):
        if("name" in kwargs):
            id = kwargs["name"]
        else :
            id = self.getUniqueID(args[0])
        self.appendMethod(id,getattr(self.m_node,"addObject"),args,kwargs)
        return

    def replaceObject(self,*args, **kwargs):
        return

    def delObject(self,*args, **kwargs):
        return

    def addChild(self,*args, **kwargs):
        if("name" in kwargs):
            id = kwargs["name"]
        else :
            id = self.getUniqueID(args[0])
        self.appendMethod(id,getattr(self.m_node,"addChild"),args,kwargs)
        return

    def replaceChild(self,*args, **kwargs):
        return

    def delChild(self,*args, **kwargs):
        return

    def addSimulatedObject(self,name,*args,**kwargs):
        child = self.addChild(name)
        ## We need to wrap the child passed to the prefab object to enforce the mechanism of "addChild"
        return SimulatedObject(RootWrapper(child),*args,**kwargs)

    def addNonSimulatedObject(self,name,*args,**kwargs):
        child = self.addChild(name)
        ## We need to wrap the child passed to the prefab object to enforce the mechanism of "addChild"
        return NonSimulatedObject(RootWrapper(child),*args,**kwargs)


    def transpile(self):
        print("TRANSPILING")
        self.instantiate(ChildWrapper(self.m_node))



def PrefabSimulation(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if len(args)>1:
            node = method(RootWrapper(args[0]),*args[1:],**kwargs)
        else:
            node = method(RootWrapper(args[0]),**kwargs)
        node.transpile()
        return node
    return wrapper

