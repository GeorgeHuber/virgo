import tkinter as tk
from tkinter import ttk

from virgo import functions, graph, utils
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

"""
Widgets are visuals passed to the Draggable node
object to be rendered on the canvas. Nodes on the other 
hand are defined by their behavior and override the render 
method to provide non-default behavior. In this file three
such classes, the base GraphNode, FunctionalNode and DataSourceNode class.
"""
class DataSourceWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Data Source").grid()
        self.dataName = tk.StringVar()
        self.dataSelect = ttk.OptionMenu(self, self.dataName)
        self.dataSelect.grid()
        # Update dropdown options
        if self.app.data:
            variables = self.app.data.variables.keys()
            self.dataSelect['menu'].delete(0, 'end')
            # TODO: make thsi work when file changes without rebuild
            for dataName in variables:
                self.dataSelect['menu'].add_command(label=dataName, command=lambda x=dataName: self.set_data_handler(x))
            default = list(variables)[0]
            self.dataName.set(default)
            self.set_data_handler(default)
    def set_data_handler(self, dataName):
        self.dataName.set(dataName)
        self.node.outs = [graph.Output(self.node, None, description=dataName)]
        self.node.module = functions.get_default_return_print(self.app.data[dataName])
        # Object will not contain draggable node in initial setup run
        if hasattr(self.node, "draggableWidget"):
            utils.destroy_children(self.node.draggableWidget.varFrame)
            self.node.draggableWidget.update_outs()
            self.node.draggableWidget.varFrame.grid()


class DataSourceNode(graph.Node):
    description = "data source"
    def __init__(self, app, **kwargs):
        super().__init__(app, outs=[graph.Output(self, None, description="")],**kwargs)
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widget=DataSourceWidget)

class GraphWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Graph Widget").grid()
        ttk.Button(self, text="options").grid()

class GraphNode(graph.Node):
    description = "default"
    def __init__(self, app, **kwargs):
        super().__init__(app,**kwargs, module=self.module_wrapper)
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widget=GraphWidget)
    def module_wrapper(self, *args):
        fig = Figure(figsize = (8, 8), 
                 dpi = 100) 
        self.plot(*args, fig)
        canvas = FigureCanvasTkAgg(fig, master=tk.Toplevel(self.app.root))   
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0)
    def plot(self, *args):
        pass


class FunctionalWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Functional Widget").grid()
        ttk.Button(self, text="options")


class FunctionalNode(graph.Node):
    description = "default"
    def __init__(self, app, **kwargs):
        super().__init__(app,**kwargs, module=self.module_wrapper)
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widget=FunctionalWidget)   
    def module_wrapper(self, *args):
        outputs = self.function(*args)
        return outputs
    def function(self, *args):
        return args

