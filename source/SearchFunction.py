class SearchFunction:
    def __init__(self) -> None:
        pass
    #--------METHOD SEARCH------------------------------------------------------  
    def search_text(self, event=None) -> None:
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

    def switch2_search_entry(self, event=None) -> None:
        self.entry_search.focus_set()


def main() -> int:
    return 0
if __name__ == "__main__":
    main()