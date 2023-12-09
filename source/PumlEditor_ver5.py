import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
import tkinter.filedialog as filedialog
from GuiBaseClass import GuiBaseClass
import os, sys
import re
from tkinter import colorchooser
from KrokiEncoder import KrokiEncoder
from no_img_icon import no_img_icon


class PumlEditor(GuiBaseClass):
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
        
#-------View: buttons minimize left/right/even_split -------------------------------------------------------
    # add minimizing frame
        self.minimizing_frame = ttk.Frame(self.frame)
        self.minimizing_frame.pack(fill = 'both', expand = False, side='top')
        # add button left_minimizing to minimizing frame
        self.button_left_minimizing = ttk.Button(self.minimizing_frame, 
                                       text = "<-- left",
                                       command=self.left_minimizing)
        self.button_left_minimizing.pack(side = 'left', fill = 'x', expand = True)
        # add button even_split to minimizing frame
        self.button_even_split = ttk.Button(self.minimizing_frame, 
                                       text = "| Split |",
                                       command=self.even_split)
        self.button_even_split.pack(side = 'left', fill = 'x', expand = True)
        # add button right_minimizing to minimizing_frame
        self.button_right_minimizing = ttk.Button(self.minimizing_frame, 
                                       text = "Right -->",
                                       command=self.right_minimizing)
        self.button_right_minimizing.pack(side = 'right', fill = 'x', expand = True)

#-------------------View: Focus Mode Frame------------------------------------------------------        
        # add focus_mode frame
        self.focus_mode_frame = tk.Frame(self.frame)
        self.focus_mode_frame.pack(fill = 'both', expand = False, side='top')
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

        
#---------KEYS BINDING TO ROOT--------------------------------------------------------------------
        # open file
        self.root.bind("<Control-o>", self.file_open)
        # save file
        self.root.bind("<Control-s>", self.file_save)
        # save file as
        self.root.bind("<Control-Shift-s>", self.file_save_as)
        # convert to image
        self.root.bind("<Control-Return>", self.convert2_image_button_func)
        # search
        self.root.bind("<Control-f>", self.search_text)
        

#---------Methods: OPEN, SAVE FILE--------------------------------------------------------------------

    def file_open(self,event=None):
        self.filename=filedialog.askopenfilename(initialdir=self.previous_dir) 
        if self.filename != "":
            self.text.delete('1.0','end')
            file= open(self.filename,"rt")
            for line in file:
                self.text.insert("end",line)
            self.message(f"File {self.filename} was opened!")
            self.setAppTitle(self.filename)
            self.file_save()
            self.previous_dir=self.filename

    def file_save(self, event=None) -> None:
        if self.filename is not None:
            file = open(self.filename,"w")
            file.write(self.text.get("0.0","end"))
            file.close()
            self.setAppTitle (self.filename)           
        else :
            self.file_save_as()

    def file_save_as(self, event=None) -> None:
        self.filedialog=filedialog.asksaveasfile( 
        initialdir=self.previous_dir,
        filetypes= [("plantuml",".pml"),
                    ("erd",".erd"),
                    ("text",".txt"),
                    ("other",".*")],
        defaultextension=("text",".txt"))
        if self.filedialog!= None :
            self.filename=self.filedialog.name
            self.previous_dir=self.filename
            self.file_save()


#-------METHOD CONVERT TEXT DIAGRAM TO IMAGE-----------------------------------------------    
    
    def convert2_image(self,event=None) -> None:
        # instantiate a KrokiEncoder instance: filepath, diagram type, image type is png
        self.kroki_diagram = KrokiEncoder(self.filename, 
                                        self.combobox.get(),
                                        "png")
        imgfile = re.sub(".[a-z]+$",".png",self.filename)
        #write image to file
        self.kroki_diagram.export_image(imgfile)
        #show image in ImageWidget
        if os.path.exists(imgfile):
                self.image.configure(file=imgfile)
                self.message(f"Displaying {imgfile}")
        
    def convert2_image_button_func(self, event=None) -> None:
        # instantiate a KrokiEncoder instance: filepath, diagram type, image type is png
        self.file_save()
        self.convert2_image()

#--------METHOD SEARCH------------------------------------------------------
        
    def search_text(self,event=None) -> None:
        if self.query != self.entry_search.get(): # when users change the query string while clicking the find-Next button for current query.
            self.query = self.entry_search.get()
            for tag in self.text.tag_names(index=None):
                self.text.tag_remove(tag, "1.0", "end")
            self.first_letter_index = None
            self.last_letter_index = None
            self.start_search_idx = "1.0"
            self.end_search_idx = "end"
        if self.last_letter_index is not None: # when users want to find the next occurrence.
            self.start_search_idx = self.last_letter_index
        self.first_letter_index:str = self.text.search(
                                            self.query, 
                                            index=self.start_search_idx, 
                                            nocase=True, 
                                            stopindex=self.end_search_idx)
        if self.first_letter_index == "": # When the search reaches the end of text widget.
            for tag in self.text.tag_names(index=None):
                self.text.tag_remove(tag, "1.0", "end")
            self.first_letter_index = None
            self.last_letter_index = None
            self.start_search_idx = "1.0"
            self.end_search_idx = "end"
        else:
            line, character = self.first_letter_index.split(sep=".", 
                                                                maxsplit=1)
            self.last_letter_index = f"{line}.{int(character)+len(self.query)}"
            self.text.tag_add("highlight", 
                            self.first_letter_index, 
                            self.last_letter_index)
            self.text.tag_configure("highlight", background="yellow")
            self.text.see(self.last_letter_index)

    def reset_search_text(self,event=None) -> None:
        for tag in self.text.tag_names(index=None):
            self.text.tag_remove(tag, "1.0", "end")
        self.entry_search.delete("0","end")

#-------left/right/even_split minimizing METHODS----------------------------------------------------------
    def left_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=5,y=100) # 5 pixels from the left and 100 pixels from top
    
    def right_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=1195,y=100) # 1195 pixels from the left and 100 pixels from top
    
    def even_split(self,event=None) -> None:
        self.panwind.sash_place(0,x=600,y=100) # 600 pixels from the left and 100 pixels from top
#--------------------Focus Mode METHOD-------------------------------------------------------       
    def change2_dark_mode_color(self,event=None) -> None:
        self.text.configure(background="#1e1f1e",
                                foreground="#9bd9f6",
                                insertbackground="#FCFEFE")
        self.imagewidget.configure(background="#121213")
        self.focus_mode_frame.configure(background="#1e1f1e")
        self.button_focus_mode.configure(background="#1e1f1e",
                                             foreground="#21a143")
    def change2_light_mode_color(self,event=None) -> None:
        self.text.configure(background="#DDE9E9",
                                foreground="#022222",
                                insertbackground="#101313")
        self.imagewidget.configure(background="#C2CDCD")
        self.focus_mode_frame.configure(background="#DDE9E9")
        self.button_focus_mode.configure(background="#DDE9E9",
                                             foreground="#022222")
        
    def focus_mode(self,event=None) -> None:
        if self.focus_mode_var:
            # hide the search frame
            self.convert2_img_frame.pack_forget()
            self.search_frame.pack_forget()
            self.minimizing_frame.pack_forget()
            # change to dark mode
            self.change2_dark_mode_color()
            self.focus_mode_var = not self.focus_mode_var # change state in the variable
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
            self.minimizing_frame.pack(after=self.panwind,
                                       fill = 'both', 
                                       expand = False, 
                                       side='top')
            self.change2_light_mode_color()
            self.focus_mode_var = not self.focus_mode_var # change state in the variable

#-------OTHER METHODS----------------------------------------------------------
    def text_color(self,event=None) -> None:
        choose_color=colorchooser.askcolor()
        self.text.configure(fg=choose_color[1])

    def textblack(self,event=None) -> None:
        self.text.configure(fg="black")

    def backgroundcolor(self,event=None) -> None:
        choose_color=colorchooser.askcolor()
        self.text.configure(background=choose_color[1])

    def whitebackground(self,event=None) -> None:
        self.text.configure(background="white")
    
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
    root=tk.Tk()
    root.geometry("1200x700")
    pedit = PumlEditor(root)
    root.title("PumlEditor 2023")
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            pedit.file_open(sys.argv[1])
    pedit.mainLoop() 
