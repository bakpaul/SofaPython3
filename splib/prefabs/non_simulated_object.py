from splib.core.node_wrapper import BasePrefab
from splib.core.utils import getParameterSet

from splib.topology.loader import *
from splib.topology.dynamic import *
from splib.topology.static import *


class NonSimulatedObject(BasePrefab):
    def __init__(self, node,
                 template, elemType:ElementType=None,_dynamicTopo=False,filename=None, source=None,*args,**kwargs):
        super().__init__(node)

        if(elemType is not None):
            if((source is not None) and (filename is not None)):
                print("[Warning] you cannot have multiple sources for your topology, taking filename")
            topoSrc=None
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




