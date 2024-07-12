import tkinter as tk
def destroy_children(parent):
    for widget in parent.winfo_children():
        widget.destroy()

def bind_all_recur(cur, root=None, exclude=[]):
    if not root:
        root = cur
    for child in cur.winfo_children():
        if child not in exclude:
            child.bindtags((root.id,)+child.bindtags())
            bind_all_recur(child, root, exclude=exclude)

def index(arr, elem, comparator=lambda x,y:x==y):
    for i in range(len(arr)):
        x = arr[i]
        if comparator(x, elem):
            return i
    return -1