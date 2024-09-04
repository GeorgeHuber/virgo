from __future__ import annotations

from tkinter import ttk
import tkinter as tk
import os, json, PIL

from virgo.nodes import base_nodes, graphical, functional
from virgo.ui.components import scrollable_frame
from virgo import utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from virgo.app import App

def Page(self: App):
    page = tk.Frame(self.root)
    page.label = "Canvas"
    page.grid(column=0, row=0, sticky="nsew")
    page.bind("<Configure>", self.resize_handler)
    
    page.grid_columnconfigure(0, weight=1, uniform="page1")
    page.grid_columnconfigure(1, weight=3, uniform="page1")
    page.grid_rowconfigure(0, weight=1)
    
    self.canvas = tk.Canvas(page, highlightbackground="black", highlightthickness=1)
    self.canvas.grid(column=1, row=0, sticky="nsew")
    self.canvas.grid_rowconfigure(0, weight=1)
    self.canvas.grid_columnconfigure(0, weight=1)
    self.canvas.bind('<Motion>', self.canvas_motion_handler)
    self.canvas.bind('<ButtonPress-1>', self.canvas_click_handler)

    # Create Notebook
    panelBorder = tk.Frame(page, highlightbackground="black", highlightthickness=1)
    panelBorder.grid(column=0, row=0, sticky="nsew")
    panelBorder.grid_rowconfigure(0, weight=1)
    panelBorder.grid_columnconfigure(0, weight=1)

    buttonFrame = tk.Frame(panelBorder)
    ttk.Button(buttonFrame, text="Run Canvas", command=self.run_canvas).grid(pady=12)
    ttk.Button(buttonFrame, text="Clear Canvas", command=self.clear_canvas).grid(pady=12)
    buttonFrame.grid(column=0, row=1, sticky="ns")
    panel = ttk.Notebook(panelBorder, style="CanvasPage.TNotebook")

    # Info Box
    self.canvas.create_text(400, 300, text="Welcome to Virgo!\nUse the top menu to open a file and get started")
    self.canvasIcon = PIL.ImageTk.PhotoImage(self.iconBase.resize((64, 64)))
    ttk.Label(self.canvas, image=self.canvasIcon, width=10).grid(row=0, column=0, sticky="ne", padx=10, pady=10)

    # Widget panel and config panel in notebook
    self.widgetMenu = tk.Frame(panel)
    self.configMenu = tk.Frame(panel)

    # Widget Menu Code
    self.widgetMenu.grid_rowconfigure(0, weight=1)  # Make it expandable from top to bottom
    self.widgetMenu.grid_columnconfigure(0, weight=1)
    
    # Create a canvas within the widgetMenu to hold the scrollable content
    canvas = tk.Canvas(self.widgetMenu)
    canvas.grid(row=0, column=0, sticky="nsew")
    
    # Add a vertical scrollbar to the right of the canvas
    scrollbar = ttk.Scrollbar(self.widgetMenu, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Create a frame within the canvas to hold the actual widgets
    widgetsFrame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=widgetsFrame, anchor="nw")
    
    # Populate widgetsFrame with the scrollable content
    ttk.Label(widgetsFrame, text="Data:", style="H3.TLabel").pack(anchor="w", pady=5)
    ttk.Button(widgetsFrame, text="Add a Data Source", command=lambda x=base_nodes.DataSourceNode: self.add_source_node_to_canvas(x)).pack(anchor="w", pady=5)

    ttk.Label(widgetsFrame, text="Graph Type:", style="H3.TLabel").pack(anchor="w", pady=5)
    for nodeType in graphical.__all__:
        ttk.Button(widgetsFrame, text="add {}:".format(nodeType.description), command=lambda x=nodeType: self.add_node_to_canvas(x)).pack(anchor="w", pady=5)

    ttk.Label(widgetsFrame, text="Functions:", style="H3.TLabel").pack(anchor="w", pady=5)
    for nodeType in functional.__all__:
        ttk.Button(widgetsFrame, text="{}".format(nodeType.description), command=lambda x=nodeType: self.add_node_to_canvas(x)).pack(anchor="w", pady=5)

    # Update the scroll region after adding widgets
    widgetsFrame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Bind the scroll functionality to the mouse wheel
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    # Configure the widgetMenu frame to expand
    self.widgetMenu.pack(fill="both", expand=True, padx=10, pady=10)

    # Configurations Code
    self.configMenu.grid_rowconfigure(0, weight=1)
    self.configMenu.grid_columnconfigure(0, weight=1)
    
    # Create a canvas within the configMenu to hold the scrollable content
    canvas_config = tk.Canvas(self.configMenu)
    canvas_config.grid(row=0, column=0, sticky="nsew")
    
    # Add a vertical scrollbar to the right of the canvas
    scrollbar_config = ttk.Scrollbar(self.configMenu, orient="vertical", command=canvas_config.yview)
    scrollbar_config.grid(row=0, column=1, sticky="ns")
    
    # Configure the canvas to work with the scrollbar
    canvas_config.configure(yscrollcommand=scrollbar_config.set)
    
    # Create a frame within the canvas to hold the actual configurations
    configFrame = tk.Frame(canvas_config)
    canvas_config.create_window((0, 0), window=configFrame, anchor="nw")

    # Populate configFrame with the scrollable content
    def build_configurations():
        utils.destroy_children(configFrame)
        ttk.Label(configFrame, text="Prebuilt Configurations", style="H3.TLabel").pack(anchor="w", pady=5)
        
        try:
            configPaths = os.listdir("configurations")
        except Exception as e:
            print(e)
            configPaths = []

        for path in configPaths:
            if ".virgo" in path:
                with open(os.path.join("configurations", path), "r") as file:
                    json_data = file.read()
                    data = json.loads(json_data)
                    title = data["metadata"]["title"] if "metadata" in data and "title" in data["metadata"] else "Untitled"
                    description = data["metadata"]["description"] if "metadata" in data and "description" in data["metadata"] else "No description"

                ttk.Button(configFrame, text="{}".format(title), command=lambda x=f"configurations/{path}": self.load_canvas(x)).pack(anchor="w", pady=5)
                ttk.Label(configFrame, text=f"info: {description}\n@ {path}").pack(anchor="w", pady=5)

    build_configurations()

    # Update the scroll region after adding configurations
    configFrame.update_idletasks()
    canvas_config.config(scrollregion=canvas_config.bbox("all"))
    
    # Bind the scroll functionality to the mouse wheel
    canvas_config.bind_all("<MouseWheel>", on_mousewheel)

    # Configure the configMenu frame to expand
    self.configMenu.pack(fill="both", expand=True, padx=10, pady=10)

    def tab_change_handler(event):
        canvas.config(scrollregion=canvas.bbox("all"))
        widgetsFrame.update_idletasks()
        build_configurations()

    panel.bind('<<NotebookTabChanged>>', tab_change_handler)
    panel.add(self.widgetMenu, text='Nodes') 
    panel.add(self.configMenu, text='Configurations') 
    panel.grid(column=0, row=0, sticky="nsew")
    
    return page