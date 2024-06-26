from core.node_wrapper import *

@PrefabMethod
def addImplicitODE(node,_static=False,**kwargs):
    if(_static):
        node.addObject("EulerImplicitSolver",name="ODESolver",**kwargs)
    else:
        node.addObject("StaticSolver",name="ODESolver",**kwargs)

@PrefabMethod
def addExplicitODE(node,**kwargs):
    node.addObject("EulerExplicitSolver",name="ODESolver",**kwargs)


