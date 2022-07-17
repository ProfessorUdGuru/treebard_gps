# main.py


import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from files import current_drive, get_current_file, global_db_path
from widgets import (
    Frame, LabelH2, LabelH3, Label, Button, Canvas, ButtonBigPic, Toplevel, 
    Radiobutton, LabelFrame, Border, TabBook, Scrollbar, fix_tab_traversal,
    EntryAutoPerson, EntryAutoPersonHilited, FontPicker, redraw_person_tab, 
    open_message, Separator, Entry, Checkbutton, Combobox, EntryAutoPlace)
from right_click_menu import RightClickMenu, make_rc_menus
from toykinter_widgets import run_statusbar_tooltips   
from families import NuclearFamiliesTable
from findings_table import FindingsTable
from dates import DatePreferences, OK_MONTHS, get_date_formats
from gallery import Gallery
from colorizer import Colorizer
from messages import main_msg
from messages_context_help import main_help_msg
from persons import (
    make_all_names_dict_for_person_select, check_name, get_original,
    update_person_autofill_values, 
    open_new_person_dialog)
from search import PersonSearch
from query_strings import (
    select_images_elements_main_image, select_current_person_id,
    select_finding_id_birth, select_person_gender_by_id, update_name_type_sorter,
    select_person_id_finding, select_date_finding, select_finding_event_type,
    select_finding_id_death, select_name_all_current, select_all_name_types,
    select_name_type_id_by_string, insert_name_and_type)
import dev_tools as dt
from dev_tools import looky, seeline




MAIN_TABS = (
    ("person", "P"), ("names", "N"), ("assertions", "A"), ("places", "L"), 
    ("sources", "S"), ("reports", "R"), ("charts", "Z"), ("projects", "J"), 
    ("graphics", "G"), ("links", "K"), ("search", "H"), ("types", "T"), 
    ("preferences", "E"))

RIGHT_PANEL_TABS = (("images", "I"), ("do list", "O"))

PREFS_TABS = (
    ("general", "X"), ("colors", "C"), ("fonts", "F"), ("dates", "D"), 
    ("images", "M"))

NUKEFAM_HEADS = ("NAME OF CHILD", "GENDER", "DATE OF BIRTH", "DATE OF DEATH")

def get_current_person():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person_id)
    current_person = cur.fetchone()[0]
    cur.close()
    conn.close()
    return current_person

from widgets import FrameStay
class Main(FrameStay):
    def __init__(self, master, root, treebard, *args, **kwargs):
        FrameStay.__init__(self, master, *args, **kwargs)
        self.master = master # the main canvas (instance of Border class)
        self.root = root
        self.treebard = treebard

        self.current_person = get_current_person()
        self.current_person_name = "" # could be got from index 2 above

        self.place_data = EntryAutoPlace.get_place_values()
        # self.place_data, self.nestings, self.existing_place_names = EntryAutoPlace.get_place_values()

        self.tabbook_x = 300
        self.tabbook_y = 300
        self.SCREEN_SIZE = []
        self.SCREEN_SIZE.append(self.winfo_screenwidth())
        self.SCREEN_SIZE.append(self.winfo_screenheight())

        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        self.person_autofill_values = make_all_names_dict_for_person_select()
        self.make_widgets()
        self.get_current_values()
        self.nukefam_table.make_nukefam_inputs(on_load=True)

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

        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))

        self.make_scrollbars()

        scridth = 20
        scridth_n = Frame(self, height=scridth)
        scridth_w = Frame(self, width=scridth)
        current_person_area = Frame(self)
        self.main_tabs = TabBook(
            self, root=self.root, tabs=MAIN_TABS, 
            selected='person', case='upper', miny=0.66, takefocus=0)
        persons_tab = Frame(self.main_tabs.store["person"])
        places_tab = Frame(self.main_tabs.store["places"], name="placetab")
        sources_tab = Frame(self.main_tabs.store["sources"], name="sourcetab")
        self.names_tab = Frame(self.main_tabs.store["names"])
        prefs_tab = Frame(self.main_tabs.store["preferences"])

        self.current_person_label = LabelH2(current_person_area)
        change_current_person = LabelH3(
            current_person_area, text="Change current person to:")
        self.person_entry = EntryAutoPersonHilited(
            current_person_area, 
            width=36,
            autofill=True)
        EntryAutoPerson.person_autofills.append(self.person_entry)
        person_change = Button(
            current_person_area, text="OK", command=self.change_person)
        person_search = Button(
            current_person_area, 
            text="ADD/FIND", 
            command=self.open_person_search)

        minx = self.tabbook_x/self.SCREEN_SIZE[0]
        miny = self.tabbook_y/self.SCREEN_SIZE[1]

        self.right_panel = TabBook(
            persons_tab, root=self.root, tabs=RIGHT_PANEL_TABS, 
            side="se", selected='images', case='upper', miny=0.25, minx=0.20,
            takefocus=0)
        self.top_pic_button = ButtonBigPic(
            self.right_panel.store['images'],
            command=self.open_person_gallery)

        self.findings_table = FindingsTable(
            persons_tab, 
            self.root, 
            self.treebard, 
            self,  
            self.current_person,
            self.person_autofill_values,
            self.place_data)

        self.nukefam_table = NuclearFamiliesTable(
            persons_tab,
            self.root, 
            self.treebard,
            self.current_person, 
            self.findings_table, 
            self.right_panel,
            self.person_autofill_values)

        fix_tab_traversal(self.nukefam_table, self.findings_table) 

        septor = Separator(persons_tab)

        current_file, current_dir = get_current_file()

        # this does not run on redraw_person_tab, just on load
        if len(current_dir) != 0:
            self.show_top_pic(current_file, current_dir, self.current_person)

        place_gallery = Gallery(
            places_tab, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
            self.root, 
            self.treebard,
            self.SCREEN_SIZE,
            current_place_name="Laramie County, Wyoming, USA")

        source_gallery = Gallery(
            sources_tab, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
            self.root, 
            self.treebard,
            self.SCREEN_SIZE,
            current_source_name="1900 US Census")

        lab665 = LabelH3(self.names_tab, text="Change Current Person Name")

        lab472 = Label(
            self.names_tab, 
            text="Make new name for the current person:", anchor="e")
        self.new_name_input = Entry(self.names_tab, width=25)
        cur.execute(select_all_name_types)
        name_types = [" ".join(i) for i in cur.fetchall()]
        self.new_name_type_cbo = Combobox(self.names_tab, self.root, values=name_types)
        self.new_name_sort_order = Entry(self.names_tab, width=25) # FIX TAB ORDER
        sortbutt = Button(
            self.names_tab, text="Alphabetize as:", 
            command=lambda ent=self.new_name_input, sortent=self.new_name_sort_order: self.make_default_sort_order(ent, sortent))

        for child in (
                self.new_name_input, self.new_name_type_cbo, 
                sortbutt, self.new_name_sort_order):
            child.lift()

        all_names = self.get_current_person_names(conn, cur)
        frm = Frame(self.names_tab)

        self.namevars = {}

        for idx, tup in enumerate(all_names):
            var = tk.IntVar()
            name_id, name, name_type = tup
            chk = Checkbutton(frm, variable=var)
            lab = Label(
                frm,
                anchor="e",
                text="Change name '{}' (name type '{}') to:".format(
                    name, name_type))
            ent = Entry(frm, width=25)
            cbo = Combobox(frm, self.root, values=name_types)
            sortent = Entry(frm, width=25) # FIX TAB ORDER
            self.namevars[name_id] = [var, ent, cbo, sortent]
            bqw = Button(
                frm, text="Alphabetize as:", 
                command=lambda ent=ent, sortent=sortent: self.make_default_sort_order(ent, sortent))

            chk.grid(column=0, row=idx, padx=(12,0))
            lab.grid(column=1, row=idx, sticky="ew")
            ent.grid(column=2, row=idx, padx=(6,0))
            cbo.grid(column=3, row=idx, padx=(12,0))
            bqw.grid(column=4, row=idx, padx=(12,0))
            sortent.grid(column=5, row=idx, padx=12)

            for child in (ent, cbo, bqw, sortent):
                child.lift()

        butt = Button(
            self.names_tab, text="OK", width=8, 
            command=self.update_name)

        options_tabs = TabBook(
            prefs_tab, root=self.root, tabs=PREFS_TABS, 
            side="se", selected='general', case='upper', miny=0.5, minx=0.66)

        general = Frame(options_tabs.store['general'])
        general.columnconfigure(0, weight=1)
        general.rowconfigure(0, weight=1)  
              
        about = Label(
            general, 
            text="Treebard GPS is free, portable, open-source, public domain "
                "software written in Python, Tkinter and SQLite. Treebard's "
                "purpose is to showcase functionalities that could inspire "
                "developers and users of genealogy database software to expect a "
                "better user experience. GPS stands for "    
                "'Genieware Pattern Simulation' because GPS is here to show "
                "the way. Created 2015 - 2022 by Scott Robertson. Email: "
                "stumpednomore-at-gmail.com. "
                "forum/blog: http://treebard.proboards.com. website: "
                "http://treebard.com. repo: https://github.com/ProfessorUdGuru/treebard_gps. ",
            justify='left', 
            wraplength=960)
        general.grid(column=0, row=0, sticky='news')
        about.grid(column=0, row=0, sticky='news', padx=24, pady=24)

        colorizer = Colorizer(
            options_tabs.store['colors'],
            self.root,
            self.rc_menu,
            tabbook=self.right_panel)
        colorizer.grid(column=0, row=0)

        self.fontpicker = FontPicker(options_tabs.store['fonts'], self.root, self)
        self.fontpicker.grid(column=0, row=0)
        self.date_options = DatePreferences(
            options_tabs.store['dates'])
        self.date_options.grid(column=0, row=0)

        # children of self.master i.e. root
        # top_menu & ribbon_menu etc. are gridded in window_border.py

        # children of self
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.rowconfigure(2, weight=1)
        current_person_area.grid(
            column=1, row=1, sticky='w', padx=(0,24), pady=(0,12))
        self.main_tabs.grid(column=1, row=2, sticky='ew')

        # children of main tabs
        persons_tab.grid(column=0, row=0, sticky='news')
        places_tab.grid(column=0, row=0, sticky='news')
        sources_tab.grid(column=0, row=0, sticky='news')
        self.names_tab.grid(column=0, row=0, sticky='news')
        prefs_tab.grid(column=0, row=0, sticky='news')

        # children of persons_tab
        self.nukefam_table.grid(column=0, row=0, sticky="news", padx=12, pady=12)
        septor.grid(column=0, row=1, sticky="we", padx=(12,0))
        self.right_panel.grid(column=1, row=0, sticky='e', padx=12, pady=12)
        self.findings_table.grid(
            column=0, row=2, columnspan=2, padx=12, pady=12)

        # children of self.nukefam_table gridded in families.py
        persons_tab.columnconfigure(1, weight=1)

        # children of places tab
        place_gallery.grid(column=0, row=0)

        # children of sources tab
        source_gallery.grid(column=0, row=0)

        # children of self.names_tab
        lab665.grid(column=0, row=0, padx=12, pady=12)
        lab472.grid(column=0, row=1, sticky="e", padx=(12,0), pady=12)
        self.new_name_input.grid(column=1, row=1, sticky="w", padx=(6,0))
        self.new_name_type_cbo.grid(column=2, row=1, padx=(12,0))
        sortbutt.grid(column=3, row=1, padx=(12,0))
        self.new_name_sort_order.grid(column=4, row=1, padx=12)
        frm.grid(column=0, row=2, columnspan=5)
        butt.grid(column=1, row=3, pady=12)

        # children of preferences tab
        options_tabs.grid(column=0, row=0, sticky="news", padx=12, pady=12)

        # children of current_person_area
        self.current_person_label.pack(side="left", fill="x", expand="0", padx=(0,12))
        change_current_person.pack(side="left", padx=(0,12))
        self.person_entry.pack(side="left", padx=(0,12))
        person_change.pack(side="left", padx=(0,12))
        person_search.pack(side="right")

        # children of images tab
        self.right_panel.store['images'].columnconfigure(0, weight=1)
        self.right_panel.store['images'].rowconfigure(0, weight=1)
        self.top_pic_button.grid(column=0, row=0, sticky='news', padx=3, pady=3)

        visited = (
            (self.person_entry,
                "New Current Person Entry",
                "Name of a change-to current person will auto-fill when you "
                    "start typing. Start or end a new person with a plus sign."),
            (person_change,
                "New Current Person OK Button",
                "Press OK to change current person as per input to the left."),
            (person_search,
                "Person Search Button",
                "Any name or ID of any person in the tree can be searched, "
                    "or a new person can be created."),
            (self.top_pic_button,
                "Current Person Main Image",
                "The current person's main image can be clicked to open a "
                    "gallery  of all that person's linked images."),
            (self.findings_table.finding_input,
                "New Conclusion Input",
                "Input for new conclusions including new event types."),
            (self.findings_table.add_finding_button,
                "New Conclusion Input Button",
                "Press to submit new conclusion indicated to the left."),
            (self.fontpicker.output_sample,
                "",
                "Sample of selected font."),
            (self.fontpicker.font_sizer,
                "Font Size Select",
                "Arrow keys or mouse selects the default text size."),
            (self.fontpicker.cbo.entry,
                "Font Family Select",
                "Select the font family for output text."),
            (self.fontpicker.preview_button,
                "Font Preview Button",
                "Apply selections to sample text only."),
            (self.fontpicker.apply_button,
                "Font Apply Button",
                "Apply selections to all output text."),
            (colorizer.current_display,
                "",
                "Click ID to highlight currently applied swatch."),
            (colorizer.swatch_window,
                "Color Scheme Samples",
                "Click color scheme to try."),
            (colorizer.copy_button,
                "Copy Color Scheme Button",
                "Press to fill inputs with selected color scheme; "
                    "change one or more copied color."),
            (colorizer.apply_button,
                "Apply Color Scheme Button",
                "Apply selected color scheme to everything."),
            (colorizer.add_button,
                "New Color Scheme Button",
                "Save new color scheme using colors filled into the "
                    "four inputs."),
            (colorizer.bg1,
                "Background Color 1 Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.bg2,
                "Background Color 2 Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.bg3,
                "Background Color 3 Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.fg1,
                "Font Color Input",
                "Type hex color string or double-click to open color chooser."),
            (self.findings_table.headers[0],
                "",
                "Press delete key to delete this conclusion row."),
            (self.findings_table.headers[1],
                "",
                "Enter simple or compound date in free order with text for "
                    "month, e.g.: '28 f 1845 to 1846 mar 31'."),
            (self.findings_table.headers[2],
                "",
                "Existing places will auto-fill when you start typing, "
                    "starting with places used most recently."),
            (self.findings_table.headers[3],
                "",
                "Use for short notes. Press button in Notes column to input "
                    "longer notes."),
            (self.findings_table.headers[4],
                "",
                "Age at time of event, in any format."),
            (self.findings_table.headers[5],
                "",
                "Create, add and edit roles adjunct to this event."),
            (self.findings_table.headers[6],
                "",
                "Create, add and edit notes regarding this conclusion."),
            (self.findings_table.headers[7],
                "",
                "View and edit sources, citations and assertions linked to "
                    "this conclusion."), 
            (self.date_options.test_frm, 
                "", 
                "Use top area to test input; bottom area for display settings."),
            (self.date_options.prefcombos['General'], 
                "General Date Format",
                "Select a general type of date display."), 
            (self.date_options.prefcombos['Estimated'], 
                "Estimated Date Prefix",
                "Use estimated dates for unsourced guessed dates."), 
            (self.date_options.prefcombos['Approximate'], 
                "Approximate Date Prefix",
                "Use approximated dates for sourced imprecise dates."), 
            (self.date_options.prefcombos['Calculated'], 
                "Calculated Date Prefix",
                "Calculated dates derived from other data such as age."), 
            (self.date_options.prefcombos['Before/After'], 
                "Before or After Date Prefix",
                "When you know something happened before or after some date."), 
            (self.date_options.prefcombos['Epoch'], 
                "Epoch Date Suffix",
                "'BC' and 'AD' now have more politically correct variations."), 
            (self.date_options.prefcombos['Julian/Gregorian'], 
                "Calendar Era Date Suffix",
                "Mark dates 'old style' or 'new style' for events during "
                "calendar transition times."), 
            (self.date_options.prefcombos['From...To...'], 
                "Format Two Dates in a Span",
                "Something started at one time and lasted till another time."), 
            (self.date_options.prefcombos['Between...And...'], 
                "Format Two Dates in a Range",
                "Something happened within a range between two dates."),  
            (self.date_options.submit, 
                "Submit Changes",
                "The changes you selected will be saved."), 
            (self.date_options.revert, 
                "Revert to Defaults",
                "Date formats will revert to defaults."))

        run_statusbar_tooltips(
            visited, 
            self.master.statusbar.status_label, 
            self.master.statusbar.tooltip_label)

        rcm_widgets = (
            self.person_entry, person_change, person_search, 
            self.top_pic_button, self.findings_table.finding_input, 
            self.fontpicker.font_sizer, self.fontpicker.cbo.entry, 
            self.fontpicker.apply_button,            
            colorizer.header, colorizer.current_display, 
            colorizer.copy_button, colorizer.apply_button,
            colorizer.add_button, colorizer.bg1, colorizer.fg1,
            self.findings_table.headers[0], self.findings_table.headers[1], 
            self.findings_table.headers[2], self.findings_table.headers[3], 
            self.findings_table.headers[4], self.findings_table.headers[5], 
            self.findings_table.headers[6], self.findings_table.headers[7], 
            self.date_options.tester_head,  
            self.date_options.date_test['Date Input I'], 
            self.date_options.date_test['Date Input II'],
            self.date_options.date_test['Date Input III'], 
            self.date_options.pref_head,
            self.date_options.prefcombos['General'].entry, 
            self.date_options.prefcombos['Estimated'].entry, 
            self.date_options.prefcombos['Approximate'].entry, 
            self.date_options.prefcombos['Calculated'].entry, 
            self.date_options.prefcombos['Before/After'].entry, 
            self.date_options.prefcombos['Epoch'].entry, 
            self.date_options.prefcombos['Julian/Gregorian'].entry, 
            self.date_options.prefcombos['From...To...'].entry, 
            self.date_options.prefcombos['Between...And...'].entry, 
            self.date_options.submit, self.date_options.revert)
                
        make_rc_menus(rcm_widgets, self.rc_menu, main_help_msg)

        cur.execute("DETACH tree")
        cur.close()
        conn.close()

    def get_current_values(self):
        self.current_person_name = self.person_autofill_values[self.current_person][0]["name"]       
        self.current_person_label.config(
            text="Current Person (ID): {} ({})".format(
                self.current_person_name, self.current_person))
        self.person_entry.values = self.person_autofill_values
        self.person_entry.focus_force()

    def open_person_search(self):
        person_search_dialog = PersonSearch(
            self, 
            self.root,
            self.treebard,
            self.person_entry, 
            self.findings_table,
            self.show_top_pic,
            self.person_autofill_values)    

    def change_person(self):

        def err_done1(entry, msg):
            entry.delete(0, 'end')
            msg1[0].grab_release()
            msg1[0].destroy()
            entry.focus_set()

        name_data = check_name(ent=self.person_entry)
        if name_data is None:
            msg1 = open_message(
                self, 
                main_msg[0], 
                "Person Name Unknown", 
                "OK")
            msg1[0].grab_set()
            msg1[2].config(
                command=lambda entry=self.person_entry, msg=msg1: err_done1(
                    entry, msg))
            return
        elif name_data == "add_new_person":
            old_current_person = self.current_person
            self.current_person = open_new_person_dialog(
                self, self.person_entry, self.root, self.treebard, 
                person_autofill_values=self.person_autofill_values)
            if self.current_person is None:
                self.current_person = old_current_person 
            else:
                self.person_autofill_values = update_person_autofill_values()
        else:
            self.current_person_name = name_data[0]["name"]
            self.current_person = name_data[1]

        self.findings_table.current_person = self.current_person
        redraw_person_tab(
            main_window=self, 
            current_person=self.current_person, 
            current_name=self.current_person_name)

    def open_person_gallery(self):
        person_gallery_dlg = Toplevel(self.root)
        gallery_canvas = Border(person_gallery_dlg, self.root)
           
        person_gallery = Gallery(
            gallery_canvas, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
            self.root, 
            self.treebard,
            self.SCREEN_SIZE,
            dialog=person_gallery_dlg,
            current_person=self.current_person,
            current_person_name=self.current_person_name)

    def show_top_pic(self, current_file, current_dir, current_person):
        """ Trying to change the file names on the default images created an
            unprecedented problem I'll note here to save time in the future.
            The program kept trying to use old values for image strings that
            no longer existed anywhere. To solve it I had to hard code a value
            for top_pic below (see 'SAVE FOREVER') and when the correct line was
            uncommented, the old values had cleared and all was well. It took
            two hours to get around to trying something so weird because SQLite
            has never let me down before, however I suspect it might have been
            Pillow that was trying to use a cached value, not SQLite. Or it
            could be my mistake that I haven't found yet.
        """
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        # Due to a possible Pillow glitch, manually changing image names in db might
        #   result in anomalous use of old values. If so, exchange these 2 lines
        #   for the commented line below, then change back. SAVE FOREVER*****
        cur.execute(select_images_elements_main_image, (current_person,)) #****      
        top_pic = cur.fetchone() #************
        # top_pic = "0_default_image_unisex.jpg" # SAVE FOREVER************
        cur.close()
        conn.close()
        if top_pic:
            img_stg = ''.join(top_pic)
            new_stg = '{}treebard_gps/data/{}/images/{}'.format(
                current_drive, current_dir, img_stg)
            top = Image.open(new_stg)
            img1 = ImageTk.PhotoImage(top, master=self.master)

            self.top_pic_button.config(image=img1)
            self.top_pic_button.image = img1

            self.tabbook_x = top.width
            self.tabbook_y = top.height

    def get_current_person_names(self, conn, cur):

        cur.execute(select_name_all_current, (self.current_person,))
        all_names = cur.fetchall()

        return all_names

    def update_name(self):

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        for k,v in self.namevars.items():
            if v[0].get() == 1:
                ent, cbo, sortent = v[1:]
                name = ent.get()
                name_id = k
                name_type = cbo.entry.get()
                sorter = sortent.get()
                cur.execute(select_name_type_id_by_string, (name_type,))
                name_type_id = cur.fetchone()[0]
                cur.execute(update_name_type_sorter, (name, name_type_id, sorter, name_id))
                conn.commit()
                ent.delete(0, "end")
                cbo.entry.delete(0, "end")
                sortent.delete(0, "end")

        new_name = self.new_name_input.get()
        name_type = self.new_name_type_cbo.entry.get()
        if len(new_name) == 0 or len(name_type) == 0:
            cur.close()
            conn.close()
            return
        cur.execute(select_name_type_id_by_string, (name_type,))
        name_type_id = cur.fetchone()[0]
        cur.execute(
            insert_name_and_type, (
                new_name, name_type_id, 
                self.current_person, 
                self.new_name_sort_order.get()))
        conn.commit()
        self.new_name_input.delete(0, 'end')
        self.new_name_type_cbo.entry.delete(0, 'end')
        self.new_name_sort_order.delete(0, "end")

        cur.close()
        conn.close()

    def make_default_sort_order(self, ent, sortent):
        new_name = ent.get().split()
        last = new_name.pop()
        last = "{},".format(last)
        new_name.insert(0, last)
        new_name = " ".join(new_name)
        sortent.delete(0, "end")        
        sortent.insert(0, new_name)  
        




        






