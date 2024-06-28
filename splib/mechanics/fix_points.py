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
@MapKeywordArg("fixedConstraints",["_indices","indices"],["_fixAll","fixAll"])
def addFixation(node,type:ConstraintType,_boxROIs=None, _sphereROIs=None, _indices=None, _fixAll=None,**kwargs):
    if (_indices is None):
        if(_boxROIs is not None):
            node.addObject("BoxROI",name='fixedBoxROI',box=_boxROIs,**kwargs)
            kwargs["fixedConstraints"]["indices"]="@fixedBoxROI.indices"
        if(_sphereROIs is not None):
            node.addObject("SphereROI",name='fixedSphereROI',centers=_sphereROIs[0],radii=_sphereROIs[1],**kwargs)
            kwargs["fixedConstraints"]["indices"]="@fixedSphereROI.indices"

    match type:
        case ConstraintType.PROJECTIVE:
            node.addObject("FixedProjectiveConstraint",name="fixedConstraints",**kwargs)
            return
        case ConstraintType.WEAK:
            node.addObject("FixedWeakConstraint",name="fixedConstraints",**kwargs)
            return
        case ConstraintType.LAGRANGIAN:
            node.addObject("LagrangianFixedConstraint",name="fixedConstraints",**kwargs)
            return
        case _:
            print('Contraint type is either ConstraintType.PROJECTIVE, ConstraintType.WEAK or ConstraintType.LAGRANGIAN')
            return
