from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename

import matplotlib
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import numpy as np
import netCDF4 as nc

import utils
"""TODOS:
    Support multiple edges
    backtrace edges to account for readjustment on two way connections
"""
DEBUG = False
class DraggableNode(tk.Frame):
    def __init__(self, ins, outs, app, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = 0, 0
        self.app = app
        self.canvas = self.app.canvas
        self.ins = ins
        self.outs = outs
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

class App:
    def __init__(self, root: tk.Tk):
        """Initializes a new NAME app

        Args:
            root (tkinter.Tk): root tkinter instance
        """
        self.root = root
        self.root.geometry("1200x900")

        self.root.title("Panopoly who?")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_propagate(False)
        self.page1 = None
        self.page2 = None
        self.curPage = None
        self.selectedNodeVar = None

        self.filePath = ""
        self.data = None

        # self._drag_data = {}

        self.plotTypes = ["Line Plot", "Color Map"]

        self.create_canvas_page()
        self.create_data_view_page()
        self.set_main_menu()
        self.set_active_page(self.page1)

        if DEBUG:
            self.filePath = "/Users/grhuber/Downloads/2018_High_Vertical.geosgcm_gwd.20180201.nc4"
            self.load_data()

    def set_main_menu(self):
        """Configures highest level menu bar for the app.
        """
        self.menuBar = tk.Menu(self.root)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New", command=None)
        self.fileMenu.add_command(label="Open", command=self.select_file)
        self.fileMenu.add_command(label="Save", command=None)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit", command=self.root.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        self.windowMenu = tk.Menu(self.menuBar, tearoff=0)
        self.windowMenu.add_command(label="Canvas", command=lambda: self.set_active_page(self.page1))
        self.windowMenu.add_command(label="Data", command=lambda: self.set_active_page(self.page2))
        self.menuBar.add_cascade(label="Window", menu=self.windowMenu)
        self.root.config(menu=self.menuBar)

    def create_canvas_page(self):
        self.page1 = tk.Frame(self.root)
        self.page1.grid(column=0, row=0,sticky ="nsew")
        
        self.page1.grid_columnconfigure(0, weight=1,uniform="page1")
        self.page1.grid_columnconfigure(1, weight=3,uniform="page1")
        self.page1.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.page1, highlightbackground="black", highlightthickness=1)
        self.canvas.grid(column=1, row=0, sticky="nsew")

        self.canvas.bind('<Motion>', self.canvas_motion_handler)
        self.canvas.bind('<ButtonPress-1>', self.canvas_click_handler)

        self.widgetMenu = tk.Frame(self.page1, highlightbackground="black", highlightthickness=1)
        self.widgetMenu.grid(column=0, row=0, sticky="nsew")
        ttk.Label(self.canvas, text="Panopoly The Sequel", padding=10).grid()
        ttk.Button(self.widgetMenu, text="add node", command=self.add_node_to_canvas).grid()

        
    def add_node_to_canvas(self, node_id=None):
        n = Node(self)
        n.ins = [Input(n, int,"a"), Input(n, int, "b")]
        n.outs = [Output(n, int, "c"), Output(n, int, "d")]
        n.render()

    def update_canvas_page(self):
        pass
    
    def create_data_view_page(self):
        if self.page2:
            utils.destroy_children(self.page2)
        else:
            self.page2 = ttk.Frame(self.root)
            self.page2.grid(column=0, row=0,sticky ="nsew")
            # self.page2.configure(yscrollcommand=ttk.Scrollbar(self.page2).set)
        # TODO: fix window management adn the current variable
        ttk.Label(self.page2, text="Data Properties", padding=10).grid(column=0, row=0)
        ttk.Label(self.page2, text="Metadata").grid()
        if self.data:
            for property in self.data.ncattrs():
                ttk.Label(self.page2, text=property).grid()
                ttk.Label(self.page2, text=self.data.getncattr(property)).grid()
        ttk.Label(self.page2, text="Variables").grid()
        if self.data:
            for variable in self.data.variables.keys():
                ttk.Label(self.page2, text=variable).grid()
                try:
                    ttk.Label(self.page2, text=self.data.variables[variable].long_name).grid()
                except:
                    pass

    def select_file(self):
        """Selects a file via os specific interface. See also: load data
        """
        self.filePath = askopenfilename()
        if self.filePath:
            self.load_data()

    def load_data(self):
        """Loads in a netcdf file as a nc4 Dataset object. Throws error if failed open. 
        Updates data sources on main canvas page and recreates data view page.
        """
        try:
            self.data = nc.Dataset(self.filePath)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load NetCDF file: {e}")
            return
        self.update_canvas_page()
        self.create_data_view_page()

    def set_active_page(self, page):
        """Brings page to top level of tkinter rendering. 

        Args:
            page (tkinter.Frame): page to bring 
        """
        page.tkraise()
        self.curPage = page
    def canvas_motion_handler(self, event):
        """Called any time the mouse is moved on the canvas. The
        currently selected nodeVar's line should move with the 
        mouse. If the current node is none, nothing is done.

        Args:
            event (_type_): _description_
        """
        if not self.selectedNodeVar:
            return
        x, y = event.x, event.y
        #TODO: support multiple edges.
        if self.selectedNodeVar not in self.selectedNodeVar.node.draggableNode.lines:
            lines = self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar] = {}
            lines["None"] = self.canvas.create_line(0, 0, x, y)
        else:
            lines = self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar]
            if "None" not in lines:
                #We need to create a new one
                lines["None"] = self.canvas.create_line(0, 0, x, y)
            lineId = lines["None"]
            newCoords = self.canvas.coords(lineId)[:2] + [x, y]
            self.canvas.coords(lineId, *newCoords)
        self.selectedNodeVar.node.draggableNode.update_output_lines()
    def canvas_click_handler(self, event):
        #TODO: add remove functionality
        if self.selectedNodeVar:
            lineId = self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar]["None"]
            self.canvas.delete(lineId)
            del self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar]["None"]
            self.selectedNodeVar = None
    def node_select_handler(self, nodeVar: NodeVar):
        """Called when a nodeVar is selected for creating an edge. If 
        self.selectedNodeVar is not None, then an edge must be created between 
        selected node and the new nodeVar

        Args:
            nodeVar (NodeVar): the new input or output being selected
        """
        if not self.selectedNodeVar and isinstance(nodeVar, Output):
            self.selectedNodeVar = nodeVar
        elif self.selectedNodeVar:
            if isinstance(nodeVar, Input):
            # Handle new connection
                self.selectedNodeVar.edges.append(nodeVar)
                nodeVar.edges.append(self.selectedNodeVar)
                self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar][nodeVar] = self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar]["None"]
                del self.selectedNodeVar.node.draggableNode.lines[self.selectedNodeVar]["None"]
                nodeVar.node.draggableNode.update_input_lines()
                self.selectedNodeVar = None


def main():
    matplotlib.use('agg')  
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()