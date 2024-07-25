from virgo.nodes.base_nodes import GraphNode
from virgo.graph import Input

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
class Simple2D(GraphNode):
    description = "2Var-Line Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
        ins = [
            Input(self, any, "x"),
            Input(self, any, "y")
        ],
        )
    def plot(self, axis1, axis2, fig: Figure):
        print("graphing",axis1.shape,axis2.shape)
        ax = fig.add_subplot(111)
        ax.plot(axis1, axis2)
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        ax.set_title("{} vs {}".format(axis2.attrs["long_name"],axis1.attrs["long_name"], ))
        

class SimpleColorMesh(GraphNode):
    description = "Color Mesh Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "x-axis"),
            Input(self, any, "y-axis"),
            Input(self, any, "var to plot")
        ])
    def plot(self, axis1, axis2, var, fig: Figure):
        print("graphing")
        ax = fig.add_subplot(111) 
        mesh = ax.pcolormesh(var)
        fig.colorbar(mesh, ax=ax)
        ax.set_xlabel(axis1.attrs["long_name"])
        ax.set_ylabel(axis2.attrs["long_name"])
        ax.set_title("{}".format(var.attrs["long_name"]))

class SimpleContourPlot(GraphNode):
    description = "Contour Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "x-axis"),
            Input(self, any, "y-axis"),
            Input(self, any, "data")
        ])
    def plot(self, axis1, axis2, var, fig: Figure):
        print("graphing")
        ax = fig.add_subplot(111) 
        X, Y = np.meshgrid(axis1, axis2)
        print(X.shape, Y.shape, var.shape)
        g = ax.contourf(X, Y, var,levels=12, cmap="bwr")
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        fig.colorbar(g, label="{} {}".format(var.attrs["long_name"], "["+var.attrs['units']+"]" if 'units' in var.attrs else ""))