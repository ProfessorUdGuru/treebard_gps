# main.py

import tkinter as tk
from widgets import Frame, LabelH3, Label
from window_border import Border
from scrolling import Scrollbar    
from events_table import EventsTable
import dev_tools as dt



class Main(Frame):
    def __init__(self, master, view, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master # the main canvas (instance of Border class)
        self.view = view
        self.treebard = treebard
        # print('19 self.view is', self.view)
        self.make_widgets()

    def make_menus(self):
        
        menu = Label(self.master.menu, text='menu bar')
        icon1 = Label(self.master.ribbon, text='ribbon menu')

        menu.grid()
        icon1.grid()

    def make_scrollbars(self):

        self.vsb = Scrollbar(
            self.view, 
            hideable=True, 
            command=self.master.yview,
            width=20)
        self.hsb = Scrollbar(
            self.view, 
            hideable=True, 
            width=20, 
            orient='horizontal',
            command=self.master.xview)
        self.master.config(
            xscrollcommand=self.hsb.set, 
            yscrollcommand=self.vsb.set)
        self.vsb.grid(column=2, row=4, sticky='ns')
        self.hsb.grid(column=1, row=5, sticky='ew')

    def make_widgets(self):

        self.make_scrollbars()

        self.make_menus()

        scridth = 20
        scridth_n = Frame(self, height=scridth)
        scridth_w = Frame(self, width=scridth)
        header = Frame(self)     
        heading = LabelH3(header, text='header text')
        self.main_tabs = Frame(self)
        persons_tab = Frame(self.main_tabs)
        footer = Frame(self)
        boilerplate = Label(footer, text='footer')

        current_person_area = Frame(persons_tab)
        current_person = LabelH3(current_person_area)
        right_panel = Frame(persons_tab)
        attributes_table = Label(right_panel, text='attributes table')

        findings_table = EventsTable(persons_tab, self.view, self.treebard)

        # children of self
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        header.grid(column=1, row=1, sticky='ew')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.main_tabs.grid(column=1, row=2, sticky='ew')
        footer.grid(column=1, row=3, sticky='ew')

        # children of header
        heading.grid(column=0, row=0, sticky='ew')

        # children of self.main_tabs
        persons_tab.grid(column=0, row=0, sticky='news')

        # children of persons_tab
        current_person_area.grid(column=0, row=0, sticky='w')
        right_panel.grid(column=1, row=0, sticky='e')
        findings_table.grid(column=0, row=1, columnspan=2, sticky='news')

        # children of current_person_area
        current_person.grid(column=0, row=0, sticky='w')

        # children of right_panel
        attributes_table.grid(column=0, row=0, sticky='news')

        # children of footer
        boilerplate.grid()








