from core.node_wrapper import *
from core.utils import *
from enum import Enum



class ConstraintType(Enum):
    PROJECTIVE = 1
    WEAK       = 2
    LAGRANGIAN = 3

##centers radii
##box

@PrefabMethod
@MapKeywordArg("hyperelastic",["_indices","indices"],["_fixAll","fixAll"])
def addFixation(node,type:ConstraintType,_boxROIs=None, _sphereROIs=None, _indices=None, _fixAll=None,**kwargs):
    if (_indices is None):
        if(_boxROIs is not None):
            node.addObject("BoxROI",name='fixedBoxROI',box=_boxROIs,**kwargs)
        if(_sphereROIs is not None):
            node.addObject("SphereROI",name='fixedSphereROI',centers=_sphereROIs[0],radii=_sphereROIs[1],**kwargs)

    match type:
        case ConstraintType.PROJECTIVE:
            node.addObject("FixedProjectiveConstraint",name="hyperelasticFF",**kwargs)
            return
        case ConstraintType.WEAK:
            node.addObject("FixedWeakConstraint",name="hyperelasticFF",**kwargs)
            return
        case ConstraintType.LAGRANGIAN:
            node.addObject("TetrahedronHyperelasticityFEMForceField",name="hyperelasticFF",**kwargs)
            return
        case _:
            print('Hyperelasticity model only exist for Tetrahedron elements.')
            return
