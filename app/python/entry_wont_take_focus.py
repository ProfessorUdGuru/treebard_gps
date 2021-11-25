# entry_wont_take_focus

import tkinter as tk



topicslist = [
    "Lorem", "ipsum", "dolor", "sit", "ame", "consectetur adipiscing", "eli", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore"]

short_note = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
'''

class NotesDialog(tk.Toplevel):

    def __init__(self, master, topicslist, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        self.master = master
        self.topicslist = topicslist

        self.make_containers()
        self.make_toc_scrollable() 
        self.make_inputs()   
        self.toc_width = 20 * 11     
        self.make_table_of_contents() 
        self.size_toc()
        # self.bind_class('Label', '<Tab>', self.stop_tab_traversal)
        # self.bind_class('Label', '<Shift-Tab>', self.stop_tab_traversal)
           
        self.bind_all("<Key-Up>", self.focus_topicslist)
        self.bind_all("<Key-Down>", self.focus_topicslist)
        
        self.focus_set()
        
        self.bind("<Tab>", self.print_focused_widget, add="+")

    def print_focused_widget(self, evt):
        print(self.focus_get())

    def make_containers(self):
        spacer = tk.Frame(self)
        self.left_panel = tk.Frame(self)
        self.right_panel = tk.Frame(self)
        self.bottom_panel = tk.Frame(self)

        spacer.grid(column=0, row=0, sticky="news")
        self.left_panel.grid(column=0, row=1, sticky="news", padx=(12,0))
        self.right_panel.grid(column=1, row=0, sticky="news", rowspan=2)
        self.bottom_panel.grid(column=0, row=2, columnspan=2, sticky="news")

    def focus_topicslist(self, evt):
        widg = evt.widget
        if widg in self.topics or widg == self.note:
            return
        last = self.topics[len(self.topics) - 1]
        first = self.topics[0]
        sym = evt.keysym
        if sym == "Up":
            last.focus_set()
        elif sym == "Down":
            first.focus_set()

    def make_inputs(self):
        self.toc_head = tk.Label(self.left_panel, text="TABLE OF CONTENTS")
        self.note_header = tk.Entry(self.right_panel, width=36)
        self.note = tk.Text(self.right_panel)
        rad = tk.Radiobutton(self.bottom_panel)

        self.toc_head.grid(column=0, row=0, sticky="news", pady=3)
        self.note_header.grid(column=0, row=0, sticky="w", padx=(12,0), pady=6)
        self.note.grid(column=0, row=1, padx=12)
        rad.grid()  

        self.note.insert(1.0, short_note)

    def size_toc(self):
        self.update_idletasks()
        scroll_height = self.toc.winfo_reqheight()
        panel_height = self.right_panel.winfo_reqheight()
        self.toc_height = note_height = self.note.winfo_reqheight()
        title_height = self.toc_head.winfo_reqheight()
        self.toc_canvas.config(
            width=self.toc_width,
            height=note_height - title_height,
                scrollregion=(0, 0, self.toc_width, scroll_height))

    def make_toc_scrollable(self):
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(1, weight=1)
        self.toc_canvas = tk.Canvas(self.left_panel)
        self.toc = tk.Frame(self.toc_canvas)
        self.toc_canvas.create_window(0, 0, anchor='nw', window=self.toc)
        sbv = tk.Scrollbar(
            self.left_panel, 
            command=self.toc_canvas.yview)
        self.toc_canvas.config(yscrollcommand=sbv.set)

        self.toc_canvas.grid(column=0, row=1, sticky="news")
        sbv.grid(column=1, row=1, sticky="ns")

    # def stop_tab_traversal(self, evt):
        # lab = evt.widget
        # if lab not in self.topics:
            # return
        # self.note.focus_set()
        # return('break')

    def traverse_on_arrow(self, evt):
        lab = evt.widget
        sym = evt.keysym
        nexxt = lab.tk_focusNext()
        prev = lab.tk_focusPrev()
        first = self.topics[0]
        last = self.topics[len(self.topics) - 1]
        if sym == "Up":
            if prev.winfo_class() == "Label":
                prev.focus_set()
            else:
                last.focus_set()
        elif sym == "Down":
            if nexxt.winfo_class() == "Label":
                nexxt.focus_set()
            else:
                first.focus_set()
        else:
            print("widget", lab, "is not in self.topics")

    def make_table_of_contents(self):
        for child in self.toc.winfo_children():
            child.destroy()
        self.topics = []
        r = 0
        for stg in self.topicslist:
            text = self.topicslist[r]
            lab = tk.Label(
                self.toc, takefocus=1, anchor="w", 
                text=text, width=self.toc_width)
            self.topics.append(lab)
            lab.grid(column=0, row=r+1, sticky="ew")
            lab.bind("<Button-1>", self.switch_note_on_click) 
            lab.bind("<FocusIn>", self.highlight)
            lab.bind("<FocusOut>", self.unhighlight)
            lab.bind("<Enter>", self.highlight)
            lab.bind("<Leave>", self.unhighlight)
            lab.bind("<Key-Up>", self.traverse_on_arrow, add="+") 
            lab.bind("<Key-Down>", self.traverse_on_arrow, add="+")
            r += 1

    def make_new_note(self, final):

        self.topicslist.insert(0, final)
        self.make_table_of_contents()
        # self.topics[0].focus_set()

        self.size_toc()        

    def switch_note_on_click(self, evt):
        widg = evt.widget

        widg.focus_set()
        widg.config(bg="bisque")

    def highlight(self, evt):
        evt.widget.config(bg="white")

    def unhighlight(self, evt):
        evt.widget.config(bg="bisque")

if __name__ == "__main__":

    root = tk.Tk()

    def open_note():
        note_dlg = NotesDialog(root, topicslist)
        note_dlg.geometry("+800+300")

    b = tk.Button(root, text=" ... ", command=open_note)
    b.grid()
    b.focus_set()

    root.mainloop()



# Why does the Entry fail to ever takefocus if the Labels are takefocus=1?
# The commented code was the culprit. But other focus glitches occurred. This didn't answer much, except to do what I did in the custom_combobox_widget.py and remove focus from all the labels when they don't need it.


