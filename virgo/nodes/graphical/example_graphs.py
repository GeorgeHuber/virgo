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
        options=["defaultName", "name"]
        )
    def plot(self, axis1, axis2, fig: Figure):
        options = self.options.get()
        print("graphing",axis1.shape,axis2.shape)
        ax = fig.add_subplot(111)
        ax.plot(axis1, axis2)
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        defaultName = "{} vs {}".format(axis2.attrs["long_name"],axis1.attrs["long_name"])
        ax.set_title(defaultName if options["defaultName"] == "True" else options["name"])
        

class SimpleColorMesh(GraphNode):
    description = "Color Mesh Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "x-axis"),
            Input(self, any, "y-axis"),
            Input(self, any, "var to plot")
        ],
        options=["cmap", "defaultName", "name"])
    def plot(self, axis1, axis2, var, fig: Figure):
        options = self.options.get()
        print("graphing")
        ax = fig.add_subplot(111) 
        X, Y = np.meshgrid(axis1, axis2)
        mesh = ax.pcolormesh(X, Y, var,cmap=options["cmap"])
        fig.colorbar(mesh, ax=ax)
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        ax.set_title(var.attrs["long_name"] if options["defaultName"] == "True" else options["name"])

class SimpleContourPlot(GraphNode):
    description = "Contour Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "x-axis"),
            Input(self, any, "y-axis"),
            Input(self, any, "data")
        ],
        options=['cmap', "defaultName", "name"])
    def plot(self, axis1, axis2, var, fig: Figure):
        options = self.options.get()
        print("graphing")
        ax = fig.add_subplot(111) 
        X, Y = np.meshgrid(axis1, axis2)
        print(X.shape, Y.shape, var.shape)
        g = ax.contourf(X, Y, var,levels=12, cmap=options["cmap"])
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        defaultName = "{} {}".format(var.attrs["long_name"], "["+var.attrs['units']+"]" if 'units' in var.attrs else "")
        fig.colorbar(g, label=defaultName if options["defaultName"] == "True" else options["name"])