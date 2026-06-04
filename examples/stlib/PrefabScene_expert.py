from stlib.geometries.plane import PlaneParameters
from stlib.geometries.file import FileParameters
from stlib.geometries.extract import ExtractParameters
from stlib.materials.deformable import DeformableBehaviorParameters
from stlib.collision import Collision, CollisionParameters
from stlib.entities import Entity, EntityParameters
from stlib.visual import Visual, VisualParameters
from stlib.node_modifiers import NodeModifier
from stlib.node_modifiers.footers import SimulationSolversParameters, SimulationSettingsParameters
from stlib.node_modifiers.attachments import FixConstraintParameters, AttachmentConstraintParameters

from splib.core.enum_types import CollisionPrimitive, ElementType, ConstitutiveLaw
from stlib.core.basePrefab import BasePrefab
from stlib.geometries import Geometry, GeometryParameters

from stlib.core.baseParameters import BaseParameters
import dataclasses

import numpy as np


@dataclasses.dataclass
class EnvironmentObjectParameters(BaseParameters):
    name : str = "Entity"

    collision : CollisionParameters = None
    visual : VisualParameters = None

class EnvironmentObject(BasePrefab):

    def __init__(self, parameters: EnvironmentObjectParameters):
        BasePrefab.__init__(self, parameters)

    def init(self):
        self.collision = self.add(Collision, parameters=self.parameters.collision)
        self.visual = self.collision.add(Visual, parameters=self.parameters.visual)


def createScene(root):
    root.gravity = [0, 0, 9.81]

    LogoParams = EntityParameters(name = "Logo",
                                  geometry = FileParameters(filename="mesh/SofaScene/Logo.vtk"),
                                  material = DeformableBehaviorParameters(),
                                  collision = CollisionParameters(),
                                  visual = VisualParameters())

    LogoParams.geometry.elementType = ElementType.TETRAHEDRA
    LogoParams.material.constitutiveLawType = ConstitutiveLaw.ELASTIC
    LogoParams.material.parameters = [200, 0.4]
    LogoParams.material.massDensity = 0.003261

    LogoParams.collision.primitives = [CollisionPrimitive.POINTS]
    LogoParams.collision.geometry = ExtractParameters(sourceElementType=ElementType.TETRAHEDRA)

    LogoParams.visual.color = [0.7, .35, 0, 0.8]
    LogoParams.visual.geometry = FileParameters(filename="mesh/SofaScene/Logo.vtk")

    Logo = root.add(Entity, parameters = LogoParams)

    PLaneEnvParams = EnvironmentObjectParameters(name = "Ground",
                                                 collision=CollisionParameters(),
                                                 visual=VisualParameters())
    ## Let's start with the environment : a ground
    PLaneEnvParams.collision.name = "Collision"
    PLaneEnvParams.collision.primitives = [CollisionPrimitive.TRIANGLES]
    PLaneEnvParams.collision.geometry = PlaneParameters(center = np.array([15,0,0]),
                                                     normal = np.array([0,0,-1]),
                                                     lengthNormal = np.array([0, 1, 0]),
                                                     lengthNbEdge = 1,
                                                     widthNbEdge = 2,
                                                     lengthSize = 30,
                                                     widthSize = 70)

    ## We can modify unexposed mparameters (advanced)
    PLaneEnvParams.collision.kwargs = {"TriangleCollision" : {"moving" : False, "simulated" : False}}

    ## Now we add it to the graph
    plane = root.add(EnvironmentObject, parameters = PLaneEnvParams)



    ## Deal with solvers + constraints / collision settings (boiling plate code, copy/pasted for nearly every one)
    ## This will add the Integration scheme and linear solvers
    root.add(NodeModifier, on = [Logo], parameters = SimulationSolversParameters())
    ## This will add the constraint solvers, constraint correction and collision pipeline and setup the button setting
    root.add(NodeModifier, on = [root], parameters = SimulationSettingsParameters(displayFlags = ["showVisualModels", "showInteractionForceFields"],
                                                                                  enableCollisionDetection = True,
                                                                                  useLagrangian = True,
                                                                                  parallelComputing = False,
                                                                                  alarmDistance=0.3, contactDistance=0.02,
                                                                                  frictionCoef=0.5, tolerance=1.0e-4, maxIterations=20))

    return root
