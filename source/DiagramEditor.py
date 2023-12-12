import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
from GuiBaseClass import GuiBaseClass
import os, sys
from no_img_icon import no_img_icon
from LeftRightSplit import LeftRightSplit
from SearchFunction import SearchFunction
from Convert2Image import Convert2Image
from FocusMode import FocusMode
from OpenSaveFile import OpenSaveFile
from ChangeColor import ChangeColor


class DiagramEditor(GuiBaseClass,
                    OpenSaveFile,
                    Convert2Image,
                    SearchFunction, 
                    LeftRightSplit,
                    FocusMode,
                    ChangeColor):
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
                            "UMLet"]
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
        
        # Create textWidget
        self.text = tk.Text(self.panwind, wrap="word", undo=True, width=50)
        self.text.pack(side="left",fill="both", expand=True)
        
        #Create ImageWidget
        self.imagewidget = tk.Label(self.panwind,
                                    text="Display Image Here",
                                    background="white")
        self.imagewidget.pack(side="right",fill="both", expand=True)
        

        # Add text and imagewidget to panedwindow
        self.panwind.add(self.text)
        self.panwind.add(self.imagewidget)
        
        # Add image to imagewidget window
        imgdata= no_img_icon
        self.image = tk.PhotoImage(data=imgdata)
        self.imagewidget.configure(image=self.image)
                
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

        # Variable to store the checkbutton button_focus_mode state
        self.focus_mode_var = tk.BooleanVar(value=False)
        # add button focus_mode to focus_mode_frame
        self.button_focus_mode = tk.Checkbutton(self.focus_mode_frame, 
                                       text = "Focus Mode",
                                       variable=self.focus_mode_var,
                                       indicatoron=False,
                                       command=self.focus_mode)
        self.button_focus_mode.pack(side = 'right', fill = 'x', expand = False)

#--------View: Status Bar Frame--------------------------------------------------------
        # create the statusbar
        self.stbar = GuiBaseClass.statusbar
        GuiBaseClass.message(self, msg="Waiting ......")

#----------------instance attributes-------------------------------------------------------

        # Used to save the directory of the opened file
        self.previous_dir: str = os.getcwd()
        self.filename: None = None

        self.kroki_diagram = None

        # Variable for function search_text
        self.query: str = self.entry_search.get()
        self.first_letter_index: None = None
        self.last_letter_index: None = None
        self.start_search_idx: str = "1.0"
        self.end_search_idx: str = "end"

        
#---------KEYS BINDING --------------------------------------------------------------------
        # open file
        self.root.bind("<Control-o>", self.file_open)
        # save file
        self.root.bind("<Control-s>", self.file_save)
        # save file as
        self.root.bind("<Control-Shift-s>", self.file_save_as)
        # convert to image
        self.root.bind("<Control-Alt-n>", self.convert2_image_button_func)
        # search
        self.root.bind("<Control-Alt-s>", self.search_text)
        # switch to search entry
        self.root.bind("<Control-f>", self.switch2_search_entry)
        # Turn on focus mode
        self.root.bind("<Control-k><f>", self.focus_mode)


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


def main() -> int:
    return 0
if __name__ == '__main__':
     main()
