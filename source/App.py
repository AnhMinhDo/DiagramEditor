import tkinter as tk
from DiagramEditor import DiagramEditor
import os
import sys

def main() -> int:
    root=tk.Tk()
    root.geometry("1200x700")
    pedit = DiagramEditor(root)
    root.title("PumlEditor 2023")
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            pedit.file_open(sys.argv[1])
    pedit.mainLoop()
    return 0

if __name__ == "__main__":
    main()