from virgo.nodes.base_nodes import GraphNode
from virgo.graph import Input

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class ContourPlotAnimation(GraphNode):
    description = "Contour Plot Animated Over Time"
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
        g = ax.contourf(X, Y, var[{"time":0}], levels=12, cmap="bwr")
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        fig.colorbar(g, label="{} {}".format(var.attrs["long_name"], "["+var.attrs['units']+"]" if 'units' in var.attrs else ""))
        ims = []
        for frame in range(len(var["time"])):
            # ax.clear()
            # print(frame)
            data = var[{"time":frame}]
            t = ax.text(0.5,1.05,f't = {frame}',horizontalalignment='center',
     verticalalignment='center', transform=ax.transAxes)
            g = ax.contourf(X, Y, data, levels=12, cmap="bwr")
            ims.append([g,t])
        self.ani = animation.ArtistAnimation(fig, ims, blit=False, interval=400)
        writer = animation.PillowWriter(fps=10)
        self.ani.save("test.gif", writer=writer)