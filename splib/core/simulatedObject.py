from typing import List, Callable, Tuple, Dict
class PrefabricatedObject():
    instanciationMethods : List[Tuple[Callable, Dict]]

    def __init__(self,_name):
        self.name = _name
    def instantiate(self, _node):
        self.node = _node.addChild(self.name)
        for tup in self.instanciationMethods:
           tup[0](self.node,tup[1])



class SimulatedObject(PrefabricatedObject):
    def __init__(self,_template=None,**kwargs):
        self.template = _template


    def defaultConstruction(self,_solverParams,_topologyParams,_mechaParams):
        self.addSolvers(_solverParams)
        self.addTopology(_topologyParams)
        self.addMecha(_mechaParams)

    def addSolvers(self,some,args,**kwargs):
        self.instanciationMethods.append((SimulatedObject._implAddSolvers,{"some" : some, "args" : args, kwargs : kwargs}))

    def addTopology(self,some,args,**kwargs):
        self.instanciationMethods.append((SimulatedObject._implAddTopology,{"some" : some, "args" : args, kwargs : kwargs}))

    def addMecha(self,some,args,**kwargs):
        self.instanciationMethods.append((SimulatedObject._implAddMecha,{"some" : some, "args" : args, kwargs : kwargs}))

    def addCollisionModel(self,some,args,**kwargs):
        self.instanciationMethods.append((SimulatedObject._implAddCollisionModel,{"some" : some, "args" : args, kwargs : kwargs}))

    @staticmethod
    def _implAddSolvers(node, odeType:str = "EulerImplicit", linearSolverType:str="SparseLDLSolver",**kwargs) -> None:
        node.addObject(odeType,kwargs["ODEParams"])
        node.addObject(linearSolverType,kwargs["LinearSolverParams"])

    @staticmethod
    def _implAddTopology(node, elemType:str = "points", linearSolverType:str="SparseLDLSolver",**kwargs) -> None:
        pass

    @staticmethod
    def _implAddMecha(node, odeType:str = "EulerImplicit", linearSolverType:str="SparseLDLSolver",**kwargs) -> None:
        pass


    @staticmethod
    def _implAddCollisionModel(node, odeType:str = "EulerImplicit", linearSolverType:str="SparseLDLSolver",**kwargs) -> None:
        #Use of addMappedObjects...
        pass


def addMappedObjects(parentNode, obj:PrefabricatedObject, mappingType:str = "Barycentric") -> None:
    obj.instantiate(parentNode)
    obj.node.addObject(mappingType + "Mapping")





