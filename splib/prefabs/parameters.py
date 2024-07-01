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

class LinearSolverParams(object):
    def __init__(self, _template=None):
        self._template=_template

class IterativeLinearSolverParams(LinearSolverParams):
    def __init__(self, _iterations=None,_tolerance=None,_threshold=None,_template=None):
        self.super().__init__(_template)
        self._iterations=_iterations
        self._tolerance=_tolerance
        self._threshold=_threshold

class ConstitutiveLawParams(object):
    def __init__(self):
        return
class LinearConstitutiveLawParams(ConstitutiveLawParams):
    def __init__(self, _materialName=None, _parameterSet=None, _matrixRegularization=None):
        self._materialName=_materialName
        self._parameterSet=_parameterSet
        self._matrixRegularization=_matrixRegularization

class HyperelasticConstitutiveLawParams(ConstitutiveLawParams):
    def __init__(self, _youngModulus=None, _poissonRatio=None, _method=None):
        self._youngModulus=_youngModulus
        self._poissonRatio=_poissonRatio
        self._method=_method

class MassParams(object):
    def __init__(self,_totalMass=None, _massDensity=None):
        self._totalMass=_totalMass
        self._massDensity=_massDensity

