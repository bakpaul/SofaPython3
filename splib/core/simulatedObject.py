
class SimulatedObject():
    def __init__(self, parentNode, _name, _template):
        self.node = parentNode.addChild(_name)
        self.node.addObject("MechanicalObject", name='MState',template=_template)




def addDefaultImplicitSolvers(Obj:SimulatedObject, iterative=False,_iterations=25,_tolerance=1e-5,_threshold=1e-5):
    Obj.node.addObject('EulerImplicitSolver', name='ODESolver')
    if iterative:
        Obj.node.addObject('CGLinearSolver', name='LinearSolver', iterations=_iterations, tolerance=_tolerance, threshold=_threshold)
    else:
        Obj.node.addObject('SparseLDLSolver', name='LinearSolver', template='CompressedRowSparseMatrix')


