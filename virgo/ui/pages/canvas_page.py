from __future__ import annotations

from tkinter import ttk
import tkinter as tk
import os, json, PIL

from virgo.nodes import base_nodes, graphical, functional
from virgo.ui.components import scrollable_frame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from virgo.app import App

#TODO: turn this into a class and refactor
def Page(self: App):
    page = tk.Frame(self.root)
    page.label = "Canvas"
    page.grid(column=0, row=0,sticky ="nsew")
    page.bind("<Configure>", self.resize_handler)
    
    page.grid_columnconfigure(0, weight=1,uniform="page1")
    page.grid_columnconfigure(1, weight=3,uniform="page1")
    page.grid_rowconfigure(0, weight=1)
    self.canvas = tk.Canvas(page, highlightbackground="black",highlightthickness=1)
    self.canvas.grid(column=1, row=0, sticky="nsew")
    self.canvas.grid_rowconfigure(0, weight=1)
    self.canvas.grid_columnconfigure(0, weight=1)
    self.canvas.bind('<Motion>', self.canvas_motion_handler)
    self.canvas.bind('<ButtonPress-1>', self.canvas_click_handler)

    # Create Notebook
    panelBorder = tk.Frame(page, highlightbackground="black",highlightthickness=1)
    panelBorder.grid(column=0, row=0, sticky="nsew")
    panelBorder.grid_rowconfigure(0, weight=1)
    panelBorder.grid_columnconfigure(0, weight=1)
    panel = ttk.Notebook(panelBorder, style="CanvasPage.TNotebook")

    # Info Box
    infoBox = ttk.Frame(self.canvas)
    infoBox.grid()
    ttk.Label(infoBox, text="Welcome to Virgo").grid()
    ttk.Label(infoBox, text="Use the top menu to open a file and get started").grid()
    self.canvasIcon = PIL.ImageTk.PhotoImage(self.iconBase.resize((64, 64)))
    ttk.Label(self.canvas, image=self.canvasIcon, width=10).grid(row=0, column=0, sticky="ne", padx=10, pady=10)

    # Widget panel and config panel in notebook
    self.widgetMenu = tk.Frame(panel)
    self.configMenu = tk.Frame(panel)
    

    # Widget Menu Code
    self.widgetMenu.grid_rowconfigure(0, weight=1)
    self.widgetMenu.grid_columnconfigure(0, weight=1)

    widgets = scrollable_frame.ScrollableFrame(self.widgetMenu)
    widgetsFrame = widgets.get()
    
    #List of different widgets to add to the canvas
    ttk.Label(widgetsFrame, text="Data:", style="H3.TLabel").grid()
    ttk.Button(widgetsFrame, text="Add a Data Source", command=lambda x=base_nodes.DataSourceNode: self.add_source_node_to_canvas(x)).grid()

    ttk.Label(widgetsFrame, text="Graph Type:", style="H3.TLabel").grid()
    for nodeType in graphical.__all__:
        ttk.Button(widgetsFrame, text="add {}:".format(nodeType.description), command=lambda x=nodeType: self.add_node_to_canvas(x)).grid()

    ttk.Label(widgetsFrame, text="Functions:", style="H3.TLabel").grid()
    for nodeType in functional.__all__:
        ttk.Button(widgetsFrame, text="{}".format(nodeType.description), command=lambda x=nodeType: self.add_node_to_canvas(x)).grid()

    ttk.Button(widgetsFrame, text="Run Canvas", command=self.run_canvas).grid(pady=20)
    ttk.Button(widgetsFrame, text="Clear Canvas", command=self.clear_canvas).grid(pady=20)
   

    # Configurations Code
    self.configMenu.grid_rowconfigure(0, weight=1)
    self.configMenu.grid_columnconfigure(0, weight=1)
    config = scrollable_frame.ScrollableFrame(self.configMenu)
    configFrame = config.get()

    ttk.Label(configFrame, text="Prebuilt Configurations", style="H3.TLabel").grid()
    try:
        #TODO:  Dont hard code this for max & linux
        configPaths = os.listdir("configurations")
    except Exception as e:
        print(e)
        configPaths = []
    for path in configPaths:
        if ".virgo" in path:
            with open(os.path.join("configurations",path), "r") as file:
                #TODO: redundant load> low priority
                json_data = file.read()
                data = json.loads(json_data)
                title = data["metadata"]["title"] if "metadata" in data and "title" in data["metadata"] else "Untitled"
                description = data["metadata"]["description"] if "metadata" in data and "description" in data["metadata"] else "No description"
            ttk.Button(configFrame,text="{}".format(title), command=lambda x=f"configurations/{path}": self.load_canvas(x)).grid()
            ttk.Label(configFrame, text=f"info: {description}\n@ {path}").grid()
    
    def scroll_handler(event):
        tabIdx = panel.index(panel.select())
        if tabIdx == 0:
            widgets.on_mousewheel(event)
        elif tabIdx == 1:
            config.on_mousewheel(event)

    widgets.build(master_scroll=scroll_handler)
    config.build(master_scroll=scroll_handler)
    
    widgets.grid(column=0, row=0, sticky="nsew")
    config.grid(column=0, row=0, sticky="nsew")

    def tab_change_handler(event):
        widgets.hackyRefresh()
        config.hackyRefresh()
        self.root.update_idletasks()
        # pass
    panel.bind('<<NotebookTabChanged>>', tab_change_handler)
    panel.add(self.widgetMenu, text='Nodes') 
    panel.add(self.configMenu, text='Configurations') 
    panel.grid(column=0, row=0, sticky="nsew")
    return page