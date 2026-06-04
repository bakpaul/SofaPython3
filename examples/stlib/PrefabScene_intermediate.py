from scipy._lib.pyprima.cobyla import geometry

from stlib.geometries.plane import PlaneParameters
from stlib.geometries.file import FileParameters
from stlib.geometries.extract import ExtractParameters
from stlib.materials.deformable import DeformableBehaviorParameters
from stlib.collision import Collision, CollisionParameters
from stlib.entities import Entity, EntityParameters
from stlib.visual import VisualParameters
from stlib.node_modifiers import NodeModifier
from stlib.node_modifiers.footers import SimulationSolversParameters, SimulationSettingsParameters
from stlib.node_modifiers.attachments import FixConstraintParameters, AttachmentConstraintParameters

from splib.core.enum_types import CollisionPrimitive, ElementType, ConstitutiveLaw

def createScene(root):
    root.gravity = [0, 0, -9.81]

    LogoParams = EntityParameters(name = "Logo",
                                  geometry = FileParameters(filename="mesh/SofaScene/Logo.vtk"),
                                  material = DeformableBehaviorParameters(),
                                  visual = VisualParameters())

    LogoParams.geometry.elementType = ElementType.TETRAHEDRA
    LogoParams.material.constitutiveLawType = ConstitutiveLaw.ELASTIC
    LogoParams.material.parameters = [200, 0.4]
    LogoParams.material.massDensity = 0.003261
    LogoParams.visual.color = [0.7, .35, 0, 0.8]
    LogoParams.visual.geometry = FileParameters(filename="mesh/SofaScene/LogoVisu.obj")

    Logo = root.add(Entity, parameters = LogoParams)

    ## Fix a subpart of the logo
    Logo.add(NodeModifier, on = [Logo], parameters = FixConstraintParameters( boxROIs=[[-1, -2, -13, 3, 2, -7]]))

    ## Deal with solvers + constraints / collision settings (boiling plate code, copy/pasted for nearly every one)
    ## This will add the Integration scheme and linear solvers
    root.add(NodeModifier, on = [root], parameters = SimulationSolversParameters())
    ## This will add the constraint solvers, constraint correction and collision pipeline and setup the button setting
    root.add(NodeModifier, on = [root], parameters = SimulationSettingsParameters(displayFlags=["showVisualModels"]))

    return root
