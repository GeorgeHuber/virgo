from virgo.nodes.base_nodes import FunctionalNode
from virgo.graph import Input, Output

import numpy as np

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
        alt.attrs |= {
            "units": "km",
            "long_name": "Altitude"
        }
        return (alt,)
    