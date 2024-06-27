from core.node_wrapper import *
from enum import Enum
from topology.utils import *

# class syntax

class ElementType(Enum):
    POINTS      = 1
    EDGES       = 2
    TRIANGLES   = 3
    QUAT        = 4
    TETRA       = 5
    HEXA        = 6



@PrefabMethod
def addPointTopology(node,_position=None,_source=None,**kwargs):
    node.addObject("PointSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("PointSetTopologyContainer", name="container",
                   src=_source,
                   position=_position,
                   **kwargs)
    node.addObject("PointSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addEdgeTopology(node,_position=None,_edges=None,_source=None,**kwargs):
    node.addObject("EdgeSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("EdgeSetTopologyContainer", name="container",
                   src=_source,
                   position=_position,
                   edges=_edges,
                   **kwargs)
    node.addObject("EdgeSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addTriangleTopology(node,_position=None,_edges=None,_triangles=None,_source=None,**kwargs):
    node.addObject("TriangleSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TriangleSetTopologyContainer", name="container",
                   src=_source,
                   position=_position,
                   edges=_edges,
                   triangles=_triangles,
                   **kwargs)
    node.addObject("TriangleSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addQuadTopology(node,_position=None,_edges=None,_quads=None,_source=None,**kwargs):
    node.addObject("QuadSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("QuadSetTopologyContainer", name="container",
                   src=_source,
                   position=_position,
                   edges=_edges,
                   quads=_quads,
                   **kwargs)
    node.addObject("QuadSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addTetrahedronTopology(node,_position=None,_edges=None,_triangles=None,_tetrahedra=None,_source=None,**kwargs):
    node.addObject("TetrahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TetrahedronSetTopologyContainer", name="container",
                   src=_source,
                   position=_position,
                   edges=_edges,
                   triangles=_triangles,
                   tetrahedra= _tetrahedra,
                   **kwargs)
    node.addObject("TetrahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addHexahedronTopology(node,_position=None,_edges=None,_quads=None,_hexahedra=None,_source=None,**kwargs):
    node.addObject("HexahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("HexahedronSetTopologyContainer", name="container",
                   src=_source,
                   position=_position,
                   edges=_edges,
                   quads=_quads,
                   hexahedra= _hexahedra,
                   **kwargs)
    node.addObject("HexahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

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
