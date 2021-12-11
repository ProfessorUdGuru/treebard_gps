# dropdown.py

import tkinter as tk
import sqlite3
from files import (
    handle_new_tree_event, handle_open_event, save_as, save_copy_as, 
    rename_tree, close_tree, exit_app, global_db_path, get_recent_files,
    new_file_path, change_tree_title, set_current_file, save_recent_tree)  
from widgets import Frame, FrameHilited2, LabelHilited3, ToplevelHilited
from scrolling import Scrollbar
from messages import open_input_message2, opening_msg
from styles import config_generic, make_formats_dict
from query_strings import (
    select_closing_state_recent_files, update_closing_state_recent_files)
import dev_tools as dt
from dev_tools import looky, seeline







'''
    Replaces Tkinter Menu. Unlike Tkinter's dropdown menu, this widget
        --is used and configured like other Tkinter widgets.
        --doesn't use Windows colors.

    Currently this dropdown menu only uses the mouse, but it could be 
    improved to use keyboard navigation also.

    I just found out, long after creating a replacement for the Windows border
    and putting it on all my main dialogs and the root window, that the 
    Tkinter dropdown menu doesn't even work with my "Toykinter" border. Not
    that I wanted to use tkinter.Menu anyway since its colors can't be changed 
    (maybe depending on the Windows theme in use). Tkinter's dropdown menu 
    doesn't use any of Tkinter's geometry managers (`grid`, `pack` or `place`),
    since it's assumed that the menu is always going to be right below the
    Windows title bar. Since the Toykinter title bar is gridded like any other
    widget, the Tkinter menu bar attaches above the Toykinter title bar and I 
    doubt there's anything that can be done about it, but it doesn't matter, I 
    just had to write a little code, like everyone does in HTML anyway when 
    they need a dropdown menu for a web app.

    At this time I'm keeping it as simple as possible by making the dropdown
    menu respond only to mouse events. To me this seems like the right way
    to use a dropdown menu since I want to tab through GUI functionalities
    quickly to get to the right one, without having to first tab through a 
    bunch of icons and text menu items. Normally I'd rather type than
    click, but prior efforts to make a dropdown menu that works with both mouse
    and keyboard got bogged down in conflicting events and focus handling.

    This widget is hard-coded to handle three levels of menu items: 1) The 
    Labels permanently gridded horizontally across the menu bar; 2) the first
    dropdown that pops open or closed on click and hover events; 3) the second 
    dropdown which flies out to the right of its parent.

    Since there will never be more than one set of `drop0`, `drop1`, and `drop2`
    open at a time, only one set exists. Each of the three drops is a permanent 
    widget which is withdrawn, deiconified and populated with destroyable labels 
    as needed.

    The dropdown is a Toplevel window since it's the only Tkinter widget that
    is made to overlap other widgets without pushing them to the side.
    The Toplevel also doesn't rely on `grid`, `pack` or `place`. Instead, the 
    Toplevel dropdown uses the geometry() method to appear next to its host 
    widget. If the window moves, the dropdown is withdrawn.
'''

formats = make_formats_dict()

IMPORT_TYPES = (
    ("From Treebard", "", ""), 
    ("From GEDCOM", "", ""))

EXPORT_TYPES = (
    ("To Treebard", "", ""), 
    ("To GEDCOM", "", ""))

MOD_KEYS = ("Ctrl", "Alt", "Shift", "Ctrl+Alt", "Ctrl+Shift", "Alt+Shift")

def placeholder(evt=None, name=""):
    print('menu test:', name.upper()) 
    print('evt:', evt) 

class DropdownMenu(FrameHilited2):
    def __init__(
            self, master, root, treebard, callback=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master 
        self.root = root
        self.treebard = treebard
        self.callback = callback

        self.recent_trees = []
        self.formats = make_formats_dict()

        self.drop1_is_open = False
        self.drop2_is_open = False
        self.expand = False 

        self.clicked = None

        self.host1 = None
        self.drop_delay = 250
        self.ipady = 3
        self.screen_height = self.winfo_screenheight()

        self.drop1 = ToplevelHilited(self, bd=1, relief="raised")
        self.drop2 = ToplevelHilited(self, bd=1, relief="raised")
        self.current_file = ""

        self.drop_items = {
            "file": (
                ("new", lambda evt, root=self.root, tbard=self.treebard, 
                    openfunx=open_input_message2, 
                    msg=opening_msg: handle_new_tree_event(
                        evt, root, tbard, openfunx, msg),
                    "n"),
                ("open", lambda evt, tbard=self.treebard: handle_open_event(
                    evt, tbard), "..."),
                ("save", lambda evt, name="save (redraw)": placeholder(evt, name), "s"),
                ("save as", lambda evt, root=self.root: save_as(evt, root), "CAs"),
                ("save copy as", lambda evt: save_copy_as(), "t"),
                ("rename", lambda evt, root=self.root: rename_tree(evt, root), "h"),
                ("recent trees", lambda evt: self.show_recent_trees(evt), 
                    ">", self.recent_trees),
                ("import tree", self.show_list, ">", IMPORT_TYPES),
                ("export tree", self.show_list, ">", EXPORT_TYPES),
                ("close", lambda evt, tbard=self.treebard: close_tree(evt, tbard), ""),
                ("exit", lambda evt, root=self.root: exit_app(evt, root), "")),

            "edit": (
                ("cut", lambda evt, name="cut": placeholder(evt, name), "x"), 
                ("copy", lambda evt, name="copy": placeholder(evt, name), "c"), 
                ("paste", lambda evt, name="paste": placeholder(evt, name), "v")),

            "elements": (
                ("add person", 
                    lambda evt, name="add person": placeholder(evt, name), ""),
                ("add place", 
                    lambda evt, name="add place": placeholder(evt, name), ""),
                ("add event",
                    lambda evt, name="add event": placeholder(evt, name), ""),
                ("add assertion", 
                    lambda evt, name="add assertion": placeholder(evt, name), ""),
                ("add source",  
                    lambda evt, name="add source": placeholder(evt, name), ""),
                ("add image",  
                    lambda evt, name="add image": placeholder(evt, name), ""),),

            "output": (
                ("charts", 
                    lambda evt, name="charts": placeholder(evt, name), ""),
                ("reports", 
                    lambda evt, name="reports": placeholder(evt, name), ""),),

            "research": (
                ("do list", 
                    lambda evt, name="do list": placeholder(evt, name), ""),
                ("add research goals", 
                    lambda evt, name="research goals": placeholder(evt, name), ""),
                ("contacts",
                    lambda evt, name="contacts": placeholder(evt, name), ""),
                ("correspondence",  
                    lambda evt, name="correspondence": placeholder(evt, name), ""),),

            "tools": (
                ("relationship calculator", 
                    lambda evt, name="relationship calculator": placeholder(evt, name), ""), 
                ("date calculator",  
                    lambda evt, name="date calculator": placeholder(evt, name), ""), 
                ("dupes & matches detector",  
                    lambda evt, name="dupes & matches detector": placeholder(evt, name), ""), 
                ("unlikelihood detector",  
                    lambda evt, name="unlikelihood detector": placeholder(evt, name), ""), 
                ("certainty calculator",  
                    lambda evt, name="certainty calculator": placeholder(evt, name), "")),  

            "help": (
                ("about treebard", 
                    lambda evt, name="about treebard": placeholder(
                        evt, name), ""),
                ("users' manual",  
                    lambda evt, name="users' manual": placeholder(
                        evt, name), ""),
                ("genealogy tips & tricks", 
                    lambda evt, name="genealogy tips & tricks": placeholder(
                        evt, name), ""),
                ("treebard website",
                    lambda evt, name="treebard website": placeholder(
                        evt, name), ""),
                ("forum & blog", 
                    lambda evt, name="forum & blog": placeholder(
                        evt, name), ""),
                ("help search",  
                    lambda evt, name="help search": placeholder(
                        evt, name), ""),
                ("contact",
                    lambda evt, name="contact": placeholder(
                        evt, name), ""),
                ("feature requests", 
                    lambda evt, name="feature requests": placeholder(
                    evt, name), ""),
                ("source code",  
                    lambda evt, name="source code": placeholder(
                        evt, name), ""),
                ("donations",  
                    lambda evt, name="donations": placeholder(
                        evt, name), ""),)}

        self.make_drop0()

        for drop in (self.drop1, self.drop2):
            drop.wm_overrideredirect(1)
            drop.withdraw()
        
        self.root.bind("<Button-1>", self.close_drop_on_click, add="+")

    def make_drop0(self):
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

    def make_drop1(self, evt):
        for child in self.drop1.winfo_children():
            child.destroy()
        self.host1 = widg = evt.widget
        cmd = widg.cget("text").lower()
        for k,v in self.drop_items.items():
            if cmd == k:
                format_strings = []
                text = ""
                lengths = []
                widgets = []
                row = 0
                for lst in self.drop_items[cmd]:
                    lab = LabelHilited3(self.drop1, text=lst[0].title())
                    symval = lst[2]
                    if symval == ">":
                        text = "{}    >".format(lst[0].title())
                    elif symval == "...":
                        text = "{}...    {}".format(lst[0].title(), " ")
                    elif len(symval) != 0:
                        if symval.startswith("CA"):
                            symval = symval[2]
                            mod_key = MOD_KEYS[3]
                        else:
                            mod_key = MOD_KEYS[0]
                        text = "{}    {}+{}".format(lst[0].title(), mod_key, symval.upper())
                    elif len(symval) == 0:
                        text = "{}    ".format(lst[0].title())
                    else:
                        print("line", looky(seeline()).lineno, "case not handled:")

                    lab.grid(column=0, row=row, sticky='ew')
                    self.bind_command(lab, text, v[row])
                    format_strings.append(text)
                    lengths.append(len(text))
                    widgets.append(lab)
                    row += 1
                self.fix_strings(
                    lengths, self.drop_items[cmd], format_strings, widgets)
     
        self.position_drop1()
        self.drop1.deiconify()

    def fix_strings(self, lengths, stringslist, format_strings, widgets):
        maxx = max(lengths)
        j = 0
        for lst in stringslist:
            rightsym = False
            if len(lst[2]) != 0:
                rightsym = True
            if rightsym:
                diff = maxx - lengths[j] + 4
            else:
                diff = maxx - lengths[j]
            stgs = format_strings[j].split("    ")
            new_string = "{}{}{}".format(stgs[0], " " * (diff), stgs[1])

            if not rightsym:
                new_string = "{}    ".format(new_string)
            widgets[j].config(text=new_string, width=maxx + 4)
            j += 1

    def bind_command(self, lab, text, v_row): 
        lab.bind('<Enter>', self.highlight)
        lab.bind('<Leave>', self.unhighlight)
        lab.bind("<Enter>", self.detect_drop2, add="+")
        lab.bind("<Leave>", self.close_drop2, add="+")
        lab.bind("<ButtonRelease-1>", self.close_drop_on_click, add="+")
        if ">" in text:
            return
        lab.bind("<Button-1>", v_row[1], add="+")

    def highlight(self, evt):
        evt.widget.config(bg=formats["bg"])

    def unhighlight(self, evt):
        evt.widget.config(bg=formats["highlight_bg"])

    def detect_drop2(self, evt):    

        def run_drop_delay(delay):
            self.after(delay, self.make_drop2, evt, row, sym, text)            

        widg = evt.widget
        row = widg.grid_info()['row']
        text = widg.cget('text').lower()
        for k,v in self.drop_items.items():
            if k != self.clicked:
                break
            if ">" in text:
                if v[row][0] == text.rstrip(">").rstrip():
                    sym = ">"
                    run_drop_delay(self.drop_delay)
                    break
            else:
                self.expand = False
                self.close_drop2()

    def show_recent_trees(self, evt):
        def populate_drop2_recent_files():
            x = 0
            for i in range(20):
                lab = LabelHilited3(self.drop2, anchor="w")
                if len(recent_files) >= x + 1:
                    lab.config(text=recent_files[x])
                    lab.grid(sticky='ew')
                    lab.bind("<ButtonRelease-1>", use_recent_tree, add="+")
                    lab.bind('<Enter>', self.highlight)
                    lab.bind('<Leave>', self.unhighlight)
                else:
                    break
                x += 1   

        def use_recent_tree(event):
            nonlocal recent_files
            close_tree(treebard=self.treebard)
            tree_title = event.widget.cget("text")
            current_file = "{}.tbd".format(tree_title.replace(" ", "_").lower())
            set_current_file(current_file)            
            save_recent_tree(tree_title, recent_files)
            for child in self.drop2.winfo_children():
                child.destroy()
            populate_drop2_recent_files()
            change_tree_title(self.treebard)
            self.treebard.make_main_window()                

        recent_files = get_recent_files() 
        populate_drop2_recent_files()

    def show_list(self, list_to_use):
        format_strings = []
        text = ""
        lengths = []
        widgets = []
        row = 0
        for lst in list_to_use:
            lab = LabelHilited3(self.drop2, text=lst[0].title())
            symval = lst[2]
            if symval == ">":
                text = "{}    >".format(lst[0].title())
            elif symval == "...":
                text = "{}...    {}".format(lst[0].title(), " ")
            elif len(symval) != 0:                
                if symval.startswith("AA"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[0]
                elif symval.startswith("SS"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[1]
                elif symval.startswith("CA"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[2]
                elif symval.startswith("CS"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[3]
                elif symval.startswith("AS"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[4]
                else:
                    mod_key = MOD_KEYS[5]
                text = "{}    {}+{}".format(lst[0].title(), mod_key, symval.upper())
            elif len(symval) == 0:
                text = "{}    {}".format(lst[0].title(), " ")
            else:
                print("line", looky(seeline()).lineno, "case not handled:")

            lab.grid(column=0, row=row, sticky='w')
            lab.bind('<Enter>', self.highlight)
            lab.bind('<Leave>', self.unhighlight)
            lab.bind("<Button-1>", self.close_drop_on_click, add="+")
            format_strings.append(text)
            lengths.append(len(text))
            widgets.append(lab)
            row += 1

        self.fix_strings(
            lengths, list_to_use, format_strings, widgets)

    def make_drop2(self, evt, row, sym, text):
        for child in self.drop2.winfo_children():
            child.destroy()
        self.host2 = evt.widget
        for k,v in self.drop_items.items():
            row = 0
            for lst in v:
                text = text.split("    ")[0]
                if text == v[row][0]:
                    v[row][1](v[row][3])
                row += 1
        self.position_drop2()
        self.drop2.deiconify()
        self.drop2_is_open = True
        self.expand = True

    def position_drop2(self):
        self.drop2.geometry("+{}+{}".format(
            self.drop1.winfo_rootx() - 3 + self.drop1.winfo_reqwidth(), 
            self.host2.winfo_rooty())) 

    def close_drop2(self, evt=None):
        if self.drop1_is_open is True and self.expand is True:
            return

        def withdraw_drop2():
            self.drop2.withdraw()
            for child in self.drop2.winfo_children():
                child.destroy()

        def run_drop_delay(delay):
            self.after(delay, withdraw_drop2)

        run_drop_delay(self.drop_delay)
        self.drop2_is_open = False
        self.expand = False

    def position_drop1(self):
        app_west = self.root.winfo_rootx()
        app_north = self.root.winfo_rooty()
        west = self.host1.winfo_rootx()
        north = (
            self.host1.winfo_rooty() + self.host1.winfo_reqheight() + 
                (self.ipady * 2))
        self.drop1.geometry("+{}+{}".format(west, north))

    def open_drop1_on_click(self, evt):
        if self.drop1_is_open is True:
            if self.drop1_is_open is False:
                return
            if self.drop2_is_open is True and self.expand is False:
                return
            for child in self.drop1.winfo_children():
                child.destroy()
            self.drop1_is_open = False
            self.expand = False
            self.make_border(evt) 
            self.drop1.withdraw()
            return
        self.make_drop1(evt)
        self.clicked = evt.widget.cget("text").lower()
        self.drop1_is_open = True
        self.make_border(evt)  

    def open_drop1_on_hover(self, evt):
        if self.drop1_is_open is False:
            return
        self.make_drop1(evt)
        self.clicked = evt.widget.cget("text").lower() 

    def make_border(self, evt):
        if self.drop1_is_open is True:
            evt.widget.config(relief="sunken")
        elif self.drop1_is_open is False:
            evt.widget.config(relief="raised")

    def flatten_border(self, evt):
        evt.widget.config(relief="flat")

    def close_drop_on_click(self, evt):
        '''
            Handle miscellaneous clicks that should or should not close 
            the dropdown.
        '''        
        def close_it():
            self.drop1.withdraw()
            self.drop2.withdraw()
            self.drop1_is_open = False
            self.drop2_is_open = False
            self.expand = False

        if self.drop1_is_open is False:
            return

        if evt.widget.master != self:
            widg = evt.widget
            if widg.winfo_class() == "Label":
                text = widg.cget("text")
                if ">" not in text:
                    close_it()               
            else:
                close_it()

if __name__ == "__main__":

    from window_border import Border
    from widgets import Button, Label

    def make_widgets():
        root.columnconfigure(1, weight=1)
        canvas = Border(root, root, size=3, menubar=True)
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

        dropdown = DropdownMenu(canvas.menu_frame, root)
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
            text='Sample App')
        search_dlg_heading.grid(column=0, row=0, pady=(24,0))

        instrux = Label(
            header, text='Lorem ipsum epsom litsum')
        instrux.grid(column=0, row=1, sticky='e', padx=24, pady=12)

    def cancel():
        root.quit()

    root = tk.Tk()
    root.geometry("600x400+1200+200")
    root.config(bg="black")

    make_widgets()

    config_generic(root)

    root.mainloop()

