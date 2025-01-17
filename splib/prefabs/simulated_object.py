from typing import List, Callable, Tuple, Dict
from splib.core.node_wrapper import BaseWrapper
from splib.core.utils import getParameterSet, isDefault
from splib.prefabs.parameters  import *
from splib.simulation.headers import *
from splib.simulation.ode_solvers import *
from splib.simulation.linear_solvers import *
from splib.mechanics.collision_model import *
from splib.mechanics.linear_elasticity import *
from splib.mechanics.mass import *
from splib.mechanics.fix_points import *
from splib.topology.loader import *
from splib.topology.dynamic import *
from splib.topology.static import *
from splib.core.enum_types import *

from applications.plugins.SofaPython3.splib.core.utils import DEFAULT_VALUE


class SimulatedObject(BaseWrapper):

    mappedTopology : Dict

    # This constructor initialize the component until the Mechanical Object.
    # Because @ReusableMethod are used, kwargs can contain dictionary which associated key word correspond to the object name
    # Here the name list you can affect is :
    # - ODESolver               (added by add_____ODE)
    # - LinearSolver            (added by addLinearSolver)
    # - meshLoader              (added by loadMesh)
    # - container               (added by addStaticTopology or addDynamicTopology)
    # - {modifier, algorithms}  (added by addDynamicTopology)
    # - mstate                  (added directly)
    def __init__(self, node,
                 template, elemType:ElementType=None,
                 ODEType=ODEType.IMPLICIT, SolverType=SolverType.DIRECT,
                 linearSolverParams=LinearSolverParameters(), collisionType=CollisionType.NONE,
                 topologyParams=TopologyParameters(),**kwargs):

        super().__init__(node)
        self.template = template
        self.elemType = elemType
        self.mappedTopology = {}


        if(ODEType == ODEType.IMPLICIT):
            addImplicitODE(self.node,static=False,**kwargs)
        else:
            addExplicitODE(self.node,**kwargs)

        if("Vec3" in self.template):
            linearSolverParams.template = "CompressedRowSparseMatrixMat3x3"
        else:
            linearSolverParams.template = "CompressedRowSparseMatrix"


        addLinearSolver(self.node,iterative=(SolverType == SolverType.ITERATIVE),**(linearSolverParams.__dict__),**kwargs)

        if(not(isDefault(topologyParams.source)) and not(isDefault(topologyParams.filename))):
            print("[Warning] you cannot have multiple sources for your topology, taking filename")

        if(not(isDefault(topologyParams.filename))):
            loadMesh(self.node,topologyParams.filename, **kwargs)
            topoSrc = "@meshLoader"
        elif(not(isDefault(topologyParams.source ))):
            topoSrc = topologyParams.source

        if(topologyParams.generateSparseGrid):
            self.node.addObject("SparseGridRamificationTopology",name="SparseGrid",position=topoSrc+".position",n=topologyParams.sparseGridSize,**kwargs)
            topoSrc = "@SparseGrid"

        if(self.elemType is not None):
            if(topologyParams.dynamic):
                addDynamicTopology(self.node,self.elemType,source=topoSrc,**kwargs)
            else:
                addStaticTopology(self.node,source=topoSrc,**kwargs)

        self.mechanicalObject = self.node.addObject("MechanicalObject",name="mstate", template=template, **kwargs)

        if(collisionType == CollisionType.LAGRANGIAN):
            self.mechanicalObject = self.node.addObject("LinearSolverConstraintCorrection",name="constraintCorrection", **kwargs)




    def addConstitutiveModel(self,
                             law:ConstitutiveLaw=None,
                             lawParams=ConstitutiveLawParameters(),
                             massParams=MassParameters(),
                             **kwargs):
        ##ADD selasticity
        ## ADD Mass
        if(law==ConstitutiveLaw.LINEAR_COROT):
            addLinearElasticity(self.node,self.elemType,**(lawParams.__dict__),**kwargs)
        elif(law is not None):
            addHyperelasticity(self.node,self.elemType,**(lawParams.__dict__),**kwargs)

        if(not(massParams.__dict__ == {})):
            addMass(self.node,self.template,**(massParams.__dict__),**kwargs)

        return

    def addDirichletConditions(self,
                               constraintType = ConstraintType.PROJECTIVE,
                               fixationParams=FixationParameters(),
                               **kwargs):
        addFixation(self.node,constraintType,**(fixationParams.__dict__),**kwargs)
        return


    @staticmethod
    def _addMappedSurface(node,parentElemType:ElementType,extractSurfaceFromParent=False,filename=None,source=None,elemInFile:ElementType=None,**kwargs):
        if(filename is not None):
            loadMesh(node,filename, **kwargs)
            if(elemInFile is None):
                print("[Warning] You have to specify the surfacic element type when loading a surface from a file. The surface topology will be set to static.")
                addStaticTopology(node,source="@meshLoader",**kwargs)
            else:
                addDynamicTopology(node,elemInFile,source="@meshLoader",**kwargs)
        elif(source is not None):
            if(elemInFile is None):
                print("[Warning] You have to specify the surfacic element type when loading a surface from a file. The surface topology will be set to static.")
                addStaticTopology(node,source=source,**kwargs)
            else:
                addDynamicTopology(node,elemInFile,source=source,**kwargs)
        elif(extractSurfaceFromParent):
            if(parentElemType == ElementType.TETRA):
                addDynamicTopology(node,ElementType.TRIANGLES,**kwargs)
                node.addObject("Tetra2TriangleTopologicalMapping", name="TopologicalMapping",  input="@../container", output="@container",**kwargs)
                return
            elif(parentElemType == ElementType.HEXA):
                addDynamicTopology(node,ElementType.QUAD,**kwargs)
                node.addObject("Hexa2QuadTopologicalMapping", name="TopologicalMapping",  input="@../container", output="@container",**kwargs)
                return


    # @MapKeywordArg("OglModel",["color","color"])
    def addVisualModel(self,color=DEFAULT_VALUE,extractSurfaceFromParent=False,filename=None,source=None,elemTypeInFile:ElementType=None,**kwargs):
        if(    (extractSurfaceFromParent and (filename is not None))
            or (extractSurfaceFromParent and (source is not None))
            or ((filename is not None) and (source is not None))):
            print("[Warning] You have to choose between extraction, source or mesh loading")
            if(filename is not None):
                source = None
            extractSurfaceFromParent = False
        elif(not(extractSurfaceFromParent) and (filename is None) and (source is None)):
            print("[Error] You should specify either a surface extraction, a source or a filename, the surface will be extracted by default. ")
            extractSurfaceFromParent = True

        self.visualModel = self.node.addChild("VisualModel")
        SimulatedObject._addMappedSurface( self.visualModel,self.elemType,extractSurfaceFromParent=extractSurfaceFromParent,filename=filename, source=source,elemInFile=elemTypeInFile,**kwargs)
        self.visualModel.addObject("OglModel", name="OglModel", color=color,  topology="@container",**kwargs)

        if((filename is not None) or (source is not None)):
            if(self.template == "Rigid3"):
                self.visualModel.addObject("RigidMapping",name="Mapping",isMechanical=False,globalToLocalCoords=True,**kwargs)
            else:
                self.visualModel.addObject("BarycentricMapping",name="Mapping",isMechanical=False,**kwargs)
        elif(extractSurfaceFromParent):
            self.visualModel.addObject("IdentityMapping",name="Mapping",isMechanical=False,**kwargs)
        return self.visualModel

    def addCollisionModel(self,collisionParameters:CollisionParameters,extractSurfaceFromParent=False,filename=None,source=None,elemTypeInFile:ElementType=None,**kwargs):
        if(    (extractSurfaceFromParent and (filename is not None))
                or (extractSurfaceFromParent and (source is not None))
                or ((filename is not None) and (source is not None))):
            print("[Warning] You have to choose between extraction, source or mesh loading.")
            if(filename is not None):
                source = None
            extractSurfaceFromParent = False
        elif(not(extractSurfaceFromParent) and (filename is None) and (source is None)):
            print("[Error] You should specify either a surface extraction, a source or a filename, the surface will be extracted by default. ")
            extractSurfaceFromParent = True

        self.collisionModel = self.node.addChild("CollisionModel")
        SimulatedObject._addMappedSurface( self.collisionModel,self.elemType,extractSurfaceFromParent=extractSurfaceFromParent,filename=filename,source=source,elemInFile=elemTypeInFile,**kwargs)
        if(extractSurfaceFromParent):
            self.collisionModel.addObject("MechanicalObject",name="mstate",rest_position="@../mstate.rest_position")
        else:
            self.collisionModel.addObject("MechanicalObject",name="mstate",src="@container")


        addCollisionModels( self.collisionModel,**(collisionParameters.__dict__),**kwargs)


        if((filename is not None) or (source is not None)):
            if(self.template == "Rigid3"):
                self.collisionModel.addObject("RigidMapping",name="Mapping",isMechanical=True,globalToLocalCoords=True,**kwargs)
            else:
                self.collisionModel.addObject("BarycentricMapping",name="Mapping",isMechanical=True,**kwargs)
        elif(extractSurfaceFromParent):
            self.collisionModel.addObject("IdentityMapping",name="Mapping",isMechanical=True,**kwargs)
        return self.collisionModel

    def addMappedTopology(self, name, template, elemType:ElementType,dynamicTopo=False,isMechanical=False,**kwargs):
        if(name in self.mappedTopology):
            print("[ERROR] A mapped node with the name " + name + " already exist.")
            return

        self.mappedTopology[name] = self.node.addChild(name)


        if(dynamicTopo):
            addDynamicTopology(self.mappedTopology[name],elemType,**kwargs)
        else:
            addStaticTopology(self.mappedTopology[name],**kwargs)

        self.mappedTopology[name].addObject("MechanicalObject",name="mstate", template=template, **kwargs)


        if(self.template == "Rigid3"):
            self.mappedTopology[name].addObject("RigidMapping",name="Mapping",isMechanical=isMechanical,globalToLocalCoords=True,**kwargs)
        else:
            self.mappedTopology[name].addObject("BarycentricMapping",name="Mapping",isMechanical=isMechanical,**kwargs)

        return self.mappedTopology[name]