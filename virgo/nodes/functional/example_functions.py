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
        # alt["name"] = "alt"
        new_data.attrs |= {
            "units":data.attrs.units+"* 10^2"
        }
        return (new_data,)
    
class PartialDerivative(FunctionalNode):
    description = "Take the partial derivative: dY/dX"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "X"),
            Input(self, any, "Y"),
        ],
        outs = [
            Output(self, any, "dY/dX"),
        ],
        )
    
    def function(self, X, Y):
        #Copy variable and then assign new attributes
        idx = Y.dims.index(X.dims[0])
        data=np.gradient(Y, X, axis=idx)
        dYdX = Y.copy(data=data)
        dYdX.attrs = Y.attrs
        dYdX.attrs |= {
            "units":Y.attrs["units"]+"/"+X.attrs["units"],
            "long_name":f"Derivative of {Y.attrs["long_name"]} with respect to {X.attrs["long_name"]}"
        }
        return (dYdX,)