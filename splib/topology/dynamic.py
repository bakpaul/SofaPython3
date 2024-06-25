from NodeWrapper import *
from enum import Enum
from utils import *

# class syntax

class ElementType(Enum):
    POINTS      = 1
    EDGES       = 2
    TRIANGLES   = 3
    QUAT        = 4
    TETRA       = 5
    HEXA        = 6

def _addDynamicTopologyFromString(elementName:str,node:NodeWrapper,**kwargs):
    node.addObject(elementName+"SetTopologyModifier", name="modifier",**kwargs)
    node.addObject(elementName+"SetTopologyContainer", name="container",**kwargs)
    node.addObject(elementName+"SetGeometryAlgorithms", name="algorithms",**kwargs)


@PrefabMethod
@PointsTopo
def addPointTopology(node,_position=None,_source=None,**kwargs):
    _addDynamicTopologyFromString("Point",node,**kwargs)
@PrefabMethod
@PointsTopo
@EdgesTopo
def addEdgeTopology(node,_position=None,_edges=None,_source=None,**kwargs):
    _addDynamicTopologyFromString("Edge",node,**kwargs)

@PrefabMethod
@PointsTopo
@EdgesTopo
@TrianglesTopo
def addTriangleTopology(node,_position=None,_edges=None,_triangles=None,_source=None,**kwargs):
    _addDynamicTopologyFromString("Triangle",node,**kwargs)

@PrefabMethod
@PointsTopo
@EdgesTopo
@QuadsTopo
def addQuadTopology(node,_position=None,_edges=None,_quads=None,_source=None,**kwargs):
    _addDynamicTopologyFromString("Quad",node,**kwargs)

@PrefabMethod
@PointsTopo
@EdgesTopo
@TrianglesTopo
@TetrahedronTopo
def addTetrahedronTopology(node,_position=None,_edges=None,_triangles=None,_tetrahedra=None,_source=None,**kwargs):
    _addDynamicTopologyFromString("Tetrahedron",node,**kwargs)

@PrefabMethod
@PointsTopo
@EdgesTopo
@QuadsTopo
@HexahedronTopo
def addHexahedronTopology(node,_position=None,_edges=None,_quads=None,_hexahedra=None,_source=None,**kwargs):
    _addDynamicTopologyFromString("Hexahedron",node,**kwargs)


def addDynamicTopology(node,_type:ElementType,**kwargs):

    match _type:
        case ElementType.POINTS.value:
            addPointTopology(node,**kwargs)
            return
        case ElementType.EDGES.value:
            addEdgeTopology(node,**kwargs)
            return
        case ElementType.TRIANGLES.value:
            addTriangleTopology(node,**kwargs)
            return
        case ElementType.QUAT.value:
            addQuadTopology(node,**kwargs)
            return
        case ElementType.TETRA.value:
            addTetrahedronTopology(node,**kwargs)
            return
        case ElementType.HEXA.value:
            addHexahedronTopology(node,**kwargs)
            return
        case _:
            print('Topology type should be one of the following : "ElementType.POINTS, ElementType.EDGES, ElementType.TRIANGLES, ElementType.QUAT, ElementType.TETRA, ElementType.HEXA" ')
            return
