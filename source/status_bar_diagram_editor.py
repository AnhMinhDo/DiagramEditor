import tkinter as tk
import tkinter.ttk as ttk
import os
import requests


class StatusBarDiaEdit(ttk.Frame):
    def __init__(self, master_frame:ttk.Frame) -> None:
        ttk.Frame.__init__(self,master_frame)
        self.master_frame = master_frame
        # create notification bar
        self.notification = ttk.Label(self, border=1,
                                relief='sunken',
                                anchor='w',
                                width=20)
        self.notification.pack(side='left',padx=4,pady=2,fill='x',expand=True)
        # create a display for line and column position
        self.cursor_line = '1'
        self.cursor_col = '0'
        self.cursor_line_col = ttk.Label(self,
                                  relief="flat",
                                  anchor='w',
                                  text=f'Line {self.cursor_line}, Col {self.cursor_col}')
        self.cursor_line_col.pack(side='left',
                           fill='both',
                           expand=False,
                           padx=4)
        # create a display for internet connection
        self.wifi_on_icon_path: str = "./data/icons/wifi_on.png"
        self.wifi_on_icon: tk.PhotoImage = tk.PhotoImage(file=self.wifi_on_icon_path)
        self.wifi_off_icon_path: str = "./data/icons/wifi_off.png"
        self.wifi_off_icon: tk.PhotoImage = tk.PhotoImage(file=self.wifi_off_icon_path)
        
        self.internet_status = ttk.Label(self,
                                  relief="flat",
                                  anchor='center',
                                  text="On",
                                  image=self.wifi_on_icon,
                                  compound='left')
        self.internet_status.pack(side='left',
                           fill='both',
                           expand=False,
                           padx=4)
        
        # create progess bar
        self.pb = ttk.Progressbar(self,
            length=60,mode='determinate')
        self.pb.configure(value=100)
        self.pb.pack(side='right',padx=4,pady=2)


    def set(self, format, *args):
      self.notification.config(text=format % args)
      self.master_frame.update_idletasks()

    def clear(self):
      self.notification.config(text="")
      self.master_frame.update_idletasks()

    def progress(self,n):
      self.pb.configure(value=n)
      self.master_frame.update_idletasks()  

    def update_ln_col(self, cursor_index: str) -> None:
        line, col = cursor_index.split(sep='.')
        self.cursor_line = line
        self.cursor_col = col
        self.cursor_line_col.config(text=f'Line {self.cursor_line}, Col {self.cursor_col}')
        self.master_frame.update_idletasks()

    def update_internet_status(self) -> None:
        try:
           requests.get("https://www.google.com", timeout=5)
           self.internet_status.config(text="On",
                                       image=self.wifi_on_icon)
           self.master_frame.update_idletasks()
        except requests.ConnectionError:
           self.internet_status.config(text="Off",
                                       image=self.wifi_off_icon)
           self.master_frame.update_idletasks()
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Display Diagram")
    root.geometry("800x600")
    statusFrame = ttk.Frame(root)
    statusFrame.pack(fill = 'both', expand = True, side='top')
    app = StatusBarDiaEdit(statusFrame)
    app.pack(side='bottom', fill='x', expand=False)
    app.update_internet_status()
    root.mainloop()
