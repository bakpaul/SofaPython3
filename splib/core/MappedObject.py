
def addMappedObject(node,_mapping="BarycentricMapping",_template="Vec3"):
    node.addObject("MechanicalObject", name='mstate',template=_template)
    node.addObject("BarycentricMapping")
    return node
