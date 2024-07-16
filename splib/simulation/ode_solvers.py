from splib.core.node_wrapper import PrefabMethod

@PrefabMethod
def addImplicitODE(node,static=False,**kwargs):
    if( not(static) ):
        node.addObject("EulerImplicitSolver",name="ODESolver",rayleighStiffness="0.1", rayleighMass="0.1",**kwargs)
    else:
        node.addObject("StaticSolver",name="ODESolver",**kwargs)

@PrefabMethod
def addExplicitODE(node,**kwargs):
    node.addObject("EulerExplicitSolver",name="ODESolver",**kwargs)


