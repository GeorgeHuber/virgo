import tkinter as tk
from tkinter import ttk
from virgo import utils
from virgo.ui.components import node_buttons

import cartopy

OPTIONS = {
    "cmap":[
        "coolwarm",
        "viridis",
        'plasma',
        'inferno',
        'magma', 
        'cividis'
    ],
    "projection":[
        "PlateCarree",
        "NorthPolarStereo",
        "Mercator",
        "Geostationary",
        'InterruptedGoodeHomolosine',
        "EckertI"
    ]
}

class OptionsManager:
    def __init__(self, node, options=None):
        self.options = self.build_options_dict(options)
        self.node = node
    def build_options_dict(self, options):
        if not options:
            return None
        optionDict = {}
        self.optionVars = {}
        for optionName in options:
            #TODO: support string options
            if optionName in OPTIONS:
                allowed = OPTIONS[optionName]
                if isinstance(allowed, list):
                    optionDict[optionName] = 0
                    self.optionVars[optionName] = tk.StringVar(value=allowed[0])
        return optionDict
    def get_state(self):
        return self.options
    def set_state(self, options):
        self.options = options
        for optionName in options:
            #TODO: support string options
            if optionName in OPTIONS:
                allowed = OPTIONS[optionName]
                if isinstance(allowed, list):
                    self.optionVars[optionName].set(allowed[options[optionName]])
    def get(self):
        res = {}
        for optionName in self.options:
            value = self.options[optionName]
            #value stored is an index for main array
            if isinstance(value, int):
                res[optionName] = OPTIONS[optionName][value]
            #handle string case
            else:
                res[optionName] = value
        return res
    def show(self,*args,**kwargs):
        print(self.options)
        frame = tk.Toplevel(self.node.app.root, *args, padx=6, pady=10, **kwargs)
        tk.Label(frame, text="Options Menu").grid()
        if not self.options:
            tk.Label(frame, text="No options specified for widget.")
            return
        #Supports list dropdown options
        for optionName in self.options:
            value = self.options[optionName]
            #value stored is an index for main array
            if isinstance(value, int):
                tk.Label(frame, text=optionName+": ").grid()
                default = OPTIONS[optionName][self.options[optionName]]
                print(default)
                optionSelect = ttk.OptionMenu(frame, self.optionVars[optionName])
                optionSelect.grid()
                for i, optionValue in enumerate(OPTIONS[optionName]):
                    optionSelect['menu'].add_command(label=optionValue, command=lambda i=i, name=optionName: self.list_option_change(i, name))
    def list_option_change(self, i, name):
        self.optionVars[name].set(OPTIONS[name][i])
        self.options[name] = i
        