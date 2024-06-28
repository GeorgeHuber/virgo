import tkinter as tk
from tkinter import ttk
from virgo import utils
class DraggableWidget(tk.Frame):
    def __init__(self, node, app, widgetClass=None, **kwargs):
        super().__init__(**kwargs, highlightthickness=1, highlightbackground="black")
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

        if self.widget and hasattr(self.widget, 'exclude'):
            utils.bind_all_recur(self, exclude=self.widget.exclude)
        else:
            utils.bind_all_recur(self)
    def create_ui(self):
        if self.widgetClass:
            self.widget = self.widgetClass(self, self.node, self.app)
            self.widget.grid(row=0, column=0)
        else:
            ttk.Label(self,text="empty widget").grid(row=0, column=0)
        self.varFrame = ttk.Frame(self)
        self.varFrame.grid_columnconfigure(0,weight=1)
        self.varFrame.grid_columnconfigure(2, weight=1)
        self.set_ins()
        self.set_outs()
        self.varFrame.grid(sticky ="nsew")
    def set_ins(self):
        if len(self.node.ins):
            inputBox = ttk.Frame(self.varFrame)
            ttk.Label(inputBox, text="Inputs").grid()
            for inVar in self.node.ins:
                inButton = ttk.Button(inputBox, text="<-{}".format(inVar.description), command=lambda x=inVar:self.app.node_select_handler(x))
                self.inButtons[inVar] = inButton
                inButton.grid()
            inputBox.grid(column=0, row=0)
    def set_outs(self):
        if len(self.node.outs):
            outputBox = ttk.Frame(self.varFrame)
            ttk.Label(outputBox, text="Outputs").grid()
            for out in self.node.outs:
                outButton = ttk.Button(outputBox, text="{}->".format(out.description), command=lambda x=out:self.app.node_select_handler(x))
                self.outButtons[out] = outButton
                outButton.grid()
            outputBox.grid(column=0, row=1)
    def update_outs(self):
        for out in self.node.outs:
            button =  self.outButtons[out]
            button["text"] = "{}->".format(out.description)
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
                lineId = outVar.node.draggableWidget.lines[outVar][inVar]
                curCoords = self.canvas.coords(lineId)
                wx, wy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
                bx, by = self.inButtons[inVar].winfo_rootx(), self.inButtons[inVar].winfo_rooty()
                w, h =self.inButtons[inVar].winfo_width() ,  self.inButtons[inVar].winfo_height()
                x = bx - wx + (w)*0.2
                y = by - wy + (h)/2
                self.canvas.coords(lineId, curCoords[:2], x, y)