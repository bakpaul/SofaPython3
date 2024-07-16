from splib.core.enum_types import *

##centers radii
class LinearSolverParameters(object):
    def __init__(self, template=None):
        self.template=template

class IterativeLinearSolverParameters(LinearSolverParameters):
    def __init__(self, iterations=None,tolerance=None,threshold=None,template=None,parallelInverseProduct=False):
        super().__init__(template=template)
        self.iterations=iterations
        self.tolerance=tolerance
        self.threshold=threshold
        self.parallelInverseProduct = parallelInverseProduct


class DirectLinearSolverParameters(LinearSolverParameters):
    def __init__(self,constantSparsity=False,template=None):
        super().__init__(template=template)
        self.constantSparsity = constantSparsity

class ConstitutiveLawParameters(object):
    def __init__(self):
        return
class HyperelasticConstitutiveLawParameters(ConstitutiveLawParameters):
    def __init__(self, materialName=None, parameterSet=None, matrixRegularization=None):
        self.materialName=materialName
        self.parameterSet=parameterSet
        self.matrixRegularization=matrixRegularization

class LinearConstitutiveLawParameters(ConstitutiveLawParameters):
    def __init__(self, youngModulus=None, poissonRatio=None, method=None):
        self.youngModulus=youngModulus
        self.poissonRatio=poissonRatio
        self.method=method

class MassParameters(object):
    def __init__(self,totalMass=None, massDensity=None):
        self.totalMass=totalMass
        self.massDensity=massDensity

class FixationParameters(object):
    def __init__(self,boxROIs=None, sphereROIs=None, indices=None, fixAll=None):
        self.boxROIs=boxROIs
        self.sphereROIs=sphereROIs
        self.indices=indices
        self.fixAll=fixAll

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


class TopologyParameters(object):
    def __init__(self,dynamic=False, source=None, filename=None, generateSparseGrid=False, sparseGridSize=[2,2,2] ):
        self.dynamic=dynamic
        self.source=source
        self.filename=filename
        self.generateSparseGrid=generateSparseGrid
        self.sparseGridSize=sparseGridSize