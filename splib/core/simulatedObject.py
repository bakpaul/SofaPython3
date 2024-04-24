def _addDefaultImplicitSolvers(node, iterative=False,_iterations=25,_tolerance=1e-5,_threshold=1e-5):
    node.addObject('EulerImplicitSolver', name='TimeIntegrationSchema')
    if iterative:
        node.addObject('CGLinearSolver', name='LinearSolver', iterations=_iterations, tolerance=_tolerance, threshold=_threshold)

    node.addObject('SparseLDLSolver', name='LinearSolver', template='CompressedRowSparseMatrix')
    return node


def addSimulatedObject(node,_name,_addSolver=_addDefaultImplicitSolvers,_template="Vec3"):
    simu = node.addChild(_name)
    _addSolver(simu)
    simu.addObject("MechanicalObject", name='mstate',template=_template)
    return node