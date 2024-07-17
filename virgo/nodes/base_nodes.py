import tkinter as tk
from tkinter import ttk

from virgo import functions, graph, utils
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

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
        self.dimInfo= tk.StringVar()
        self.dataSelect = ttk.OptionMenu(self, self.dataName)
        self.dataSelect.grid()
        self.dimInfoLabel = tk.Label(self, textvariable=self.dimInfo)
        self.dimInfoLabel.grid()
        # Update dropdown options
        self.on_data_change()
        self.exclude = [self.dataSelect]
    def on_data_change(self):
        if not self.app.data:
            return
        variables = self.app.data.variables.keys()
        self.dataSelect['menu'].delete(0, 'end')
        for dataName in variables:
            self.dataSelect['menu'].add_command(label=dataName, command=lambda x=dataName: self.set_data_handler(x))
        dataName = self.dataName.get()
        if dataName not in list(variables):
            dataName = list(variables)[0]
            self.dataName.set(dataName)
        self.set_data_handler(dataName)
    def set_data_handler(self, dataName):
        data = self.app.data[dataName]
        self.dataName.set(dataName)

        # self.dimInfo.set(" ".join(["{}->{}".format(data.dims[i], data.shape[i]) for i in range(len(data.dims))]))
        self.dimInfo.set(str(data.dims)+"\n"+str(data.shape))
        newOut = graph.Output(self.node, None, description=dataName)
        curOut = self.node.outs[0]
        curOut.type, curOut.description = newOut.type, newOut.description
        self.node.module = functions.get_copy_return_print(data)
        # Object will not contain draggable node in initial setup run
        if self.node.draggableWidget:
            self.node.draggableWidget.update_outs()
            self.node.draggableWidget.varFrame.grid()
    def get_state(self):
        state = {
            "varName": self.dataName.get()
        }
        return state
    def set_state(self, state):
        self.dataName.set(state["varName"])
        self.on_data_change()


class DataSourceNode(graph.Node):
    description = "data source"
    def __init__(self, app, **kwargs):
        super().__init__(app, outs=[graph.Output(self, None, description="")],**kwargs)
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widgetClass=DataSourceWidget)
    def on_data_change(self):
        if self.draggableWidget:
            self.draggableWidget.widget.on_data_change()

class GraphWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text=node.description).grid()
        ttk.Button(self, text="options").grid()

class GraphNode(graph.Node):
    description = "Graph Node"
    def __init__(self, app, **kwargs):
        #TODO: make sure description inherits correctly
        super().__init__(app,**kwargs, description=self.description, module=self.module_wrapper)
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widgetClass=GraphWidget)
    def module_wrapper(self, *args):
        fig = Figure(figsize = (8, 8), 
                 dpi = 100) 
        main = tk.Toplevel(self.app.root)
        canvas = FigureCanvasTkAgg(fig, master=main)  
        toolbar = NavigationToolbar2Tk(canvas, main)
        toolbar.update() 
        canvas.get_tk_widget().pack()
        self.plot(*args, fig)
    def plot(self, *args):
        pass


class FunctionalWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text=node.description).grid()
        ttk.Button(self, text="options")


class FunctionalNode(graph.Node):
    description = "Functional Node"
    def __init__(self, app, **kwargs):
        super().__init__(app,**kwargs, description=self.description, module=self.module_wrapper)
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widgetClass=FunctionalWidget)   
    def module_wrapper(self, *args):
        outputs = self.function(*args)
        return outputs
    def function(self, *args):
        return args

