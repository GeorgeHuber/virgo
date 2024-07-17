import tkinter as tk
from tkinter import ttk
from virgo import utils
from virgo.ui.components import node_buttons

class DraggableWidget(tk.Frame):
    def __init__(self, node, app, widgetClass=None, **kwargs):
        super().__init__(highlightthickness=2, highlightbackground="#2A9D8F", **kwargs)
        self.start_pos = 0, 0
        self.app = app
        self.canvas = self.app.canvas
        self.node = node
        self.widgetClass = widgetClass
        self.widget = None
        self.inButtons = {}
        self.outButtons = {}
        self.lines = {}
        self.create_ui()
        self.id = self.canvas.create_window(400, 400, window=self)
        #TODO: figure out why this is breaking
        self.bind_class(self.id, "<ButtonPress-1>", self.on_drag_start)
        self.bind_class(self.id, "<ButtonRelease-1>", self.on_drag_stop)
        self.bind_class(self.id, "<B1-Motion>", self.on_drag_motion)
        self.bind_class(self.id, "<Double-Button-1>", self.on_double_click)

        if self.widget and hasattr(self.widget, 'exclude'):
            utils.bind_all_recur(self, exclude=self.widget.exclude)
        else:
            utils.bind_all_recur(self)
    def get_state(self):
        state = {
            "x": self.winfo_rootx(),
            "y": self.winfo_rooty(),
        }
        if self.widget and hasattr(self.widget, "get_state"):
            state |= self.widget.get_state()
        return state
    def set_state(self, state):
        if self.widget and hasattr(self.widget, "set_state"):
            self.widget.set_state(state)
    def create_ui(self):
        if self.widgetClass:
            self.widget = self.widgetClass(self, self.node, self.app)
            self.widget.grid(row=0, column=0)
        else:
            ttk.Label(self,text="empty widget").grid(row=0, column=0)
        self.varFrame = tk.Frame(self)
        self.varFrame.grid_columnconfigure(0,weight=1)

        self.set_ins()
        self.set_outs()
        self.varFrame.grid(sticky ="nsew")
    def set_ins(self):
        if len(self.node.ins):
            inputBox = tk.Frame(self.varFrame)
            inputBox.grid_columnconfigure(0, weight=1)
            ttk.Label(inputBox, text="Inputs").grid()
            for inVar in self.node.ins:
                inButton = node_buttons.InButton(inputBox, inVar.description, inVar, self.app)
                self.inButtons[inVar] = inButton
                inButton.grid(sticky="ew")
            inputBox.grid(column=0, row=0, sticky="ew")
    def set_outs(self):
        if len(self.node.outs):
            outputBox = tk.Frame(self.varFrame)
            ttk.Label(outputBox, text="Outputs").grid()
            outputBox.grid_columnconfigure(0, weight=1)
            for out in self.node.outs:
                outButton = node_buttons.OutButton(outputBox, out.description, out, self.app)
                self.outButtons[out] = outButton
                outButton.grid(sticky="ew")
            outputBox.grid(column=0, row=1, sticky="ew")
    def update_outs(self):
        for out in self.node.outs:
            button =  self.outButtons[out]
            button.setText(out.description)
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
    def on_double_click(self, event):
        self.app.delete_node_handler(self.node)
    def update_output_lines(self):
        for outVar in self.lines.keys():
            for lineId in self.lines[outVar].values():
                self.update_output_line(outVar, lineId)
    def update_output_line(self, outVar, lineId):
        curCoords = self.canvas.coords(lineId)
        wx, wy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        bx, by = self.outButtons[outVar].winfo_rootx(), self.outButtons[outVar].winfo_rooty()
        w, h =self.outButtons[outVar].winfo_width() ,  self.outButtons[outVar].winfo_height()
        x = bx - wx + (w)*1 + 4
        y = by - wy + (h)/2
        self.canvas.coords(lineId, x, y, *curCoords[2:])
        # print(wx,wy, bx, by, w, h)
    def update_input_lines(self):
        for inVar in self.node.ins:
            for outVar in inVar.edges:
                lineId = outVar.node.draggableWidget.lines[outVar][inVar]
                self.update_input_line(inVar, lineId)
    def update_input_line(self, inVar, lineId):
        curCoords = self.canvas.coords(lineId)
        wx, wy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        bx, by = self.inButtons[inVar].winfo_rootx(), self.inButtons[inVar].winfo_rooty()
        w, h = self.inButtons[inVar].winfo_width() ,  self.inButtons[inVar].winfo_height()
        x = bx - wx + (w)*0 - 4
        y = by - wy + (h)/2
        # print(wx,wy, bx, by, w, h)
        self.canvas.coords(lineId, *curCoords[:2], x, y)
    def move_to(self, x, y):
        self.canvas.moveto(self.id, x, y)

