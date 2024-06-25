from virgo.nodes.base_nodes import GraphNode
from virgo.graph import Input

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
class Simple2D(GraphNode):
    description = "Simple 2D Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "axis1"),
            Input(self, any, "axis2")
        ],
        )
    def plot(self, axis1, axis2, fig: Figure):
        print(axis1, axis2)
        ax = fig.add_subplot(111) 
        ax.plot(axis1[:], axis2[:])
        ax.set_xlabel(axis1.long_name)
        ax.set_ylabel(axis2.long_name)
        

class SimpleColorMesh(GraphNode):
    description = "Simple Color Mesh"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "axis1"),
            Input(self, any, "axis2"),
            Input(self, any, "variable")
        ])
    def plot(self, axis1, axis2, var, fig: Figure):
        ax = fig.add_subplot(111) 
        mesh = ax.pcolormesh(var[0,0,:,:])
        fig.colorbar(mesh, ax=ax)
        ax.set_xlabel(axis1.long_name)
        ax.set_ylabel(axis2.long_name)
        ax.set_title("{}".format(var.long_name))