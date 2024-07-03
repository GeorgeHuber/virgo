from virgo.nodes.base_nodes import FunctionalNode
from virgo.graph import Input, Output

import numpy as np
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
    
class hPa_to_Km(FunctionalNode):
    description = "Convert from hPa to km"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "lev - Hpa"),
        ],
        outs = [
            Output(self, any, "altitude - km"),
        ],
        )
    
    def function(self, lev):
        #Copy variable and then assign new attributes
        alt_values=7.*np.log(1000./lev)
        alt = lev.copy(data=alt_values)
        alt["name"] = "alt"
        alt.attrs["long_name"] = "Altitude"
        return (alt,)
    
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
        #maintain attributes
        newArr.attrs = arr.attrs
        print("transposed:", arr.shape, newArr.shape)
        return (newArr,)
    
class scaleBy100(FunctionalNode):
    description = "Convert from scale by 100"
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
        data = data.copy(data=new_values)
        # alt["name"] = "alt"
        data.attrs["long_name"] = "Altitude"
        return (data,)