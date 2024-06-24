def destroy_children(parent):
    for widget in parent.winfo_children():
        widget.destroy()

def bind_all_recur(cur, root=None):
    if not root:
        root = cur
    for child in cur.winfo_children():
        child.bindtags((root.id,)+child.bindtags())
        bind_all_recur(child, root)