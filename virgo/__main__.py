import matplotlib

from .app import App
import tkinter as tk
from tkinter import ttk

"""TODOS:
    Delete node functionality
    Styling!!!!
    Tooltips above each widget
    Know that you opened the file
    Function to slice/index data
    Save graph files
    Ensure 1 input max connections
    
    BUGS:
    Selection of a data file affects placement on screen of widgets


    DONE:
    Move functional node to bottom of options panel
    Glitch when selecting the dropdown
    Glitch when going out of the window and back in
    Support multiple edges
    Backtrace edges to account for readjustment on two way connections
    Make debug env variable rather than hard coding
"""

if __name__ == "__main__":
    matplotlib.use('agg')  
    root = tk.Tk()
    app = App(root)
    root.mainloop()