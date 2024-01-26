import os 
import sys
import re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

class NewFile(tk.Toplevel):
    filename_class_attribute: str = ""

    def __init__(self, initialdir:str|None=None, **kwargs) -> None:
        super().__init__(**kwargs)
        # assign attributes
        self.initialdir: str|None = initialdir
        # set window title create new file
        self.title("Create New File")
        # First Frame
        self.frame1: ttk.Frame = ttk.Frame(self)
        self.frame1.pack(fill="both", expand=False, side='top', padx=5, pady=3)
        self.entry_label: ttk.Label = ttk.Label(self.frame1,
                                                text="New File Name:")
        self.entry_label.pack(fill="x",expand=False,padx=5, side="left")
        self.input_file_name_entry: ttk.Entry = ttk.Entry(self.frame1,
                                validate="key",
                                validatecommand=(self.register(self.checkFileName),'%S'))
        self.input_file_name_entry.pack(fill="x",side="left",padx=4,expand=False)
        
        self.warning_file_name: ttk.Label = ttk.Label(self.frame1,
                text="File name must not contain white space , * : ? < > | \" \' ` ~ () [] ! # @ / \\")
        self.warning_file_name.pack(after=self.input_file_name_entry,
                                    fill="x",
                                    side="left",
                                    padx=5,
                                    expand=False)
        #Second Frame
        self.frame2: ttk.Frame = ttk.Frame(self)
        self.frame2.pack(fill="both", expand=False, side='top', padx=5, pady=3)
        self.choose_dir_btn: ttk.Button = ttk.Button(self.frame2,
                                                     text="Directory",
                                                     command=self.get_directory_path)
        self.choose_dir_btn.pack(fill="x",expand=False,padx=5, side="left")
        self.dir_label: ttk.Label = ttk.Label(self.frame2,
                                              text="")
        self.dir_label.pack(fill="x",expand=False,padx=9, side="left")
        # Third Frame
        self.frame3: ttk.Frame = ttk.Frame(self)
        self.frame3.pack(fill="both", expand=False, side='top', padx=5, pady=3)
        self.diagram_type_label:ttk.Label=ttk.Label(self.frame3, text="Diagram Type:")
        self.diagram_type_label.pack(fill="x",expand=False,padx=5, side="left")
        self.diagram_type_list: list = ["plantuml","erd",
                            "graphviz", "ditaa",
                            "mermaid", "TikZ",
                            "Vega", "wireviz",
                            "UMLet", "BlockDiag",
                            "SeqDiag", "ActDiag",
                            "NwDiag", "PacketDiag",
                            "RackDiag", "Structurizr"]
        self.combobox: ttk.Combobox = ttk.Combobox(self.frame3,
                                     state = 'readonly',
                                     values=self.diagram_type_list,
                                     width=15)
        self.combobox.pack(side = 'left', fill = 'y', expand = False)
        self.combobox.set(self.diagram_type_list[0])
        # create new file button
        self.create_new_file_btn: ttk.Button = ttk.Button(self,
                                                          text="Create New File",
                                                          command=self.set_class_filename)
        self.create_new_file_btn.pack(fill="none",side="top",padx=5, expand=False, pady=3)
        

    def get_directory_path(self, event=None) -> None:
        new_dir_path:str = filedialog.askdirectory(initialdir=self.initialdir)
        self.dir_label.configure(text=new_dir_path)

    def isValidFileName(self, characters: str, event=None) -> bool:
        invalid_character: list = [" ", ",", "*",
                                    ":", "?", "<",
                                    ">", "|", "\"",
                                    "\'", "`", "~",
                                    "#", "@", "!",
                                    "(", ")", "[", "]",
                                    "/", "\\"]
        for char in invalid_character:
            if char in characters:
                return False
        return True
    
    def checkFileName(self, characters: str) -> None:
        is_valid: bool = self.isValidFileName(characters=characters)
        if not is_valid:
            # show error message
            self.warning_file_name.pack(after=self.input_file_name_entry,
                                    fill="x",
                                    side="left",
                                    padx=5,
                                    expand=False)

        else:
            # remove error message
            self.warning_file_name.pack_forget()
        return is_valid
    
    def set_class_filename(self, event=None) -> None:
        # check directory
        if self.dir_label.cget("text") != "" and self.input_file_name_entry.get() != "":
            self.filename_class_attribute = f'{self.dir_label.cget("text")}/{self.input_file_name_entry.get()}'
            self.destroy()
            
    @classmethod
    def askfilename(cls, root: tk.Tk) -> str:
        #create new instance of new file topLevel: the instanace modified the class attribute
        win_ask_file_name: NewFile = cls()
        win_ask_file_name.transient(root)
        root.wait_window(win_ask_file_name)
        # create and assign a new variable the value of the class attribute
        new_file_path: str = cls.filename_class_attribute
        print(new_file_path)
        # reset the class attribute
        cls.filename_class_attribute = ""
        # return the new variable
        print(new_file_path)
        return new_file_path
    

if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    root.geometry("800x600")
    fil: str = NewFile.askfilename(root=root)
    print(fil)
    root.mainloop()
