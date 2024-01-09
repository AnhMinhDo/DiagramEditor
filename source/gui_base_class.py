import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
import os
import sys
from source.DGStatusBar import DGStatusBar


class GuiBaseClass():
  def __init__(self,root):
      # create widgets
      self.root=root
      self.root.option_add('*tearOff', False)
      self.menu=dict()
      self.menubar = tk.Menu(root)         
      menu_file = tk.Menu(self.menubar)
      self.menubar.add_cascade(menu=menu_file,label='File',underline=0)
      menu_file.add_separator()
      menu_file.add_command(label='Exit', 
                            command=self.Exit,underline=1)       
      menu_help = tk.Menu(self.menubar)
      self.menubar.add_cascade(menu=menu_help,label='Help',underline=0)
      menu_help.add_command(label='About', command=self.About,underline=0)       
      root.config(menu=self.menubar)


      # ....
      self.menu['menubar'] = self.menubar
      self.menu['File']    = menu_file        
      self.menu['Help']    = menu_help              
      self.frame = ttk.Frame(root)
      self.frame.pack(fill='both',expand=True)

  def setAppTitle(self, filepath):
    self.basename = os.path.basename(filepath)
    self.root.title(self.basename)
  
  def message(self, msg):
    self.status.set(msg)


  # public functions
  def mainLoop(self):
      self.root.mainloop()

  def getFrame(self):
      return(self.frame)  
  
  def getMenu(self,entry):
      if entry in self.menu:
        return (self.menu[entry])
      else:
        # we create a new one
        last = self.menu['menubar'].index('end')   
        self.menu[entry]= tk.Menu(self.menubar)
        self.menu['menubar'].insert_cascade(
          last, menu=self.menu[entry],label=entry)
        return(self.menu[entry])
 
  # private functions
  def Exit(self,ask=True):
      answer = mbox.askyesno(title="Close Application",message="Do you want to quit the application?")
      if answer is True:
          sys.exit(0)
 
  def About(self):
      print("print I am your GuiBaseClass")

if __name__ == '__main__':
    frame=tk.Tk()
    bapp = GuiBaseClass(frame)
    # example for using the BaseClass in other applications
    mnu=bapp.getMenu('Edit')
    mnu.add_command(label='Copy',command=lambda: print('Copy'))  
    # example for using getFrame
    frm=bapp.getFrame()
    btn=ttk.Button(frm,text="Button X",command=lambda: sys.exit(0))
    btn.pack()
    bapp.mainLoop()
