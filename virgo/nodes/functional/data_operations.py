import tkinter as tk
from tkinter import ttk

from virgo import functions, utils, graph
from virgo.nodes import base_nodes

import numpy as np

"""
These widgets are all a little more tricky because they require dropdowns"""

class DimensionSliceWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Index Dimension").grid()
        self.dimName = tk.StringVar()
        self.dimValue = tk.StringVar()
        self.dimSelect = ttk.OptionMenu(self, self.dimName)
        self.exclude = [self.dimSelect]
        self.dimSelect.grid()
        self.dimValueSelect = ttk.Combobox(self, values=[], textvariable=self.dimValue, width=5)
        self.dimValueSelect.bind("<<ComboboxSelected>>", self.set_dim_value_handler)
        self.dimValueSelect.grid()
        self.dimensions = list(self.app.data.dims.keys())
        # Update dropdown options
        if self.app.data:
            self.dimSelect['menu'].delete(0, 'end')
            # TODO: make thsi work when file changes without rebuild
            for dimName in self.dimensions:
                self.dimSelect['menu'].add_command(label=dimName, command=lambda x=dimName: self.set_dim_handler(x))
            
            default = list(self.dimensions)[0]
            self.set_dim_handler(default)

    def set_dim_handler(self, dimName):
        self.dimName.set(dimName)
        # dim = self.dimensions.index(dimName)
        #TODO get passed var
        self.dimValueSelect["values"] = [str(x) for x in range(len(self.app.data[dimName]))]
        self.dimValue.set("0")
        self.set_dim_value_handler()

    def set_dim_value_handler(self, event=None):
        dimName = self.dimName.get()
        if event:
            self.dimValue.set(event.widget.get())
        dimVal = int(self.dimValue.get())
        def function(data):
            print("before slice", data.dims)
            idx = {}
            idx[dimName] = dimVal
            slicedData = data[idx]
            print("after slices", slicedData.dims)
            return (slicedData,)
        self.node.function = function
    



class DimensionSlice(base_nodes.FunctionalNode):
    description = "Index a dimension"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
                         **kwargs,
                         ins=[graph.Input(self, None, description="data")],
                         outs=[graph.Output(self, None, description="sliced data")],
                        )
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widgetClass=DimensionSliceWidget)


class DimensionMeanWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Mean").grid()
        self.dimName = tk.StringVar()
        self.dimSelect = ttk.OptionMenu(self, self.dimName)
        self.exclude = [self.dimSelect]
        self.dimSelect.grid()
        self.dimensions = list(self.app.data.dims.keys())
        # Update dropdown options
        if self.app.data:
            self.dimSelect['menu'].delete(0, 'end')
            # TODO: make thsi work when file changes without rebuild
            for dimName in self.dimensions:
                self.dimSelect['menu'].add_command(label=dimName, command=lambda x=dimName: self.set_dim_handler(x))
            
            default = list(self.dimensions)[0]
            self.set_dim_handler(default)

    def set_dim_handler(self, dimName):
        self.dimName.set(dimName)
        # dim = self.dimensions.index(dimName)
        #TODO get passed var
        
        def function(data):
            newData = data.mean(dimName)
            print(newData)
            newData.attrs = data.attrs
            return (newData,)
        self.node.function = function
    



class DimensionMean(base_nodes.FunctionalNode):
    description = "Take the mean of a dimension"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
                         **kwargs,
                         ins=[graph.Input(self, None, description="data")],
                         outs=[graph.Output(self, None, description="augmented data")],
                        )
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widgetClass=DimensionMeanWidget)