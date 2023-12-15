import os
import sys
import tkinter.filedialog as filedialog
import yaml

class OpenSaveFile:
    def __init__(self) -> None:
        pass
        
#---------METHODS: OPEN, SAVE FILE--------------------------------------------------------------------
    def write2_config(self, event=None) -> None:
        with open("F:/Python_files/DiagramEditor/DiagramEditor/source/config.yaml","w") as config_file:
                yaml.safe_dump(self.config_info, config_file, sort_keys=False)

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
            self.config_info["filename"] = self.filename
            self.previous_dir= os.path.dirname(self.filename)
            self.write2_config()

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


def main() -> int:
    return 0
if __name__ == "__main__":
    main()