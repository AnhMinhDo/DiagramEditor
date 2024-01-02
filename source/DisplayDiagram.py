import tkinter as tk
import tkinter.ttk as ttk
import os

class DisplayDiagram():
    def __init__(self, frame:ttk.Frame, side:str) -> None:
        self.frame = frame
        self.side = side
        self.image_widget = tk.Label(self.frame,
                                    text="Display Image Here",
                                    background="white")
        self.image_widget.pack(side=self.side,fill="both", expand=True)
        self.image = None

    def load_image(self, image_path:str) -> None:
        self.image = tk.PhotoImage(file=image_path)
        self.image_widget.configure(image=self.image)

    def update_image(self, image_path:str) -> None:
        self.image.configure(file=image_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Display Diagram")
    root.geometry("800x600")
    displayFrame = ttk.Frame(root)
    displayFrame.pack(fill = 'both', expand = True, side='top')
    app = DisplayDiagram(displayFrame, side="right")
    IMAGE_PATH = ".\data\icons\default_icon.png"
    if os.path.exists(IMAGE_PATH):
        app.load_image(image_path=IMAGE_PATH)
    root.mainloop()

# Author: Anh-Minh Do, 01.2024, Potsdam, Germany
# License: MIT