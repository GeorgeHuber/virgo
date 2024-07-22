import tkinter as tk
from tkinter import ttk

from virgo import functions, utils, graph
from virgo.nodes import base_nodes

import numpy as np

"""
These widgets are all a little more tricky because they require dropdowns"""

class DimensionIndexWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Index Dimension").grid()
        self.dimName = tk.StringVar()
        self.dimValue = tk.StringVar()
        self.dimSelect = ttk.OptionMenu(self, self.dimName)
        self.dimName.trace("w", self.set_dim_handler)
        self.exclude = [self.dimSelect]
        self.dimSelect.grid()
        self.dimValueSelect = ttk.Combobox(self, values=[], textvariable=self.dimValue, width=5)
        self.dimValue.trace("w", self.set_dim_value_handler)
        self.dimValueSelect.grid()
        self.dimensions = []
        # Update dropdown options
        self.on_data_change()
    def on_data_change(self):
        if not self.app.data:
            return
        self.dimensions = list(self.app.data.dims.keys())
        self.dimSelect['menu'].delete(0, 'end')
       
        dimName = self.dimName.get()
        if dimName not in list(self.dimensions):
            dimName = list(self.dimensions)[0]
        self.dimSelect.set_menu(dimName, *self.dimensions)
        self.set_dim_handler(dimName=dimName)
    def set_dim_handler(self, varName=None, idx=None, op=None, dimName=None):
        if dimName:
            self.dimName.set(dimName)
        else:
            dimName = self.dimName.get()
        # dim = self.dimensions.index(dimName)
        #TODO get passed var
        self.dimValueSelect["values"] = [str(x.data) for x in self.app.data[dimName]]
        if self.dimValue.get() not in self.dimValueSelect["values"]:
            self.dimValue.set(self.dimValueSelect["values"][0])
        self.set_dim_value_handler()

    def set_dim_value_handler(self, varName=None, idx=None, op=None):
        dimName = self.dimName.get()
        dimVal = self.dimValue.get()
        try:
            dimIdx = utils.index(self.dimValueSelect["values"], dimVal, lambda x, y: float(x)==float(y))
            if dimIdx == -1:
                return
        except Exception:
            return
        self.dimValue.set(str(float(dimVal)))
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



class DimensionIndex(base_nodes.FunctionalNode):
    description = "Index a dimension"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
                         **kwargs,
                         ins=[graph.Input(self, None, description="data")],
                         outs=[graph.Output(self, None, description="sliced data")],
                        )
    def render(self):
        self.draggableWidget = graph.DraggableWidget(self, app=self.app, widgetClass=DimensionIndexWidget)
    def on_data_change(self):
        if self.draggableWidget:
            self.draggableWidget.widget.on_data_change()


class DimensionSliceWidget(tk.Frame):
    #TODO: Support slices of nondefault axis
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="Slice Dimension").grid()
        self.dimName = tk.StringVar()
        self.dimStart = tk.StringVar()
        self.dimStop = tk.StringVar()
        self.dimStep = tk.StringVar()
        self.dimSelect = ttk.OptionMenu(self, self.dimName)
        self.dimName.trace("w", self.set_dim_handler)
        self.dimSelect.grid()
        ttk.Label(self, text="start").grid()
        self.dimStartSelect = ttk.Combobox(self, values=[], textvariable=self.dimStart, width=5)
        self.dimStart.trace("w", self.set_slice_handler)
        self.dimStartSelect.grid()
        ttk.Label(self, text="stop").grid()
        self.dimStopSelect = ttk.Combobox(self, values=[], textvariable=self.dimStop, width=5)
        self.dimStop.trace("w", self.set_slice_handler)
        self.dimStopSelect.grid()
        ttk.Label(self, text="step").grid()
        self.dimStepSelect = ttk.Combobox(self, values=[], textvariable=self.dimStep, width=5)
        self.dimStep.trace("w", self.set_slice_handler)
        self.dimStepSelect.grid()
        self.exclude = [self.dimSelect, self.dimStartSelect, self.dimStopSelect, self.dimStepSelect]
        self.dimensions = []
        # Update dropdown options
        self.on_data_change()
    def on_data_change(self):
        if not self.app.data:
            return
        self.dimensions = list(self.app.data.dims.keys())
        self.dimSelect['menu'].delete(0, 'end')
       
        dimName = self.dimName.get()
        if dimName not in list(self.dimensions):
            dimName = list(self.dimensions)[0]
        self.dimSelect.set_menu(dimName, *self.dimensions)
        self.set_dim_handler(dimName=dimName)
    def set_dim_handler(self, varName=None, idx=None, op=None, dimName=None):
        if dimName:
            self.dimName.set(dimName)
        else:
            dimName = self.dimName.get()
        # dim = self.dimensions.index(dimName)
        #TODO get passed var
        indicies = [str(x.data) for x in self.app.data[dimName]]
        self.dimStartSelect["values"] = indicies
        self.dimStopSelect["values"] = indicies + [ "END" ]
        self.dimStepSelect["values"] = [str(i) for i in range(1, len(indicies))]
        if self.dimStart.get() not in self.dimStartSelect["values"]:
            self.dimStart.set(self.dimStartSelect["values"][0])
        if self.dimStop.get() not in self.dimStopSelect["values"]:
            self.dimStop.set(self.dimStopSelect["values"][-1])
        if self.dimStep.get() not in self.dimStepSelect["values"]:
            self.dimStep.set(self.dimStepSelect["values"][0])
        self.set_slice_handler()

    def set_slice_handler(self, varName=None, idx=None, op=None):
        print("handler triggered")
        dimName = self.dimName.get()
        dimStart = self.dimStart.get()
        dimStop = self.dimStop.get()
        dimStep = self.dimStep.get()
        #TODO: Dont chekc start, stop, step every time only the one that changes
        def compare_floats(x, y):
            if x == "END" or y == "END":
                return x == y
            return float(x)==float(y)
        try:
            dimStart = utils.index(self.dimStartSelect["values"], dimStart, compare_floats)
            if dimStart == -1:
                return
            dimStop = utils.index(self.dimStopSelect["values"], dimStop, compare_floats)
            if dimStop == -1:
                return
            dimStep = int(dimStep)
        except Exception as e:
            print(e)
            return
        #TODO: check that this passes metadata correctly
        def function(axis, data):
            print("before actual slice", data.dims)
            idx = {}
            idx[dimName] = slice(dimStart, dimStop, dimStep)
            slicedData = data[idx]
            slicedAxis = axis[idx]
            print("after slices", slicedData.dims)
            return (slicedAxis, slicedData)
        self.node.function = function
    def get_state(self):
        state = {
            "varName": self.dimName.get(),
            "start": self.dimStart.get(),
            "stop": self.dimStop.get(),
            "step": self.dimStep.get()
        }
        return state
    def set_state(self, state):
        self.dimName.set(state["varName"])
        self.dimStart.set(state["start"])
        self.dimStop.set(state["stop"])
        self.dimStep.set(state["step"])
        self.on_data_change()



class DimensionSlice(base_nodes.FunctionalNode):
    description = "Slice a dimension"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, 
                         **kwargs,
                         ins=[graph.Input(self, None, description="axis"), graph.Input(self, None, description="data")],
                         outs=[graph.Output(self, None, description="sliced axis"), graph.Output(self, None, description="sliced data")],
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