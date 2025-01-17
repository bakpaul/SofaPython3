from splib.core.node_wrapper import ReusableMethod
from enum import Enum


class CollisionType(Enum):
    NONE = 1
    PENALITY = 2
    LAGRANGIAN = 3


@ReusableMethod
def setupDefaultHeader(node, displayFlags = "showVisualModels", backgroundColor=[1,1,1,1], parallelComputing=False,**kwargs):

    node.addObject('VisualStyle', displayFlags=displayFlags)
    node.addObject('BackgroundSetting', color=backgroundColor)

    node.addObject("RequiredPlugin", name="requiredPlugins", pluginName=['Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 'Sofa.Component.IO.Mesh',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.ODESolver.Forward',
                                                 'Sofa.Component.Topology.Container.Dynamic',
                                                 'Sofa.Component.Visual',
                                                 ],
                                                  **kwargs)
    node.addObject('DefaultAnimationLoop',name="animation", parallelODESolving=parallelComputing, **kwargs)

    return node


@ReusableMethod
def setupPenalityCollisionHeader(node,  displayFlags = "showVisualModels",backgroundColor=[1,1,1,1], stick=False, parallelComputing=False,**kwargs):
    node.addObject('VisualStyle', displayFlags=displayFlags)
    node.addObject('BackgroundSetting', color=backgroundColor)

    node.addObject("RequiredPlugin", name="requiredPlugins", pluginName=['Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 'Sofa.Component.IO.Mesh',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.ODESolver.Forward',
                                                 'Sofa.Component.Topology.Container.Dynamic',
                                                 'Sofa.Component.Visual',
                                                 ],
                                                 **kwargs)

    parallelPrefix = ""
    if(parallelComputing):
        parallelPrefix="Parallel"

    node.addObject('DefaultAnimationLoop',name="animation", **kwargs)
    node.addObject('CollisionPipeline', name="collisionPipeline", **kwargs)
    node.addObject(parallelPrefix+'BruteForceBroadPhase', name="broadPhase", **kwargs)
    node.addObject(parallelPrefix+'BVHNarrowPhase',  name="narrowPhase", **kwargs)

    if(stick):
        node.addObject('CollisionResponse',name="ContactManager", response="BarycentricStickContact",**kwargs)
    else:
        node.addObject('CollisionResponse',name="ContactManager", response="BarycentricPenalityContact",**kwargs)
    node.addObject('LocalMinDistance' ,name="Distance", **kwargs)

    return node


# TODO add alarm settings
@ReusableMethod
def setupLagrangianCollision(node,  displayFlags = "showVisualModels",backgroundColor=[1,1,1,1], parallelComputing=False, stick=False, frictionCoef=0.0, tolerance=0.0, maxIterations=100, **kwargs):
    node.addObject('VisualStyle', displayFlags=displayFlags)
    node.addObject('BackgroundSetting', color=backgroundColor)

    node.addObject("RequiredPlugin", name="requiredPlugins", pluginName=['Sofa.Component.Constraint.Lagrangian',
                                                 'Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 'Sofa.Component.IO.Mesh',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.ODESolver.Forward',
                                                 'Sofa.Component.Topology.Container.Dynamic',
                                                 'Sofa.Component.Visual',
                                                 ],
                                                 **kwargs)


    node.addObject('FreeMotionAnimationLoop',name="animation",
                   parallelCollisionDetectionAndFreeMotion=parallelComputing,
                   parallelODESolving=parallelComputing,
                   **kwargs)

    parallelPrefix = ""
    if(parallelComputing):
        parallelPrefix="Parallel"

    node.addObject('CollisionPipeline', name="collisionPipeline",
                   **kwargs)

    node.addObject(parallelPrefix+'BruteForceBroadPhase', name="broadPhase",
                   **kwargs)

    node.addObject(parallelPrefix+'BVHNarrowPhase',  name="narrowPhase",
                   **kwargs)

    if(stick):
        node.addObject('CollisionResponse',name="ContactManager", response="StickContactConstraint", responseParams="tol="+str(tolerance),**kwargs)
    else:
        node.addObject('CollisionResponse',name="ContactManager", response="FrictionContact", responseParams="mu="+str(frictionCoef),**kwargs)

    node.addObject('NewProximityIntersection' ,name="Distance", **kwargs)
    node.addObject('GenericConstraintSolver',name="ConstraintSolver", tolerance=tolerance, maxIterations=maxIterations, multithreading=parallelComputing,**kwargs)
    node.addObject("ConstraintAttachButtonSetting")

    return node
