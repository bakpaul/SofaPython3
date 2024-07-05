from core.node_wrapper import PrefabMethod
from core.utils import MapKeywordArg

@PrefabMethod
@MapKeywordArg("container",["source","src"])
def addStaticTopology(node,source=None,**kwargs):
    node.addObject("MeshTopology", name="container",**kwargs)

