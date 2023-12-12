from tkinter import colorchooser


class ChangeColor:
    def __init__(self) -> None:
        pass
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
 

def main() -> int:
    return 0
if __name__ == "__main__":
    main()