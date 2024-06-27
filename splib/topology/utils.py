from core.utils import *
from functools import wraps

def BaseTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_source" in kwargs) and kwargs["_source"]:
            containerParams["src"] = kwargs["_source"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper

def PointsTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_position" in kwargs) and kwargs["_position"]:
            containerParams["position"] = kwargs["_position"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper

def EdgesTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_edges" in kwargs) and kwargs["_edges"]:
            containerParams["edges"] = kwargs["_edges"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper

def TrianglesTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_triangles" in kwargs) and kwargs["_triangles"]:
            containerParams["triangles"] = kwargs["_triangles"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper

def QuadsTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_quads" in kwargs) and kwargs["_quads"]:
            containerParams["quads"] = kwargs["_quads"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper

def TetrahedronTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_tetrahedra" in kwargs) and kwargs["_tetrahedra"]:
            containerParams["tetrahedra"] = kwargs["_tetrahedra"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper

def HexahedronTopo(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        containerParams = getParameterSet("container",kwargs)
        if ("_hexahedra" in kwargs) and kwargs["_hexahedra"]:
            containerParams["hexahedra"] = kwargs["_hexahedra"]
        kwargs["container"] = containerParams
        return method(*args,**kwargs)
    return wrapper