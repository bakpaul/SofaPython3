from NodeWrapper import PrefabMethod

@PrefabMethod
def setupDefaultHeader(node, _displayFlags = "showVisualModels", _parallelComputing=False,**kwargs):

    node.addObject('VisualStyle', displayFlags=_displayFlags)

    node.addObject("RequiredPlugin", pluginName=['Sofa.Component.Constraint.Projective',
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
def setupCollisionHeader(node,  _displayFlags = "showVisualModels", _parallelComputing=False,**kwargs):

    node.addObject('VisualStyle', displayFlags=_displayFlags)

    node.addObject("RequiredPlugin", pluginName=['Sofa.Component.Constraint.Lagrangian',
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

    node.addObject('DefaultContactManager',name="ContactManager",**kwargs)
    node.addObject('LocalMinDistance' ,name="Distance", **kwargs)
    node.addObject('GenericConstraintSolver',name="ConstraintSolver", tolerance=1e-6, maxIterations=1000, **kwargs)

    return node
