from KrokiEncoder import KrokiEncoder
import re
import os

class Convert2Image:
    def __init__(self) -> None:
        pass
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


def main() -> int:
    return 0
if __name__ == "__main__":
    main()