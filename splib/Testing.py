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

from splib.core.node_wrapper import ChildWrapper, ObjectWrapper


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
        setattr(self,name,exportScene(name))
        return getattr(self,name)

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
    Liver0=rootNode.addChild("Liver0")
    Liver0.addObject("EulerImplicitSolver",name="ODESolver",rayleighStiffness="0",rayleighMass="0")
    Liver0.addObject("SparseLDLSolver",name="LinearSolver",template="CompressedRowSparseMatrixMat3x3",parallelInverseProduct="False")
    Liver0.addObject("MeshGmshLoader",name="meshLoader",filename="mesh/liver.msh")
    Liver0.addObject("TetrahedronSetTopologyModifier",name="modifier")
    Liver0.addObject("TetrahedronSetTopologyContainer",name="container",src="@meshLoader")
    Liver0.addObject("TetrahedronSetGeometryAlgorithms",name="algorithms")
    Liver0.addObject("MechanicalObject",name="mstate",template="Vec3d")
    Liver0.addObject("LinearSolverConstraintCorrection",name="constraintCorrection")
    Liver0.addObject("TetrahedronFEMForceField",name="constitutiveLaw",youngModulus="3000",poissonRatio="0.3",method="large")
    Liver0.addObject("MeshMatrixMass",name="mass",massDensity="1")
    Liver0.addObject("BoxROI",name="fixedBoxROI",box="0 3 0 2 5 2")
    Liver0.addObject("FixedProjectiveConstraint",name="fixedConstraints",indices="@fixedBoxROI.indices")
    Visu=Liver0.addChild("Visu")
    Visu.addObject("TriangleSetTopologyModifier",name="modifier")
    Visu.addObject("TriangleSetTopologyContainer",name="container")
    Visu.addObject("TriangleSetGeometryAlgorithms",name="algorithms")
    Visu.addObject("Tetra2TriangleTopologicalMapping",name="TopologicalMapping",input="@../container",output="@container")
    Visu.addObject("OglModel",name="OglModel",topology="@container",color="[1.0, 0.2, 0.8]")
    Visu.addObject("IdentityMapping",name="Mapping",isMechanical="False")


    SimulatedLiver1 = rootNode.addChild("Liver1")
    addImplicitODE(SimulatedLiver1)
    addLinearSolver(SimulatedLiver1,iterative=False, template="CompressedRowSparseMatrixMat3x3")
    loadMesh(SimulatedLiver1,filename="mesh/liver.msh")
    addDynamicTopology(SimulatedLiver1,type=ElementType.TETRA,source="@meshLoader")
    SimulatedLiver1.addObject("MechanicalObject",name="mstate", template='Vec3d')
    SimulatedLiver1.addObject("LinearSolverConstraintCorrection",name="constraintCorrection")
    addLinearElasticity(SimulatedLiver1,ElementType.TETRA, poissonRatio="0.3", youngModulus="3000", method='large')
    addMass(SimulatedLiver1,template='Vec3d',massDensity="2")
    addFixation(SimulatedLiver1,ConstraintType.PROJECTIVE,boxROIs=[0, 3, 0, 2, 5, 2])

    SimulatedLiverVisu = SimulatedLiver1.addChild("Visu")
    addDynamicTopology(SimulatedLiverVisu,ElementType.TRIANGLES)
    SimulatedLiverVisu.addObject("Tetra2TriangleTopologicalMapping", name="TopologicalMapping",  input="@../container", output="@container")
    SimulatedLiverVisu.addObject("OglModel", name="OglModel",  topology="@container",color=[1.0,0.2,0.8])
    SimulatedLiverVisu.addObject("IdentityMapping",name="Mapping",isMechanical=False)




    SimulatedLiver2 = rootNode.addSimulatedObject("Liver2",
                                                 template="Vec3d",
                                                 elemType=ElementType.TETRA,
                                                 topologyParams=TopologyParameters(filename="mesh/liver.msh"),
                                                 collisionType=CollisionType.LAGRANGIAN)

    SimulatedLiver2.addConstitutiveModel(law=ConstitutiveLaw.LINEAR_COROT,
                                         lawParams=LinearConstitutiveLawParameters(poissonRatio="0.3", youngModulus="3000", method='large'),
                                         massParams=MassParameters(massDensity="3"))

    SimulatedLiver2.addCollisionModel(name="Collision",collisionParameters =CollisionParameters(points=True,edges=True,triangles=True,proximity=0.2),
                                     extractSurfaceFromParent=True)

    SimulatedLiver2.addVisualModel(color=[1.0,1.0,0.2],extractSurfaceFromParent=True)

    SimulatedLiver2.addDirichletConditions(ConstraintType.PROJECTIVE,
                                          fixationParams=FixationParameters(boxROIs=[0, 3, 0, 2, 5, 2]))
    return rootNode



if __name__ == "__main__":
    Node = exportScene()
    createScene(Node)






