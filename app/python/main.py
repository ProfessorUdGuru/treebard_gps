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

        self.current_person = None
        self.current_person_name = ""
        self.tabbook_x = 300
        self.tabbook_y = 300
        self.SCREEN_SIZE = []
        self.SCREEN_SIZE.append(self.winfo_screenwidth())
        self.SCREEN_SIZE.append(self.winfo_screenheight())

        # self.date_prefs = get_date_formats(tree_is_open=1)
        # self.newkinvar = tk.IntVar()
        # self.current_person_parents = [{},{}]

        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        all_names = make_all_names_list_for_person_select()
        self.person_autofill_values = EntryAutoHilited.create_lists(all_names)
        self.make_widgets()
        self.get_current_values()

        # self.make_nuke_inputs()   
        # nuke = NuclearFamiliesTable()
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
            current_person_area, 
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
            persons_tab, root=self.root, tabs=RIGHT_PANEL_TABS, side="se", 
            selected='images', case='upper', miny=0.25, minx=0.20, takefocus=0)
        self.top_pic_button = ButtonBigPic(
            self.right_panel.store['images'],
            command=self.open_person_gallery)

        # self.nuke_table = Frame(persons_tab)
        # self.nuke_canvas = Canvas(self.nuke_table)
        # self.nuke_window = Frame(self.nuke_canvas)
        # self.nuke_canvas.create_window(0, 0, anchor="nw", window=self.nuke_window)
        # nuke_sbv = Scrollbar(
            # self.nuke_table, command=self.nuke_canvas.yview, hideable=True)
        # self.nuke_canvas.config(yscrollcommand=nuke_sbv.set)
        # nuke_sbh = Scrollbar(
            # self.nuke_table, orient='horizontal', 
            # command=self.nuke_canvas.xview, hideable=True)
        # self.nuke_canvas.config(xscrollcommand=nuke_sbh.set)

        # self.nuke_table = NuclearFamiliesTable(
            # persons_tab, self.current_person, person_autofill_values=self.person_autofill_values)

        self.findings_table = EventsTable(
            persons_tab, self.root, self.treebard, self)

        EventsTable.instances.append(self.findings_table)
        self.current_person = self.findings_table.current_person

        self.att = EventsTable(
            attributes_tab, self.root, self.treebard, self, attrib=True)
        EventsTable.instances.append(self.att)

        # moved here from above since it seems necessary to pass self.current_person
        #   but that might effect tab order and if so then better to get currper
        #   locally inside of the nuke class
        self.nuke_table = NuclearFamiliesTable(
            persons_tab, 
            self.current_person, 
            self.findings_table, 
            self.right_panel,
            person_autofill_values=self.person_autofill_values)

        current_file, current_dir = get_current_file()
        # this does not run on redraw, just on load
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

        options_tabs = TabBook(
            prefs_tab, root=self.root, tabs=PREFS_TABS, side="se", 
            selected='general', case='upper', miny=0.5, minx=0.66)

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
            tabbook=self.right_panel)
        colorizer.grid(column=0, row=0)

        self.fontpicker = FontPicker(options_tabs.store['fonts'], self.root, self)
        self.fontpicker.grid(column=0, row=0)
        self.date_options = DatePreferences(options_tabs.store['dates'])
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

        # children of self.nuke_table gridden in families.py
        persons_tab.columnconfigure(1, weight=1)
        # self.nuke_canvas.grid(column=0, row=0, sticky="news")
        # nuke_sbv.grid(column=1, row=0, sticky="ns")
        # nuke_sbh.grid(column=0, row=1, sticky="ew")

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

        # Force everything to format on load the same as on calling redraw().
        #   This is a confusion workaround hack. (Couldn't find the 
        #   formatting glitch in a reasonable amount of time--uncomment this 
        #   and look at the child row columns in multi-brood current person 
        #   on load--or run this and don't worry about it).
        # self.findings_table.redraw()

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

    # def make_nuke_frames(self):
        # self.pardlabs = []
        # parentslab = LabelFrame(self.nuke_window) 
        # labelwidget = LabelH3(parentslab, text="Parents of the Current Person")
        # self.pardlabs.append(labelwidget)
        # parentslab.config(labelwidget=labelwidget)
        # parentslab.grid(column=0, row=0, sticky="w")
        # malab = Label(parentslab, text="Mother")
        # malab.grid(column=0, row=0, sticky="w", padx=(12,0), pady=(6,12))
        # self.ma_input = EntryAuto(
            # parentslab, width=30, autofill=True, 
            # values=self.person_autofill_values, name="ma")
        # self.ma_input.grid(column=1, row=0, pady=(6,12), padx=(6,0))
        # palab = Label(parentslab, text="Father")
        # palab.grid(column=2, row=0, sticky="w", padx=(18,0), pady=(6,12))
        # self.pa_input = EntryAuto(
            # parentslab, width=30, autofill=True, 
            # values=self.person_autofill_values, name="pa")
        # self.pa_input.grid(column=3, row=0, pady=(6,12), padx=(6,12))
        # self.nuke_inputs.append(self.ma_input)
        # self.nuke_inputs.append(self.pa_input)

    # def fix_buttons(self):
        
        # if self.newkinvar.get() == 100:
            # self.childmaker.config(state="disabled")
            # self.pardmaker.config(state="normal")
            # if len(self.pardrads) == 0:
                # self.kinradnew.config(state="normal")
        # elif self.newkinvar.get() == 999:
            # self.pardmaker.config(state="normal")
            # self.childmaker.config(state="normal")
            # if len(self.pardrads) == 0:
                # self.kinradnew.config(state="disabled")
        # else:
            # self.pardmaker.config(state="disabled")
            # self.childmaker.config(state="normal")
            # if len(self.pardrads) == 0:
                # self.kinradnew.config(state="normal") 

    # def make_new_kin_inputs(self):
        # new_kin_frame = Frame(self.nuke_window)
        # new_kin_frame.grid(column=0, row=self.last_row, sticky="ew")
        # self.kinradnew = Radiobutton(
            # new_kin_frame, variable=self.newkinvar,
            # value=100, anchor="w", 
            # command=self.fix_buttons)
        # self.kinradnew.grid(column=0, row=0)
        # new_kin_input = EntryAutoHilited(
            # new_kin_frame, width=48, 
            # autofill=True, 
            # values=self.person_autofill_values)
        # new_kin_input.grid(column=1, row=0)
        # self.pardmaker = Button(
            # new_kin_frame, 
            # text="ADD PARTNER", width=12, 
            # command=self.edit_partner)
        # self.pardmaker.grid(column=2, row=0, padx=(6,0), pady=(12,0))
        # self.childmaker = Button(
            # new_kin_frame, 
            # text="ADD CHILD", width=12, 
            # command=self.edit_child)
        # self.childmaker.grid(column=3, row=0, padx=(6,0), pady=(12,0))
        
    # def edit_partner(self):
        # print("howdy pardner")

    # def edit_child(self):
        # print("hey kid")

    # def bind_inputs(self):
        # for widg in self.nuke_inputs:
            # widg.bind("<FocusIn>", self.get_original, add="+")
            # widg.bind("<FocusOut>", self.get_final, add="+")

    # def get_original(self, evt):
        # self.original = evt.widget.get()

    # def edit_parent(self, final, widg):
        # unlink = False
        # if "#" in final:
            # new_parent_id = final.split("#")[1]
        # elif len(final) == 0:
            # new_parent_id = None
            # unlink = True
        # else:
            # new_parent_id = open_new_person_dialog(
                # self, widg, self.root, self.treebard)
        # return new_parent_id, unlink 

    # def update_mother(self, final, conn, cur, widg):
        # new_parent_id, unlink = self.edit_parent(final, widg)
        # birth_id = self.current_person_parents[0][1]
        # old_ma_id = self.current_person_parents[1]["id"]
        # birth_fpid = self.current_person_parents[0][0]
        # if self.birth_record[3] == 1:
            # which = 1
        # elif self.birth_record[5] == 1:
            # which = 2  
        # if unlink is False:
            # if which == 1:
                # query = update_findings_persons_by_id1
            # elif which == 2:
                # query = update_findings_persons_by_id2 
        # elif unlink is True:
            # if which == 1:
                # query = update_findings_persons_by_id1_unlink
            # elif which == 2:
                # query = update_findings_persons_by_id2_unlink
        # cur.execute(query, (new_parent_id, birth_fpid))
        # conn.commit()

    # def update_father(self, final, conn, cur, widg):
        # new_parent_id, unlink = self.edit_parent(final, widg)
        # birth_id = self.current_person_parents[0][1]
        # old_pa_id = self.current_person_parents[2]["id"]
        # birth_fpid = self.current_person_parents[0][0]
        # if self.birth_record[3] == 2:
            # which = 1
        # elif self.birth_record[5] == 2:
            # which = 2  
        # if unlink is False:
            # if which == 1:
                # query = update_findings_persons_by_id1
            # elif which == 2:
                # query = update_findings_persons_by_id2 
        # elif unlink is True:
            # if which == 1:
                # query = update_findings_persons_by_id1_unlink
            # elif which == 2:
                # query = update_findings_persons_by_id2_unlink
        # cur.execute(query, (new_parent_id, birth_fpid))
        # conn.commit()

    # def update_partner(self, final, conn, cur, widg):
    
        # def update_partners_child(birth_fpid, order, parent_type, new_partner_id):
            # query1 = '''
                # UPDATE findings_persons
                # SET (person_id2, age2) = (?, "")
                # WHERE findings_persons_id = ?
             # '''

            # query2 = '''
                # UPDATE findings_persons
                # SET (person_id1, age1) = (?, "")
                # WHERE findings_persons_id = ?
             # '''
            
            # if parent_type == "Mother":
                # if order == "1-2":                    
                    # cur.execute(query2, (new_partner_id, birth_fpid))
                # elif order == "2-1":                    
                    # cur.execute(query1, (new_partner_id, birth_fpid))  
            # elif parent_type == "Father":
                # if order == "1-2":                    
                    # cur.execute(query1, (new_partner_id, birth_fpid))
                # elif order == "2-1":                    
                    # cur.execute(query2, (new_partner_id, birth_fpid))
            # conn.commit()

        # def get_new_partner_id(final, widg):
            # new_partner_id = 0
            # if "#" in final:
                # new_partner_id = final.split("#")[1]    
            # elif len(final) == 0:
                # # user unlinks partner by deleting existing name in entry
                # pass
            # else:
                # new_partner_id = open_new_person_dialog(
                    # self, widg, self.root, self.treebard)
            # return new_partner_id     

        # orig = self.original
        # new_partner_id = get_new_partner_id(final, widg)
        # # if dialog canceled change nothing in db
        # if new_partner_id is None:
            # widg.delete(0, 'end')
            # widg.insert(0, orig)
            # return
        # elif new_partner_id == 0:
            # new_partner_id = None
        # s = 0
        # for brood in self.brood_dicts:
            # for k,v in brood.items():
                # if widg != v[0]["widget"]:
                    # continue
                # for child in v[1]:
                    # update_partners_child(
                        # child["birth_fpid"], 
                        # child["order"], 
                        # v[0]["parent_type"], 
                        # new_partner_id)
                # break
            # s += 1        

    # def get_final(self, evt):
        # current_file = get_current_file()[0]
        # conn = sqlite3.connect(current_file)
        # conn.execute('PRAGMA foreign_keys = 1')
        # cur = conn.cursor()
        # widg = evt.widget
        # self.final = widg.get()
        # if self.final == self.original: return
        # col = widg.grid_info()["column"]
        # widg_name = widg.winfo_name()
        # if widg_name == "ma":
            # self.update_mother(self.final, conn, cur, widg)
        # elif widg_name == "pa":
            # self.update_father(self.final, conn, cur, widg)
        # elif widg_name.startswith("pard"):
            # if col == 2:
                # self.update_partner(self.final, conn, cur, widg)                
            # else:
                # print(
                    # "line", 
                    # looky(seeline()).lineno, 
                    # "case not handled for col", col)
        # else:
            # if col == 1:
                # print("line", looky(seeline()).lineno, "self.final:", self.final)
            # elif col == 2:
                # print("line", looky(seeline()).lineno, "self.final:", self.final)
            # elif col == 3:
                # print("line", looky(seeline()).lineno, "self.final:", self.final)
            # elif col == 5:
                # print("line", looky(seeline()).lineno, "self.final:", self.final)
            # else:
                # print("line", looky(seeline()).lineno, "case not handled:")    

        # cur.close()
        # conn.close()

    # def make_nuke_inputs(self, current_person=None):
        # self.nuke_inputs = []
        # if current_person:
            # self.current_person = current_person
        # self.make_nuke_frames()
        # self.make_nuke_dicts()
        # self.populate_nuke_tables()
        # self.bind_inputs()
        # self.make_new_kin_inputs()
        # self.update_idletasks()
        # wd = self.nuke_window.winfo_reqwidth() + 12
        # ht = self.right_panel.winfo_reqheight()
        # # The +72 is a hack only needed when a broodless current person
        # #   precedes a brooded one. Don't know what causes the new brooded
        # #   person to get prior reqheight but this fixed it for now.
        # self.nuke_canvas.config(width=wd, height=ht+72)        
        # self.nuke_canvas.config(scrollregion=(0, 0, wd, ht+72))
        # if len(self.brood_dicts) != 0:
            # self.newkinvar.set(100)
        # else:
            # # set to non-existent value so no Radiobutton will be selected
            # self.newkinvar.set(999)
        # self.fix_buttons()

    # def populate_nuke_tables(self):
        # formats = make_formats_dict()
        # lst = [
            # self.current_person_parents[1]["name"], 
            # self.current_person_parents[2]["name"]]
        # for name in lst:
            # if name == "name unknown":
                # idx = lst.index(name)
                # lst[idx] = ""
        # self.ma_input.insert(0, lst[0])
        # self.pa_input.insert(0, lst[1])
        # self.pardrads = []
        # n = 1

        # for brood in self.brood_dicts:
            # for k,v in brood.items():
                # name, ma_pa, pard_id = (v[0]["partner_name"], v[0]["parent_type"], k)
            # ma_pa = "Children's {}:".format(ma_pa)
            # pard = "pard_{}_{}".format(pard_id, n)
            # pardframe = Frame(self.nuke_window)
            # pardframe.grid(column=0, row=n, sticky="ew")
            # pardrad = Radiobutton(
                # pardframe, variable=self.newkinvar, 
                # value=n, anchor="w", command=self.fix_buttons)
            # self.pardrads.append(pardrad)
            # pardrad.grid(column=0, row=n)
            # pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            # self.pardlabs.append(pardlab)
            # pardlab.grid(column=1, row=n)
            # pardent = EntryAuto(
                # pardframe, width=48, autofill=True, 
                # values=self.person_autofill_values, name=pard)
            # pardent.insert(0, name)
            # pardent.grid(column=2, row=n)
            # v[0]["widget"] = pardent
            # self.nuke_inputs.append(pardent)
            # brood_frame = Frame(self.nuke_window)
            # brood_frame.grid(column=0, row=n+1) 
            # r = 0
            # for dkt in v[1]:
                # c = 0
                # for i in range(6):
                    # if c == 0:
                        # spacer = Frame(brood_frame, width=48)
                        # spacer.grid(column=c, row=r)
                    # elif c == 1:
                        # text = dkt["name"]
                        # ent = EntryAuto(
                            # brood_frame, width=0, autofill=True, 
                            # values=self.person_autofill_values)
                        # if len(text) > self.findings_table.kin_widths[c]:
                            # self.findings_table.kin_widths[c] = len(text)
                        # ent.insert(0, text)
                        # ent.grid(column=c, row=r, sticky="w")
                        # self.nuke_inputs.append(ent)
                        # dkt["name_widg"] = ent
                    # elif c == 2:
                        # text = dkt["gender"]
                        # ent = EntryAuto(brood_frame, width=0)
                        # if len(text) > self.findings_table.kin_widths[c]:
                            # self.findings_table.kin_widths[c] = len(text)
                        # ent.insert(0, text)
                        # ent.grid(column=c, row=r, sticky="w")
                        # self.nuke_inputs.append(ent)
                        # dkt["gender_widg"] = ent
                    # elif c == 3:
                        # text = dkt["birth"]
                        # ent = EntryAuto(brood_frame, width=0)
                        # if len(text) > self.findings_table.kin_widths[c]:
                            # self.findings_table.kin_widths[c] = len(text)
                        # ent.insert(0, text)
                        # ent.grid(column=c, row=r, sticky="w")
                        # self.nuke_inputs.append(ent)
                        # dkt["birth_widg"] = ent
                    # elif c == 4:
                        # text = "to"
                        # if len(text) > self.findings_table.kin_widths[c]:
                            # self.findings_table.kin_widths[c] = len(text)
                        # lab = LabelEntry(brood_frame, text=text, anchor="w")
                        # lab.grid(column=c, row=r, sticky="w")
                    # elif c == 5:
                        # text = dkt["death"]
                        # ent = EntryAuto(brood_frame, width=0)
                        # if len(text) > self.findings_table.kin_widths[c]:
                            # self.findings_table.kin_widths[c] = len(text)
                        # ent.insert(0, text)
                        # ent.grid(column=c, row=r, sticky="w")
                        # self.nuke_inputs.append(ent)
                        # dkt["death_widg"] = ent 
                    # c += 1
                # r += 1
            # top_row = brood_frame.grid_slaves(row=0)
            # top_row.reverse()
            # top_row_values = []
            # for widg in top_row[1:]:
                # if widg.winfo_class() == 'Entry':
                    # top_row_values.append(widg.get())
                # else:
                    # top_row_values.append(widg.cget("text"))
            # z = 1
            # for widg in top_row[1:]:
                # widg.config(width=self.findings_table.kin_widths[z] + 2)
                # z += 1
            # n += 2
        # self.last_row = n

        # # don't know why config_generic isn't enough here
        # for widg in self.pardlabs:
            # widg.config(font=formats["heading3"])

    # def make_parents_dict(self):
        # birth_fpid, birth_id = self.birth_record[0:2]
        # parent1 = self.birth_record[2:4]
        # parent2 = self.birth_record[4:]
        # if parent1[1] == 1:
            # ma_id = parent1[0]
            # pa_id = parent2[0]
        # elif parent1[1] == 2:
            # ma_id = parent2[0]
            # pa_id = parent1[0]
        # self.current_person_parents.insert(0, (self.birth_record[0:2]))
        # ma_name = get_any_name_with_id(ma_id)
        # pa_name = get_any_name_with_id(pa_id)

        # self.current_person_parents[1]["id"] = ma_id
        # self.current_person_parents[2]["id"] = pa_id
        # self.current_person_parents[1]["name"] = ma_name
        # self.current_person_parents[2]["name"] = pa_name
        # self.current_person_parents[1]["widget"] = self.ma_input
        # self.current_person_parents[2]["widget"] = self.pa_input

    # def make_nuke_dicts(self):
        # current_file = get_current_file()[0]
        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_finding_id_birth, (self.current_person,))
        # birth_id = cur.fetchone()
        # if birth_id:
            # birth_id = birth_id[0]
            # cur.execute(
                # '''
                    # SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 FROM findings_persons WHERE finding_id = ?
                # ''',
                # (birth_id,))
            # self.birth_record = cur.fetchall()[0]
            # self.make_parents_dict()  

        # cur.execute(
            # '''
                # SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 FROM findings_persons WHERE person_id1 = ? AND kin_type_id1 IN (1,2)
            # ''',
            # (self.current_person,))
        # result1 = cur.fetchall()
        # cur.execute(
            # '''
                # SELECT findings_persons_id, finding_id, person_id1, kin_type_id1,  person_id2, kin_type_id2 FROM findings_persons WHERE person_id2 = ? AND kin_type_id2 IN (1,2)
            # ''',
            # (self.current_person,))
        # result2 = cur.fetchall()
        # births = []
        # self.brood_dicts = []
        # births = [tup for q in (result1, result2) for tup in q]

        # broods = []
        # for tup in births:
            # if tup[2] != self.current_person:
                # if tup[2] not in broods:
                    # broods.append(tup[2])
            # elif tup[4] != self.current_person:
                # if tup[4] not in broods:
                    # broods.append(tup[4])

        # for pard_id in broods:
            # brood = {pard_id: [{}, []]}
            # self.brood_dicts.append(brood)

        # m = 0
        # for pardner in broods:
            # for tup in births:
                # order = "{}-{}".format(str(tup[3]), str(tup[5]))                
                # if tup[4] == pardner:
                    # parent_type = tup[5]
                    # pard_id = tup[4]
                    # self.make_pard_dict(pard_id, parent_type, m)
                    # if pard_id == pardner:
                        # self.brood_dicts[m][pardner][1].append(
                            # {"birth_fpid": tup[0], 
                                # "birth_id": tup[1], "order": order})
                # elif tup[2] == pardner:
                    # parent_type = tup[3]
                    # pard_id = tup[2]
                    # self.make_pard_dict(pard_id, parent_type, m) 
                    # if pard_id == pardner:
                        # self.brood_dicts[m][pardner][1].append(
                            # {"birth_fpid": tup[0], 
                                # "birth_id": tup[1], "order": order})
            # m += 1

        # for pard_id in broods:
            # for brood in self.brood_dicts:
                # for k,v in brood.items():
                    # if k == pard_id:
                        # for dkt in v[1]:
                            # self.finish_brood_dict(dkt, cur) 

        # for brood in self.brood_dicts:
            # brood_values = list(brood.values())
            # brood_values[0][1] = sorted(brood_values[0][1], key=lambda i: i["sorter"])

        # compare = []
        # for brood in self.brood_dicts:
            # for k,v in brood.items():
                # compare.append((k, v[1][0]["sorter"]))
            # compare = sorted(compare, key=lambda j: j[1])

        # copy = []
        # for tup in compare:
            # key = tup[0]
            # for brood in self.brood_dicts:
                # if brood.get(key) is None:
                    # continue
                # else:
                    # copy.append(brood) 
        # self.brood_dicts = copy

        # # instead of trying to sort this above, maybe better to insert this into the sorted list of dicts when it's done NO THE RIGHT WAY IS TO add spouses to the dict as keys as a first step so they're treated like everything else, since it will be necessary to detect marital events for brooded/non-brooded partners equally

        # spouses = self.collect_couple_events(cur)

        # cur.close()
        # conn.close()

    # def collect_couple_events(self, cur):
        # '''
            # Two means of determining partnership are used. 1) a couple has 
            # children together, or 2) a couple are linked by a common couple
            # event such as marriage or divorce regardless of whether they
            # have children together.

            # Problem is, if user unlinks a partner from current person's
            # marriage event, should Treebard auto-unlink the partner from the
            # divorce event too? Since partnerships are detected only on the
            # basis of existing marital events if there are no children, the
            # answer is yes. Not unlinking the marital events from a deleted
            # partner. or not editing a changed name on marital events if the
            # partner's name is changed... would be a disaster. And the deleted
            # partner would show up on the nukes table if the links were left
            # intact. The only way around this would be to find another way
            # to detect childless couples that doesn't involve detecting
            # marital events. (What about kin types such as spouse, wife, etc.)

            # Couple events are determined by a boolean in the events_type 
            # database table. But not all couple events are evidence for 
            # a partnership that you'd want on the nukes (nuclear family) table.
            # But all couple events are treated the same in other ways, for 
            # example, if two people get engaged, the user only has to create 
            # the event for one of them, and Treebard auto-creates the event
            # for the other person; all couple events should work this way.

            # So a second boolean is used to distinguish non-binding couple
            # events such as "first kiss" or "engagement" or "marriage banns".
            # For inclusion in the nukes table, partnership will be marked
            # by the boolean column called "marital". This category includes
            # anything that should mark a partnership even if there are no children,
            # such as marriage, wedding, divorce, cohabitation, separation, etc.

            # (The event or dated attribute "marital status" isn't even a couple
            # event, since it makes no reference to who the partner is and would
            # be asked of one person at a time. Even if both partners in a couple 
            # answered this question at the same time, the user would have to 
            # enter each answer separately for the two people.)

            # Kin types are used to state for example that a partner is a spouse,
            # wife, husband, etc. They aren't used to detect anything, because
            # they are too loose, the user just decides what to call a partner,
            # such as "boyfriend", "mistress", etc. The event should have all the
            # power, not kin type, when it comes to determining partnership if 
            # there are no children to determine it. The user should be the one
            # to decide whether to include a mistress on the nukes table, by
            # inputting a cohabitation event, for example, for a man with a 
            # second family hidden away somewhere. Unlike some genieware, Treebard
            # differentiates between "spouse" and "mother of children", so it's
            # not necessary to create a bogus spouse in order to identify the
            # parents in a nuclear family.
        # ''' 
        # cur.execute(
            # '''
                # SELECT event_type_id 
                # FROM event_type
                # WHERE marital = 1
            # ''')

        # marital_event_types = [i[0] for i in cur.fetchall()]
        # qlen = len(marital_event_types)
        # marital_event_types.insert(0, self.current_person)
        # marital_event_types.insert(0, self.current_person)
        
        # sql = '''
                # SELECT findings_persons_id, person_id1, kin_type_id1, person_id2, kin_type_id2, date
                # FROM findings_persons
                # JOIN finding
                    # ON finding.finding_id = findings_persons.finding_id
                # WHERE (person_id1 = ? OR person_id2 = ?) 
                    # AND event_type_id in ({})
            # '''.format(",".join(["?"] * qlen))
        # cur.execute(sql, marital_event_types)
        # copy = [list(i) for i in cur.fetchall()]

        # spouses = copy
        # print("line", looky(seeline()).lineno, "spouses:", spouses)
# # line 1086 copy: [[69, 632, 12, 8, 5599, 7, 'abt-1910-au-15-ad------'], [72, 646, 6, 7, 12, 8, '-1905---------'], [73, 649, 6, 7, 12, 8, '-1905---------']]

        # o = 0
        # for lst in spouses:
            # if lst[1] == self.current_person:
                # del lst[1:3]
            # elif lst[3] == self.current_person:
                # del lst[3:5]
            # o += 1
        # print("line", looky(seeline()).lineno, "spouses:", spouses)
        # for lst in spouses:
            # self.save_marital_events(lst, cur)

        # # remove partners who have children
        # g = 0
        # for brood in self.brood_dicts:
            # x = list(brood.keys())
            # key = x[0]
            # for lst in spouses:
                # if key in lst:
                    # del copy[g]
            # g += 1
        # # remove duplicates due to multiple marital events w/ same partner
        # #    what's left is a list of unique partners to add (childless)
        # childless_partners = []
        # for lst in copy:
            # if lst[1] not in childless_partners:
                # childless_partners.append(lst[1])        
        # print("line", looky(seeline()).lineno, "childless_partners:", childless_partners)
# # line 1082 copy: [[69, 632, 12, 8, 5599, 7, 'abt-1910-au-15-ad------'], [72, 646, 6, 7, 12, 8, '-1905---------'], [73, 649, 6, 7, 12, 8, '-1905---------']]
# # line 1113 childless_partners: [6]
# # line 1117 copy: [[72, 646, 6, 7, '-1905---------'], [73, 649, 6, 7, '-1905---------']] 
# # add to parents dict: marital_pfid, marital_finding_id,, marital_event_type, marital_finding_date, partner_kin_type SO THAT when a partner is edited/deleted, the change can be propagated to all marital events for that couple

                       
        # # print("line", looky(seeline()).lineno, "self.brood_dicts:", self.brood_dicts)                        
        # return spouses
 


# # line 991 self.brood_dicts: [{5635: [{'parent_type': 'Mother', 'partner_name': 'Harmony Maryland Hobgood (stage name)'}, [{'birth_fpid': 93, 'birth_id': 668, 'order': '2-1', 'gender': 'male', 'birth': '1920', 'sorter': [1920, 0, 0], 'death': '', 'name': 'Ross Aldo Marquis (stage name)', 'id': 5783}]]}, {5599: [{'parent_type': 'Mother', 'partner_name': 'Selina Savoy'}, [{'birth_fpid': 95, 'birth_id': 670, 'order': '1-2', 'gender': 'unknown', 'birth': 'Aug 1, 1915', 'sorter': [1915, 8, 1], 'death': '', 'name': 'Albertha Siu Sobel', 'id': 5711}, {'birth_fpid': 97, 'birth_id': 672, 'order': '2-1', 'gender': 'male', 'birth': 'Apr 14, 1921', 'sorter': [1921, 4, 14], 'death': 'June 29, 1961', 'name': 'Clarence Bracken', 'id': 5677}, {'birth_fpid': 94, 'birth_id': 669, 'order': '2-1', 'gender': 'female', 'birth': 'Jan 18, 1922', 'sorter': [1922, 1, 18], 'death': '', 'name': 'Moira Harding', 'id': 5740}, {'birth_fpid': 98, 'birth_id': 673, 'order': '2-1', 'gender': 'male', 'birth': 'Aug 6, 1927', 'sorter': [1927, 8, 6], 'death': '', 'name': 'Noe Whitton', 'id': 5685}, {'birth_fpid': 96, 'birth_id': 671, 'order': '2-1', 'gender': 'male', 'birth': 'Sep 30, 1929', 'sorter': [1929, 9, 30], 'death': '', 'name': "Joe-John O'Keefe", 'id': 5732}]]}]

    # def save_marital_events(self, lst, cur):
        # print("line", looky(seeline()).lineno, "lst:", lst)
# # line 1129 lst: [69, 5599, 7, 'abt-1910-au-15-ad------']
# # line 1129 lst: [72, 6, 7, '-1905---------']
# # line 1129 lst: [73, 6, 7, '-1905---------']
        # partner_id = lst[1]
        # print("line", looky(seeline()).lineno, "partner_id:", partner_id)
        # # FIRST ADD MISSING (CHILDLESS) PARTNERS TO MAIN DICT HERE
        # for brood in self.brood_dicts:
            # for k,v in brood.items():
                # print("line", looky(seeline()).lineno, "k:", k)
                # if partner_id == k:

                    # cur.execute(
                        # '''
                            # SELECT kin_types
                            # FROM kin_type
                            # WHERE kin_type_id = ?
                        # ''',
                        # (lst[2],))
                    # kin_type = cur.fetchone()[0]


                    # v[0]["partner_kin_type"] = kin_type
                    # print("line", looky(seeline()).lineno, "kin_type:", kin_type)

        # print("line", looky(seeline()).lineno, "self.brood_dicts:", self.brood_dicts          )
        # # NEXT ADD MARITAL EVENT DICTS WITH marital_event_pfid & marital_event_date

    # def make_pard_dict(self, pard_id, parent_type, m):
        # if parent_type == 1:
            # parent_type = "Mother"
        # elif parent_type == 2:
            # parent_type = "Father"
        # partner_name = get_any_name_with_id(pard_id)
        # self.brood_dicts[m][pard_id][0]["parent_type"] = parent_type
        # self.brood_dicts[m][pard_id][0]["partner_name"] = partner_name   

    # def finish_brood_dict(self, dkt, cur):   
        # cur.execute(
            # '''
                # SELECT person_id, date
                # FROM finding
                # WHERE finding_id = ?
                    # AND event_type_id = 1
            # ''',
            # (dkt["birth_id"],))
        # born_id, birth_date = cur.fetchone()

        # cur.execute(
            # '''
                # SELECT date
                # FROM finding
                # WHERE person_id = ?
                    # AND event_type_id = 4
            # ''',
            # (born_id,))
        # death_date = cur.fetchone()
        # if death_date:
            # death_date = death_date[0]
        # else:
            # death_date = "-0000-00-00-------"

        # cur.execute(
            # '''
                # SELECT gender
                # FROM person
                # WHERE person_id = ?
            # ''',
            # (born_id,))
        # gender = cur.fetchone()[0]

        # sorter = [0,0,0]
        # if birth_date != "-0000-00-00-------":
            # sorter = birth_date.split("-")[1:4] 
            # h = 0
            # for stg in sorter:
                # if len(stg) == 0:
                    # sorter[h] = '0'
                # h += 1
            # num = sorter[1]
            # if sorter[1] != '0':
                # num = OK_MONTHS.index(sorter[1]) + 1
            # else:
                # num = 0
            # sorter = [int(sorter[0]), num, int(sorter[2])]

        # name = get_any_name_with_id(born_id)

        # birth_date = format_stored_date(
            # birth_date, date_prefs=self.date_prefs)
        # death_date = format_stored_date(
            # death_date, date_prefs=self.date_prefs)                

        # dkt["gender"] = gender
        # dkt["birth"] = birth_date
        # dkt["sorter"] = sorter
        # dkt["death"] = death_date
        # dkt["name"] = name
        # dkt["id"] = born_id 

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
            names_tab=self.main_tabs.store["names"],
            pic=None)    

    def change_person(self):
        if "#" not in self.person_entry.get():
            old_current_person = self.current_person
            self.current_person = open_new_person_dialog(
                self, self.person_entry, self.root, self.treebard)
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
        gallery_canvas = Border(person_gallery_dlg, self.root)

        person_gallery = Gallery(
            gallery_canvas, 
            self.main_tabs, 
            self.main_tabs.store['graphics'],
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




        






