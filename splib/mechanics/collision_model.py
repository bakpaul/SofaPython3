from core.node_wrapper import *
from core.utils import *
from topology.dynamic import ElementType



@PrefabMethod
@MapKeywordArg("PointCollision",["selfCollision","selfCollision"],["proximity","proximity"],["contactStiffness","contactStiffness"],["contactFriction","contactFriction"])
@MapKeywordArg("EdgeCollision",["selfCollision","selfCollision"],["proximity","proximity"],["contactStiffness","contactStiffness"],["contactFriction","contactFriction"])
@MapKeywordArg("TriangleCollision",["selfCollision","selfCollision"],["proximity","proximity"],["contactStiffness","contactStiffness"],["contactFriction","contactFriction"])
@MapKeywordArg("TetraCollision",["selfCollision","selfCollision"],["proximity","proximity"],["contactStiffness","contactStiffness"],["contactFriction","contactFriction"])
@MapKeywordArg("SphereCollision",["selfCollision","selfCollision"],["proximity","proximity"],["contactStiffness","contactStiffness"],["contactFriction","contactFriction"],["spheresRadius","listRadius"])
def addCollisionModels(node,points=False, edges=False,triangles=False, spheres=False,tetrahedron=False,selfCollision=None, proximity=None, contactStiffness=None, contactFriction=None,spheresRadius=None,**kwargs):
    if(points):
        node.addObject("PointCollisionModel",name="PointCollision",**kwargs)
    if(edges):
        node.addObject("LineCollisionModel",name="EdgeCollision",**kwargs)
    if(triangles):
        node.addObject("TriangleCollisionModel",name="TriangleCollision",**kwargs)
    if(spheres):
        node.addObject("SphereCollisionModel",name="TetraCollision",**kwargs)
    if(tetrahedron):
        node.addObject("TetrahedronCollisionModel",name="SphereCollision",**kwargs)
