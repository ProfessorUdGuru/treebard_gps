# pedigree_chart

import tkinter as tk
from widgets import Canvas
from styles import make_formats_dict, config_generic
from right_click_menu import make_rc_menus, RightClickMenu
from message_strings import pedigree_person_tab_msg
import dev_tools as dt

formats = make_formats_dict()

class PedigreeChart(Canvas):
    
    def __init__(self, master, current_person_birthname, root, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.master = master
        self.current_person_birthname = current_person_birthname
        self.root = root

        self.rc_menu = RightClickMenu(self.root)

        self.make_chart()

    def make_chart(self):

        def scroll_start(event):
            self.scan_mark(event.x, event.y)

        def scroll_move(event):
            self.scan_dragto(event.x, event.y, gain=3)

        xsb = tk.Scrollbar(
            self.master, 
            orient="horizontal", 
            command=self.xview,
            width=16)
        ysb = tk.Scrollbar(
            self.master, 
            orient="vertical", 
            command=self.yview,
            width=16)
        self.configure(
            yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.configure(scrollregion=(0,0,1000,1000))

        xsb.grid(row=1, column=0, sticky="ew")
        ysb.grid(row=0, column=1, sticky="ns")
        self.grid(column=0, row=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)        

        # mockup/placeholder till the real one comes
        self.create_text(
            221, 75,
            text='Riccardo Saverio Grimaldo', 
            font=('Times', 16), 
            fill=formats['fg'])
        self.create_line(351, 73, 377, 73,
            fill=formats['fg'])
        self.create_line(351, 77, 377, 77,
            fill=formats['fg'])
        self.create_text(
            447, 75,
            text='Bellissa Ricci', 
            font=('Times', 16), 
            fill=formats['fg'])
        self.create_line(365, 90, 365, 115, 
            fill=formats['fg'])
        self.create_text(
            # 221, 75,
            621, 75,
            text='Donald Wiley Webb', 
            font=('Times', 16), 
            fill=formats['fg'])
        self.create_line(715, 73, 741, 73,
            fill=formats['fg'])
        self.create_line(715, 77, 741, 77,
            fill=formats['fg'])
        self.create_text(
            847, 75,
            text='Maria Tabitha Mullinax', 
            font=('Times', 16), 
            fill=formats['fg'])
        self.create_line(580, 102, 726, 102, 
            fill=formats['fg'])
        self.create_line(580, 102, 580, 115, 
            fill=formats['fg'])
        self.create_line(726, 90, 726, 103, 
            fill=formats['fg'])
        self.create_text(
            356, 125, 
            text='Jeremiah Laurence Grimaldo', 
            font=('Times', 16), 
            fill=formats['fg'],
            tags='current_person'
)
        self.create_line(486, 123, 514, 123,
            fill=formats['fg'])
        self.create_line(486, 127, 514, 127,
            fill=formats['fg'])
        self.create_text(
            582, 125, 
            text='Ronnie Webb', 
            font=('Times', 16), 
            fill=formats['fg'])
        self.create_line(500, 140, 500, 165, 
            fill=formats['fg'])
        self.create_line(350, 165, 650, 165, fill=formats['fg'])
        self.create_line(350, 165, 350, 190,
            fill=formats['fg'])
        self.create_line(650, 165, 650, 190,
            fill=formats['fg'])
        self.create_text(
            350, 205, 
            text='Patricia Grimaldo', 
            font=('Times', 16), 
            fill=formats['fg'])
        self.create_text(
            650, 205, 
            text='Christiana Dalia Grimaldo', 
            font=('Times', 16), 
            fill=formats['fg'])

        # enable panning with mouse
        self.bind("<ButtonPress-1>", scroll_start)
        self.bind("<B1-Motion>", scroll_move)

        rcm_widgets = (self,)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            pedigree_person_tab_msg)

        config_generic(self)

