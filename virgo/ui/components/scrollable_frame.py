import tkinter as tk
from tkinter import ttk

import virgo.utils as utils

class ScrollableFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self)
        
        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command = self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.bind(
            '<Configure>', self.on_configure
        )
        self.frame = tk.Frame(self.canvas)
    def on_mousewheel(self, e):
        #TODO: make this work on other OS
        self.canvas.yview_scroll(int(-1*(e.delta)), "units")
    def on_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def get(self):
        return self.frame
    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.id = self.canvas.create_window(0, 0, anchor="nw", window=self.frame, tags="scroll")
        #self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        utils.bind_all_recur(self)
        self.canvas.bind_class(self.id, "<MouseWheel>", self.on_mousewheel)