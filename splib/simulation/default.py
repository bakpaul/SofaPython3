def setupDefaultSimulation(node):

    node.addObject('VisualStyle', displayFlags="showBehaviorModels showForceFields")

    node.addObject("RequiredPlugin", pluginName=['Sofa.Component.Constraint.Projective',
                                                 'Sofa.Component.Engine.Select',
                                                 'Sofa.Component.LinearSolver.Direct',
                                                 'Sofa.Component.Mass',
                                                 'Sofa.Component.ODESolver.Backward',
                                                 'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                 'Sofa.Component.StateContainer',
                                                 'Sofa.Component.Topology.Container.Grid',
                                                 ])
    node.addObject('DefaultAnimationLoop')

    return node

