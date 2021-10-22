# main.py

import tkinter as tk
from widgets import Frame, LabelH2, LabelH3, Label, Button
from custom_tabbed_widget import TabBook
from autofill import EntryAutoHilited    
from scrolling import Scrollbar    
from events_table import EventsTable
from names import (
    get_name_with_id, make_values_list_for_person_select,
    open_new_person_dialog, get_any_name_with_id)
from search import PersonSearch
# from search import PersonSearch, open_names_tab
import dev_tools as dt
from dev_tools import looky, seeline







MAIN_TABS = [
    ("person", "P"), ("places", "L"), ("sources", "S"), ("names", "N"), 
    ("reports", "R"), ("charts", "A"), ("projects", "J"), ("graphics", "G"), 
    ("types", "T"), ("preferences", "E")]

RIGHT_PANEL_TABS = [("attributes", "B"), ("gallery", "Y")]   

PREFS_TABS = [("general", "X"), ("colors", "C"), ("fonts", "F"), ("dates", "D")]

class Main(Frame):
    def __init__(self, master, root, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master # the main canvas (instance of Border class)
        self.root = root
        self.treebard = treebard

        self.current_person = None
        self.current_person_name = ""
        self.make_widgets()
        self.get_current_values()

    def make_menus(self):
        
        menu = Label(self.master.menu, text='menu bar')
        icon1 = Label(self.master.ribbon, text='ribbon menu')

        menu.grid()
        icon1.grid()

    def make_scrollbars(self):

        self.vsb = Scrollbar(
            self.root, 
            hideable=True, 
            command=self.master.yview,
            width=20)
        self.hsb = Scrollbar(
            self.root, 
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
        current_person_area = Frame(self)
        self.main_tabs = TabBook(
            self, root=self.root, tabs=MAIN_TABS, 
            selected='person', case='upper', miny=0.66)
        persons_tab = Frame(self.main_tabs.store["person"])
        self.names_tab = Frame(self.main_tabs.store["names"])
        prefs_tab = Frame(self.main_tabs.store["preferences"])
        footer = Frame(self)
        boilerplate = Label(footer, text='footer')

        self.current_person_label = LabelH2(current_person_area)
        instrux = LabelH3(current_person_area, text="Change current person to: ")
        self.person_entry = EntryAutoHilited(
            current_person_area, 
            width=36,
            autofill=True)
        person_change = Button(
            current_person_area, text="OK", command=self.change_person)
        person_search = Button(
            current_person_area, 
            text="Find or Create a Person", 
            command=self.open_person_search)
        right_panel = TabBook(
            persons_tab, root=self.root, tabs=RIGHT_PANEL_TABS, side="se", 
            selected='gallery', case='upper', miny=0.25, minx=0.20)

        attributes_table = Label(
            right_panel.store["attributes"], text='attributes table')

        self.findings_table = EventsTable(persons_tab, self.root, self.treebard)

        # self.person_add = PersonAdd(
            # self.names_tab, self.person_entry, self.root, self.treebard)

        options_tabs = TabBook(
            prefs_tab, root=self.root, tabs=PREFS_TABS, side="se", 
            selected='general', case='upper', miny=0.5, minx=0.66)

        # children of self
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        current_person_area.grid(column=1, row=1, sticky='ew', pady=18)
        self.main_tabs.grid(column=1, row=2, sticky='ew')
        footer.grid(column=1, row=3, sticky='ew')

        # children of main tabs
        persons_tab.grid(column=0, row=0, sticky='news')
        self.names_tab.grid(column=0, row=0, sticky='news')
        prefs_tab.grid(column=0, row=0, sticky='news')

        # children of persons_tab
        right_panel.grid(column=1, row=0, sticky='e', padx=12, pady=12)
        self.findings_table.grid(
            column=0, row=1, columnspan=2, sticky='news', padx=12, pady=12)

        # children of self.names_tab
        # self.person_add.grid(column=0, row=0, sticky="news", padx=12, pady=12)

        # children of preferences tab
        options_tabs.grid(column=0, row=0, sticky="news", padx=12, pady=12)
        # children of current_person_area
        self.current_person_label.pack(side="top", pady=24)
        instrux.pack(side="left")
        self.person_entry.pack(side="left")
        person_change.pack(side="left", padx=6)
        person_search.pack(side="right")

        # children of right_panel
        attributes_table.grid(column=0, row=0, sticky='e')

        # children of footer
        boilerplate.grid()

    def get_current_values(self):

        all_birth_names = make_values_list_for_person_select()
        self.current_person = self.findings_table.current_person
        self.current_person_name = get_name_with_id(self.current_person)
        self.current_person_label.config(
            text="Current Person (ID): {} ({})".format(
                self.current_person_name, self.current_person))
        self.person_autofill_values = EntryAutoHilited.create_lists(
            all_birth_names)
        self.person_entry.values = self.person_autofill_values

    def open_person_search(self):
        person_search_dialog = PersonSearch(
            self, 
            self.root,
            self.treebard,
            self.person_entry, 
            self.findings_table,
            names_tab=self.main_tabs.store["names"],
            pic=None)

    

    def change_person(self):
        if "#" not in self.person_entry.get():
            self.current_person = open_new_person_dialog(
                self, self.person_entry, self.root)
        else:
            new_person = self.person_entry.get().split("#")
            self.current_person = int(new_person[1]) 
        self.current_person_name = get_any_name_with_id(self.current_person) 
        # self.current_person_name = get_name_with_id(self.current_person)
        print("line", looky(seeline()).lineno, "len(self.current_person_name):", len(self.current_person_name))
        self.findings_table.current_person = self.current_person
        self.findings_table.redraw(current_person=self.current_person)
        self.person_entry.delete(0, 'end')
        self.current_person_label.config(
            text="Current Person (ID): {} ({})".format(
                self.current_person_name, self.current_person))


        


        






