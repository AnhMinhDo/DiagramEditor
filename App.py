import os
import sys
import tkinter as tk
from source.DiagramEditor import DiagramEditor


if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1200x700")
    app = DiagramEditor(root)
    root.title("Diagram Editor")
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            app.file_open(sys.argv[1])
    app.mainLoop()
