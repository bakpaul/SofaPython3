from core.node_wrapper import *
from core.utils import *
from topology.dynamic import ElementType


@PrefabMethod
@MapKeywordArg("mass",["totalMass","totalMass"],["massDensity","massDensity"],["lumping","lumping"])
def addMass(node,template,totalMass=None,massDensity=None,lumping=None,**kwargs):
    if (totalMass is not None) and (massDensity is not None) :
        print("[warning] You defined the totalMass and the massDensity in the same time, only taking massDensity into account")
        kwargs.pop('massDensity')
    if(template=="Rigid3"):
        node.addObject("UniformMass",name="mass",**kwargs)
    else:
        node.addObject("MeshMatrixMass",name="mass",**kwargs)




