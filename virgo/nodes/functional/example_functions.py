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

class ScaleBy100(FunctionalNode):
    description = "Scale input by 10^2"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "data"),
        ],
        outs = [
            Output(self, any, "data scaled by 100"),
        ],
        )
    
    def function(self, data):
        #Copy variable and then assign new attributes
        new_values=data*100
        new_data = data.copy(data=new_values)
        new_data.attrs |= {
            "units":data.attrs.units+"* 10^2"
        }
        return (new_data,)
    

class Transpose(FunctionalNode):
    description = "Transpose array"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                       ins = [
                           Input(self, any, "axb array")
                       ],
                       outs = [
                           Output(self, any, "bxa array")
                       ],
                       )
        
    def function(self, arr):
        newArr = arr.transpose()
        print("transposed:", arr.shape, newArr.shape)
        return (newArr,)
