from __future__ import annotations

from tkinter import ttk
import tkinter as tk
import os, json

from virgo.nodes import base_nodes, graphical, functional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from virgo.app import App

#TODO: turn this into a class
def Page(self: App):
    page = tk.Frame(self.root)
    page.label = "Canvas"
    page.grid(column=0, row=0,sticky ="nsew")
    
    page.grid_columnconfigure(0, weight=1,uniform="page1")
    page.grid_columnconfigure(1, weight=3,uniform="page1")
    page.grid_rowconfigure(0, weight=1)
    self.canvas = tk.Canvas(page, highlightbackground="black",highlightthickness=1)
    self.canvas.grid(column=1, row=0, sticky="nsew")

    self.canvas.bind('<Motion>', self.canvas_motion_handler)
    self.canvas.bind('<ButtonPress-1>', self.canvas_click_handler)

    panelBorder = tk.Frame(page, highlightbackground="black",highlightthickness=1)
    panelBorder.grid(column=0, row=0, sticky="nsew")
    panel = ttk.Notebook(panelBorder, style="CanvasPage.TNotebook")

    self.widgetMenu = tk.Frame(panel)
    self.configMenu = tk.Frame(panel)
    panel.add(self.widgetMenu, text='Widgets') 
    panel.add(self.configMenu, text='Configurations') 
    
    panel.grid(column=0, row=0, sticky="nsew")
    panel.bind('<<NotebookTabChanged>>', lambda event: self.root.update_idletasks())
    
    self.widgetMenu.grid_rowconfigure(0, weight=1)
    self.widgetMenu.grid_columnconfigure(0, weight=1)
    widgets = ttk.Frame(self.widgetMenu)
    widgets.grid(column=0, row=0, sticky="nsew")
    ttk.Label(self.canvas, text="Panopoly The Sequel").grid()
    ttk.Label(self.canvas, text="Use the top menu to open a file to get started").grid()
    
    #List of different widgets to add to the canvas
    ttk.Label(widgets, text="Data:", style="H3.TLabel").grid()
    ttk.Button(widgets, text="Add a Data Source", command=lambda x=base_nodes.DataSourceNode: self.add_source_node_to_canvas(x)).grid()

    ttk.Label(widgets, text="Graph Type:", style="H3.TLabel").grid()
    for nodeType in graphical.__all__:
        ttk.Button(widgets, text="add {}:".format(nodeType.description), command=lambda x=nodeType: self.add_node_to_canvas(x)).grid()


    ttk.Label(widgets, text="Functions:", style="H3.TLabel").grid()
    for nodeType in functional.__all__:
        ttk.Button(widgets, text="{}".format(nodeType.description), command=lambda x=nodeType: self.add_node_to_canvas(x)).grid()

    ttk.Button(widgets, text="Run Canvas", command=self.run_canvas).grid(pady=20)
    ttk.Button(widgets, text="Clear Canvas", command=self.clear_canvas).grid(pady=20)
    
    self.configMenu.grid_rowconfigure(0, weight=1)
    self.configMenu.grid_columnconfigure(0, weight=1)
    config = ttk.Frame(self.configMenu)
    config.grid(column=0, row=0, sticky="nsew")


    ttk.Label(config, text="Prebuilt Configurations", style="H3.TLabel").grid()
    try:
        #TODO:  Dont hard code this for max & linux
        configPaths = os.listdir("configurations")
    except Exception as e:
        print(e)
        configPaths = []
    for path in configPaths:
        if ".virgo" in path:
            with open(f"configurations/{path}", "r") as file:
                #TODO: redundant load> low priority
                json_data = file.read()
                data = json.loads(json_data)
                title = data["metadata"]["title"] if "metadata" in data and "title" in data["metadata"] else "Untitled"
                description = data["metadata"]["description"] if "metadata" in data and "description" in data["metadata"] else "No description"
            ttk.Button(config, text="{}\n@ {}".format(title, path), command=lambda x=f"configurations/{path}": self.load_canvas(x)).grid()
    
    return page