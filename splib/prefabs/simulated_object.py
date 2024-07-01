from core.node_wrapper import BasePrefab

class SimulatedObject(BasePrefab):
    def __init__(self,node, _template, _elemType, _filename=None,_source=None,*args,**kwargs):
        super().__init__(node,*args,**kwargs)

        self.template=_template

    def addConstitutiveModel(self):
        ##ADD selasticity
        ## ADD Mass
        return

    def addDirichletConditions(self):
        ##ADD selasticity
        ## ADD Mass
        return

    def addVisualModel(self):
        return

    def addCollisionModel(self):
        return
