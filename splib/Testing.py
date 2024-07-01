from prefabs.utils import PrefabSimulation
from topology.dynamic import *
from simulation.headers import *
from simulation.ode_solvers import *
from simulation.linear_solvers import *
from mechanics.linear_elasticity import *
from mechanics.mass import *
from mechanics.fix_points import *
from topology.loader import *

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

class exportScene():
    def __init__(self,name="rootNode"):
        self.name = name

    def addObject(self,type:str,**kwargs):
        suffix = ""
        for i in kwargs:
            suffix += "," + str(i) + "=\"" + str(kwargs[i]) + "\""
        print(self.name+".addObject(\"" + type + "\"" +  suffix + ")")

    def addChild(self,name:str):
        print(name + '=' + self.name+".addChild(\"" + name + "\")")
        return exportScene(name)

@PrefabSimulation
def createScene(rootNode):

    ## TODO : make this affect the actual dt and gravity of the SOFA node
    rootNode.dt = 0.02
    rootNode.gravity = [0,-9.81,0]

    setupDefaultHeader(rootNode,requiredPlugins={"pluginName":['Sofa.Component.Constraint.Projective',
                                                               'Sofa.Component.Engine.Select',
                                                               'Sofa.Component.LinearSolver.Direct',
                                                               'Sofa.Component.Mass',
                                                               'Sofa.Component.ODESolver.Backward',
                                                               'Sofa.Component.SolidMechanics.FEM.Elastic',
                                                               'Sofa.Component.StateContainer',
                                                               'Sofa.Component.Topology.Container.Grid',
                                                               'Sofa.Component.IO.Mesh',
                                                               'Sofa.Component.LinearSolver.Direct',
                                                               'Sofa.Component.Topology.Container.Dynamic',
                                                               'Sofa.Component.Visual']})


    childNode = rootNode.addSimulatedObject("simulated1")


    ## TODO : Being able to call "childNode.addAnything" by using the __getattr__ method
    loadMesh(childNode,_filename="mesh/liver.msh")
    addImplicitODE(childNode)
    addLinearSolver(childNode,_iterative=True,_iterations="25", _tolerance="1e-09", _threshold="1e-09")
    addDynamicTopology(childNode,_type=ElementType.TETRA,_source="@meshLoader")
    childNode.addObject("MechanicalObject")
    addLinearElasticity(childNode,ElementType.TETRA, _poissonRatio="0.3", _youngModulus="3000", _method='large')
    addMass(childNode,_massDensity="1.0")
    addFixation(childNode,ConstraintType.PROJECTIVE,_indices="3 39 64")


    ## EQUIVALENT TO
    # rootNode.addObject("VisualStyle",displayFlags="showVisualModels")
    # rootNode.addObject("RequiredPlugin",name="requiredPlugins",pluginName="['Sofa.Component.Constraint.Projective', 'Sofa.Component.Engine.Select', 'Sofa.Component.LinearSolver.Direct', 'Sofa.Component.Mass', 'Sofa.Component.ODESolver.Backward', 'Sofa.Component.SolidMechanics.FEM.Elastic', 'Sofa.Component.StateContainer', 'Sofa.Component.Topology.Container.Grid', 'Sofa.Component.IO.Mesh', 'Sofa.Component.LinearSolver.Direct', 'Sofa.Component.Topology.Container.Dynamic', 'Sofa.Component.Visual']")
    # rootNode.addObject("DefaultAnimationLoop",name="animation",parallelODESolving="False")
    # simulated1=rootNode.addChild(simulated1)
    # simulated1.addObject("MeshGmshLoader",name="meshLoader",filename="mesh/liver.msh")
    # simulated1.addObject("EulerExplicitSolver",name="ODESolver")
    # simulated1.addObject("CGLinearSolver",name="LinearSolver",iterations="25",tolerance="1e-09",threshold="1e-09")
    # simulated1.addObject("TetrahedronSetTopologyModifier",name="modifier")
    # simulated1.addObject("TetrahedronSetTopologyContainer",name="container",src="@meshLoader")
    # simulated1.addObject("TetrahedronSetGeometryAlgorithms",name="algorithms")
    # simulated1.addObject("MechanicalObject")
    # simulated1.addObject("TetrahedronFEMForceField",name="elasticFF",youngModulus="3000",poissonRatio="0.3",method="large")
    # simulated1.addObject("MeshMatrixMass",name="mass",massDensity="1.0")
    # simulated1.addObject("FixedProjectiveConstraint",name="fixedConstraints",indices="3 39 64")
    return rootNode



if __name__ == "__main__":
    Node = exportScene()
    createScene(Node)






