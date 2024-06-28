from core.node_wrapper import PrefabSimulation
from topology.dynamic import *
from simulation.headers import *
from simulation.ode_solvers import *
from simulation.linear_solvers import *
from mechanics.linear_elasticity import *

class displayNode():
    def __init__(self,_level=0):
        self.prefix = ""
        for i in range(_level):
            self.prefix += "| "

    def addObject(self,type:str,**kwargs):
        print(self.prefix + type + " with " + str(kwargs))

    def addChild(self,name:str):
        print(self.prefix + "-> Node : " + name)
        return displayNode(len(self.prefix) + 1)

@PrefabSimulation
def createScene(rootNode):

    setupDefaultHeader(rootNode,requiredPlugins={"pluginName":['Sofa.Component.Constraint.Projective', 'Sofa.Component.Engine.Select']})

    childNode = rootNode.addChild("simulated1")
    addExplicitODE(childNode)
    addLinearSolver(childNode)
    addPointTopology(childNode,_source="afaeh",container={'src':'agethefa'})
    childNode.addObject("MechanicalState")
    addLinearElasticity(childNode,ElementType.EDGES, _youngModulus=10)

    return rootNode



if __name__ == "__main__":
    Node = displayNode()
    createScene(Node)






