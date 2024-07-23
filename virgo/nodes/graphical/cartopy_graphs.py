from virgo.nodes.base_nodes import GraphNode
from virgo.graph import Input

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cartopy

class ContourPlot(GraphNode):
    description = "Contour Plot v2"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, ins = [
            Input(self, any, "x-axis"),
            Input(self, any, "y-axis"),
            Input(self, any, "data")
        ])
    def plot(self, axis1, axis2, var, fig: Figure):
        ax = fig.add_subplot(111, projection=cartopy.crs.PlateCarree()) 
        matrixX, matrixY = np.meshgrid(axis1, axis2)
        g = ax.contourf(matrixX, matrixY, var,levels=12, cmap="bwr")
        ax.set_xlabel("{} {}".format(axis1.attrs["long_name"], "["+axis1.attrs['units']+"]" if 'units' in axis1.attrs else ""))
        ax.set_ylabel("{} {}".format(axis2.attrs["long_name"], "["+axis2.attrs['units']+"]" if 'units' in axis2.attrs else ""))
        v = np.arange(200, 300, 5) # Temperature contour levels
        cp = ax.contourf(matrixX, matrixY, var, v, transform=cartopy.crs.PlateCarree(), zorder=2, alpha=0.65, cmap=plt.cm.coolwarm)
        fig.colorbar(cp, label="{} {}".format(var.attrs["long_name"], "["+var.attrs['units']+"]" if 'units' in var.attrs else ""))

        ax.gridlines(draw_labels=True, zorder=1,color="grey",alpha=0.5)
        ax.add_feature(cartopy.feature.LAND)
        ax.add_feature(cartopy.feature.OCEAN)
        ax.add_feature(cartopy.feature.COASTLINE)
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':')