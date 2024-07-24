import matplotlib

from .app import App
import tkinter as tk
from tkinter import ttk
import xarray as xr

"""TODOS:
    Styling!!!!
    Tooltips above each widget
    Ensure 1 input max connections
    
    BUGS:
    Selection of a data file affects placement on screen of widgets
    some canvasses do not load properly if the screen 
    is too small. Likely the x,y are not correct for tk window offscreen, good luck :)


    DONE:
    Delete node functionality
    Move functional node to bottom of options panel
    Glitch when selecting the dropdown
    Glitch when going out of the window and back in
    Support multiple edges
    Backtrace edges to account for readjustment on two way connections
    Make debug env variable rather than hard coding
    Know that you opened the file
    Function to slice/index data
    Save graph files
"""

if __name__ == "__main__":
    matplotlib.use('agg')  
    xr.set_options(keep_attrs=True)
    root = tk.Tk()
    app = App(root)
    root.mainloop()