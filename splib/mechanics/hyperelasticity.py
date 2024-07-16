from splib.core.node_wrapper import PrefabMethod
from splib.core.utils import MapKeywordArg
from splib.core.enum_types import ElementType


@PrefabMethod
@MapKeywordArg("constitutiveLaw",["materialName","materialName"],["parameterSet","ParameterSet"],["matrixRegularization","matrixRegularization"])
def addHyperelasticity(node,elem:ElementType,materialName=None, parameterSet=None, matrixRegularization=None,**kwargs):
    match elem:
        case ElementType.TETRA:
            node.addObject("TetrahedronHyperelasticityFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case _:
            print('Hyperelasticity model only exist for Tetrahedron elements.')
            return