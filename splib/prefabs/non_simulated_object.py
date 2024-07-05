from core.node_wrapper import BasePrefab

from topology.loader import *
from topology.dynamic import *
from topology.static import *


class NonSimulatedObject(BasePrefab):
    def __init__(self, node,
                 template, _elemType:ElementType=None,_dynamicTopo=False,filename=None, source=None,*args,**kwargs):
        super().__init__(node,*args,**kwargs)

        if(_elemType is not None):
            if((source is not None) and (filename is not None)):
            print("[Warning] you cannot have multiple sources for your topology, taking filename")

            if(filename is not None):
                loadMesh(self.node,filename, **kwargs)
                topoSrc = "@meshLoader"
            elif(source is not None):
                topoSrc = source

            if(_dynamicTopo):
                addDynamicTopology(self.node,source=topoSrc,**kwargs)
            else:
                addStaticTopology(self.node,source=topoSrc,**kwargs)

        mstateParams = getParameterSet("mstate",kwargs)
        self.mechanicalObject = self.node.addObject("MechanicalObject",name="mstate", template=template, **mstateParams)




