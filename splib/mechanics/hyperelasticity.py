from core.node_wrapper import *
from core.utils import *
from topology.dynamic import ElementType


@PrefabMethod
@MapKeywordArg("constitutiveLaw",["_materialName","materialName"],["_parameterSet","ParameterSet"],["_matrixRegularization","matrixRegularization"])
def addHyperelasticity(node,elem:ElementType,_materialName=None, _parameterSet=None, _matrixRegularization=None,**kwargs):
    match elem:
        case ElementType.TETRA:
            node.addObject("TetrahedronHyperelasticityFEMForceField",name="constitutiveLaw",**kwargs)
            return
        case _:
            print('Hyperelasticity model only exist for Tetrahedron elements.')
            return