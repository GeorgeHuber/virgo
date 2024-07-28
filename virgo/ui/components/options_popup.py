import tkinter as tk
from tkinter import ttk
from virgo import utils
from virgo.ui.components import node_buttons

import cartopy
import matplotlib.pyplot as plt

OPTIONS = {
    "cmap":[
        "bwr",
        "coolwarm",
        "viridis",
        'plasma',
        'inferno',
        'magma', 
        'cividis',
        'rainbow',
        'ocean',
        'brg',
        'copper',

    ],
    "projection":[
        "PlateCarree",
        "Mercator",
        "NorthPolarStereo",
        "SouthPolarStereo",
        "Geostationary",
        'InterruptedGoodeHomolosine',
        "EckertI",
        "Hammer",
        "Aitoff",
        "RotatedPole"
    ],
    "defaultName":[
        "True",
        "False"
    ],
    "name":"Untitled"
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
                elif isinstance(allowed, str):
                    optionDict[optionName] = OPTIONS[optionName]
                    self.optionVars[optionName] = tk.StringVar(value=OPTIONS[optionName])
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
                elif isinstance(allowed, str):
                    self.optionVars[optionName].set(options[optionName])
    def get(self):
        res = {}
        for optionName in self.options:
            value = self.options[optionName]
            #value stored is an index for main array
            if isinstance(value, int):
                value = OPTIONS[optionName][value]
                if optionName == 'cmap':
                    res[optionName] = getattr(plt.cm, value)
                elif optionName == 'projection':
                    res[optionName] =  getattr(cartopy.crs, value)
                else:
                    res[optionName] = value
            #handle string case
            else:
                res[optionName] = value
        if "defaultName" not in res:
            res["defaultName"] = 'True'
        return res
    def show(self,*args,**kwargs):
        print(self.options)
        self.frame = tk.Toplevel(self.node.app.root, *args, padx=6, pady=10, **kwargs)
        self.frame.geometry('300x500')
        self.frame.protocol("WM_DELETE_WINDOW", self.outro)
        tk.Label(self.frame, text="Options Menu").grid()
        if not self.options:
            tk.Label(self.frame, text="No options specified for widget.")
            return
        #Supports list dropdown options
        for optionName in self.options:
            value = self.options[optionName]
            #value stored is an index for main array
            if isinstance(value, int):
                tk.Label(self.frame, text=optionName+": ").grid()
                optionSelect = ttk.OptionMenu(self.frame, self.optionVars[optionName])
                optionSelect.grid()
                for i, optionValue in enumerate(OPTIONS[optionName]):
                    optionSelect['menu'].add_command(label=optionValue, command=lambda name=optionName, i=i: self.list_option_change(name, i))
            #assume its a string
            elif isinstance(value, str):
                tk.Label(self.frame, text=optionName+": ").grid()
                optionSelect = ttk.Entry(self.frame, textvariable=self.optionVars[optionName], validate="focusout", validatecommand=lambda name=optionName: self.list_option_change(name) or True)
                optionSelect.grid()

    def list_option_change(self, name, i=0):
        if isinstance(OPTIONS[name], list):
            self.optionVars[name].set(OPTIONS[name][i])
            self.options[name] = i
        elif isinstance(OPTIONS[name], str):
            self.options[name] = self.optionVars[name].get()
    def outro(self):
        for optionName in self.optionVars:
            val = self.optionVars[optionName].get()
            if isinstance(self.options[optionName], str):
                self.options[optionName] = val
        self.frame.destroy()
        