import os
import sys
import tkinter as tk
from source.DiagramEditor import DiagramEditor


if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1920x1080")
    app = DiagramEditor(root)
    root.title("PumlEditor 2023")
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            app.file_open(sys.argv[1])
    app.mainLoop()
