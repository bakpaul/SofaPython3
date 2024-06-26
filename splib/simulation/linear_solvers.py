from core.node_wrapper import *
from core.utils import *

@PrefabMethod
def addLinearSolver(node,_iterative=False,_iterations=None,_tolerance=None,_threshold=None,_template=None,**kwargs):
    containerParams = getParameterSet("LinearSolver",kwargs)
    if _iterative:
        if _iterations:
            containerParams["iterations"] = _iterations
        if _tolerance:
            containerParams["tolerance"] = _tolerance
        if _threshold:
            containerParams["threshold"] = _threshold
    else:
        if not(_template) and not("template" in containerParams):
            containerParams["template"] = 'CompressedRowSparseMatrix'
    kwargs["LinearSolver"] = containerParams


    if _iterative:
        node.addObject('CGLinearSolver', name='LinearSolver', **kwargs)
    else:
        node.addObject('SparseLDLSolver', name='LinearSolver', **kwargs)