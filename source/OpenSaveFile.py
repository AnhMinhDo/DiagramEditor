import os
import sys
import tkinter.filedialog as filedialog

class OpenSaveFile:
    def __init__(self) -> None:
        pass
#---------METHODS: OPEN, SAVE FILE--------------------------------------------------------------------
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


def main() -> int:
    return 0
if __name__ == "__main__":
    main()