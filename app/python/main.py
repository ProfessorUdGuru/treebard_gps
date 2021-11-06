# main.py

import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from files import (
    get_current_file, current_drive, make_tree, open_tree, 
    save_as,save_copy_as, rename_tree, project_path)
from widgets import (
    Frame, LabelH2, LabelH3, Label, Button, Canvas, ButtonPlain, FrameHilited1,
    CanvasHilited, FrameHilited3, Toplevel, LabelBoilerplate)
from styles import config_generic
from custom_tabbed_widget import TabBook
from dropdown import DropdownMenu, placeholder
from autofill import EntryAutoHilited    
from scrolling import Scrollbar    
from events_table import EventsTable
from gallery import Gallery
from colorizer import Colorizer
from font_picker import FontPicker
from names import (
    get_name_with_id, make_all_names_list_for_person_select,
    open_new_person_dialog, get_any_name_with_id)
from search import PersonSearch
from query_strings import select_images_entities_main_image
from utes import create_tooltip
import dev_tools as dt
from dev_tools import looky, seeline







MAIN_TABS = (
    ("person", "P"), ("attributes", "B"), ("places", "L"), ("sources", "S"), 
    ("names", "N"), ("reports", "R"), ("charts", "A"), ("projects", "J"), 
    ("graphics", "G"), ("types", "T"), ("preferences", "E"))

RIGHT_PANEL_TABS = (("images", "I"), ("do list", "O"))

PREFS_TABS = (("general", "X"), ("colors", "C"), ("fonts", "F"), ("dates", "D"), ("images", "M"))

ICONS = (
    'open', 'cut', 'copy', 'paste', 'print', 'home', 'first', 
    'previous', 'next', 'last', 'search', 'add', 'settings', 
    'note', 'back', 'forward') 

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
        self.make_menus()
        self.get_current_values()

    def make_menus(self):
        self.make_top_menu()
        self.make_icon_menu()

    def make_top_menu(self):
        top_menu = DropdownMenu(self.master.menu_frame, self.root) 
        top_menu.grid(column=0, row=0)

    def make_icon_menu(self):
        ribbon = {}        
        r = 0
        for name in ICONS:
            file = '{}/images/{}.gif'.format(project_path, name)
            pil_img = Image.open(file)
            tk_img = ImageTk.PhotoImage(pil_img, master=self.master)
            icon = ButtonPlain(
                self.master.ribbon_frame,
                image=tk_img,
                command=lambda name=name: placeholder(name),
                takefocus=0)
            icon.image = tk_img
            icon.grid(column=r, row=0)
            create_tooltip(icon, name.title())
            ribbon[name] = icon
            r += 1
        
        ribbon['open'].config(command=lambda: open_tree(self.root))
        ribbon['home'].config(command=self.root.quit)


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
        footer.columnconfigure(0, weight=1)
        footer.rowconfigure(0, weight=1)  
              
        self.foot_label = LabelBoilerplate(
            footer, 
            text="Treebard GPS is free, portable, open-source, public domain "
                "software written in Python, Tkinter and SQLite.\nTreebard's "
                "purpose is to showcase functionalities that could inspire "
                "developers and users of genealogy database software to expect a "
                "better user experience.\nGPS stands for "    
                "'Genieware Pattern Simulation' because GPS is here to show "
                "the way. Created 2014 - 2022 by Scott Robertson.\nEmail: "
                "stumpednomore-at-gmail.com. Donations: http://gofundme/whearly. "
                "forum/blog: http://treebard.proboards.com. website: "
                "http://treebard.com. repo: https://github.com/ProfessorUdGuru/treebard_gps. ",
            justify='center')

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

        self.att = EventsTable(attributes_tab, self.root, self.treebard, self, attrib=True)
        EventsTable.instances.append(self.att)

        self.findings_table = EventsTable(persons_tab, self.root, self.treebard, self)
        EventsTable.instances.append(self.findings_table)

        options_tabs = TabBook(
            prefs_tab, root=self.root, tabs=PREFS_TABS, side="se", 
            selected='general', case='upper', miny=0.5, minx=0.66)

        colorizer = Colorizer(
            options_tabs.store['colors'],
            self.root,
            tabbook=self.right_panel)
        colorizer.grid(column=0, row=0)

        fontpicker = FontPicker(options_tabs.store['fonts'], self.root, self)
        fontpicker.grid(column=0, row=0)




        # children of self.master i.e. root
        # top_menu & ribbon_menu etc. are gridded in window_border.py

        # children of self
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        current_person_area.grid(column=1, row=1, sticky='w', pady=18)
        self.main_tabs.grid(column=1, row=2, sticky='ew')
        footer.grid(column=1, row=3, sticky='ew')

        # children of main tabs
        persons_tab.grid(column=0, row=0, sticky='news')
        attributes_tab.grid(column=0, row=0, sticky='news')
        self.names_tab.grid(column=0, row=0, sticky='news')
        prefs_tab.grid(column=0, row=0, sticky='news')

        # children of persons_tab
        family_table.grid(column=0, row=0, sticky="news", padx=12, pady=12)
        self.right_panel.grid(column=1, row=0, sticky='w', padx=12, pady=12)
        self.findings_table.grid(
            column=0, row=1, columnspan=2, padx=12, pady=12)

        # children of family_table
        family_canvas.grid(column=0, row=0, sticky="news")
        family_sbv.grid(column=1, row=0, sticky="ns")
        family_sbh.grid(column=0, row=1, sticky="ew")

        # children of attributes tab
        self.att.grid(column=0, row=0)

        # children of self.names_tab

        # children of preferences tab
        options_tabs.grid(column=0, row=0, sticky="news", padx=12, pady=12)

        # children of current_person_area
        self.current_person_label.pack(side="top", pady=12)
        # self.current_person_label.pack(side="top", pady=24)
        instrux.pack(side="left")
        self.person_entry.pack(side="left")
        person_change.pack(side="left", padx=6)
        person_search.pack(side="right")

        # children of images tab
        self.right_panel.store['images'].columnconfigure(0, weight=1)
        self.right_panel.store['images'].rowconfigure(0, weight=1)
        self.top_pic_button.grid(column=0, row=0, sticky='news', padx=3, pady=3)

        # children of footer
        self.foot_label.grid(column=0, row=0, pady=24)

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
        self.person_entry.focus_force()

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
        self.att.current_person = self.current_person
        self.att.redraw(current_person=self.current_person)
        self.person_entry.delete(0, 'end')
        
        self.show_top_pic(self.top_pic_button)

    def open_person_gallery(self):

        person_gallery_dlg = Toplevel(self.root)

        person_gallery_dlg.grid_columnconfigure(0, weight=1)
        person_gallery_dlg.grid_rowconfigure(0, weight=1)
# master, notebook, graphics_tab, root, canvas,
        person_gallery = Gallery(
            person_gallery_dlg, 
            self.main_tabs, 
            self.main_tabs.store['graphics'], # just pass main_tabs & extract this one in instance
            self.root, 
            self.master)

        config_generic(person_gallery_dlg)

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
            img1 = ImageTk.PhotoImage(top, master=self.master)

            top_pic_button.config(image=img1)
            top_pic_button.image = img1

            self.tabbook_x = top.width
            self.tabbook_y = top.height




        






