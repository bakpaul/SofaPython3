from typing import List, Callable, Tuple, Dict
from core.node_wrapper import BasePrefab
from core.utils import getParameterSet
from prefabs.parameters  import *
from simulation.headers import *
from simulation.ode_solvers import *
from simulation.linear_solvers import *
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
            addDynamicTopology(self.node,_source=topoSrc,**kwargs)
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
            addMass(self.node,**(massParams.__dict__),**kwargs)

        return

    def addDirichletConditions(self,
                               constraintType = ConstraintType.PROJECTIVE,
                               fixationParams=FixationParameters(),
                               **kwargs):
        addFixation(self.node,constraintType,**(fixationParams.__dict__),**kwargs)
        return

    def addVisualModel(self,_mappingType=MappingType.BARYCENTRIC,extractSurfaceFromParent=False,_filename=None):
        if(extractSurfaceFromParent and (_filename is no None)):
            print("[Warning] You have to choose between extraction and mesh loading")

        if(extractSurfaceFromParent):
            if(self.elemType == ElementType.TETRA):
                ##Add tetra2Triangles
            elif(self.elemType == ElementType.HEXA)
                ##Add Hexa2Quads
        else:
            ##USe OGL Model
        return

    def addCollisionModel(self):
        return
