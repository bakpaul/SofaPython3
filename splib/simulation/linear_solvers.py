from splib.core.node_wrapper import PrefabMethod
from splib.core.utils import *

@PrefabMethod
@MapKeywordArg("LinearSolver",["parallelInverseProduct","parallelInverseProduct"])
def addLinearSolver(node,iterative=False,iterations=None,tolerance=None,threshold=None,template=None,constantSparsity=False,parallelInverseProduct=False,**kwargs):
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
        else:
            containerParams["template"] = template
    kwargs["LinearSolver"] = containerParams
    kwargs["LinearSolver"]["parallelInverseProduct"] = parallelInverseProduct

    if(constantSparsity):
        node.addObject("ConstantSparsityPatternSystem",name='LinearSystem',**kwargs)
        kwargs["LinearSolver"]["template"] = 'CompressedRowSparseMatrix'
        kwargs["LinearSolver"]["linearSystem"]="@LinearSystem"



    if iterative:
        node.addObject('CGLinearSolver', name='LinearSolver', **kwargs)
    else:
        node.addObject('SparseLDLSolver', name='LinearSolver', **kwargs)