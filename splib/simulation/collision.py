
def setupLangrangianBasedSimulation(node,_alarmDistance, _contactDistance, _response, _frictionCoef=0.0):

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


    node.addObject('FreeMotionAnimationLoop')
    node.addObject('CollisionPipeline')

    node.addObject('BruteForceBroadPhase')
    node.addObject('BVHNarrowPhase')

    node.addObject('DefaultContactManager', responseParams="mu="+str(_frictionCoef),
                   name='Response', response='_response')
    node.addObject('LocalMinDistance',
                   alarmDistance=_alarmDistance, contactDistance=_contactDistance,
                   angleCone=0.01)
    node.addObject('GenericConstraintSolver', tolerance=1e-6, maxIterations=1000)

    return node
