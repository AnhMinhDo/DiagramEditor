import os 
import sys
import re
import tkinter as tk
import tkinter.ttk as ttk

class Keybinding(tk.Toplevel):
    def __init__(self, root=None, **kwargs) -> None:
        super().__init__(root, **kwargs)
        # set window title create new file
        self.title("Key bindings - shortcuts")
        # add a treeview widget
        self.keybind_table: ttk.Treeview = ttk.Treeview(self,
                                                        columns=('command', 'keybinding'),
                                                        show="headings")
        self.keybind_table.heading('command', text='Command')
        self.keybind_table.heading('keybinding', text='Keybindings')
        self.keybind_table.pack(fill="both",expand=True, padx=2, pady=2)
        # add keybindings
        self.shortcuts = [('Open File', 'Ctrl + O'),
                          ('Create New File', 'Ctrl + N'),
                          ('Save File', 'Ctrl + S'),
                          ('Save File As', 'Ctrl + shift + S'),
                          ('Convert Text to Image', 'Ctrl + Alt + N'),
                          ('Focus to search box', 'Ctrl + F'),
                          ('Find Next', 'Ctrl + Alt + S'),
                          ('Focus Mode', 'Ctrl + K F'),
                          ('Minimize left window', 'Ctrl + Left arrow'),
                          ('Minimize right window', 'Ctrl + Right arrow'),
                          ('Split windows', 'Ctrl + Down arrow')]
        for row in self.shortcuts:
            self.keybind_table.insert('','end',values=row)
        self.transient(root)

if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    root.geometry("800x600")
    shortcuts_list = Keybinding(root=root)
    root.mainloop()

# Author: Anh-Minh Do, 12.2023, Potsdam, Germany
# License: MIT