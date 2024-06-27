import matplotlib

from .app import App
import tkinter as tk

"""TODOS:
    Support multiple edges
    backtrace edges to account for readjustment on two way connections
    Make debug env variable rather than hard coding
    Delete node functionality
    Styling!!!!
    Tooltips above each widget
    Know that you opened the file
    Function to slice/index data
    Move functional node to bottom of options panel
    Save graph files: 
    Ensure 1 input max connections
    Glitch when selecting the dropdown
    Glitch when going out of the window and back in
"""

if __name__ == "__main__":
    matplotlib.use('agg')  
    root = tk.Tk()
    app = App(root)
    root.mainloop()