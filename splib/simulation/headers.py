from core.node_wrapper import PrefabMethod

@PrefabMethod
def setupDefaultHeader(node, _displayFlags = "showVisualModels", _parallelComputing=False,**kwargs):

    node.addObject('VisualStyle', displayFlags=_displayFlags)

    node.addObject("RequiredPlugin", name="requiredPlugins", pluginName=['Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 ])
    node.addObject('DefaultAnimationLoop',name="animation", parallelODESolving=_parallelComputing, **kwargs)

    return node


@PrefabMethod
def setupPenalityCollisionHeader(node,  _displayFlags = "showVisualModels", _stick=False, **kwargs):

    node.addObject('VisualStyle', displayFlags=_displayFlags)

    node.addObject("RequiredPlugin", name="requiredPlugins", pluginName=['Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 ])
    node.addObject('DefaultAnimationLoop',name="animation", **kwargs)

    node.addObject('CollisionPipeline', name="collisionPipeline", **kwargs)

    node.addObject('BruteForceBroadPhase', name="broadPhase", **kwargs)

    node.addObject('BVHNarrowPhase',  name="narrowPhase", **kwargs)

    if(_stick):
        node.addObject('CollisionResponse',name="ContactManager", response="BarycentricStickContact",**kwargs)
    else:
        node.addObject('CollisionResponse',name="ContactManager", response="BarycentricPenalityContact",**kwargs)
    node.addObject('LocalMinDistance' ,name="Distance", **kwargs)

    return node

@PrefabMethod
def setupLagrangianCollision(node,  _displayFlags = "showVisualModels", _parallelComputing=False, _stick=False, _frictionCoef=0.0, _tolerance=0.0, _maxIterations=100, **kwargs):

    node.addObject('VisualStyle', displayFlags=_displayFlags)

    node.addObject("RequiredPlugin", name="requiredPlugins", pluginName=['Sofa.Component.Constraint.Lagrangian',
                                                 'Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 ])


    node.addObject('FreeMotionAnimationLoop',name="animation",
                   parallelCollisionDetectionAndFreeMotion=_parallelComputing,
                   parallelODESolving=_parallelComputing,
                   **kwargs)

    node.addObject('CollisionPipeline', name="collisionPipeline",
                   **kwargs)

    node.addObject('BruteForceBroadPhase', name="broadPhase",
                   **kwargs)

    node.addObject('BVHNarrowPhase',  name="narrowPhase",
                   **kwargs)

    if(_stick):
        node.addObject('CollisionResponse',name="ContactManager", response="StickContactConstraint", responseParams="tol="+str(_tolerance),**kwargs)
    else:
        node.addObject('CollisionResponse',name="ContactManager", response="FrictionContact", responseParams="mu="+str(_frictionCoef),**kwargs)
    node.addObject('LocalMinDistance' ,name="Distance", **kwargs)
    node.addObject('GenericConstraintSolver',name="ConstraintSolver", tolerance=_tolerance, maxIterations=_maxIterations, **kwargs)

    return node
