from virgo.nodes.base_nodes import GraphNode
from virgo.graph import Input

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cartopy

class GeoContourPlot(GraphNode):
    description = "Georeferenced Contour Plot"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
            ins = [
                Input(self, any, "x-axis"),
                Input(self, any, "y-axis"),
                Input(self, any, "data")
            ],
            options=["projection", "cmap", "defaultName", "name"]
        )
    def plot(self, axis1, axis2, var, fig: Figure):
        options = self.options.get()
        cmap = options["cmap"]
        projection =  options["projection"]
        ax = fig.add_subplot(111,projection=projection())
        matrixX, matrixY = np.meshgrid(axis1, axis2)
        # g = ax.contourf(matrixX, matrixY, var, levels=12, cmap="bwr")
        cp = ax.contourf(matrixX, matrixY, var, transform=cartopy.crs.PlateCarree(), zorder=2, alpha=0.65, cmap=cmap)
        cax = fig.add_axes([0, 0, 0.1, 0.1])
        fig.subplots_adjust(hspace=0, wspace=0.01, top=0.8, left=0.1, right=0.8, bottom=0.2)
        
        cbar = fig.colorbar(cp, cax=cax, label="{} {}".format(var.attrs["long_name"], "["+var.attrs['units']+"]" if 'units' in var.attrs else ""))
        def resize_colobar(event):
            posn = ax.get_position()
            cax.set_position([posn.x0 + posn.width + 0.02, posn.y0,
                                0.04, posn.height])
        fig.canvas.mpl_connect('resize_event', resize_colobar)
        gl = ax.gridlines(draw_labels=True, zorder=1,color="grey",alpha=0.5)
        ax.add_feature(cartopy.feature.LAND)
        ax.add_feature(cartopy.feature.OCEAN)
        ax.add_feature(cartopy.feature.COASTLINE)
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
        gl.top_labels = gl.right_labels = False
        ax.set_title(var.attrs["long_name"] if options["defaultName"]=="True" else options["name"])