from core.node_wrapper import *
from enum import Enum
from core.utils import MapKeywordArg

# class syntax

class ElementType(Enum):
    POINTS      = 1
    EDGES       = 2
    TRIANGLES   = 3
    QUAT        = 4
    TETRA       = 5
    HEXA        = 6


@PrefabMethod
@MapKeywordArg("_source","container","src")
@MapKeywordArg("_position","container","position")
def addPointTopology(node,_position=None,_source=None,**kwargs):
    node.addObject("PointSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("PointSetTopologyContainer", name="container",**kwargs)
    node.addObject("PointSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("_source","container","src")
@MapKeywordArg("_position","container","position")
@MapKeywordArg("_edges","container","edges")
def addEdgeTopology(node,_position=None,_edges=None,_source=None,**kwargs):
    node.addObject("EdgeSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("EdgeSetTopologyContainer", name="container",**kwargs)
    node.addObject("EdgeSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("_source","container","src")
@MapKeywordArg("_position","container","position")
@MapKeywordArg("_edges","container","edges")
@MapKeywordArg("_triangles","container","triangles")
def addTriangleTopology(node,_position=None,_edges=None,_triangles=None,_source=None,**kwargs):
    node.addObject("TriangleSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TriangleSetTopologyContainer", name="container",**kwargs)
    node.addObject("TriangleSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("_source","container","src")
@MapKeywordArg("_position","container","position")
@MapKeywordArg("_edges","container","edges")
@MapKeywordArg("_quads","container","quads")
def addQuadTopology(node,_position=None,_edges=None,_quads=None,_source=None,**kwargs):
    node.addObject("QuadSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("QuadSetTopologyContainer", name="container",**kwargs)
    node.addObject("QuadSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("_source","container","src")
@MapKeywordArg("_position","container","position")
@MapKeywordArg("_edges","container","edges")
@MapKeywordArg("_triangles","container","triangles")
@MapKeywordArg("_tetrahedra","container","tetrahedra")
def addTetrahedronTopology(node,_position=None,_edges=None,_triangles=None,_tetrahedra=None,_source=None,**kwargs):
    node.addObject("TetrahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TetrahedronSetTopologyContainer", name="container",**kwargs)
    node.addObject("TetrahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("_source","container","src")
@MapKeywordArg("_position","container","position")
@MapKeywordArg("_edges","container","edges")
@MapKeywordArg("_quads","container","quads")
@MapKeywordArg("_hexahedra","container","hexahedra")
def addHexahedronTopology(node,_position=None,_edges=None,_quads=None,_hexahedra=None,_source=None,**kwargs):
    node.addObject("HexahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("HexahedronSetTopologyContainer", name="container",**kwargs)
    node.addObject("HexahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

def addDynamicTopology(node,_type:ElementType,**kwargs):

    match _type:
        case ElementType.POINTS:
            addPointTopology(node,**kwargs)
            return
        case ElementType.EDGES:
            addEdgeTopology(node,**kwargs)
            return
        case ElementType.TRIANGLES:
            addTriangleTopology(node,**kwargs)
            return
        case ElementType.QUAT:
            addQuadTopology(node,**kwargs)
            return
        case ElementType.TETRA:
            addTetrahedronTopology(node,**kwargs)
            return
        case ElementType.HEXA:
            addHexahedronTopology(node,**kwargs)
            return
        case _:
            print('Topology type should be one of the following : "ElementType.POINTS, ElementType.EDGES, ElementType.TRIANGLES, ElementType.QUAT, ElementType.TETRA, ElementType.HEXA" ')
            return
