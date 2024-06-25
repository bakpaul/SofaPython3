def _getContainerParamsSet(**kwargs):
    containerParams = dict
    if "container" in kwargs:
        if isinstance(kwargs["container"], dict):
            containerParams = kwargs["container"]
    return containerParams

def BaseTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_source"]:
            containerParams["src"] = kwargs["_source"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)

def PointsTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_position"]:
            containerParams["position"] = kwargs["_position"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)
    return wrapper()

def EdgesTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_edges"]:
            containerParams["edges"] = kwargs["_edges"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)
    return wrapper()

def TrianglesTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_triangles"]:
            containerParams["triangles"] = kwargs["_triangles"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)
    return wrapper()

def QuadsTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_quads"]:
            containerParams["quads"] = kwargs["_quads"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)
    return wrapper()

def TetrahedronTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_tetrahedra"]:
            containerParams["tetrahedra"] = kwargs["_tetrahedra"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)
    return wrapper()

def HexahedronTopo(method):
    def wrapper(*args, **kwargs):
        containerParams = _getContainerParamsSet(**kwargs)
        if kwargs["_hexahedra"]:
            containerParams["hexahedra"] = kwargs["_hexahedra"]
        kwargs["container"] = containerParams
        method(*args,**kwargs)
    return wrapper()