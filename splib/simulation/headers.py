from core.node_wrapper import PrefabMethod

@PrefabMethod
def setupDefaultHeader(node, displayFlags = "showVisualModels", parallelComputing=False,**kwargs):

    node.addObject('VisualStyle', displayFlags=displayFlags)

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


@PrefabMethod
def setupPenalityCollisionHeader(node,  displayFlags = "showVisualModels", stick=False, **kwargs):

    node.addObject('VisualStyle', displayFlags=displayFlags)

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

    node.addObject('DefaultAnimationLoop',name="animation", **kwargs)
    node.addObject('CollisionPipeline', name="collisionPipeline", **kwargs)
    node.addObject('BruteForceBroadPhase', name="broadPhase", **kwargs)
    node.addObject('BVHNarrowPhase',  name="narrowPhase", **kwargs)

    if(stick):
        node.addObject('CollisionResponse',name="ContactManager", response="BarycentricStickContact",**kwargs)
    else:
        node.addObject('CollisionResponse',name="ContactManager", response="BarycentricPenalityContact",**kwargs)
    node.addObject('LocalMinDistance' ,name="Distance", **kwargs)

    return node

@PrefabMethod
def setupLagrangianCollision(node,  displayFlags = "showVisualModels", parallelComputing=False, stick=False, frictionCoef=0.0, tolerance=0.0, maxIterations=100, **kwargs):

    node.addObject('VisualStyle', displayFlags=displayFlags)

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

    node.addObject('CollisionPipeline', name="collisionPipeline",
                   **kwargs)

    node.addObject('BruteForceBroadPhase', name="broadPhase",
                   **kwargs)

    node.addObject('BVHNarrowPhase',  name="narrowPhase",
                   **kwargs)

    if(stick):
        node.addObject('CollisionResponse',name="ContactManager", response="StickContactConstraint", responseParams="tol="+str(tolerance),**kwargs)
    else:
        node.addObject('CollisionResponse',name="ContactManager", response="FrictionContact", responseParams="mu="+str(frictionCoef),**kwargs)
    node.addObject('LocalMinDistance' ,name="Distance", **kwargs)
    node.addObject('GenericConstraintSolver',name="ConstraintSolver", tolerance=tolerance, maxIterations=maxIterations, **kwargs)

    return node
