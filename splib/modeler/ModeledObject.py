from typing import List, Callable, Tuple, Dict

##########
# Callable object used to store method and parameters needed to instanciate
##########
class InstanciationMethod():
    m_methodID : str
    m_method   : Callable
    m_params   : Dict

    def __init__(self,
                 _id : str,
                 _method : Callable,
                 _params : Dict):
        self.m_methodID = _id
        self.m_method = _method
        self.m_params = _params
    def __call__(self,
                 node):
        self.m_method(node,self.m_params)
    def setParams(self,_params:Dict):
        self.m_params = _params


##########
# Object constituted only of a list of InstanciationMethod acting on a Node object that will actually do the instanciation
##########
class ModeledObject(object):
    class MethodList():
        instanciationMethods : List[InstanciationMethod]

        def __init__(self):
            self.instanciationMethods = []
        def __iter__(self):
            self._iterID = -1;
            return self

        def __next__(self):
            if self._iterID + 1  < len(self.instanciationMethods):
                self._iterID += 1
                return self.instanciationMethods[self._iterID]
            else:
                raise StopIteration

        def append(self,_method : InstanciationMethod):
            for met in self.instanciationMethods:
                if met.m_methodID == _method.m_method:
                    print('Method with same id already exists in the list')
                    return UserWarning
            self.instanciationMethods.append(_method)

        def find(self, _methodID:str) -> int:
            id = -1
            acc = -1
            for met in self.instanciationMethods:
                acc += 1
                if met.m_methodID == _methodID:
                    id = acc
            return id

        def get(self, _methodID:str) :
            id = self.find(_methodID)
            if id != -1:
                return self.instanciationMethods[id]
            else:
                return RuntimeError

        def remove(self, _methodID:str) -> int:
            id = self.find(_methodID)
            if id != -1:
                self.instanciationMethods.pop(id)
            return id


    instanciationMethods : MethodList
    name                 : str
    def __init__(self,_name):
        self.name = _name
        self.instanciationMethods = ModeledObject.MethodList()
    def instantiate(self, _node):
        self.node = _node.addChild(self.name)
        for tup in self.instanciationMethods:
           tup(self.node)




##########
# Prefab specialization for simulated objects
##########
class SimulatedObject(ModeledObject):
    template : str
    def __init__(self,name:str,_template=None):
        ModeledObject.__init__(self,name)
        self.template = _template

    def defaultConstruction(self,_solverParams,_topologyParams,_mechaParams):
        self.addSolvers(_solverParams)
        self.addTopology(_topologyParams)
        self.addMecha(_mechaParams)

    def addObject(self,_objectType:str, _name:str,**kwargs):
        self.instanciationMethods.append(InstanciationMethod("AddObject(" +_objectType + ":" + _name + ")" ,SimulatedObject._implAddObject,{"_objectType" : _objectType, "_name" : _name, **kwargs}))

    def addSolvers(self,**kwargs):
        self.instanciationMethods.append(InstanciationMethod("Solvers",SimulatedObject._implAddSolvers,{**kwargs}))


    def addTopology(self,some,args,**kwargs):
        self.instanciationMethods.append(InstanciationMethod("Topology",SimulatedObject._implAddTopology,{"some" : some, "args" : args, **kwargs}))

    def addMecha(self,some,args,**kwargs):
        self.instanciationMethods.append(InstanciationMethod("Mecha",SimulatedObject._implAddMecha,{"some" : some, "args" : args, **kwargs}))

    def addCollisionModel(self,some,args,**kwargs):
        self.instanciationMethods.append(InstanciationMethod("Collision",SimulatedObject._implAddCollisionModel,{"some" : some, "args" : args, kwargs : kwargs}))

    def addMappedObject(self,
                        obj:ModeledObject,
                        mappingType:str = "Barycentric"):
        self.instanciationMethods.append(InstanciationMethod(obj.name,SimulatedObject._implAddMappedObjects,{ "obj" : obj ,"mappingType" : mappingType }))

    @staticmethod
    def _implAddObject(node, _objectType:str, _name:str, **kwargs) -> None:
        node.addObject(_objectType,name = _name,**kwargs)
    @staticmethod
    def _implAddSolvers(node, odeType:str = "EulerImplicit", linearSolverType:str="SparseLDLSolver",**kwargs) -> None:
        # node.addObject(odeType,kwargs["ODEParams"])
        # node.addObject(linearSolverType,kwargs["LinearSolverParams"])
        node.addObject(odeType,name="tata")
        node.addObject(linearSolverType,name="toto")

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

    @staticmethod
    def _implAddMappedObjects(parentNode, obj:ModeledObject, mappingType:str = "Barycentric") -> None:
        obj.instantiate(parentNode)
        obj.node.addObject(mappingType + "Mapping")


class displayNode():
    def __init__(self,_level=0):
        self.prefix = ""
        for i in range(_level):
            self.prefix += "|"
    def addObject(self,type:str,**kwargs):
        print(self.prefix + type)


    def addChild(self,name:str):
        print(self.prefix + "Node : " + name)
        return displayNode(len(self.prefix) + 1)



if __name__ == "__main__":
    Obj1 = SimulatedObject("Obj1")
    Obj2 = SimulatedObject("Obj2")

    Obj1.addSolvers()
    Obj1.addObject("TetrahedronFEMForceField","ff")

    Obj2.addSolvers()

    Obj1.addMappedObject(Obj2,"Barycentric")

    DN = displayNode()
    Obj1.instantiate(DN)


