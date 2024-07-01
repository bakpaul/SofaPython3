from core.node_wrapper import BasePrefab

class SimulatedObject(BasePrefab):
    def __init__(self,node):
        self.node = node
        self.type = "SimulatedObject"

    def __getattr__(self, item):
        return getattr(self.node,item)

