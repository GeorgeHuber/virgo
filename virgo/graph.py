import tkinter as tk
from tkinter import ttk
from virgo import utils, functions
from virgo.nodes.draggable_widget import DraggableWidget

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
    def __init__(self, app=None, module=functions.default_print, ins=None, outs=None, edges=None, description=None):
        self.ins = ins if ins else []
        self.outs = outs if outs else []
        self.app = app
        self.module = module
        self.description = description
    def render(self):
        self.draggableWidget = DraggableWidget(self, app=self.app)
    def forward(self):
        for inputVar in self.ins:
            if not inputVar.ready:
                return
        output = self.module(*[x.buffer for x in self.ins])
        #TODO: type checking to make sure ins and outs align
        for out in self.outs:
            for edge in out.edges:
                output_index = self.outs.index(out)
                edge.buffer = output[output_index]
                edge.ready = True
                edge.node.forward()

        for inputVar in self.ins:
           inputVar.ready = False
           inputVar.buffer = None
