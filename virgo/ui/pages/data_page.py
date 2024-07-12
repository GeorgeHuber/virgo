from __future__ import annotations

from tkinter import ttk
import tkinter as tk
from virgo import utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from virgo.app import App
def Page(self: App):
    page = tk.Frame(self.root)
    page.label = "Data"
    page.grid(column=0, row=0,sticky ="nsew")
        # page.configure(yscrollcommand=ttk.Scrollbar(page).set)
    # TODO: fix window management adn the current variable
    ttk.Label(page, text="Data Properties").grid(column=0, row=0)
    ttk.Label(page, text="Metadata").grid()
    if self.data:
        for property in self.data.attrs:
            ttk.Label(page, text=property).grid()
            ttk.Label(page, text=self.data.attrs[property]).grid()
    ttk.Label(page, text="Variables").grid()
    if self.data:
        for variable in self.data.variables.keys():
            ttk.Label(page, text=variable).grid()
            try:
                ttk.Label(page, text=self.data.variables[variable].attrs.long_name).grid()
            except:
                pass
    return page