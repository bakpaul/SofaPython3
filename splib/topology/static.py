from core.node_wrapper import PrefabMethod
from utils import *

@PrefabMethod
@BaseTopo
def addStaticTopology(node,_source=None,**kwargs):
    node.addObject("MeshTopology", name="container",**kwargs)

