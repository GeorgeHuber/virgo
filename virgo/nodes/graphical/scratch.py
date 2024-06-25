from virgo.nodes.base_nodes import GraphNode
from virgo.graph import Input

class Scratch(GraphNode):
    description = "Scratch Pad"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "axis1"),
            Input(self, any, "axis2"),
            Input(self, any, "axis3")
        ])