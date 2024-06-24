import tkinter as tk
from tkinter import ttk
from virgo import utils, functions
class DraggableNode(tk.Frame):
    def __init__(self, node, app, widget=None, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = 0, 0
        self.app = app
        self.canvas = self.app.canvas
        self.node = node
        self.widget = widget
        self.inButtons = {}
        self.outButtons = {}
        self.lines = {}
        self.create_ui()
        self.id = self.canvas.create_window(400, 400, window=self)
        #TODO: figure out why this is breaking
        self.bind_class(self.id, "<ButtonPress-1>", self.on_drag_start)
        self.bind_class(self.id, "<ButtonRelease-1>", self.on_drag_stop)
        self.bind_class(self.id, "<B1-Motion>", self.on_drag_motion)
        utils.bind_all_recur(self, exclude=[self.widget])

    def create_ui(self):
        if self.widget:
            self.widget(self, self.node, self.app).grid(row=0, column=0)
        else:
            ttk.Label(self,text="empty widget").grid(row=0, column=0)
        self.varFrame = ttk.Frame(self)
        self.varFrame.grid_columnconfigure(0,weight=1)
        self.varFrame.grid_columnconfigure(2, weight=1)
        self.update_ins()
        self.update_outs()
        self.varFrame.grid(sticky ="nsew")
    def update_ins(self):
        if len(self.node.ins):
            inputBox = ttk.Frame(self.varFrame)
            ttk.Label(inputBox, text="Inputs").grid()
            for inVar in self.node.ins:
                inButton = ttk.Button(inputBox, text=":{}".format(inVar.description), command=lambda x=inVar:self.app.node_select_handler(x))
                self.inButtons[inVar] = inButton
                inButton.grid()
            inputBox.grid(column=0, row=0)
    def update_outs(self):
        if len(self.node.outs):
            outputBox = ttk.Frame(self.varFrame)
            ttk.Label(outputBox, text="Outputs").grid()
            for out in self.node.outs:
                outButton = ttk.Button(outputBox, text="{}:".format(out.description), command=lambda x=out:self.app.node_select_handler(x))
                self.outButtons[out] = outButton
                outButton.grid()
            outputBox.grid(column=2, row=0)
        
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
        for inVar in self.node.ins:
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
    def __init__(self, app=None, module=functions.default_print, ins=None, outs=None, edges=None, description=None):
        self.ins = ins if ins else []
        self.outs = outs if outs else []
        self.app = app
        self.module = module
        self.description = description
    def render(self):
        self.draggableNode = DraggableNode(self, app=self.app)
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

class DataSourceWidget(tk.Frame):
    def __init__(self, parent, node, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.node = node
        ttk.Label(self, text="I AM BECOME DATA").grid()
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
        print(dataName)
        self.node.outs = [Output(self.node, None, description=dataName)]
        self.node.module = functions.get_default_return_print(self.app.data.variables[dataName])
        # Object will not contain draggable node in initial setup run
        if hasattr(self.node, "draggableNode"):
            utils.destroy_children(self.node.draggableNode.varFrame)
            self.node.draggableNode.update_outs()
            self.node.draggableNode.varFrame.grid()

        

class DataSourceNode(Node):
    def __init__(self, app, **kwargs):
        super().__init__(app, outs=[Output(self, None, description="")],**kwargs)
    def render(self):
        self.draggableNode = DraggableNode(self, app=self.app, widget=DataSourceWidget)
