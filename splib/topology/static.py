from splib.core.node_wrapper import PrefabMethod
from splib.core.utils import DEFAULT_VALUE

@PrefabMethod
def addStaticTopology(node,source=DEFAULT_VALUE,**kwargs):
    node.addObject("MeshTopology", name="container", src=source, **kwargs)

