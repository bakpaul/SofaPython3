from core.node_wrapper import *
from enum import Enum
from core.utils import MapKeywordArg

# class syntax

class ElementType(Enum):
    POINTS      = 1
    EDGES       = 2
    TRIANGLES   = 3
    QUAD        = 4
    TETRA       = 5
    HEXA        = 6


@PrefabMethod
@MapKeywordArg("container",["source","src"],["position","position"])
def addPointTopology(node,position=None,source=None,**kwargs):
    node.addObject("PointSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("PointSetTopologyContainer", name="container",**kwargs)
    node.addObject("PointSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("container",["source","src"],["position","position"],["edges","edges"])
def addEdgeTopology(node,position=None,edges=None,source=None,**kwargs):
    node.addObject("EdgeSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("EdgeSetTopologyContainer", name="container",**kwargs)
    node.addObject("EdgeSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("container",["source","src"],["position","position"],["edges","edges"]
                          ,["triangles","triangles"])
def addTriangleTopology(node,position=None,edges=None,triangles=None,source=None,**kwargs):
    node.addObject("TriangleSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TriangleSetTopologyContainer", name="container",**kwargs)
    node.addObject("TriangleSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("container",["source","src"],["position","position"],["edges","edges"]
                          ,["quads","quads"])
def addQuadTopology(node,position=None,edges=None,quads=None,source=None,**kwargs):
    node.addObject("QuadSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("QuadSetTopologyContainer", name="container",**kwargs)
    node.addObject("QuadSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("container",["source","src"],["position","position"],["edges","edges"]
                          ,["triangles","triangles"],["tetrahedra","tetrahedra"])
def addTetrahedronTopology(node,position=None,edges=None,triangles=None,tetrahedra=None,source=None,**kwargs):
    node.addObject("TetrahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TetrahedronSetTopologyContainer", name="container",**kwargs)
    node.addObject("TetrahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
@MapKeywordArg("container",["source","src"],["position","position"],["edges","edges"]
                          ,["quads","quads"],["hexahedra","hexahedra"])
def addHexahedronTopology(node,position=None,edges=None,quads=None,hexahedra=None,source=None,**kwargs):
    node.addObject("HexahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("HexahedronSetTopologyContainer", name="container",**kwargs)
    node.addObject("HexahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

def addDynamicTopology(node,type:ElementType,**kwargs):

    match type:
        case ElementType.POINTS:
            addPointTopology(node,**kwargs)
            return
        case ElementType.EDGES:
            addEdgeTopology(node,**kwargs)
            return
        case ElementType.TRIANGLES:
            addTriangleTopology(node,**kwargs)
            return
        case ElementType.QUAD:
            addQuadTopology(node,**kwargs)
            return
        case ElementType.TETRA:
            addTetrahedronTopology(node,**kwargs)
            return
        case ElementType.HEXA:
            addHexahedronTopology(node,**kwargs)
            return
        case _:
            print('Topology type should be one of the following : "ElementType.POINTS, ElementType.EDGES, ElementType.TRIANGLES, ElementType.QUAD, ElementType.TETRA, ElementType.HEXA" ')
            return
