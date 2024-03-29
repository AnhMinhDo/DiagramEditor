import os 
import sys
import re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
import tkinter.filedialog as filedialog
from tkinter import colorchooser
from source.gui_base_class import GuiBaseClass
from source.display_diagram import DisplayDiagram
from source.text_editor import TextEditor
from source.kroki_encoder import KrokiEncoder
from source.settings import Settings
from source.status_bar_diagram_editor import StatusBarDiaEdit
from source.keybindings_TopLevel import Keybinding

class DiagramEditor(GuiBaseClass):
    def __init__(self,root):
        super().__init__(root)

#------View: menu bar--------------------------------------------------------------
        mnu_file=self.getMenu('File')      
        mnu_file.insert_command(0,label=f"Open {'Ctrl O':>20}",
                                underline=0,
                                command=self.file_open)
        
        mnu_file.insert_command(1,label=f"New File {'Ctrl N':>14}",
                                underline=0,
                                command=self.new_file)
        
        mnu_file.insert_command(2,label=f"Save {'Ctrl S':>21}",
                                underline=0,
                                command=self.file_save)
        
        mnu_file.insert_command(3,label="Save As   Ctrl Shift S",
                                underline=0,
                                command=self.file_save_as)
        mnu_help=self.getMenu('Help')
        mnu_help.insert_command(0,label="Keybindings",
                                underline=0,
                                command=self.show_keybindings)
        

        # Add options menu for changing background
        menu_options = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=menu_options, label='Options')
        self.menu['options'] = menu_options

        #In Menu Options add changing background options
        menu_backgrounds=tk.Menu(menu_options)
        menu_options.add_cascade(menu=menu_backgrounds, label='Background', underline=0)
        menu_backgrounds.insert_command(0,label='Choose Background Color', command= self.backgroundcolor,underline=0)
        menu_backgrounds.insert_command(1,label='Default Background Color', command=self.whitebackground, underline=0)

        # In Menu Options add changing foreground options
        menu_textcolor = tk.Menu(menu_options)
        menu_options.add_cascade(menu=menu_textcolor, label='Text Color', underline=0)
        menu_textcolor.insert_command(0,label='Choose Text Color', command=self.text_color, underline=0)
        menu_textcolor.insert_command(1,label='Default Text Color', command=self.textblack, underline=0)

# parent Frame for both convert-to-Image frame and search frame---------------------
        self.utilities_frame = ttk.Frame(self.frame)
        self.utilities_frame.pack(fill = 'both',
                                expand = False,
                                side='top',
                                padx=5)
#-------View: Convert-to-Image frame-------------------------------------------------------------------------------
        # add convert-to-Image frame
        self.convert2_img_frame = ttk.Frame(self.utilities_frame)
        self.convert2_img_frame.pack(fill = 'both', expand = False, side='left')
        # add button convert2_image
        self.text2_image_icon_path: str = "./data/icons/imaging.png"
        self.text2_image_icon: tk.PhotoImage = tk.PhotoImage(file=self.text2_image_icon_path)
        self.button_convert2_image = ttk.Button(self.convert2_img_frame,
                                       text = "Convert to:  ",
                                       image = self.text2_image_icon,
                                       command=self.convert2_image_button_func,
                                       compound=tk.LEFT)
        self.button_convert2_image.pack(side = 'left', fill = 'none', expand = False)
        # add combobox to function frame
        self.diagram_type_list: list = ["plantuml","erd",
                            "graphviz", "ditaa",
                            "mermaid", "TikZ",
                            "Vega", "wireviz",
                            "UMLet", "BlockDiag",
                            "SeqDiag", "ActDiag",
                            "NwDiag", "PacketDiag",
                            "RackDiag", "Structurizr"]
        self.combobox: ttk.Combobox = ttk.Combobox(self.convert2_img_frame,
                                     state = 'readonly',
                                     values=self.diagram_type_list,
                                     width=15)
        self.combobox.pack(side = 'left', fill = 'y', expand = False)
        self.combobox.set(self.diagram_type_list[0])

#------View:search frame-------------------------------------------------------------
        # add search frame
        self.search_frame = ttk.Frame(self.utilities_frame)
        self.search_frame.pack(fill = 'both', expand = False, side='right')
        # add entry to search frame
        self.entry_search = ttk.Entry(self.search_frame)
        self.entry_search.pack(side = 'left', fill = 'both', expand = True)
        # add button search to search frame
        self.search_icon_path: str = "./data/icons/search.png"
        self.search_icon: tk.PhotoImage = tk.PhotoImage(file=self.search_icon_path)
        self.button_search = ttk.Button(self.search_frame,
                                       text = "Find Next",
                                       image=self.search_icon,
                                       compound=tk.LEFT,
                                       command=self.search_text)
        self.button_search.pack(side = 'left', fill = 'both', expand = True)
        # add button reset to search frame
        self.reset_icon_path: str = "./data/icons/broom.png"
        self.reset_icon: tk.PhotoImage = tk.PhotoImage(file=self.reset_icon_path)
        self.button_reset = ttk.Button(self.search_frame,
                                       text="Clear Search",
                                       image=self.reset_icon,
                                       compound=tk.LEFT,
                                       command=self.reset_search_text)
        self.button_reset.pack(side = 'left', fill = 'both', expand = True)

#------View: text widget and display Image frame-----------------------------
        # Create panedwindow
        self.panwind = tk.PanedWindow(self.frame)
        self.panwind.pack(fill="both", expand=True,padx=4)

        # Create textWidget
        self.text = TextEditor(self.panwind)

        #Create ImageWidget
        self.imagewidget = DisplayDiagram(self.panwind, "right")

        # Add text and imagewidget to panedwindow
        self.panwind.add(self.text)
        self.panwind.add(self.imagewidget.image_widget)
   
        # config the initial size of frame inside panedWindow
        self.panwind.paneconfigure(self.text, width=600)
     
        # Add image to imagewidget window
        self.imagewidget.load_image("./data/icons/diagram.png")

#-------------------View: Focus Mode Frame------------------------------------------------------        
        # add focus_mode frame
        self.focus_mode_frame = tk.Frame(self.frame)
        self.focus_mode_frame.pack(fill = 'both', expand = False, side='top')
        # add button left_minimizing to focus_mode frame
        self.left_arrow_icon_path: str = "./data/icons/left-arrow.png"
        self.left_arrow_icon: tk.PhotoImage = tk.PhotoImage(file=self.left_arrow_icon_path)
        self.button_left_minimizing = ttk.Button(self.focus_mode_frame,
                                       image=self.left_arrow_icon,
                                       command=self.left_minimizing)
        self.button_left_minimizing.pack(side = 'left', fill = 'x', expand = False)
        # add button even_split to focus_mode frame
        self.split_icon_path: str = "./data/icons/split.png"
        self.split_icon: tk.PhotoImage = tk.PhotoImage(file=self.split_icon_path)
        self.button_even_split = ttk.Button(self.focus_mode_frame,
                                       image=self.split_icon,
                                       command=self.even_split)
        self.button_even_split.pack(side = 'left', fill = 'x', expand = False)
        # add button right_minimizing to focus_mode_frame
        self.right_arrow_icon_path: str = "./data/icons/right-arrow.png"
        self.right_arrow_icon: tk.PhotoImage = tk.PhotoImage(file=self.right_arrow_icon_path)
        self.button_right_minimizing = ttk.Button(self.focus_mode_frame,
                                       image=self.right_arrow_icon,
                                       command=self.right_minimizing)
        self.button_right_minimizing.pack(side = 'left', fill = 'x', expand = False)

        # add button focus_mode to focus_mode_frame
        self.focus_mode_icon_path: str = "./data/icons/levitation.png"
        self.focus_mode_icon: tk.PhotoImage = tk.PhotoImage(file=self.focus_mode_icon_path)
        self.button_focus_mode = ttk.Button(self.focus_mode_frame,
                                       text = "Focus Mode",
                                       image=self.focus_mode_icon,
                                       compound=tk.LEFT,
                                       command=self.focus_mode)
        self.button_focus_mode.pack(side = 'right', fill = 'both', expand = False)

#--------View: Status Bar Frame--------------------------------------------------------
        # create the statusbar
        self.stbar = StatusBarDiaEdit(self.frame)
        self.stbar.pack(side="bottom", fill="x")
        self.stbar.set(format="Waiting ......")
        

#----------------instance attributes-------------------------------------------------------
        # setting file stores state of the Application
        self.setting_info: Settings = Settings("./setting.yaml")
        self.filename: str = self.setting_info.get_setting("filename")
        self.previous_dir = None if self.filename is None else os.path.dirname(self.filename)
        self.file_dialog = None

        # Store kroki diagram state
        self.kroki_diagram = None
        
#---------KEYS BINDING --------------------------------------------------------------------
        # open file
        self.root.bind("<Control-o>", self.file_open)
        # open file
        self.root.bind("<Control-n>", self.new_file)
        # save file
        self.root.bind("<Control-s>", self.file_save)
        # save file as
        self.root.bind("<Control-Shift-S>", self.file_save_as)
        # convert to image
        self.root.bind("<Control-Alt-n>", self.convert2_image_button_func)
        # search
        self.root.bind("<Control-Alt-s>", self.search_text)
        # switch to search entry
        self.root.bind("<Control-f>", self.switch2_search_entry)
        # Turn on focus mode
        self.root.bind("<Control-k><f>", self.focus_mode)
        # minimize right window
        self.root.bind("<Control-Right>", self.right_minimizing)
        # minimize left window
        self.root.bind("<Control-Left>", self.left_minimizing)
        # split window
        self.root.bind("<Control-Down>", self.even_split)

        # Update cursor position
        self.text.bind_event("<ButtonRelease-1>", self.update_cursor_position)
        self.text.bind_event("<KeyRelease>", self.update_cursor_position)

        
#---------Open previous saved working state---------------------------------------------
        # self.open_previous_file()
        self.open_previous_file()

#---------Recurrent tasks---------------------------------------------------------
        # self.root.after(5000, self.connection_status)
        self.connection_status()
#---------METHODS: OPEN, SAVE FILE--------------------------------------------------------------------
    def file_open(self,event=None):
        self.filename=filedialog.askopenfilename(initialdir=self.previous_dir)
        if self.filename != "":
            self.text.delete('1.0','end')
            with open(self.filename,"rt") as file:
                for line in file:
                    self.text.insert("end",line)
            self.stbar.set(f"File {self.filename} was opened!")
            self.setAppTitle(self.filename)
            self.convert2_image()
            self.setting_info.set_setting("filename" , self.filename)
            self.setting_info.set_setting("diagram_type" , self.combobox.get())
            self.previous_dir= os.path.dirname(self.filename)
            self.setting_info.save_settings()

    def new_file(self, event=None) -> None:
        self.file_dialog=filedialog.asksaveasfilename( 
                                    initialdir=self.previous_dir,
                                    filetypes= [("plantuml",".pml"),
                                                ("erd",".erd"),
                                                ("text",".txt"),
                                                ("other",".*")],
                                    defaultextension="text"
                                    )
        if self.file_dialog!= "" :
            self.filename=self.file_dialog
            self.previous_dir=os.path.dirname(self.filename)
            with open(self.filename, "w"):
                pass
            self.text.delete('1.0','end')
            with open(self.filename,"rt") as file:
                for line in file:
                    self.text.insert("end",line)
            self.stbar.set(f"File {self.filename} was opened!")
            self.setting_info.set_setting("filename", self.filename)
    
    def file_save(self, event=None) -> None:
        if self.filename is not None:
            with open(self.filename,"w", encoding="utf-8") as file:
                file.write(self.text.get("0.0","end"))
            self.setAppTitle(self.filename)      
        else :
            self.file_save_as()

    def file_save_as(self, event=None) -> None:
        self.file_dialog=filedialog.asksaveasfilename( 
                                    initialdir=self.previous_dir,
                                    filetypes= [("plantuml",".pml"),
                                                ("erd",".erd"),
                                                ("text",".txt"),
                                                ("other",".*")],
                                    defaultextension=("text",".txt")
                                    )
        if self.file_dialog!= None :
            self.filename=self.file_dialog.name
            self.previous_dir=os.path.dirname(self.filename)
            self.file_save()

    def open_previous_file(self) -> None:
        if self.filename != "":
            if os.path.exists(self.filename):
                self.saved_dia_type: str = self.setting_info.get_setting("diagram_type")
                self.combobox.set(self.diagram_type_list[self.diagram_type_list.index(self.saved_dia_type)])
                self.text.delete('1.0','end')
                with open(self.filename,"rt") as file:
                    for line in file:
                        self.text.insert("end",line)
                self.stbar.set(f"File {self.filename} was opened!")
                self.setAppTitle(self.filename)
                self.convert2_image()
            else:
                self.stbar.set(f"File {self.filename} does not exist")
#-------METHOD CONVERT TEXT DIAGRAM TO IMAGE-----------------------------------------------    
    def convert2_image(self,event=None) -> None:
        # instantiate a KrokiEncoder instance: filepath, diagram type, image type is png
        self.kroki_diagram = KrokiEncoder(self.filename,
                                        self.combobox.get().lower(),
                                        "png")
        imgfile_png = re.sub(".[a-z]+$",".png",self.filename)
        self.setting_info.set_setting("diagram_type", self.combobox.get())
        if self.kroki_diagram.error_message is None:
            #write image to file
            self.kroki_diagram.export_image(imgfile_png)
            #show image in ImageWidget
            if os.path.exists(imgfile_png):
                    self.imagewidget.update_image(imgfile_png)
                    self.stbar.set(f"Displaying {imgfile_png}")
        else:
            self.imagewidget.display_text(self.kroki_diagram.error_message)

    def convert2_image_button_func(self, event=None) -> None:
        # instantiate a KrokiEncoder instance: filepath, diagram type, image type is png
        self.file_save()
        self.convert2_image()

#--------METHOD SEARCH------------------------------------------------------
    def search_text(self, event=None) -> None:
        if self.text.query != self.entry_search.get(): # when users change the query string while clicking the find-Next button for current query.
            self.text.query = self.entry_search.get()
            self.text.remove_highlight()
        self.text.search_query()

    def reset_search_text(self,event=None) -> None:
        self.text.remove_highlight()
        self.entry_search.delete("0","end")

    def switch2_search_entry(self, event=None) -> None:
        self.entry_search.focus_set()

#-------METHODS: left/right/even_split minimizing -------------------------------------------------
    def get_win_width(self, event=None) -> int:
        return self.frame.winfo_width()
  
    def left_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=5,y=100) # 5 pixels from the left and 100 pixels from top

    def right_minimizing(self,event=None) -> None:
        sash_x: int = int(self.get_win_width() - 5)
        self.panwind.sash_place(0,x=sash_x,y=100) 

    def even_split(self,event=None) -> None:
        sash_x: int = int(self.get_win_width() / 2)
        self.panwind.sash_place(0,x=sash_x,y=100)

#-------METHODS: change color ----------------------------------------------------------
    def text_color(self,event=None) -> None:
        choose_color=colorchooser.askcolor()
        self.text.config_text_editor(fg=choose_color[1])

    def textblack(self,event=None) -> None:
        self.text.config_text_editor(fg="black")

    def backgroundcolor(self,event=None) -> None:
        choose_color=colorchooser.askcolor()
        self.text.config_text_editor(background=choose_color[1])

    def whitebackground(self,event=None) -> None:
        self.text.config_text_editor(background="white")

    def change2_light_mode_color(self,event=None) -> None:
        pass

    def change2_dark_mode_color(self,event=None) -> None:
        pass

#--------------------METHODS: Focus Mode -------------------------------------------------------       
    def focus_mode(self,event=None) -> None:
        if self.convert2_img_frame.winfo_ismapped():
            # hide the search frame
            self.utilities_frame.pack_forget()
            # change to dark mode
            self.change2_dark_mode_color()
        else:
            self.utilities_frame.pack(before=self.panwind,
                                    fill = 'both',
                                   expand = False,
                                   side='top')
            self.change2_light_mode_color()

#-------METHODS: statusbar----------------------------------------------------
    def update_cursor_position(self, event=None) -> None:
        self.stbar.update_ln_col(self.text.index("insert"))
        self.root.update_idletasks()

    def connection_status(self) -> None:
        self.stbar.update_internet_status()
        self.root.after(5000, self.connection_status)

#-------METHODS: Show keybindings----------------------------------------------------
    def show_keybindings(self,event=None) -> None:
        Keybinding(root=self.root)
#-------OTHER METHODS----------------------------------------------------------

    def About(self,event=None) -> None:
        mbox.showinfo(
            title="About Diagram Editor",
            message="Diagram Editor\nAuthor: Anh-Minh Do\nEmail: ahd.minh@gmail.com\nPotsdam, Germany\n2023")


if __name__ == '__main__':
    print("this is a module for import only")

# Author: Anh-Minh Do, 01.2024, Potsdam, Germany
# License: MIT
