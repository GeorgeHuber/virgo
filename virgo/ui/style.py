from tkinter import ttk

def build_style():
    s = ttk.Style()
    s.configure(
        ".",
        font=('Noto Sans Tagalog', 14),
        foreground="black"
                )
    s.configure(
        'H3.TLabel', 
        foreground="black",
        font='serif 16',
        )
    return s