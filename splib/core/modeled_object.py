from typing import List, Callable, Tuple, Dict
from hashlib import sha224

##########
# Callable object used to store method and parameters needed to instanciate
##########
class InstanciationMethod():
    m_methodID : str
    m_method   : Callable
    m_args     : List
    m_kwargs   : Dict

    def __init__(self,
                 id : str,
                 method : Callable,
                 args : List,
                 kwargs : Dict):
        self.m_methodID = id
        self.m_method = method
        self.m_args = args
        self.m_kwargs = kwargs
    def __call__(self,
                 node):
        self.m_method(node,*self.m_args,**self.m_kwargs)
    def setParams(self, args:List = None, kwargs:Dict = None):
        if(args is not None):
            self.m_args = args
        if(kwargs is not None):
            self.m_kwargs = kwargs


##########
# Object constituted only of a list of InstanciationMethod acting on a Node object that will actually do the instanciation
##########
class ModeledObject(object):
    class MethodList():
        m_methods : List[InstanciationMethod]

        def __init__(self):
            self.m_methods = []
        def __iter__(self):
            self._iterID = -1;
            return self

        def __next__(self):
            if self._iterID + 1  < len(self.m_methods):
                self._iterID += 1
                return self.m_methods[self._iterID]
            else:
                raise StopIteration

        def append(self,method : InstanciationMethod):
            for met in self.m_methods:
                if met.m_methodID == method.m_method:
                    print('Method with same id already exists in the list')
                    return UserWarning
            self.m_methods.append(method)

        def find(self, methodID:str) -> int:
            id = -1
            acc = -1
            for met in self.m_methods:
                acc += 1
                if met.m_methodID == methodID:
                    id = acc
            return id

        def get(self, methodID:str) :
            id = self.find(methodID)
            if id != -1:
                return self.m_methods[id]
            else:
                return RuntimeError

        def remove(self, methodID:str) -> int:
            id = self.find(methodID)
            if id != -1:
                self.m_methods.pop(id)
            return id


    m_instanciationMethods : MethodList
    name                 : str
    _uniqueID            : int
    def __init__(self,_name):
        self.name = _name
        self.m_instanciationMethods = ModeledObject.MethodList()
        self._uniqueID = 0

    def instantiate(self, _node):
        self.node = _node.addChild(self.name)
        for tup in self.m_instanciationMethods:
           tup(self.node)

    def printDebug(self):
        print(self.name)
        for tup in self.m_instanciationMethods:
            print("  " + tup.m_methodID)

    def appendMethod(self,id,method,args,kwargs):
        self.m_instanciationMethods.append(InstanciationMethod(id,method,args,kwargs))

    def getUniqueID(self,prefix):
        uniqueID = prefix + "_" + sha224((prefix + self.name + str(self._uniqueID)).encode('ascii')).hexdigest()[:10]
        self._uniqueID += 1
        while not(self.m_instanciationMethods.find(uniqueID) == -1):
            uniqueID = prefix + "_" + sha224((prefix + self.name + str(self._uniqueID)).encode('ascii')).hexdigest()[:10]
            self._uniqueID += 1
        return  uniqueID




