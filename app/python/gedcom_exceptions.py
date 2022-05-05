# gedcom_exceptions.py

import tkinter as tk
import sqlite3
from widgets import (
    Toplevel, Frame, Button,  LabelH2, Label,  
    configall, Border, Scrollbar, make_formats_dict, Text)
from right_click_menu import RightClickMenu, make_rc_menus
from scrolling import MousewheelScrolling, resize_scrolled_content
from toykinter_widgets import run_statusbar_tooltips
import dev_tools as dt
from dev_tools import looky, seeline



MESSAGES = (
    "", 
)



class GedcomExceptions(Toplevel):
    """ Open dialog without user's prompting when GEDCOM import is complete. """
    def __init__(self, master, root, treebard, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.master = master
        self.root = root
        self.treebard = treebard

        self.formats = make_formats_dict()

        # self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        self.make_widgets()

        self.make_text_file()

    def make_widgets(self):

        self.title('GEDCOM Import Exceptions')
        self.geometry('+100+20')

        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, self.root, self.formats)
        self.canvas.title_1.config(text="Person Search Dialog")
        self.canvas.title_2.config(text="")

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        # self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
        # self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.window.vsb = Scrollbar(
            self, 
            hideable=True, 
            command=self.canvas.yview,
            width=scridth)
        self.window.hsb = Scrollbar(
            self, 
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
        self.b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=self.cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1)
        buttonbox.grid(column=0, row=3, sticky='e', pady=6)

        self.b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.make_inputs()
        configall(self, self.formats)
        self.maxsize(
            int(self.winfo_screenwidth() * 0.90),
            int(self.winfo_screenheight() * 0.90))

    def make_inputs(self):

        self.columnconfigure(1, weight=1)

        header = Frame(self.window)
        header.grid(column=0, row=0, sticky='ew')

        self.search_dlg_heading = LabelH2(
            header, 
            text='Items Not Imported by GEDCOM')
        self.search_dlg_heading.grid(column=0, row=0, pady=(24,0))

        head_msg = "Items listed below can be input manually using Treebard's interface.\nInstructions are included for each category of failed import.\nThis document has been saved as a text file with the same name as the GEDCOM file you imported."
        instrux = Label(header, text=head_msg)
        instrux.grid(column=0, row=1, sticky='e', padx=24, pady=12)

        self.search_table = Frame(self.window)
        self.search_table.grid(
            column=0, row=1, sticky='news', padx=48, pady=48)

        # visited = (
            # (self.search_input, 
                # "Person Search Input", 
                # "Type any part of any name or ID number; table will fill "
                    # "with matches."),
            # (self.search_table, 
                # "Person Search Table", 
                # "Select highlighted row with Enter or Space key to change "
                    # "current person, or click any row."))   
     
        # run_statusbar_tooltips(
            # visited, 
            # self.canvas.statusbar.status_label, 
            # self.canvas.statusbar.tooltip_label)

        # rcm_widgets = (
            # self.search_input, self.search_dlg_heading, self.search_table)
        # make_rc_menus(
            # rcm_widgets, 
            # self.rc_menu, 
            # search_person_help_msg) 

        resize_scrolled_content(self, self.canvas, self.window)

    def make_text_file(self):
        pass

    def cancel(self):
        self.destroy()

    def close_search_dialog(self):
        self.destroy()

if __name__ == "__main__":

    root = tk.Tk()



    ged = GedcomExceptions(root, root, None)

    root.mainloop()


