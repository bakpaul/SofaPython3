from NodeWrapper import PrefabMethod

@PrefabMethod
def addStaticTopology(node,_source=None,**kwargs):
    node.addObject("MeshTopology", name="topology",**kwargs)
    if(_source):
        node.addObject("MeshTopology", name="container", src=_source,**kwargs)
    else:
        node.addObject("MeshTopology", name="container",**kwargs)
