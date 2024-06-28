from core.node_wrapper import *
from core.utils import *
from topology.dynamic import ElementType


@PrefabMethod
@MapKeywordArg("mass",["_totalMass","totalMass"],["_massDensity","massDensity"],["_lumping","lumping"])
def addMass(node,_totalMass=None,_massDensity=None,_lumping=None,**kwargs):
    if (_totalMass is not None) and (_massDensity is not None) :
        print("[warning] You defined the totalMass and the massDensity in the same time, only taking massDensity into account")
        kwargs.pop('massDensity')

    node.addObject("MeshMatrixMass",name="mass",**kwargs)


