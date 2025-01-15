from splib.prefabs.utils import PrefabSimulation
from splib.prefabs.parameters import *
from splib.topology.dynamic import *
from splib.simulation.headers import *
from splib.simulation.ode_solvers import *
from splib.simulation.linear_solvers import *
from splib.mechanics.linear_elasticity import *
from splib.mechanics.mass import *
from splib.mechanics.fix_points import *
from splib.topology.loader import *
from splib.core.node_wrapper import *

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

    def __setattr__(self, key, value):
        if(not(key == "name")):
            print(self.__dict__["name"] + "." + key + " = " + str(value))
            self.__dict__[key] = value
        else:
            self.__dict__[key] = value


@PrefabSimulation
def createScene(rootNode):
    rootNode.dt = 0.03
    rootNode.gravity = [0,-9.81,0]

    setupLagrangianCollision(rootNode,requiredPlugins={"pluginName":['Sofa.Component.Constraint.Projective',
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
    #
    #
    # ## TODO : Being able to call "childNode.addAnything" by using the __getattr__ method
    # childNode = rootNode.addChild("simulated1")
    # loadMesh(childNode,filename="mesh/liver.msh")
    # addImplicitODE(childNode)
    # addLinearSolver(childNode,iterative=True,iterations="25", tolerance="1e-09", threshold="1e-09")
    # addDynamicTopology(childNode,type=ElementType.TETRA,source="@meshLoader")
    # childNode.addObject("MechanicalObject")
    # addLinearElasticity(childNode,ElementType.TETRA, poissonRatio="0.3", youngModulus="3000", method='large')
    # addMass(childNode,massDensity="1.0")
    # addFixation(childNode,ConstraintType.PROJECTIVE,indices="3 39 64")

    SimulatedLiver = rootNode.addSimulatedObject("Liver2",
                                                 template="Vec3d",
                                                 elemType=ElementType.TETRA,
                                                 topologyParams=TopologyParameters(filename="mesh/liver.msh"),
                                                 collisionType=CollisionType.LAGRANGIAN)

    SimulatedLiver.addConstitutiveModel(law=ConstitutiveLaw.LINEAR_COROT,
                                        lawParams=LinearConstitutiveLawParameters(poissonRatio="0.3", youngModulus="3000", method='large'),
                                         massParams=MassParameters(massDensity="1.0"))

    SimulatedLiver.addCollisionModel(collisionParameters =CollisionParameters(points=True,edges=True,triangles=True,proximity=0.2),
                                     extractSurfaceFromParent=True)

    SimulatedLiver.addVisualModel(color=[1.0,1.0,0.2],extractSurfaceFromParent=True)

    SimulatedLiver.addDirichletConditions(ConstraintType.PROJECTIVE,
                                          fixationParams=FixationParameters(boxROIs=[0, 3, 0, 2, 5, 2]))
    return rootNode



if __name__ == "__main__":
    Node = exportScene()
    createScene(Node)






