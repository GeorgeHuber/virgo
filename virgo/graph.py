from virgo import utils, functions
from virgo.ui.components.draggable_widget import DraggableWidget

import tkinter as tk

class NodeVar:
    def __init__(self, parent, type, description):
        self.type = type
        self.description = description
        self.node = parent
        self.edges = []
class Input(NodeVar):
    def __init__(self, parent, type, description=None):
        super().__init__(parent, type, description)
        self.ready = False
        self.buffer = None
    def connect(self, output):
        pass    
class Output(NodeVar):
    def __init__(self, parent, type, description=None):
        super().__init__(parent, type, description)
    def connect(self, output):
        pass
class Node:
    def __init__(self, app=None, module=functions.default, ins=None, outs=None, edges=None, description=None):
        self.ins = ins if ins else []
        self.outs = outs if outs else []
        self.app = app
        self.module = module
        self.description = description
        self.draggableWidget = None
    def get_state(self):
        state = {
            "moduleName":str(self.__module__),
            "className":str(self.__class__.__name__),
            "description":self.description,
            "isSource": self in self.app.sources
        }
        if self.draggableWidget:
            state |= self.draggableWidget.get_state()
        return state
    def set_state(self, state):
        self.description = state["description"]
        if self.draggableWidget:
            self.draggableWidget.set_state(state)
            
    def render(self):
        self.draggableWidget = DraggableWidget(self, app=self.app)
    def forward(self):
        for inputVar in self.ins:
            if not inputVar.ready:
                return
        args = [x.buffer for x in self.ins]
        try:
            output = self.module(*args)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Node {self.description} failed to run: {e}")
            print("failed to run, resetting")
            for inputVar in self.ins:
                inputVar.ready = False
                inputVar.buffer = None
            return
        #TODO: type checking to make sure ins and outs align
        for out in self.outs:
            output_index = self.outs.index(out)
            for edge in out.edges:
                edge.buffer = output[output_index]
                edge.ready = True
                edge.node.forward()

        for inputVar in self.ins:
           inputVar.ready = False
           inputVar.buffer = None
