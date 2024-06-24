import tkinter as tk
from tkinter import ttk
from virgo import utils
class DraggableNode(tk.Frame):
    def __init__(self, ins, outs, app, widget=None, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = 0, 0
        self.app = app
        self.canvas = self.app.canvas
        self.ins = ins
        self.outs = outs
        self.widget = widget
        self.inButtons = {}
        self.outButtons = {}
        self.lines = {}
        self.create_ui()
        self.id = self.canvas.create_window(400, 400, window=self)
        self.bind_class(self.id, "<ButtonPress-1>", self.on_drag_start)
        self.bind_class(self.id, "<ButtonRelease-1>", self.on_drag_stop)
        self.bind_class(self.id, "<B1-Motion>", self.on_drag_motion)
        utils.bind_all_recur(self)

    def create_ui(self):
        if self.widget:
            self.widget(self).grid(row=0, column=0)
        else:
            ttk.Label(self,text="empty widget").grid(row=0, column=0)
        varFrame = ttk.Frame(self)
        varFrame.grid_columnconfigure(0,weight=1)
        varFrame.grid_columnconfigure(2, weight=1)
        inputBox = ttk.Frame(varFrame)
        ttk.Label(inputBox, text="Inputs").grid()
        for inVar in self.ins:
            inButton = ttk.Button(inputBox, text=":{}".format(inVar.description), command=lambda x=inVar:self.app.node_select_handler(x))
            self.inButtons[inVar] = inButton
            inButton.grid()
        outputBox = ttk.Frame(varFrame)
        ttk.Label(outputBox, text="Outputs").grid()
        for out in self.outs:
            outButton = ttk.Button(outputBox, text="{}:".format(out.description), command=lambda x=out:self.app.node_select_handler(x))
            self.outButtons[out] = outButton
            outButton.grid()
        inputBox.grid(column=0, row=0)
        outputBox.grid(column=2, row=0)
        varFrame.grid(sticky ="nsew")
    def on_drag_start(self, event):
        rect = self.canvas.bbox(self.id)
        self.canvas.addtag_withtag("drag", self.id)
        eventx = event.x_root - rect[0]
        eventy = event.y_root - rect[1]
        self.start_pos = eventx, eventy
    def on_drag_stop(self, event):
        self.canvas.dtag("drag")
    def on_drag_motion(self, event):
        #TODO: adjust active lines on drag
        x = min(max(event.x_root-self.start_pos[0], 0),self.canvas.winfo_width()-10)
        y = min(max(event.y_root-self.start_pos[1], 0),self.canvas.winfo_height()-10)
        self.canvas.moveto("drag", x, y)
        self.update_output_lines()
        self.update_input_lines()
    def update_output_lines(self):
        for outVar in self.lines.keys():
            for lineId in self.lines[outVar].values():
                curCoords = self.canvas.coords(lineId)
                wx, wy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
                bx, by = self.outButtons[outVar].winfo_rootx(), self.outButtons[outVar].winfo_rooty()
                w, h =self.outButtons[outVar].winfo_width() ,  self.outButtons[outVar].winfo_height()
                x = bx - wx + (w)*0.8
                y = by - wy + (h)/2
                self.canvas.coords(lineId, x, y, curCoords[2:])
    def update_input_lines(self):
        for inVar in self.ins:
            for outVar in inVar.edges:
                lineId = outVar.node.draggableNode.lines[outVar][inVar]
                curCoords = self.canvas.coords(lineId)
                wx, wy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
                bx, by = self.inButtons[inVar].winfo_rootx(), self.inButtons[inVar].winfo_rooty()
                w, h =self.inButtons[inVar].winfo_width() ,  self.inButtons[inVar].winfo_height()
                x = bx - wx + (w)*0.2
                y = by - wy + (h)/2
                self.canvas.coords(lineId, curCoords[:2], x, y)

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
    def __init__(self, app=None, module=lambda x:x, ins=None, outs=None, edges=None):
        self.ins = ins if ins else []
        self.outs = outs if outs else []
        self.app = app
        self.module = module
    def render(self):
        self.draggableNode = DraggableNode(app=self.app, ins=self.ins, outs=self.outs)
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

class DataSourceNode(Node):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    class DataSourceWidget(tk.Frame):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            ttk.Label(self, text="I AM BECOME DATA")

    def render(self):
        self.draggableNode = DraggableNode(app=self.app, ins=self.ins, outs=self.outs, widget=self.DataSourceWidget)
