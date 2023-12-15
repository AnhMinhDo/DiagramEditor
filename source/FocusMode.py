from ChangeColor import ChangeColor

class FocusMode(ChangeColor):
    def __init__(self) -> None:
        pass
    #--------------------METHODS: Focus Mode -------------------------------------------------------       

    def focus_mode(self,event=None) -> None:
        if self.focus_mode_var:
            # hide the search frame
            self.convert2_img_frame.pack_forget()
            self.search_frame.pack_forget()
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
            self.change2_light_mode_color()
            self.focus_mode_var = not self.focus_mode_var # change state in the variable


def main() -> int:
    return 0
if __name__ == "__main__":
    main()