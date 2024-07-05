from typing import List, Callable, Tuple, Dict

##########
# Callable object used to store method and parameters needed to instanciate
##########
class InstanciationMethod():
    mmethodID : str
    mmethod   : Callable
    m_params   : Dict

    def __init__(self,
                 _id : str,
                 method : Callable,
                 _params : Dict):
        self.mmethodID = _id
        self.mmethod = method
        self.m_params = _params
    def __call__(self,
                 node):
        self.mmethod(node,**self.m_params)
    def setParams(self,_params:Dict):
        self.m_params = _params


##########
# Object constituted only of a list of InstanciationMethod acting on a Node object that will actually do the instanciation
##########
class ModeledObject(object):
    class MethodList():
        mmethods : List[InstanciationMethod]

        def __init__(self):
            self.mmethods = []
        def __iter__(self):
            self._iterID = -1;
            return self

        def __next__(self):
            if self._iterID + 1  < len(self.mmethods):
                self._iterID += 1
                return self.mmethods[self._iterID]
            else:
                raise StopIteration

        def append(self,method : InstanciationMethod):
            for met in self.mmethods:
                if met.mmethodID == method.mmethod:
                    print('Method with same id already exists in the list')
                    return UserWarning
            self.mmethods.append(method)

        def find(self, methodID:str) -> int:
            id = -1
            acc = -1
            for met in self.mmethods:
                acc += 1
                if met.mmethodID == methodID:
                    id = acc
            return id

        def get(self, methodID:str) :
            id = self.find(methodID)
            if id != -1:
                return self.mmethods[id]
            else:
                return RuntimeError

        def remove(self, methodID:str) -> int:
            id = self.find(methodID)
            if id != -1:
                self.mmethods.pop(id)
            return id


    m_instanciationMethods : MethodList
    name                 : str
    def __init__(self,_name):
        self.name = _name
        self.instanciationMethods = ModeledObject.MethodList()

    def instantiate(self, _node):
        self.node = _node.addChild(self.name)
        for tup in self.m_instanciationMethods:
           tup(self.node)

    def printDebug(self):
        print(self.name)
        for tup in self.m_instanciationMethods:
            print("  " + tup.mmethodID)



##########
# Prefab specialization for simulated objects
##########
class SimulatedObject(ModeledObject):
    template : str
    def __init__(self,name:str,template=None):
        ModeledObject.__init__(self,name)
        self.template = template

    def defaultConstruction(self,_solverParams,_topologyParams,_mechaParams):
        self.addSolvers(_solverParams)
        self.addTopology(_topologyParams)
        self.addMecha(_mechaParams)

    def addObject(self,_objectType:str, _name:str,**kwargs):
        self.m_instanciationMethods.append(InstanciationMethod("AddObject(" +_objectType + ":" + _name + ")" ,SimulatedObject._implAddObject,{"_objectType" : _objectType, "_name" : _name, **kwargs}))

    def addSolvers(self,**kwargs):
        self.m_instanciationMethods.append(InstanciationMethod("Solvers",SimulatedObject._implAddSolvers,kwargs))

    def addTopology(self,some,args,**kwargs):
        self.m_instanciationMethods.append(InstanciationMethod("Topology",SimulatedObject._implAddTopology,{"some" : some, "args" : args, **kwargs}))

    def addMecha(self,some,args,**kwargs):
        self.m_instanciationMethods.append(InstanciationMethod("Mecha",SimulatedObject._implAddMecha,{"some" : some, "args" : args, **kwargs}))

    def addCollisionModel(self,some,args,**kwargs):
        self.m_instanciationMethods.append(InstanciationMethod("Collision",SimulatedObject._implAddCollisionModel,{"some" : some, "args" : args, kwargs : kwargs}))

    def addMappedObject(self,
                        obj:ModeledObject,
                        mappingType:str = "Barycentric"):
        self.m_instanciationMethods.append(InstanciationMethod("Map " + obj.name,SimulatedObject._implAddMappedObjects,{ "obj" : obj ,"mappingType" : mappingType }))

    @staticmethod
    def _implAddObject(node, _objectType:str, _name:str, **kwargs) -> None:
        node.addObject(_objectType,name = _name,**kwargs)
    @staticmethod
    def _implAddSolvers(node, odeType:str = "EulerImplicit", linearSolverType:str="SparseLDLSolver",**kwargs) -> None:
        node.addObject(odeType,**(kwargs['ODEParams']))
        node.addObject(linearSolverType,**(kwargs['LinearSolverParams']))
        # node.addObject(odeType,name="tata")
        # node.addObject(linearSolverType,name="toto")

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





if __name__ == "__main__":
    Obj1 = SimulatedObject("Obj1")
    Obj2 = SimulatedObject("Obj2")

    # Root = RootNode()

    Obj1.addSolvers(odeType="EulerImplicitHugo",ODEParams = { "some" : 1, "arg" : 3}, LinearSolverParams = { "other" : 1, "args" : 3})
    Obj1.addObject("MyAwesomeComponent","ff")

    Obj2.addSolvers(ODEParams = { "some" : 12, "arg" : 32}, LinearSolverParams = { "other" : 781, "args" : 7853})
    Obj1.addMappedObject(Obj2,"Barycentric")

    # Root.addSubNode(Obj1)
    # Root.addSimulateObject(param1 = 12, params2 = 23)

    DN = displayNode()
    Obj1.instantiate(DN)


    print("")
    Obj1.printDebug()
    print("")
    Obj2.printDebug()




