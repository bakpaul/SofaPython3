from core.node_wrapper import PrefabMethod
from core.utils import MapKeywordArg

@PrefabMethod
@MapKeywordArg("_source","container","src")
def addStaticTopology(node,_source=None,**kwargs):
    node.addObject("MeshTopology", name="container",**kwargs)

