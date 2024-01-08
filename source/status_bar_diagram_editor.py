import tkinter as tk
import tkinter.ttk as ttk
import os

class StatusBarDiaEdit(ttk.Frame):
    def __init__(self, master_frame:ttk.Frame) -> None:
        ttk.Frame.__init__(self,master_frame)
        self.label = ttk.Label(self, border=1,
                                relief='sunken',
                                anchor='w',
                                width=50)
        self.label.pack(side='left',padx=4,pady=2,fill='x',expand=True)
        self.pb = ttk.Progressbar(self,
            length=60,mode='determinate')
        self.pb.configure(value=30)
        self.pb.pack(side='right',padx=4,pady=2)
        self.master_frame=master_frame

    def set(self, format, *args):
      self.label.config(text=format % args)
      self.master.update_idletasks()

    def clear(self):
      self.label.config(text="")
      self.master.update_idletasks()

    def progress(self,n):
      self.pb.configure(value=n)
      self.master.update_idletasks()  

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Display Diagram")
    root.geometry("800x600")
    statusFrame = ttk.Frame(root)
    statusFrame.pack(fill = 'both', expand = True, side='top')
    app = StatusBarDiaEdit(statusFrame)
    root.mainloop()

# Author: Anh-Minh Do, 01.2024, Potsdam, Germany
# License: MIT
