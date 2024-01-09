import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import logging
from typing import Callable

class TextEditor(ttk.Frame):
    def __init__(self, master_frame:ttk.Frame, **kwargs) -> None:
        ttk.Frame.__init__(self,master_frame, **kwargs)
        self.master_frame = master_frame
        self.text_editor = tk.Text(self,
                                wrap="word",
                                undo=True,
                                width=50,
                                insertofftime=500,
                                insertontime=500,
                                font=("Verdana",12))
        self.text_editor.pack(side="left",
                              fill="both",
                              expand=True,
                              padx=2,
                              pady=2)
        # Change tab to 4 spaces
        self.font = tkfont.Font(font=self.text_editor["font"])
        self.tab_width = self.font.measure(" " * 4)
        self.text_editor.config(tabs=self.tab_width)
        
        # create scrollbar widgets
        self.scrollbar_vertical = ttk.Scrollbar(self,
                                       command=self.vertical_scroll,
                                       orient=tk.VERTICAL)
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.text_editor.config(yscrollcommand=self.scrollbar_vertical.set)
        # Attributes for function search_query
        self.query: None = None
        self._first_letter_index: None = None
        self._last_letter_index: None = None
        self._start_search_idx: str = "1.0"
        self._end_search_idx: str = "end"

    def get(self,start:str, end:str) -> str:
        return self.text_editor.get(start, end)

    def delete(self, start, end) -> None:
        self.text_editor.delete(start, end)

    def insert(self, start: str, insert_string: str, *args) -> None:
        self.text_editor.insert(start, insert_string, *args)

    def index(self, index_string: str) -> str:
        return self.text_editor.index(index_string)

    def remove_highlight(self) -> None:
        for tag in self.text_editor.tag_names(index=None):
            self.text_editor.tag_remove(tag, "1.0", "end")
        self._first_letter_index = None
        self._last_letter_index = None
        self._start_search_idx = "1.0"
        self._end_search_idx = "end"

    def search_query(self, event=None) -> None:  
        if self.query is None:
            logging.warning("Query string is empty!")
        if self._last_letter_index is not None: # when users want to find the next occurrence.
            self._start_search_idx = self._last_letter_index
        self._first_letter_index: str = self.text_editor.search(
                                            self.query,
                                            index=self._start_search_idx, 
                                            nocase=True,
                                            stopindex=self._end_search_idx)
        if self._first_letter_index == "": # When the search reaches the end of text widget.
            for tag in self.text_editor.tag_names(index=None):
                self.text_editor.tag_remove(tag, "1.0", "end")
            self._first_letter_index = None
            self._last_letter_index = None
            self._start_search_idx = "1.0"
            self._end_search_idx = "end"
        else:
            line, character = self._first_letter_index.split(sep=".",
                                                             maxsplit=1)
            self._last_letter_index = f"{line}.{int(character)+len(self.query)}"
            self.text_editor.tag_add("highlight",
                             self._first_letter_index,
                             self._last_letter_index)
            self.text_editor.tag_configure("highlight", background="yellow")
            self.text_editor.see(self._last_letter_index)
    
    def vertical_scroll(self, *args) -> None:
        self.text_editor.yview(*args)

    def bind_event(self, event:str, callback_func:Callable) -> None:
        self.text_editor.bind(event, func=callback_func)

    def config_text_editor(self, **kwargs) -> None:
        self.text_editor.configure(**kwargs)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Text Editor")
    root.geometry("800x600")
    text_frame = ttk.Frame(root)
    text_frame.pack(fill = 'both', expand = True, side='top')
    app = TextEditor(text_frame)
    app.pack(side="top",fill="both", expand=True)
    root.mainloop()

# Author: Anh-Minh Do, 01.2024, Potsdam, Germany
# License: MIT
