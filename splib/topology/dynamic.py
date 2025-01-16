from splib.core.node_wrapper import PrefabMethod
from enum import Enum
from splib.core.utils import MapKeywordArg, DEFAULT_VALUE
from splib.core.enum_types import ElementType



@PrefabMethod
def addPointTopology(node,position=DEFAULT_VALUE,source=DEFAULT_VALUE, **kwargs):
    node.addObject("PointSetTopologyModifier", name="modifier", **kwargs)
    node.addObject("PointSetTopologyContainer", name="container", src=source, position=position, **kwargs)
    node.addObject("PointSetGeometryAlgorithms", name="algorithms", **kwargs)

@PrefabMethod
def addEdgeTopology(node,position=DEFAULT_VALUE,edges=DEFAULT_VALUE,source=DEFAULT_VALUE,**kwargs):
    node.addObject("EdgeSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("EdgeSetTopologyContainer", name="container", src=source, position=position, edges=edges, **kwargs)
    node.addObject("EdgeSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addTriangleTopology(node,position=DEFAULT_VALUE,edges=DEFAULT_VALUE,triangles=DEFAULT_VALUE,source=DEFAULT_VALUE,**kwargs):
    node.addObject("TriangleSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TriangleSetTopologyContainer", name="container", src=source, position=position, edges=edges, triangles=triangles, **kwargs)
    node.addObject("TriangleSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addQuadTopology(node,position=DEFAULT_VALUE,edges=DEFAULT_VALUE,quads=DEFAULT_VALUE,source=DEFAULT_VALUE,**kwargs):
    node.addObject("QuadSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("QuadSetTopologyContainer", name="container", src=source, position=position, edges=edges, quads=quads, **kwargs)
    node.addObject("QuadSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addTetrahedronTopology(node,position=DEFAULT_VALUE,edges=DEFAULT_VALUE,triangles=DEFAULT_VALUE,tetrahedra=DEFAULT_VALUE,source=DEFAULT_VALUE,**kwargs):
    node.addObject("TetrahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("TetrahedronSetTopologyContainer", name="container", src=source, position=position, edges=edges, triangles=triangles, tetrahedra=tetrahedra, **kwargs)
    node.addObject("TetrahedronSetGeometryAlgorithms", name="algorithms",**kwargs)

@PrefabMethod
def addHexahedronTopology(node,position=DEFAULT_VALUE,edges=DEFAULT_VALUE,quads=DEFAULT_VALUE,hexahedra=DEFAULT_VALUE,source=DEFAULT_VALUE,**kwargs):
    node.addObject("HexahedronSetTopologyModifier", name="modifier",**kwargs)
    node.addObject("HexahedronSetTopologyContainer", name="container", src=source, position=position, edges=edges, quads=quads, hexahedra=hexahedra, **kwargs)
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
