from splib.core.node_wrapper import PrefabMethod
from splib.core.utils import getParameterSet

@PrefabMethod
def addLinearSolver(node,iterative=False,iterations=None,tolerance=None,threshold=None,template=None,constantSparsity=False,**kwargs):
    containerParams = getParameterSet("LinearSolver",kwargs)
    if iterative:
        if iterations:
            containerParams["iterations"] = iterations
        if tolerance:
            containerParams["tolerance"] = tolerance
        if threshold:
            containerParams["threshold"] = threshold
    else:
        if not(template) and not("template" in containerParams):
            containerParams["template"] = 'CompressedRowSparseMatrix'
    kwargs["LinearSolver"] = containerParams

    if(constantSparsity):
        node.addObject("ConstantSparsityPatternSystem",name='LinearSystem',**kwargs)
        kwargs["LinearSolver"]["linearSystem"]="@LinearSystem"


    if iterative:
        node.addObject('CGLinearSolver', name='LinearSolver', **kwargs)
    else:
        node.addObject('SparseLDLSolver', name='LinearSolver', **kwargs)