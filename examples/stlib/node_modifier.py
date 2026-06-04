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

import numpy as np


def createScene(root):
    root.gravity=[0,0,9.81]
    root.dt=0.01

    ## Let's start with the environment : a ground
    plane1_collisionParams = CollisionParameters()
    plane1_collisionParams.name = "UP"
    plane1_collisionParams.primitives = [CollisionPrimitive.TRIANGLES]
    plane1_collisionParams.geometry = PlaneParameters(center = np.array([15,0,5]),
                                                      normal = np.array([0,0,-1]),
                                                      lengthNormal = np.array([0, 1, 0]),
                                                      lengthNbEdge = 1,
                                                      widthNbEdge = 2,
                                                      lengthSize = 30,
                                                      widthSize = 70)

    ## We can modify unexposed mparameters (advanced)
    plane1_collisionParams.kwargs = {"TriangleCollision" : {"moving" : False, "simulated" : False}}

    ## Now we add it to the graph
    plane1 = root.add(Collision, parameters = plane1_collisionParams)

    ## We can still modify it afterward, in the end it is a node like any other one
    plane1_visu = plane1.addChild("Visu")
    plane1_visu.addObject("OglModel", name="VisualModel", src="@../Geometry/container")


    ### Logo
    ModelsNode = root.addChild("ModelsNode")

    LogoParams = EntityParameters(name = "Logo1",
                                  geometry = FileParameters(filename="mesh/SofaScene/Logo.vtk"),
                                  material = DeformableBehaviorParameters(),
                                  visual = VisualParameters())

    LogoParams.geometry.elementType = ElementType.TETRAHEDRA
    LogoParams.material.constitutiveLawType = ConstitutiveLaw.ELASTIC
    LogoParams.material.parameters = [200, 0.4]
    LogoParams.material.massDensity = 0.003261
    LogoParams.visual.color = [0.7, .35, 0, 0.8]
    LogoParams.visual.geometry = FileParameters(filename="mesh/SofaScene/LogoVisu.obj")

    Logo = ModelsNode.add(Entity, parameters = LogoParams)

    ## Fix a subpart of the logo
    Logo.add(NodeModifier, on = [Logo], parameters = FixConstraintParameters( boxROIs=[[-1, -2, -13, 3, 2, -7]]))


    ### Letter S
    # Topology comes from a file
    # It is supposed to be a deformable body
    # It will support collision
    # It will integrate a visualization model
    SParams = EntityParameters( name = "S",
                                geometry = FileParameters(filename="mesh/SofaScene/S.vtk"),
                                material = DeformableBehaviorParameters(),
                                collision = CollisionParameters(),
                                visual = VisualParameters())

    # We are looking for tetrahedra in the file
    SParams.geometry.elementType = ElementType.TETRAHEDRA

    # Specify material laws (elements are taken from the geometry)
    SParams.material.constitutiveLawType = ConstitutiveLaw.ELASTIC
    SParams.material.parameters = [200, 0.45]
    SParams.material.massDensity = 0.011021

    # Specify Collision primitives + how to get them, here we extract them from the volumetric mesh
    SParams.collision.primitives = [CollisionPrimitive.TRIANGLES]
    SParams.collision.geometry = ExtractParameters(sourceElementType=ElementType.TETRAHEDRA)

    # Setup the visualization part
    SParams.visual.color = [0.7, .7, 0.7, 0.8]
    SParams.visual.geometry = FileParameters(filename="mesh/SofaScene/SVisu.obj")

    ## 10 lines to add a tetrahedron-based soft body using rorrotationnal linar material + extracted collision model + visual
    S = ModelsNode.add(Entity, parameters = SParams)


    ## Let's attach the towo models with springs
    ModelsNode.add(NodeModifier, on = [S, Logo], parameters = AttachmentConstraintParameters(name = "AttachmentConstraintParameters",
                                                                                             indices1=[26,20,119,121], indices2=[722,732,574,573],
                                                                                             stiffness=0.5, damping=0.0, length=[1.075]))


    ## Deal with solvers + constraints / collision settings (boiling plate code, copy/pasted for nearly every one)
    ## This will add the Integration scheme and linear solvers
    root.add(NodeModifier, on = [ModelsNode], parameters = SimulationSolversParameters(constantSparsity=False))

    ## This will add the constraint solvers, constraint correction and collision pipeline and setup the button setting
    root.add(NodeModifier, on = [root], parameters = SimulationSettingsParameters(displayFlags = ["showVisualModels", "showInteractionForceFields"],
                                                                                  enableCollisionDetection = True,
                                                                                  useLagrangian = True,
                                                                                  parallelComputing = False,
                                                                                  alarmDistance=0.3, contactDistance=0.02,
                                                                                  frictionCoef=0.5, tolerance=1.0e-4, maxIterations=20))

