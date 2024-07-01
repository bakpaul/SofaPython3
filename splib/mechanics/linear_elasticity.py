from core.node_wrapper import *
from core.utils import *
from topology.dynamic import ElementType


@PrefabMethod
@MapKeywordArg("constitutiveLaw",["_youngModulus","youngModulus"],["_poissonRatio","poissonRatio"],["_method","method"])
def addLinearElasticity(node,elem:ElementType,_youngModulus=None, _poissonRatio=None, _method=None,**kwargs):
    match elem:
        case ElementType.EDGES:
            node.addObject("BeamFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case ElementType.TRIANGLES:
            node.addObject("TriangleFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case ElementType.QUAT:
            node.addObject("QuadBendingFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case ElementType.TETRA:
            node.addObject("TetrahedronFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case ElementType.HEXA:
            node.addObject("HexahedronFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case _:
            print('Linear elasticity is only available for topology of type EDGES, TRIANGLES, QUADS, TETRAHEDRON, HEXAHEDRON')
            return