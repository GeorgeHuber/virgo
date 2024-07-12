from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilenames, askopenfilename

import matplotlib
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import numpy as np
import xarray as xr
import os
import json, importlib, datetime, time, pathlib

from virgo import utils, graph
from virgo.serialization import serialize_nodes
from virgo.ui.pages import canvas_page, data_page
from virgo.ui import style
DEBUG = os.getenv('DEBUG') == "True"


class App:
    def __init__(self, root: tk.Tk):
        """Initializes a new NAME app

        Args:
            root (tkinter.Tk): root tkinter instance
        """
        self.root = root
        self.style = style.build_style()
        self.root.geometry("1200x900")
        
        self.root.title("Panopoly who?")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_propagate(False)
        self.curPage = None
        self.selectedNodeVar = None

        self.filePaths = []
        self.data = None

        self.configurationsPath = pathlib.Path(os.getcwd()).joinpath("configurations").absolute()
        self.sources = []
        self.nodes = []

        self.pages = [
            canvas_page.Page(self),
            data_page.Page(self)
        ]

        self.set_main_menu()
        self.set_active_page(0)

        if DEBUG:
            self.filePaths.append("/Users/grhuber/Downloads/High-01-29.geosgcm_prog.2018227.nc4")
            self.filePaths = [
                "/Users/grhuber/Downloads/GEOS_DATA/Start_Date_2018-01-29/High-01-29.geosgcm_prog.20180207.nc4",
                # "/Users/grhuber/Downloads/GEOS_DATA/Start_Date_2018-01-29/High-01-29.geosgcm_prog.20180206.nc4"
            ]
            
            now = time.time()
            self.load_data()
            print(f"Loaded in : {time.time() - now} seconds")
            self.canvasPath = "configurations/2dlineplot.virgo"
            self.load_canvas(self.canvasPath)

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
        for i, page in enumerate(self.pages):
            self.windowMenu.add_command(label=page.label, command=lambda i=i: self.set_active_page(i))
        self.menuBar.add_cascade(label="Window", menu=self.windowMenu)

        self.canvasMenu = tk.Menu(self.menuBar, tearoff=0)
        self.canvasMenu.add_command(label="Load Canvas from Disk", command=self.load_canvas)
        self.canvasMenu.add_command(label="Save Canvas to Disk", command=self.save_canvas)
        if DEBUG:
            self.canvasMenu.add_command(label="Print Canvas", command=self.print_canvas)
        self.menuBar.add_cascade(label="Canvas", menu=self.canvasMenu)

        self.root.config(menu=self.menuBar)


    def add_node_to_canvas(self, nodeType):
        n = nodeType(self)
        n.render()
        self.nodes.append(n)
        return n
    def add_source_node_to_canvas(self, nodeType):
        n = self.add_node_to_canvas(nodeType)
        self.sources.append(n)
    def run_canvas(self):
        for node in self.sources:
            node.forward()
    def clear_canvas(self):
        self.selectedNodeVar = None
        self.sources = []
        self.nodes = []
        self.canvas.delete('all')
    def update_canvas_page(self):
        pass

    def select_file(self):
        """Selects a file via os specific interface. See also: load data
        """
        self.filePaths = askopenfilenames()
        if self.filePaths:
            self.load_data()

    def load_data(self):
        """Loads in a netcdf file as a nc4 Dataset object. Throws error if failed open. 
        Updates data sources on main canvas page and recreates data view page.
        """
        datum = []
        try:
            for f in self.filePaths:
                datum.append(xr.open_dataset(f, decode_times=False, chunks="auto"))
            
            # Case with one file
            if len(datum) == 1:
                self.data = datum[0]

            # Variables are the same so we should concat the files along time
            # TODO: allow the user to select how to handle multiple files
            elif datum[0].variables.keys() == datum[1].variables.keys():
                #TODO: the following code is useful for GEOS but not every file (change)
                timeCorrected = []
                for dataset in datum:
                    timeStr = str(dataset["time"].attrs["begin_date"])
                    timeFormat = "%Y%m%d"
                    newTime = dataset["time"] + int(datetime.datetime.strptime(timeStr, timeFormat).timestamp()/60)
                    newTime.attrs = dataset["time"].attrs
                    timeCorrected.append(dataset.assign_coords(time=newTime))
                self.data = xr.concat(timeCorrected, "time") #TODO: defrost this var (since it's hard coded)
                self.data = self.data.sortby("time")
            # Otherwise merge them since vars should be different
            else:
                self.data = xr.merge(datum, compat="override")
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", f"Failed to load NetCDF file: {e}")
            return
        self.update_canvas_page()
        self.pages[1].destroy()
        self.pages[1] = data_page.Page(self)

        self.set_active_page(0)
        for node in self.nodes:
            if hasattr(node, "on_data_change"):
                node.on_data_change()

    def set_active_page(self, page):
        """Brings page to top level of tkinter rendering. 

        Args:
            page (tkinter.Frame): page to bring 
        """
        self.pages[page].tkraise()
        if page == 0:
            self.clear_canvas()
            for node in self.nodes:
                node.render()
            self.canvas.update_idletasks()
            self.draw_lines()

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
        if self.selectedNodeVar not in self.selectedNodeVar.node.draggableWidget.lines:
            lines = self.selectedNodeVar.node.draggableWidget.lines[self.selectedNodeVar] = {}
            #TODO: Add delete handler on double click
            lines["None"] = self.canvas.create_line(0, 0, x, y, width=3, arrow=tk.LAST)
        else:
            lines = self.selectedNodeVar.node.draggableWidget.lines[self.selectedNodeVar]
            if "None" not in lines:
                lines["None"] = self.canvas.create_line(0, 0, x, y, width=3, arrow=tk.LAST)
            lineId = lines["None"]
            newCoords = self.canvas.coords(lineId)[:2] + [x, y]
            self.canvas.coords(lineId, *newCoords)
        self.selectedNodeVar.node.draggableWidget.update_output_lines()
    def canvas_click_handler(self, event):
        #TODO: add remove functionality
        if self.selectedNodeVar:
            lines = self.selectedNodeVar.node.draggableWidget.lines
            lineId = lines[self.selectedNodeVar]["None"]
            self.canvas.delete(lineId)
            del lines[self.selectedNodeVar]["None"]
            self.selectedNodeVar = None
    def node_select_handler(self, nodeVar: graph.NodeVar):
        """Called when a nodeVar is selected for creating an edge. If 
        self.selectedNodeVar is not None, then an edge must be created between 
        selected node and the new nodeVar

        Args:
            nodeVar (NodeVar): the new input or output being selected
        """
        if not self.selectedNodeVar and isinstance(nodeVar, graph.Output):
            self.selectedNodeVar = nodeVar
        elif self.selectedNodeVar:
            if isinstance(nodeVar, graph.Input):
            # Handle new connection
                self.selectedNodeVar.edges.append(nodeVar)
                nodeVar.edges.append(self.selectedNodeVar)
                line = self.selectedNodeVar.node.draggableWidget.lines[self.selectedNodeVar]["None"]
                self.selectedNodeVar.node.draggableWidget.lines[self.selectedNodeVar][nodeVar] = line
                print(line)
                self.canvas.tag_bind(line, '<Double-Button-1>', lambda _, out=self.selectedNodeVar, inVar=nodeVar: self.delete_line_handler(out, inVar))
                del self.selectedNodeVar.node.draggableWidget.lines[self.selectedNodeVar]["None"]
                nodeVar.node.draggableWidget.update_input_lines()
                self.selectedNodeVar = None
    def delete_line_handler(self, outVar: graph.Output, inVar: graph.Input):
        outVar.edges.remove(inVar)
        inVar.edges.remove(outVar)
        self.canvas.delete(outVar.node.draggableWidget.lines[outVar][inVar])
        del outVar.node.draggableWidget.lines[outVar][inVar]
        print("deleted line")
    def draw_lines(self):
        for node in self.nodes:
            for out in node.outs:
                out.node.draggableWidget.lines[out] = {}
                for inp in out.edges:
                    line = self.canvas.create_line(0,0,100,100, width=3, arrow=tk.LAST)
                    out.node.draggableWidget.lines[out][inp] = line
                    self.canvas.tag_bind(line, '<Double-Button-1>', lambda _, out=out, inVar=inp: self.delete_line_handler(out, inVar))
                    self.root.update_idletasks() 
                    inp.node.draggableWidget.update_input_line(inp, line)
                    out.node.draggableWidget.update_output_line(out, line)
    def print_canvas(self):
        print(self.sources)
    def load_canvas(self, filename = None):
        print("Loading Canvas")
        if not filename:
            filename = askopenfilename(initialdir=self.configurationsPath, filetypes=[("Canvas files", "*.virgo")])
        if filename:
            with open(filename, 'r') as file:
                print("Canvas loaded successfully.")
                json_data = file.read()
                data = json.loads(json_data)
                self.clear_canvas()
                self.nodes = []
                self.sources = []
                for n in data["nodes"]:
                    NodeClass = getattr(importlib.import_module(n["moduleName"]), n["className"])
                    node: graph.Node = NodeClass(self)
                    self.nodes.append(node)
                    if n["isSource"]:
                        self.sources.append(node)
                inList = []
                for inp in data["ins"]:
                    inList.append(graph.Input(
                        self.nodes[inp["parent"]],
                        any, #TODO:typing support
                        inp["description"]
                        ))
                outList = []
                for out in data["outs"]:
                    outList.append(graph.Output(
                        self.nodes[out["parent"]],
                        any, #TODO:typing support
                        out["description"]
                        ))
                for i in range(len(data["ins"])):
                    inp = inList[i]
                    for outNum in data["ins"][i]["edges"]:
                        inp.edges.append(outList[outNum])
                for i in range(len(data["outs"])):
                    out = outList[i]
                    for inNum in data["outs"][i]["edges"]:
                        out.edges.append(inList[inNum])
                for i in range(len(data["nodes"])):
                    n = data["nodes"][i]
                    node = self.nodes[i]
                    node.ins = []
                    for inp in n["ins"]:
                        node.ins.append(inList[inp])
                    node.outs = []
                    for out in n["outs"]:
                        node.outs.append(outList[out]) 
                    node.render()
                    self.root.update_idletasks()
                    cx, cy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
                    x,y = n["x"] - cx, n["y"] - cy
                    print(x,y)
                    node.draggableWidget.move_to(x,y)
                    node.set_state(n)
                self.draw_lines()

            # except Exception as e:
            #     tk.messagebox.showerror("Error", f"Failed to load canvas: {e}")
    def save_canvas(self):
        title = tk.simpledialog.askstring(title="Canvas Metadata",
                                  prompt="Enter a title:")
        description = tk.simpledialog.askstring(title="Canvas Metadata",
                                  prompt="Enter a description:")
        filename = tk.filedialog.asksaveasfilename(initialfile="canvas",initialdir=self.configurationsPath,defaultextension=".virgo", filetypes=[("Canvas files", "*.virgo")])
        if filename:
            inData, outData, nodeData = serialize_nodes(self.nodes)
            data = {
                "nodes":nodeData,
                "ins":inData,
                "outs":outData,
                "metadata": {
                    "title": title,
                    "description":description
                    }
                }

            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
                print("Canvas saved successfully.")
            # except Exception as e:
            #     tk.messagebox.showerror("Error", f"Failed to save canvas: {e}")
    
        print("Saving Canvas")