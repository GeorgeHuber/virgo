import tkinter as tk
from tkinter import ttk

class OutButton(tk.Frame):
    def __init__(self, parent, text, outVar, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.button = ttk.Button(self, command=lambda x=outVar:self.app.node_select_handler(x), padding=1)
        self.button.grid(sticky="e")
        self.setText(text)
    def setText(self, newText):
        self.button["text"] = "{}->".format(newText)

class InButton(tk.Frame):
    def __init__(self, parent, text, inVar, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.button = ttk.Button(self, command=lambda x=inVar:self.app.node_select_handler(x), padding=1)
        self.button.grid(sticky="w")
        self.setText(text)
    def setText(self, newText):
        self.button["text"] = "<-{}".format(newText)
        