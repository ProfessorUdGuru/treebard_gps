# main.py

import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from files import get_current_file, current_drive
from widgets import (
    Frame, LabelH2, LabelH3, Label, Button, Canvas, ButtonPlain, FrameHilited1,
    CanvasHilited, FrameHilited3, Toplevel)
from custom_tabbed_widget import TabBook
from autofill import EntryAutoHilited    
from scrolling import Scrollbar    
from events_table import EventsTable
from names import (
    get_name_with_id, make_all_names_list_for_person_select,
    open_new_person_dialog, get_any_name_with_id)
from search import PersonSearch
from query_strings import select_images_entities_main_image
import dev_tools as dt
from dev_tools import looky, seeline







MAIN_TABS = (
    ("person", "P"), ("attributes", "B"), ("places", "L"), ("sources", "S"), 
    ("names", "N"), ("reports", "R"), ("charts", "A"), ("projects", "J"), 
    ("graphics", "G"), ("types", "T"), ("preferences", "E"))

RIGHT_PANEL_TABS = (("images", "I"), ("do list", "O"))

PREFS_TABS = (("general", "X"), ("colors", "C"), ("fonts", "F"), ("dates", "D"))

class Main(Frame):
    def __init__(self, master, root, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master # the main canvas (instance of Border class)
        self.root = root
        self.treebard = treebard

        self.current_person = None
        self.current_person_name = ""
        self.tabbook_x = 300
        self.tabbook_y = 300
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()


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
            selected='person', case='upper', miny=0.66, takefocus=0)
        persons_tab = Frame(self.main_tabs.store["person"])
        attributes_tab = Frame(self.main_tabs.store["attributes"])
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

        family_table = Frame(persons_tab)
        family_table.columnconfigure(0, weight=1)
        family_table.rowconfigure(0, weight=1)
        family_canvas = Canvas(family_table, width=800, height=400)
        family_window = Frame(family_canvas)
        family_canvas.create_window(0, 0, anchor="nw", window=family_window)
        family_canvas.config(scrollregion=(0, 0, 1000, 700))
        family_sbv = Scrollbar(
            family_table, 
            command=family_canvas.yview)
        family_canvas.config(yscrollcommand=family_sbv.set)

        family_sbh = Scrollbar(
            family_table, 
            orient='horizontal', 
            command=family_canvas.xview)
        family_canvas.config(xscrollcommand=family_sbh.set)

        minx = self.tabbook_x/self.screen_width
        miny = self.tabbook_y/self.screen_height

        self.right_panel = TabBook(
            persons_tab, root=self.root, tabs=RIGHT_PANEL_TABS, side="se", 
            selected='images', case='upper', miny=0.25, minx=0.20, takefocus=0)

        self.top_pic_button = ButtonPlain(
            self.right_panel.store['images'],
            command=self.open_person_gallery)

        self.show_top_pic(self.top_pic_button)

        self.att = EventsTable(attributes_tab, self.root, self.treebard, attrib=True)
        EventsTable.instances.append(self.att)

        self.findings_table = EventsTable(persons_tab, self.root, self.treebard)
        EventsTable.instances.append(self.findings_table)
        print("line", looky(seeline()).lineno, "EventsTable.instances:", EventsTable.instances)

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
        attributes_tab.grid(column=0, row=0, sticky='news')
        self.names_tab.grid(column=0, row=0, sticky='news')
        prefs_tab.grid(column=0, row=0, sticky='news')

        # children of persons_tab
        family_table.grid(column=0, row=0, sticky="news", padx=12, pady=12)
        self.right_panel.grid(column=1, row=0, sticky='e', padx=12, pady=12)
        self.findings_table.grid(
            column=0, row=1, columnspan=2, sticky='news', padx=12, pady=12)

        # children of family_table
        family_canvas.grid(column=0, row=0, sticky="news")
        family_sbv.grid(column=1, row=0, sticky="ns")
        family_sbh.grid(column=0, row=1, sticky="ew")

        # children of attributes tab
        self.att.grid(column=0, row=0, sticky='e')

        # children of self.names_tab

        # children of preferences tab
        options_tabs.grid(column=0, row=0, sticky="news", padx=12, pady=12)

        # children of current_person_area
        self.current_person_label.pack(side="top", pady=24)
        instrux.pack(side="left")
        self.person_entry.pack(side="left")
        person_change.pack(side="left", padx=6)
        person_search.pack(side="right")

        # children of images tab
        self.right_panel.store['images'].columnconfigure(0, weight=1)
        self.right_panel.store['images'].rowconfigure(0, weight=1)
        self.top_pic_button.grid(column=0, row=0, sticky='news', padx=3, pady=3)

        # children of footer
        boilerplate.grid()

    def get_current_values(self):
        all_names = make_all_names_list_for_person_select()
        self.current_person = self.findings_table.current_person
        self.current_person_name = get_any_name_with_id(self.current_person)
        if type(self.current_person_name) is tuple:
            use_name = list(self.current_person_name)
            self.current_person_name = "({}) {}".format(use_name[1], use_name[0])
        self.current_person_label.config(
            text="Current Person (ID): {} ({})".format(
                self.current_person_name, self.current_person))
        self.person_autofill_values = EntryAutoHilited.create_lists(
            all_names)
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
            old_current_person = self.current_person
            self.current_person = open_new_person_dialog(
                self, self.person_entry, self.root)
            if self.current_person is None:
                self.current_person = old_current_person
        else:
            new_person = self.person_entry.get().split("#")
            self.current_person = int(new_person[1])
        self.current_person_name = get_any_name_with_id(self.current_person)
        if type(self.current_person_name) is tuple:
            currents = list(self.current_person_name)
            self.current_person_name = currents[0]
            name_type = currents[1]
            self.current_person_label.config(
                text="Current Person (ID): ({}) {} ({})".format(
                    name_type, self.current_person_name, self.current_person))
        else:
            self.current_person_label.config(
                text="Current Person (ID): {} ({})".format(
                    self.current_person_name, self.current_person))
        self.findings_table.current_person = self.current_person
        self.findings_table.redraw(current_person=self.current_person)
        self.person_entry.delete(0, 'end')
        
        self.show_top_pic(self.top_pic_button)

    def open_person_gallery(self):
        pass

    def show_top_pic(self, top_pic_button):
        current_file_tup = get_current_file()
        current_file = current_file_tup[0]
        image_dir = current_file_tup[1]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_images_entities_main_image)

        top_pic = cur.fetchone()
        cur.close()
        conn.close()

        if top_pic:
            img_stg = ''.join(top_pic)
            new_stg = '{}treebard_gps/data/{}/images/{}'.format(
                current_drive, image_dir, img_stg)

            top = Image.open(new_stg)
            img1 = ImageTk.PhotoImage(top)

            top_pic_button.config(image=img1)
            top_pic_button.image = img1

            self.tabbook_x = top.width
            self.tabbook_y = top.height



        






