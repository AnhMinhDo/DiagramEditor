import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
from source.GuiBaseClass import GuiBaseClass
import os, sys
import re
import yaml
import tkinter.filedialog as filedialog
from source.DisplayDiagram import DisplayDiagram
from source.TextEditor import TextEditor
from source.KrokiEncoder import KrokiEncoder
from tkinter import colorchooser
from source.Settings import Settings

class DiagramEditor(GuiBaseClass):
    def __init__(self,root):
        super().__init__(root)

#------View: menu bar--------------------------------------------------------------
        mnu_file=self.getMenu('File')      
        mnu_file.insert_command(0,label=f"Open {'Ctrl O':>20}", 
                                underline=0,
                                command=self.file_open)
        
        mnu_file.insert_command(1,label=f"Save {'Ctrl S':>21}", 
                                underline=0, 
                                command=self.file_save)
        
        mnu_file.insert_command(2,label="Save As   Ctrl Shift S", 
                                underline=0, 
                                command=self.file_save_as)
        
        # Add options menu for changing background
        menu_options = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=menu_options, label='Options')
        self.menu['options'] = menu_options
        menu_options.add_separator()
        # Variable to store the checkbutton state
        self.checkbutton_var = tk.BooleanVar(value=True)
        menu_options.add_checkbutton(label='Ask when exit', 
                                     variable=self.checkbutton_var,
                                     command=self.toggle_checkButton)
        
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

        # overwrite windows exit button
        root.protocol('WM_DELETE_WINDOW', self.Exit) 

#-------View: Convert-to-Image frame-------------------------------------------------------------------------------
        # add action frame
        self.convert2_img_frame = ttk.Frame(self.frame)
        self.convert2_img_frame.pack(fill = 'both', expand = False, side='top')
        # add combobox to function frame
        diagram_type: list = ["plantuml","erd",
                            "graphviz", "ditaa",
                            "mermaid", "TikZ",
                            "Vega", "wireviz",
                            "UMLet", "BlockDiag",
                            "SeqDiag", "ActDiag",
                            "NwDiag", "PacketDiag",
                            "RackDiag", "Structurizr"]
        self.combobox = ttk.Combobox(self.convert2_img_frame, 
                                     state = 'readonly', 
                                     values=diagram_type)
        self.combobox.pack(side = 'left', fill = 'x', expand = True)
        self.combobox.set(diagram_type[0])       
        # add button convert2_image
        self.button_convert2_image = ttk.Button(self.convert2_img_frame, 
                                       text = "Convert to Image",
                                       command=self.convert2_image_button_func)
        self.button_convert2_image.pack(side = 'left', fill = 'x', expand = True)
        

#------View:search frame-------------------------------------------------------------
        # add search frame
        self.search_frame = ttk.Frame(self.frame)
        self.search_frame.pack(fill = 'both', expand = False, side='top')
        # add entry to search frame
        self.entry_search = ttk.Entry(self.search_frame)
        self.entry_search.pack(side = 'left', fill = 'x', expand = True)
        # add button search to search frame
        self.button_search = ttk.Button(self.search_frame, 
                                       text = "Find Next",
                                       command=self.search_text)
        self.button_search.pack(side = 'left', fill = 'x', expand = True)
        # add button reset to search frame
        self.button_reset = ttk.Button(self.search_frame, 
                                       text = "Reset Search",
                                       command=self.reset_search_text)
        self.button_reset.pack(side = 'right', fill = 'x', expand = True)
        
#------View: text widget and display Image frame-----------------------------
        # Create panedwindow
        self.panwind = tk.PanedWindow(self.frame)
        self.panwind.pack(fill="both", expand=True)
        
        # Create frame for textWidget
        self.text_frame = ttk.Frame(self.panwind)
        self.text_frame.pack(fill="both", expand=True)
        # Create textWidget
        self.text = TextEditor(self.text_frame, side="left")

        #Create ImageWidget
        self.imagewidget = DisplayDiagram(self.panwind, "right")

        # Add text and imagewidget to panedwindow
        self.panwind.add(self.text_frame)
        self.panwind.add(self.imagewidget.image_widget)
        
        # config the initial size of frame inside panedWindow
        self.panwind.paneconfigure(self.text_frame, width=600)
        
        # Add image to imagewidget window
        self.imagewidget.load_image(".\data\icons\default_icon.png")

#-------------------View: Focus Mode Frame------------------------------------------------------        
        # add focus_mode frame
        self.focus_mode_frame = tk.Frame(self.frame)
        self.focus_mode_frame.pack(fill = 'both', expand = False, side='top')
        # add button left_minimizing to focus_mode frame
        self.button_left_minimizing = ttk.Button(self.focus_mode_frame, 
                                       text = "<-- left",
                                       command=self.left_minimizing)
        self.button_left_minimizing.pack(side = 'left', fill = 'x', expand = True)
        # add button even_split to focus_mode frame
        self.button_even_split = ttk.Button(self.focus_mode_frame, 
                                       text = "| Split |",
                                       command=self.even_split)
        self.button_even_split.pack(side = 'left', fill = 'x', expand = True)
        # add button right_minimizing to focus_mode_frame
        self.button_right_minimizing = ttk.Button(self.focus_mode_frame, 
                                       text = "Right -->",
                                       command=self.right_minimizing)
        self.button_right_minimizing.pack(side = 'left', fill = 'x', expand = True)

        
        # add button focus_mode to focus_mode_frame
        self.button_focus_mode = ttk.Button(self.focus_mode_frame, 
                                       text = "Focus Mode",
                                       command=self.focus_mode)
        self.button_focus_mode.pack(side = 'right', fill = 'x', expand = False)

#--------View: Status Bar Frame--------------------------------------------------------
        # create the statusbar
        self.stbar = GuiBaseClass.statusbar
        GuiBaseClass.message(self, msg="Waiting ......")

#----------------instance attributes-------------------------------------------------------
        # setting file stores state of the Application
        self.setting_info = Settings("./setting.yaml")
        # with open("./setting.yaml","r") as setting_file:
        #     self.setting_info = yaml.safe_load(setting_file)
        self.filename = self.setting_info.get_setting("filename")
        self.previous_dir = None if self.filename is None else os.path.dirname(self.filename)
        self.file_dialog = None

        # Store kroki diagram state
        self.kroki_diagram = None
        
#---------KEYS BINDING --------------------------------------------------------------------
        # open file
        self.root.bind("<Control-o>", self.file_open)
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

#---------METHODS: OPEN, SAVE FILE--------------------------------------------------------------------
    # def write2_setting(self, event=None) -> None:
    #     with open("./setting.yaml","w") as setting_file:
    #             yaml.safe_dump(self.setting_info, setting_file, sort_keys=False)

    def file_open(self,event=None):
        self.filename=filedialog.askopenfilename(initialdir=self.previous_dir) 
        if self.filename != "":
            self.text.delete('1.0','end')
            file= open(self.filename,"rt")
            for line in file:
                self.text.insert("end",line)
            self.message(f"File {self.filename} was opened!")
            self.setAppTitle(self.filename)
            self.convert2_image()
            self.setting_info.set_setting("filename" , self.filename)
            self.previous_dir= os.path.dirname(self.filename)
            self.setting_info.save_settings()

    def file_save(self, event=None) -> None:
        if self.filename is not None:
            file = open(self.filename,"w")
            file.write(self.text.get("0.0","end"))
            file.close()
            self.setAppTitle(self.filename)           
        else :
            self.file_save_as()

    def file_save_as(self, event=None) -> None:
        self.file_dialog=filedialog.asksaveasfile( 
                                    initialdir=self.previous_dir,
                                    filetypes= [("plantuml",".pml"),
                                                ("erd",".erd"),
                                                ("text",".txt"),
                                                ("other",".*")],
                                    defaultextension=("text",".txt")
                                    )
        if self.file_dialog!= None :
            self.filename=self.filedialog.name
            self.previous_dir=self.filename
            self.file_save()

#-------METHOD CONVERT TEXT DIAGRAM TO IMAGE-----------------------------------------------    
    def convert2_image(self,event=None) -> None:
        # instantiate a KrokiEncoder instance: filepath, diagram type, image type is png
        self.kroki_diagram = KrokiEncoder(self.filename, 
                                        self.combobox.get(),
                                        "png")
        imgfile_png = re.sub(".[a-z]+$",".png",self.filename)

        #write image to file
        self.kroki_diagram.export_image(imgfile_png)

        #show image in ImageWidget
        if os.path.exists(imgfile_png):
                self.imagewidget.update_image(imgfile_png)
                self.message(f"Displaying {imgfile_png}")
        
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

#-------METHODS: left/right/even_split minimizing ----------------------------------------------------------
    def left_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=5,y=100) # 5 pixels from the left and 100 pixels from top
    
    def right_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=1195,y=100) # 1195 pixels from the left and 100 pixels from top
    
    def even_split(self,event=None) -> None:
        self.panwind.sash_place(0,x=600,y=100) # 600 pixels from the left and 100 pixels from top

#-------METHODS: change color ----------------------------------------------------------
    def text_color(self,event=None) -> None:
        choose_color=colorchooser.askcolor()
        self.text.text_editor.configure(fg=choose_color[1])

    def textblack(self,event=None) -> None:
        self.text.text_editor.configure(fg="black")

    def backgroundcolor(self,event=None) -> None:
        choose_color=colorchooser.askcolor()
        self.text.text_editor.configure(background=choose_color[1])

    def whitebackground(self,event=None) -> None:
        self.text.configure(background="white")

    def change2_light_mode_color(self,event=None) -> None:
        self.text.text_editor.configure(background="#FFFFFF",
                                foreground="#000000",
                                insertbackground="#FFFFFF")
        self.imagewidget.image_widget.configure(background="#FFFFFF")
        self.focus_mode_frame.configure(background="#FFFFFF")
        self.button_focus_mode.configure(background="#FFFFFF",
                                         foreground="#000000")
        
    def change2_dark_mode_color(self,event=None) -> None:
        self.text.text_editor.configure(background="#1e1f1e",
                                foreground="#9bd9f6",
                                insertbackground="#FCFEFE")
        self.imagewidget.image_widget.configure(background="#121213")
        self.focus_mode_frame.configure(background="#1e1f1e")
        self.button_focus_mode.configure(background="#1e1f1e",
                                             foreground="#21a143")

#--------------------METHODS: Focus Mode -------------------------------------------------------       
    def focus_mode(self,event=None) -> None:
        if self.convert2_img_frame.winfo_ismapped():
            # hide the search frame
            self.convert2_img_frame.pack_forget()
            self.search_frame.pack_forget()
            # change to dark mode
            self.change2_dark_mode_color()
        else:
            self.convert2_img_frame.pack(before=self.panwind,
                                         fill = 'both', 
                                         expand = False, 
                                         side='top')
            self.search_frame.pack(before=self.panwind,
                                   after=self.convert2_img_frame,
                                    fill = 'both', 
                                   expand = False, 
                                   side='top')
            self.change2_light_mode_color()

#-------OTHER METHODS----------------------------------------------------------
        
    def toggle_checkButton(self,event=None) -> None:
        self.checkbutton_var = not self.checkbutton_var
    
    def Exit(self,event=None):
        if self.checkbutton_var:
            self.ask_exit()
        else:
            sys.exit(0)
      
    def ask_exit(self) -> None:
        answer = mbox.askyesno(title="Close Application",message="Do you want to quit the application?")
        if answer is True:
            sys.exit(0)

    def About(self,event=None) -> None:
        mbox.showinfo(
            title="About PlantUML Editor",
            message="PlantUML Editor 2023\nAuthor: Anh-Minh Do\nPotsdam, Germany")
    

if __name__ == '__main__':
    print("this is a module for import only")

