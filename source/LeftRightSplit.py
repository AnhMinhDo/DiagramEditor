class LeftRightSplit:
    def __init__(self) -> None:
        pass
    #-------METHODS: left/right/even_split minimizing ----------------------------------------------------------
    def left_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=5,y=100) # 5 pixels from the left and 100 pixels from top
    
    def right_minimizing(self,event=None) -> None:
        self.panwind.sash_place(0,x=1195,y=100) # 1195 pixels from the left and 100 pixels from top
    
    def even_split(self,event=None) -> None:
        self.panwind.sash_place(0,x=600,y=100) # 600 pixels from the left and 100 pixels from top


def main() -> int:
    return 0
if __name__ == "__main__":
    main()