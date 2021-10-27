# dropdown.py

import tkinter as tk
from widgets import (
    Frame, FrameHilited2, LabelHilited3, ToplevelHilited, LabelHilited
)
from scrolling import Scrollbar
from styles import config_generic, make_formats_dict
import dev_tools as dt
from dev_tools import looky, seeline






'''
    Replaces Tkinter Menu. Unlike Tkinter's dropdown menu, this widget...
        --is used and configured like other Tkinter widgets.
        --doesn't use Windows colors.

    Currently this dropdown menu only uses the mouse, but it could be 
    improved to use keyboard navigation also.

    I just found out, long after creating a replacement for the Windows border
    and putting it on all my main dialogs and the root window, that the 
    Tkinter dropdown menu doesn't even work with my "Toykinter" border. Not
    that I wanted to use tkinter.Menu anyway since its colors can't be changed. Tkinter's dropdown menu doesn't use any of
    Tkinter's geometry managers (`grid`, `pack` or `place`), since it's assumed that
    the menu is always going to be right below the Windows title bar. Since the
    Toykinter title bar is gridded like any other widget, the Tkinter menu bar
    attaches above the Toykinter title bar and I doubt there's anything that
    can be done about it, but it doesn't matter, I just had to write a little
    code, like everyone does in HTML anyway when they need a dropdown menu for
    a web app.

    At this time I'm keeping it as simple as possible by making the dropdown
    menu respond only to mouse events. To me this seems like the right way
    to use a dropdown menu since I want to tab through GUI functionalities
    quickly to get to the right one, without having to first tab through a 
    bunch of icons and text menu items first. Normally I'd rather type than
    click, but prior efforts to make a dropdown menu that works with both mouse
    and keyboard got bogged down in conflicting events and focus handling.

    This widget is hard-coded to handle three levels of menu items. The Labels
    permanently gridded horizontally across the menu bar. The first dropdown 
    that pops open or closed on click and hover events. And the second and last
    dropdown which flies out to the right of its parent.

    Since there will never be more than one set of `drop0`, `drop1`, and `drop2`
    open at a time, only one set exists. Each of the three drops is a permanent 
    widget which is withdrawn, deiconified and populated with labels as needed.

    The dropdown is a Toplevel window since it's the only Tkinter widget that
    can easily be made to overlap other widgets without pushing them to the side.
    The Toplevel is also the only widget that doesn't rely on `grid`, `pack` or 
    `place`. So it's not hard to get the Toplevel to appear next to its host 
    widget.
'''

class DropdownMenu(FrameHilited2):
    def __init__(
            self, master, drop_items, root, callback=None, 
            *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master 
        self.root = root
        self.drop_items = drop_items
        self.callback = callback
    
        self.formats = make_formats_dict()

        self.drop_is_open = False

        self.host1 = None
        
        self.ipady = 3
        self.screen_height = self.winfo_screenheight()

        self.make_widgets()
        
        self.root.bind("<Button-1>", self.close_drop_on_click_elsewhere, add="+")

    def make_widgets(self):

        d = 0
        for key in self.drop_items:
            lab = LabelHilited3(self, text=key.title(), bd=1)
            lab.grid(column=d, row=0, ipadx=6, ipady=self.ipady)
            lab.bind('<Button-1>', self.open_drop1_on_click)
            lab.bind('<Enter>', self.make_border)
            lab.bind('<Leave>', self.flatten_border)
            lab.bind('<Enter>', self.open_drop1_on_hover, add="+")
            lab.bind('<Leave>', self.open_drop1_on_hover, add="+")
            d += 1

        self.drop1 = ToplevelHilited(self, bd=1, relief="raised")

        self.drop2 = ToplevelHilited(self, bd=1, relief="raised")

        for drop in (self.drop1, self.drop2):
            drop.wm_overrideredirect(1)
            drop.withdraw()
            drop.columnconfigure(1, weight=1)

    def make_drop1(self, evt):
        for child in self.drop1.winfo_children():
            child.destroy()
        self.host1 = widg = evt.widget
        cmd = widg.cget("text").lower()
        for k,v in self.drop_items.items():
            if cmd == k:
                row = 0
                for item in self.drop_items[cmd]:
                    lab = LabelHilited(self.drop1, text=item.title(), anchor='w')
                    lab.grid(column=0, row=row, sticky='w', padx=12)
                    spacer = LabelHilited(self.drop1)
                    spacer.grid(column=1, row=row, sticky='ew')
                    caret =  LabelHilited(self.drop1, text=">", anchor='e')
                    caret.grid(column=2, row=row, sticky='e', padx=12)
                    row += 1
        self.position_drop1()
        self.drop1.deiconify()

    def position_drop1(self):
        self.update_idletasks()
        app_west = self.root.winfo_rootx()
        app_north = self.root.winfo_rooty()
        west = self.host1.winfo_rootx()
        north = self.host1.winfo_rooty() + self.host1.winfo_reqheight() + (self.ipady * 2)
        self.drop1.geometry("+{}+{}".format(west, north))

    def open_drop1_on_click(self, evt):
        if self.drop_is_open is True:
            self.close_drop1(evt)
            self.drop1.withdraw()
            return
        self.make_drop1(evt)
        self.drop_is_open = True
        self.make_border(evt)  

    def open_drop1_on_hover(self, evt):
        if self.drop_is_open is False:
            return
        self.make_drop1(evt)

    def close_drop1(self, evt=None):
        if self.drop_is_open is False:
            return
        for child in self.drop1.winfo_children():
            child.destroy()
        self.drop_is_open = False
        self.make_border(evt)  

    def make_border(self, evt):
        if self.drop_is_open is True:
            evt.widget.config(relief="sunken")
        elif self.drop_is_open is False:
            evt.widget.config(relief="raised")

    def flatten_border(self, evt):
        evt.widget.config(relief="flat")

    def close_drop_on_click_elsewhere(self, evt):
        if evt.widget.master != self:
            self.drop1.withdraw()


 




if __name__ == "__main__":

    from window_border import Border
    from widgets import Button, Label

    def make_widgets():
        root.columnconfigure(1, weight=1)
        canvas = Border(root, size=3, menubar=True)
        canvas.title_1.config(text="Person Search Dialog")
        canvas.title_2.config(text="")

        window = Frame(canvas)
        canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

        window.vsb = Scrollbar(
            root, 
            hideable=True, 
            command=canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            root, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        dropdown = DropdownMenu(canvas.menu, drop_items, root)
        dropdown.grid(column=0, row=0, sticky='ew')

        buttonbox = Frame(window)
        b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        window.columnconfigure(2, weight=1)
        window.rowconfigure(1, weight=1)
        buttonbox.grid(column=0, row=3, sticky='e', pady=6)

        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        make_inputs(window)

    def make_inputs(window):

        root.columnconfigure(1, weight=1)

        header = Frame(window)
        header.grid(column=0, row=0, sticky='ew')

        search_dlg_heading = Label(
            header, 
            text='Person Search')
        search_dlg_heading.grid(column=0, row=0, pady=(24,0))

        instrux = Label(
            header, text='Search for person by name(s) or id number:')
        instrux.grid(column=0, row=1, sticky='e', padx=24, pady=12)

    def cancel():
        root.quit()

    drop_items = {
        "file": {
            "new": [ 
                "create new tree", 
                ["<Control-N>", "<Control-n>"],
                ""],
            "open": [ 
                "open existing tree",
                ["<Control-O>", "<Control-o>"], 
                "..."], 
            "recent files": [ 
                "funx uses list items as params to open recent files",
                [], 
                ">"]}, 
        "edit": {
            "cut": ["cut", ["<Control-X>", "<Control-x>", ""]], 
            "copy": ["copy", ["<Control-C>", "<Control-c>"], ""], 
            "paste": ["paste", ["<Control-V>", "<Control-v>"], ""]}, 
        "tools": {}}

    root = tk.Tk()
    root.geometry("1600x400+200+200")
    root.config(bg="black")

    make_widgets()

    config_generic(root)

    root.mainloop()

