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
    def change2_light_mode_color(self,event=None) -> None:
        self.text.configure(background="#FFFFFF",
                                foreground="#000000",
                                insertbackground="#FFFFFF")
        self.imagewidget.configure(background="#FFFFFF")
        self.focus_mode_frame.configure(background="#FFFFFF")
        self.button_focus_mode.configure(background="#FFFFFF",
                                         foreground="#000000")
    def change2_dark_mode_color(self,event=None) -> None:
        self.text.configure(background="#1e1f1e",
                                foreground="#9bd9f6",
                                insertbackground="#FCFEFE")
        self.imagewidget.configure(background="#121213")
        self.focus_mode_frame.configure(background="#1e1f1e")
        self.button_focus_mode.configure(background="#1e1f1e",
                                             foreground="#21a143")
        

def main() -> int:
    return 0
if __name__ == "__main__":
    main()