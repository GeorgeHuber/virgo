import tkinter as tk
from tkinter import ttk
import sys
import virgo.utils as utils

class ScrollableFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self)
        self.hackyRefreshRect = None
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        self.frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window(0, 0, anchor="nw", window=self.frame)
        self.frame.bind("<Configure>", self.on_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        os_type = sys.platform
        self.offset = 1.2 if os_type == "darwin" else 120

    def on_mousewheel(self, e):
        # Normalize mouse wheel event delta for cross-platform compatibility
        delta = -1 * (e.delta // self.offset)
        self.canvas.yview_scroll(int(delta), "units")
        self.canvas.update_idletasks()

    def on_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get(self):
        return self.frame
    
    def build(self, master_scroll=None):
        self.id = self.canvas.create_window(0, 0, anchor="nw", window=self.frame, tags="scroll")
        utils.bind_all_recur(self)
        if master_scroll:
            self.canvas.bind_class(self.id, "<MouseWheel>", master_scroll)
        else:
            self.canvas.bind_class(self.id, "<MouseWheel>", self.on_mousewheel)

    def hackyRefresh(self):
        if self.hackyRefreshRect:
            self.canvas.delete(self.hackyRefreshRect)
        self.hackyRefreshRect =  self.canvas.create_rectangle(0,0,10,10,fill="blue")