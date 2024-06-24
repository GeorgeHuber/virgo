import matplotlib

from .app import App
import tkinter as tk

"""TODOS:
    Support multiple edges
    backtrace edges to account for readjustment on two way connections
    Make debug env variable
"""
DEBUG = False


def main():
    matplotlib.use('agg')  
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()