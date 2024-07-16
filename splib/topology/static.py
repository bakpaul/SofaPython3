from splib.core.node_wrapper import PrefabMethod
from splib.core.utils import MapKeywordArg

@PrefabMethod
@MapKeywordArg("container",["source","src"])
def addStaticTopology(node,source=None,**kwargs):
    node.addObject("MeshTopology", name="container",**kwargs)

