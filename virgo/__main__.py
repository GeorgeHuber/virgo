import matplotlib

from .app import App
import tkinter as tk

"""TODOS:
    Support multiple edges
    backtrace edges to account for readjustment on two way connections
    Make debug env variable rather than hard coding
    Delete node functionality
"""

if __name__ == "__main__":
    matplotlib.use('agg')  
    root = tk.Tk()
    app = App(root)
    root.mainloop()