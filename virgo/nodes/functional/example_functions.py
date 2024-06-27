from virgo.nodes.base_nodes import FunctionalNode
from virgo.graph import Input, Output

class DoNothing(FunctionalNode):
    description = "This node does nothing"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "a"),
            Input(self, any, "b")
        ],
        outs = [
            Output(self, any, "c"),
            Output(self, any, "d")
        ],
        )
    
    def function(self, in1, in2):
        return in1, in2