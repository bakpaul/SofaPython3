from splib.core.node_wrapper import PrefabMethod
from splib.core.utils import MapKeywordArg
from splib.core.enum_types import ConstraintType
from enum import Enum


##box

@PrefabMethod
@MapKeywordArg("fixedConstraints",["indices","indices"],["fixAll","fixAll"])
def addFixation(node,type:ConstraintType,boxROIs=None, sphereROIs=None, indices=None, fixAll=None,**kwargs):
    if (indices is None):
        if(boxROIs is not None):
            node.addObject("BoxROI",name='fixedBoxROI',box=boxROIs,**kwargs)
            kwargs["fixedConstraints"]["indices"]="@fixedBoxROI.indices"
        if(sphereROIs is not None):
            node.addObject("SphereROI",name='fixedSphereROI',centers=sphereROIs[0],radii=sphereROIs[1],**kwargs)
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
