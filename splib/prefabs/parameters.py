from enum import Enum

class ConstitutiveLaw(Enum):
    LINEAR_COROT    = 1
    HYPERELASTIC    = 2

class ODEType(Enum):
    EXPLICIT    = 1
    IMPLICIT    = 2

class SolverType(Enum):
    DIRECT    = 1
    ITERATIVE = 2

class MappingType(Enum):
    BARYCENTRIC = 1
    IDENTITY    = 2
    RIGID       = 3

class LinearSolverParameters(object):
    def __init__(self, _template=None):
        self._template=_template

class IterativeLinearSolverParameters(LinearSolverParameters):
    def __init__(self, _iterations=None,_tolerance=None,_threshold=None,_template=None):
        self.super().__init__(_template)
        self._iterations=_iterations
        self._tolerance=_tolerance
        self._threshold=_threshold

class ConstitutiveLawParameters(object):
    def __init__(self):
        return
class HyperelasticConstitutiveLawParameters(ConstitutiveLawParameters):
    def __init__(self, _materialName=None, _parameterSet=None, _matrixRegularization=None):
        self._materialName=_materialName
        self._parameterSet=_parameterSet
        self._matrixRegularization=_matrixRegularization

class LinearConstitutiveLawParameters(ConstitutiveLawParameters):
    def __init__(self, _youngModulus=None, _poissonRatio=None, _method=None):
        self._youngModulus=_youngModulus
        self._poissonRatio=_poissonRatio
        self._method=_method

class MassParameters(object):
    def __init__(self,_totalMass=None, _massDensity=None):
        self._totalMass=_totalMass
        self._massDensity=_massDensity

class FixationParameters(object):
    def __init__(self,_boxROIs=None, _sphereROIs=None, _indices=None, _fixAll=None):
        self._boxROIs=_boxROIs
        self._sphereROIs=_sphereROIs
        self._indices=_indices
        self._fixAll=_fixAll

class CollisionParameters(object):
    def __init__(self,points=False, edges=False,triangles=False, spheres=False,tetrahedron=False,selfCollision=False, proximity=None, contactStiffness=None, contactFriction=None,spheresRadius=None):
        self.points=points
        self.edges=edges
        self.triangles=triangles
        self.spheres=spheres
        self.tetrahedron=tetrahedron
        self.selfCollision=selfCollision
        self.proximity=proximity
        self.contactStiffness=contactStiffness
        self.contactFriction=contactFriction
        self.spheresRadius=spheresRadius