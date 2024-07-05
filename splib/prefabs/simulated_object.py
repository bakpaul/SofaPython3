from typing import List, Callable, Tuple, Dict
from core.node_wrapper import BasePrefab
from core.utils import getParameterSet
from prefabs.parameters  import *
from simulation.headers import *
from simulation.ode_solvers import *
from simulation.linear_solvers import *
from simulation.collision_model import *
from mechanics.linear_elasticity import *
from mechanics.mass import *
from mechanics.fix_points import *
from topology.loader import *
from topology.dynamic import *
from topology.static import *

class SimulatedObject(BasePrefab):

    # This constructor initialize the component until the Mechanical Object.
    # Because @PrefabMethod are used, kwargs can contain dictionary which associated key word correspond to the object name
    # Here the name list you can affect is :
    # - ODESolver               (added by add_____ODE)
    # - LinearSolver            (added by addLinearSolver)
    # - meshLoader              (added by loadMesh)
    # - container               (added by addStaticTopology or addDynamicTopology)
    # - {modifier, algorithms}  (added by addDynamicTopology)
    # - mstate                  (added directly)
    def __init__(self, node,
                 _template, _elemType:ElementType,
                 _ODEType=ODEType.IMPLICIT, _SolverType=SolverType.DIRECT, _dynamicTopo=False,
                 _linearSolverParams=LinearSolverParameters(),
                 _filename=None, _source=None,
                 *args,**kwargs):

        super().__init__(node,*args,**kwargs)
        self.template = _template
        self.elemType = _elemType


        if(_ODEType == ODEType.IMPLICIT):
            addImplicitODE(self.node,_static=False,**kwargs)
        else:
            addExplicitODE(self.node,**kwargs)


        addLinearSolver(self.node,_iterative=(_SolverType == SolverType.ITERATIVE),**(_linearSolverParams.__dict__),**kwargs)

        if((_source is not None) and (_filename is not None)):
            print("[Warning] you cannot have multiple sources for your topology, taking filename")

        if(_filename is not None):
            loadMesh(self.node,_filename, **kwargs)
            topoSrc = "@meshLoader"
        elif(_source is not None):
            topoSrc = _source

        if(_dynamicTopo):
            addDynamicTopology(self.node,self.elemType,_source=topoSrc,**kwargs)
        else:
            addStaticTopology(self.node,_source=topoSrc,**kwargs)

        mstateParams = getParameterSet("mstate",kwargs)
        self.mechanicalObject = self.node.addObject("MechanicalObject",name="mstate", template=_template, **mstateParams)



    def addConstitutiveModel(self,
                             law:ConstitutiveLaw=None,
                             lawParams=ConstitutiveLawParameters(),
                             massParams=MassParameters(),
                             **kwargs):
        ##ADD selasticity
        ## ADD Mass
        if(law==ConstitutiveLaw.LINEAR_COROT):
            addLinearElasticity(self.node,self.elemType,**(lawParams.__dict__),**kwargs)
        else:
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
    def _addMappedSurface(node,parentElemType:ElementType,extractSurfaceFromParent=False,_filename=None,_visualElemInFile:ElementType=None,**kwargs):
        if(_filename is not None):
            loadMesh(node,_filename, **kwargs)
            if(_visualElemInFile is None):
                print("[Warning] You have to specify the surfacic element type when loading a surface from a file. The surface topology will be set to static.")
                addStaticTopology(node,_source="@meshLoader",**kwargs)
            else:
                addDynamicTopology(node,_visualElemInFile,_source="@meshLoader",**kwargs)
        elif(extractSurfaceFromParent):
            if(parentElemType == ElementType.TETRA):
                node.addObject("Tetra2TriangleTopologicalMapping", name="TopologicalMapping",  input="@../container", output="@container",**kwargs)
                return
            elif(parentElemType == ElementType.HEXA):
                node.addObject("Hexa2QuadTopologicalMapping", name="TopologicalMapping",  input="@../container", output="@container",**kwargs)
                return


    def addVisualModel(self,extractSurfaceFromParent=False,_filename=None,_elemTypeInFile:ElementType=None,**kwargs):
        if(extractSurfaceFromParent and (_filename is not None)):
            print("[Warning] You have to choose between extraction and mesh loading")
        elif(not(extractSurfaceFromParent) and (_filename is None)):
            print("[Error] You should specify either a surface extraction of a filename, the surface will be extracted by default. ")
            extractSurfaceFromParent = True

        self.visualModel = self.addchild("VisualModel")
        SimulatedObject._addMappedSurface( self.visualModel,self.elemType,extractSurfaceFromParent=extractSurfaceFromParent,_filename=_filename,_visualElemInFile=_elemTypeInFile,**kwargs)
        self.visualModel.addObject("OglModel", name="OglModel",  topology="@container")

        if(_filename is not None):
            if(self.template == "Rigid3"):
                self.visualModel.addObject("RigidMapping",name="Mapping",isMechanical=False,globalToLocalCoords=True,**kwargs)
            else:
                self.visualModel.addObject("BarycentricMapping",name="Mapping",isMechanical=False,**kwargs)
        elif(extractSurfaceFromParent):
            self.visualModel.addObject("IdentityMapping",name="Mapping",isMechanical=False,**kwargs)
        return

    def addCollisionModel(self,collisionParameters:CollisionParameters,extractSurfaceFromParent=False,_filename=None,_elemTypeInFile:ElementType=None,**kwargs):
        if(extractSurfaceFromParent and (_filename is not None)):
            print("[Warning] You have to choose between extraction and mesh loading")
        elif(not(extractSurfaceFromParent) and (_filename is None)):
            print("[Error] You should specify either a surface extraction of a filename, the surface will be extracted by default. ")
            extractSurfaceFromParent = True

        self.collisionModel = self.addchild("CollisionModel")
        SimulatedObject._addMappedSurface( self.collisionModel,self.elemType,extractSurfaceFromParent=extractSurfaceFromParent,_filename=_filename,_visualElemInFile=_elemTypeInFile,**kwargs)
        addCollisionModels( self.collisionModel,**(collisionParameters.__dict__),**kwargs)


        if(_filename is not None):
            if(self.template == "Rigid3"):
                self.collisionModel.addObject("RigidMapping",name="Mapping",isMechanical=True,globalToLocalCoords=True,**kwargs)
            else:
                self.collisionModel.addObject("BarycentricMapping",name="Mapping",isMechanical=True,**kwargs)
        elif(extractSurfaceFromParent):
            self.collisionModel.addObject("IdentityMapping",name="Mapping",isMechanical=True,**kwargs)
        return
