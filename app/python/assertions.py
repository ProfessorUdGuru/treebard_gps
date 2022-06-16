# assertions.py

import tkinter as tk
import sqlite3
from widgets import (
    Toplevel, Frame, Button, Label, RadiobuttonBig, LabelHeader, 
    Entry, ButtonQuiet, configall, Border, Scrollbar, open_message,
    EntryAuto, Separator, make_formats_dict)
from right_click_menu import RightClickMenu, make_rc_menus
from toykinter_widgets import run_statusbar_tooltips
from scrolling import resize_scrolled_content
from files import get_current_file
import dev_tools as dt
from dev_tools import looky, seeline





class AssertionsDialog():
    def __init__(self, master, treebard, finding_id, text, widg):

        self.master = master # root
        self.treebard = treebard
        self.finding_id = finding_id
        self.source_count = text
        self.inwidg = widg

        self.formats = make_formats_dict()

        self.rc_menu = RightClickMenu(self.master, treebard=self.treebard)
        self.make_widgets()
        self.make_inputs()

        configall(self.assertions_dialog, self.formats)
        resize_scrolled_content(self.assertions_dialog, self.canvas, self.window)

        self.assertions_dialog.focus_set()

        print("line", looky(seeline()).lineno, "master, treebard, finding_id, text, widg:", master, treebard, finding_id, text, widg)

    def make_widgets(self):

        def ok():
            self.assertions_dialog.destroy()
        
        def cancel():
            self.assertions_dialog.destroy()

        size = (
            self.master.winfo_screenwidth(), self.master.winfo_screenheight())
        self.assertions_dialog = Toplevel(self.master)
        self.assertions_dialog.geometry("+120+24")
        self.assertions_dialog.maxsize(
            width=int(size[0] * 0.85), height=int(size[1] * 0.95))
        self.assertions_dialog.columnconfigure(1, weight=1)
        self.assertions_dialog.rowconfigure(4, weight=1)
        self.canvas = Border(self.assertions_dialog, self.master)            
        self.canvas.title_1.config(text="Assertions, Citations, Sources & Repositories")
        self.canvas.title_2.config(text="input: {}".format(self.finding_id))

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.window.vsb = Scrollbar(
            self.assertions_dialog, 
            hideable=True, 
            command=self.canvas.yview,
            width=scridth)
        self.window.hsb = Scrollbar(
            self.assertions_dialog, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=self.window.hsb.set, 
            yscrollcommand=self.window.vsb.set)
        self.window.vsb.grid(column=2, row=4, sticky='ns')
        self.window.hsb.grid(column=1, row=5, sticky='ew')

        buttonbox = Frame(self.window)
        b1 = Button(buttonbox, text="OK", width=7, command=ok)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, minsize=60)
        buttonbox.grid(column=1, row=3, sticky='se', pady=6)

        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.frm = Frame(self.window)
        self.frm.grid(column=1, row=2, sticky='news', pady=12)

        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(1, weight=1)
        lab = LabelHeader(
            self.window, text=self.finding_id, justify='left', wraplength=600)
        lab.grid(column=1, row=1, sticky='news', ipady=6, ipadx=6)

    def make_inputs(self):
        print("line", looky(seeline()).lineno, "self.source_count, self.inwidg, self.finding_id:", self.source_count, self.inwidg, self.finding_id)




''' DB TABLES
finding
person
citation
place
claim                      
claims_citations                      
claims_findings                       
claims_notes                
claims_roles
repository
links_links           
contact                                
source
sources_repositories
'''  