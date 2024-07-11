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
        self.dimensions = []
        # Update dropdown options
        self.on_data_change()
    def on_data_change(self):
        if not self.app.data:
            return
        self.dimensions = list(self.app.data.dims.keys())
        self.dimSelect['menu'].delete(0, 'end')
       
        for dimName in self.dimensions:
            self.dimSelect['menu'].add_command(label=dimName, command=lambda x=dimName: self.set_dim_handler(x))
        dimName = self.dimName.get()
        if dimName not in list(self.dimensions):
            dimName = list(self.dimensions)[0]
        self.set_dim_handler(dimName)
    def set_dim_handler(self, dimName):
        self.dimName.set(dimName)
        # dim = self.dimensions.index(dimName)
        #TODO get passed var
        self.dimValueSelect["values"] = [str(x.data) for x in self.app.data[dimName]]
        if self.dimValue.get() not in self.dimValueSelect["values"]:
            self.dimValue.set(self.dimValueSelect["values"][0])
        self.set_dim_value_handler()

    def set_dim_value_handler(self, event=None):
        dimName = self.dimName.get()
        if event:
            self.dimValue.set(event.widget.get())
        dimVal = self.dimValue.get()
        dimIdx = self.dimValueSelect["values"].index(dimVal)
        def function(data):
            print("before slice", data.dims)
            idx = {}
            idx[dimName] = dimIdx
            slicedData = data[idx]
            print("after slices", slicedData.dims)
            return (slicedData,)
        self.node.function = function
    def get_state(self):
        state = {
            "varName": self.dimName.get(),
            "index": self.dimValue.get()
        }
        return state
    def set_state(self, state):
        self.dimName.set(state["varName"])
        self.dimValue.set(state["index"])
        self.on_data_change()



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
    def on_data_change(self):
        if self.draggableWidget:
            self.draggableWidget.widget.on_data_change()


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
        self.dimensions = []
        # Update dropdown options
        self.on_data_change()
    def on_data_change(self):
        if not self.app.data:
            return
        self.dimensions = list(self.app.data.dims.keys())
        self.dimSelect['menu'].delete(0, 'end')
        # TODO: make thsi work when file changes without rebuild
        for dimName in self.dimensions:
            self.dimSelect['menu'].add_command(label=dimName, command=lambda x=dimName: self.set_dim_handler(x))
        
        dimName = self.dimName.get()
        if dimName not in list(self.dimensions):
            dimName = list(self.dimensions)[0]
        self.set_dim_handler(dimName)
    def set_dim_handler(self, dimName):
        self.dimName.set(dimName)
        # dim = self.dimensions.index(dimName)
        #TODO get passed var 
        def function(data):
            newData = data.mean(dimName)
            print(newData)
            return (newData,)
        self.node.function = function
    def get_state(self):
        state = {
            "varName": self.dimName.get()
        }
        return state
    def set_state(self, state):
        self.dimName.set(state["varName"])
        self.on_data_change()

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
    
    def on_data_change(self):
        if self.draggableWidget:
            self.draggableWidget.widget.on_data_change()