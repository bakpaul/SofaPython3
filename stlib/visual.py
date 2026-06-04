from stlib.core.basePrefab import BasePrefab
from stlib.core.baseParameters import BaseParameters, Optional, dataclasses
from stlib.geometries import Geometry, GeometryParameters
from stlib.geometries.file import FileParameters
from splib.core.utils import DEFAULT_VALUE
from Sofa.Core import Object 

@dataclasses.dataclass
class VisualParameters(BaseParameters):
    name : str = "Visual"

    color : Optional[list[float]] = DEFAULT_VALUE
    texture :  Optional[str] = DEFAULT_VALUE

    geometry : Optional[GeometryParameters] = None


class Visual(BasePrefab):

    def __init__(self, parameters: VisualParameters):
        BasePrefab.__init__(self, parameters)

    def init(self):
        if (self.parameters.geometry is not None):
            self.geometry = self.add(Geometry, parameters=self.parameters.geometry)
            src_geom = self.geometry.container.linkpath
        else:
            src_geom = "@../Geometry/container"
        self.addObject("OglModel", color=self.parameters.color, src=src_geom)


    @staticmethod
    def getParameters(**kwargs) -> VisualParameters:
        return VisualParameters(**kwargs)


def createScene(root):

    # Create a visual from a mesh file
    parameters = Visual.getParameters() 
    parameters.name = "LiverVisual"
    parameters.geometry = FileParameters(filename="mesh/liver.obj")
    root.add(Visual, parameters)