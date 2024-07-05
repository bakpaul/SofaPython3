from core.node_wrapper import BasePrefab

from topology.loader import *
from topology.dynamic import *
from topology.static import *


class NonSimulatedObject(BasePrefab):
    def __init__(self, node,
                 _template, _elemType:ElementType=None,_dynamicTopo=False,_filename=None, _source=None,*args,**kwargs):
        super().__init__(node,*args,**kwargs)

        if(_elemType is not None):
            if((_source is not None) and (_filename is not None)):
            print("[Warning] you cannot have multiple sources for your topology, taking filename")

            if(_filename is not None):
                loadMesh(self.node,_filename, **kwargs)
                topoSrc = "@meshLoader"
            elif(_source is not None):
                topoSrc = _source

            if(_dynamicTopo):
                addDynamicTopology(self.node,_source=topoSrc,**kwargs)
            else:
                addStaticTopology(self.node,_source=topoSrc,**kwargs)

        mstateParams = getParameterSet("mstate",kwargs)
        self.mechanicalObject = self.node.addObject("MechanicalObject",name="mstate", template=_template, **mstateParams)




