from NodeWrapper import PrefabMethod
from enum import Enum

# class syntax

class ElementType(Enum):
    POINTS      = 1
    EDGES       = 2
    TRIANGLES   = 3
    QUAT        = 4
    TETRA       = 5
    HEXA        = 6

def _addDynamicTopologyFromString(elementName:str,node,_source=None,**kwargs):
    node.addObject(elementName+"SetTopologyModifier", name="modifier",**kwargs)
    if(_source):
        node.addObject(elementName+"SetTopologyContainer", name="container", src=_source,**kwargs)
    else:
        node.addObject(elementName+"SetTopologyContainer", name="container",**kwargs)

    node.addObject(elementName+"SetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addPointTopology(node,_source=None,**kwargs):
    _addDynamicTopologyFromString("Point",node,_source=_source,**kwargs)
@PrefabMethod
def addEdgeTopology(node,_source=None,**kwargs):
    _addDynamicTopologyFromString("Edge",node,_source=_source,**kwargs)

@PrefabMethod
def addTriangleTopology(node,_source=None,**kwargs):
    _addDynamicTopologyFromString("Triangle",node,_source=_source,**kwargs)

@PrefabMethod
def addQuadTopology(node,_source=None,**kwargs):
    _addDynamicTopologyFromString("Quad",node,_source=_source,**kwargs)

@PrefabMethod
def addTetrahedronTopology(node,_source=None,**kwargs):
    _addDynamicTopologyFromString("Tetrahedron",node,_source=_source,**kwargs)

@PrefabMethod
def addHexahedronTopology(node,_source=None,**kwargs):
    _addDynamicTopologyFromString("Hexahedron",node,_source=_source,**kwargs)


def addDynamicTopology(node,_type:ElementType,_source=None,**kwargs):

    match _type:
        case ElementType.POINTS.value:
            addEdgeTopology(node,_source,**kwargs)
            return
        case ElementType.EDGES.value:
            addEdgeTopology(node,_source,**kwargs)
            return
        case ElementType.TRIANGLES.value:
            addEdgeTopology(node,_source,**kwargs)
            return
        case ElementType.QUAT.value:
            addEdgeTopology(node,_source,**kwargs)
            return
        case ElementType.TETRA.value:
            addEdgeTopology(node,_source,**kwargs)
            return
        case ElementType.HEXA.value:
            addEdgeTopology(node,_source,**kwargs)
            return
        case _:
            print('Topology type should be one of the following : "ElementType.POINTS, ElementType.EDGES, ElementType.TRIANGLES, ElementType.QUAT, ElementType.TETRA, ElementType.HEXA" ')
            return
