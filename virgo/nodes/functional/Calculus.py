from virgo.nodes.base_nodes import FunctionalNode
from virgo.graph import Input, Output

import numpy as np

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
        dYdX.attrs |= {
            "units":Y.attrs["units"]+"/"+X.attrs['units'],
            "long_name":f"Derivative of {Y.attrs['long_name']} with respect to {X.attrs['long_name']}"
        }
        return (dYdX,)