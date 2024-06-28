from core.node_wrapper import PrefabMethod
from core.utils import MapKeywordArg

@PrefabMethod
@MapKeywordArg("container",["_source","src"])
def addStaticTopology(node,_source=None,**kwargs):
    node.addObject("MeshTopology", name="container",**kwargs)

