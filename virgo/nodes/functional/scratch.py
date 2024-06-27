from virgo.nodes.base_nodes import FunctionalNode
from virgo.graph import Input, Output

class Scratch(FunctionalNode):
    description = "Scratch Function"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "a"),
        ],
        outs = [
            Output(self, any, "c"),
            Output(self, any, "d")
        ],
        )
    
    def function(self, in1):
        return (in1, in1)