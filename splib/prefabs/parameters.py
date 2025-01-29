from splib.core.enum_types import *
from splib.core.utils import DEFAULT_VALUE

##centers radii
class LinearSolverParameters(object):
    def __init__(self, template=DEFAULT_VALUE,parallelInverseProduct=False):
        self.template=template
        self.parallelInverseProduct = parallelInverseProduct

class IterativeLinearSolverParameters(LinearSolverParameters):
    def __init__(self, iterations=DEFAULT_VALUE,tolerance=DEFAULT_VALUE,threshold=DEFAULT_VALUE,**kwargs):
        super().__init__(**kwargs)
        self.iterations=iterations
        self.tolerance=tolerance
        self.threshold=threshold


class DirectLinearSolverParameters(LinearSolverParameters):
    def __init__(self,constantSparsity=DEFAULT_VALUE,**kwargs):
        super().__init__(**kwargs)
        self.constantSparsity = constantSparsity

class ConstitutiveLawParameters(object):
    def __init__(self):
        return
class HyperelasticConstitutiveLawParameters(ConstitutiveLawParameters):
    def __init__(self, materialName=DEFAULT_VALUE, parameterSet=DEFAULT_VALUE, matrixRegularization=DEFAULT_VALUE):
        self.materialName=materialName
        self.parameterSet=parameterSet
        self.matrixRegularization=matrixRegularization

class LinearConstitutiveLawParameters(ConstitutiveLawParameters):
    def __init__(self, youngModulus=DEFAULT_VALUE, poissonRatio=DEFAULT_VALUE, method=DEFAULT_VALUE):
        self.youngModulus=youngModulus
        self.poissonRatio=poissonRatio
        self.method=method

class MassParameters(object):
    def __init__(self,totalMass=DEFAULT_VALUE, massDensity=DEFAULT_VALUE):
        self.totalMass=totalMass
        self.massDensity=massDensity

class FixationParameters(object):
    def __init__(self,boxROIs=DEFAULT_VALUE, sphereROIs=DEFAULT_VALUE, indices=DEFAULT_VALUE, fixAll=DEFAULT_VALUE):
        self.boxROIs=boxROIs
        self.sphereROIs=sphereROIs
        self.indices=indices
        self.fixAll=fixAll

class CollisionParameters(object):
    def __init__(self,points=False, edges=False,triangles=False, spheres=False,tetrahedron=False,selfCollision=False, proximity=DEFAULT_VALUE, group=DEFAULT_VALUE, contactStiffness=DEFAULT_VALUE, contactFriction=DEFAULT_VALUE,spheresRadius=DEFAULT_VALUE):
        self.points=points
        self.edges=edges
        self.triangles=triangles
        self.spheres=spheres
        self.tetrahedron=tetrahedron
        self.selfCollision=selfCollision
        self.proximity=proximity
        self.group=group
        self.contactStiffness=contactStiffness
        self.contactFriction=contactFriction
        self.spheresRadius=spheresRadius


class TopologyParameters(object):
    def __init__(self,dynamic=False, source=DEFAULT_VALUE, filename=DEFAULT_VALUE, generateSparseGrid=False, sparseGridSize=[2,2,2] ):
        self.dynamic=dynamic
        self.source=source
        self.filename=filename
        self.generateSparseGrid=generateSparseGrid
        self.sparseGridSize=sparseGridSize