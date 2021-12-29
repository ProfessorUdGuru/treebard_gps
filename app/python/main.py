# main.py

'''
    Dev Terminology:
    "brood": the children of a specific biological mother and father, without
        regard for whether or not the two people are married to each other. 
    "nuke": nuclear family, from the perspective of the current person only, so
        this includes his two biological parents, a person with whom he/she has
        bred, and the brood of that coupling. Don't use words like "spouse", 
        which assume that a brood's parents are married to each other. Treebard
        has kin types and there may come a time (reports?) where it will be
        appropriate to use kin types which the user specifies, such as
        "spouse", "fiancee", etc.
    
'''

import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from files import current_drive, get_current_file
from styles import make_formats_dict
from widgets import (
    Frame, LabelH2, LabelH3, Label, Button, Canvas, ButtonBigPic, FrameHilited1,
    CanvasHilited, FrameHilited3, Toplevel, LabelBoilerplate, LabelEntry,
    Radiobutton, LabelFrame)
from window_border import Border
from custom_tabbed_widget import TabBook
from autofill import EntryAutoHilited, EntryAuto    
from scrolling import Scrollbar    
from families import NuclearFamiliesTable
from events_table import EventsTable
from dates import DatePreferences, OK_MONTHS, get_date_formats
from gallery import Gallery
from colorizer import Colorizer
from toykinter_widgets import run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from messages_context_help import main_help_msg
from font_picker import FontPicker
from names import (
    make_all_names_list_for_person_select, open_new_person_dialog, 
    get_any_name_with_id)
from search import PersonSearch
from query_strings import (
    select_images_elements_main_image, select_current_person_id,
    select_finding_id_birth, select_findings_persons_ma_id1, 
    select_findings_persons_pa_id1, select_findings_persons_ma_id2, 
    select_findings_persons_pa_id2, select_findings_persons_partner1,
    select_findings_persons_partner2, select_person_id_gender,
    select_person_id_finding, select_date_finding, select_finding_event_type,
    select_finding_id_death, select_finding_death_date, 
    select_findings_persons_id_kin_type1, select_findings_persons_id_kin_type2,
    update_findings_persons_by_id1, update_findings_persons_by_id2,
    update_findings_persons_by_id1_unlink, update_findings_persons_by_id2_unlink,
)
import dev_tools as dt
from dev_tools import looky, seeline



MAIN_TABS = (
    ("person", "P"), ("attributes", "B"), ("places", "L"), ("sources", "S"), 
    ("names", "N"), ("reports", "R"), ("charts", "A"), ("projects", "J"), 
    ("graphics", "G"), ("links", "K"), ("search", "H"), ("types", "T"), 
    ("preferences", "E"))

RIGHT_PANEL_TABS = (("images", "I"), ("do list", "O"))

PREFS_TABS = (("general", "X"), ("colors", "C"), ("fonts", "F"), ("dates", "D"), 
    ("images", "M"))

NUKE_HEADS = ("NAME OF CHILD", "GENDER", "DATE OF BIRTH", "DATE OF DEATH")

class Main(Frame):
    def __init__(self, master, root, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master # the main canvas (instance of Border class)
        self.root = root
        self.treebard = treebard

        self.formats = make_formats_dict()
        self.current_person = None
        self.current_person_name = ""
        self.tabbook_x = 300
        self.tabbook_y = 300
        self.SCREEN_SIZE = []
        self.SCREEN_SIZE.append(self.winfo_screenwidth())
        self.SCREEN_SIZE.append(self.winfo_screenheight())

        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        all_names = make_all_names_list_for_person_select()
        self.person_autofill_values = EntryAutoHilited.create_lists(all_names)
        self.make_widgets()
        self.get_current_values()

        self.nuke_table.make_nuke_inputs()

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
        places_tab = Frame(self.main_tabs.store["places"], name="placetab")
        sources_tab = Frame(self.main_tabs.store["sources"], name="sourcetab")
        self.names_tab = Frame(self.main_tabs.store["names"])
        prefs_tab = Frame(self.main_tabs.store["preferences"])

        self.current_person_label = LabelH2(current_person_area)
        change_current_person = LabelH3(
            current_person_area, text="Change current person to:")
        self.person_entry = EntryAutoHilited(
            current_person_area, self.formats, 
            width=36,
            autofill=True)
        person_change = Button(
            current_person_area, text="OK", command=self.change_person)
        person_search = Button(
            current_person_area, 
            text="Find or Create a Person", 
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

        self.findings_table = EventsTable(
            persons_tab, self.root, self.treebard, self, self.formats)

        EventsTable.instances.append(self.findings_table)
        self.current_person = self.findings_table.current_person

        self.att = EventsTable(
            attributes_tab, self.root, self.treebard, 
            self, self.formats, attrib=True)
        EventsTable.instances.append(self.att)

        self.nuke_table = NuclearFamiliesTable(
            persons_tab,
            self.root, 
            self.treebard,
            self.current_person, 
            self.findings_table, 
            self.right_panel,
            self.formats,
            person_autofill_values=self.person_autofill_values)

        current_file, current_dir = get_current_file()
        # this does not run on redraw, just on load
        if len(current_dir) != 0:
            self.show_top_pic(current_file, current_dir, self.current_person)

        place_gallery = Gallery(
            places_tab, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
            self.formats,
            self.root, 
            self.treebard,
            self.SCREEN_SIZE,
            current_place_name="Laramie County, Wyoming, USA")

        source_gallery = Gallery(
            sources_tab, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
            self.formats,
            self.root, 
            self.treebard,
            self.SCREEN_SIZE,
            current_source_name="1900 US Census")

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
                "the way. Created 2014 - 2022 by Scott Robertson. Email: "
                "stumpednomore-at-gmail.com. Donations: http://gofundme/whearly. "
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
            self.formats,
            tabbook=self.right_panel)
        colorizer.grid(column=0, row=0)

        self.fontpicker = FontPicker(options_tabs.store['fonts'], self.root, self)
        self.fontpicker.grid(column=0, row=0)
        self.date_options = DatePreferences(
            options_tabs.store['dates'], self.formats)
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
        attributes_tab.grid(column=0, row=0, sticky='news')
        places_tab.grid(column=0, row=0, sticky='news')
        sources_tab.grid(column=0, row=0, sticky='news')
        self.names_tab.grid(column=0, row=0, sticky='news')
        prefs_tab.grid(column=0, row=0, sticky='news')

        # children of persons_tab
        self.nuke_table.grid(column=0, row=0, sticky="news", padx=12, pady=12)
        self.right_panel.grid(column=1, row=0, sticky='e', padx=12, pady=12)
        self.findings_table.grid(
            column=0, row=1, columnspan=2, padx=12, pady=12)

        # children of self.nuke_table gridded in families.py
        persons_tab.columnconfigure(1, weight=1)

        # children of attributes tab
        self.att.grid(column=0, row=0)

        # children of places tab
        place_gallery.grid(column=0, row=0)

        # children of sources tab
        source_gallery.grid(column=0, row=0)

        # children of self.names_tab

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
                "Any name of new current person and their ID will auto-fill "
                    "when you start typing; a new person can be entered also. "),
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
            (self.findings_table.event_input,
                "New Event or Attribute Input",
                "Input for new events or attributes including new event types."),
            (self.findings_table.add_event_button,
                "New Event or Attribute Input Button",
                "Press to submit new event or attribute indicated to the left."),
            (self.att.event_input,
                "New Event or Attribute Input",
                "Input for new events or attributes including new event types."),
            (self.att.add_event_button,
                "New Event or Attribute Input Button",
                "Press to submit new event or attribute indicated to the left."),
            (self.fontpicker.output_sample,
                "",
                "Sample of selected font."),
            (self.fontpicker.font_size,
                "Font Size Select",
                "Select the font size for normal text."),
            (self.fontpicker.cbo.entry,
                "Font Family Select",
                "Select the font family for output text."),
            (self.fontpicker.apply_button,
                "Apply Button",
                "Apply selections to all output text. Input font family is "
					"chosen by Treebard."),
            (colorizer.swatch_window,
                "Color Scheme Samples",
                "Click color scheme to try."),
            (colorizer.try_button,
                "Try Color Scheme Button",
                "Try selected color scheme when tabbing through samples."),
            (colorizer.copy_button,
                "Copy Color Scheme Button",
                "Press to fill inputs with selected color scheme; "
                    "change one or more copied color."),
            (colorizer.apply_button,
                "Apply Color Scheme Button",
                "Apply selected color scheme to everything."),
            (colorizer.new_button,
                "New Color Scheme Button",
                "Store new color scheme using colors filled into the "
                    "four inputs."),
            (colorizer.entries_combos[0],
                "Background Color 1 Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.entries_combos[1],
                "Background Color 2 Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.entries_combos[2],
                "Background Color 3 Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.entries_combos[3],
                "Font Color Input",
                "Type hex color string or double-click to open color chooser."),
            (colorizer.domain_tips[0],
                "",
                "Choose the main background color."),
            (colorizer.domain_tips[1],
                "",
                "Choose the main highlight color."),
            (colorizer.domain_tips[2],
                "",
                "Choose the secondary highlight color."),
            (colorizer.domain_tips[3],
                "",
                "If background colors are dark, choose a light color for fonts, "
                    "or vice-versa."),
            (self.findings_table.headers[0],
                "",
                "Press delete key to delete this event."),
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
                "Create, add and edit notes regarding this event."),
            (self.findings_table.headers[7],
                "",
                "View and edit sources, citations and assertions linked to "
                    "this event."), 
            (self.att.headers[0],
                "",
                "Press delete key to delete this attribute."),
            (self.att.headers[1],
                "",
                "Entering a date here will move this attribute to the Events "
                    "Table."),
            (self.att.headers[2],
                "",
                "Existing places will auto-fill when you start typing, "
                    "starting with places used most recently."),
            (self.att.headers[3],
                "",
                "Leave date column blank to move event to Attributes Tab; "
                    "attribute dates could go here."),
            (self.att.headers[4],
                "",
                "Age at time of attribute, if applicable."),
            (self.att.headers[5],
                "",
                "Create, add and edit roles adjunct to this attribute."),
            (self.att.headers[6],
                "",
                "Create, add and edit notes regarding this attribute."),
            (self.att.headers[7],
                "",
                "View and edit sources, citations and assertions linked to "
                    "this attribute."),
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
            self.top_pic_button, self.findings_table.event_input, 
            self.att.event_input,self.fontpicker.output_sample, 
            self.fontpicker.font_size, self.fontpicker.cbo.entry, 
            self.fontpicker.apply_button,  
            colorizer.try_button, colorizer.copy_button, 
            colorizer.apply_button, colorizer.new_button, 
            colorizer.entries_combos[0], colorizer.entries_combos[3],
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

    def get_current_values(self):
        self.current_person_name = get_any_name_with_id(self.current_person)
        if type(self.current_person_name) is tuple:
            use_name = list(self.current_person_name)
            self.current_person_name = "({}) {}".format(use_name[1], use_name[0])
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
            self.att,
            self.show_top_pic,
            self.formats,
            names_tab=self.main_tabs.store["names"],
            pic=None)    

    def change_person(self):
        if "#" not in self.person_entry.get():
            old_current_person = self.current_person
            self.current_person = open_new_person_dialog(
                self, self.person_entry, self.root, self.treebard, self.formats)
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
        self.findings_table.kin_widths = [0, 0, 0, 0, 0]
        self.findings_table.redraw()
        self.att.current_person = self.current_person
        self.att.redraw()
        self.person_entry.delete(0, 'end')
        current_file, current_dir = get_current_file()
        self.show_top_pic(current_file, current_dir, self.current_person)

    def open_person_gallery(self):
        person_gallery_dlg = Toplevel(self.root)
        gallery_canvas = Border(person_gallery_dlg, self.root, self.formats)
           
        person_gallery = Gallery(
            gallery_canvas, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
            self.formats,
            self.root, 
            self.treebard,
            self.SCREEN_SIZE,
            dialog=person_gallery_dlg,
            current_person_name=self.current_person_name)

    def show_top_pic(self, current_file, current_dir, current_person):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        if current_person is None:
            cur.execute(select_current_person_id)
            current_person = cur.fetchone()[0]
        cur.execute(select_images_elements_main_image, (current_person,))        
        top_pic = cur.fetchone()
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




        






