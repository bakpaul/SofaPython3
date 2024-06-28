from core.node_wrapper import PrefabMethod

@PrefabMethod
def loadMesh(node,_filename,**kwargs):
    splitedName = _filename.split('.')
    if len(splitedName) == 1:
        print('[Error] : A file name without extension was provided.')
        return

    if splitedName[-1] in ['vtk','obj','stl','msh']:
        if splitedName[-1] == "msh":
            return node.addObject("MeshGmshLoader", name="meshLoader",filename=_filename, **kwargs)
        else:
            return node.addObject("Mesh"+splitedName[-1].upper()+"Loader", name="meshLoader",filename=_filename, **kwargs)
    else:
        print('[Error] : File extension ' + splitedName[-1] + ' not recognised.')




