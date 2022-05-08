# gedcom_import.py
import tkinter as tk
import sqlite3
from re import sub
from datetime import datetime
from files import get_current_file, current_drive
from widgets import (
    Toplevel, Frame, Button,  LabelH2, Label, ScrolledText,
    configall, Border, Scrollbar, make_formats_dict, Text)
from right_click_menu import RightClickMenu, make_rc_menus
from scrolling import MousewheelScrolling, resize_scrolled_content
from toykinter_widgets import run_statusbar_tooltips
from gedcom_tags import all_tags, no_fam_tag_sources
from query_strings_gedcom import (
    insert_person, insert_name, update_name, 
    insert_source, delete_person_all, delete_name_all, delete_finding_all, 
    delete_source_all, update_gender_default_person, update_name_default_person,
    insert_finding_default_person, insert_finding_birth, insert_claims_person,

)
import dev_tools as dt
from dev_tools import looky, seeline




ZERO_LEVEL_TAGS = ("HEAD", "TRLR", "FAM", "INDI", "OBJE", "NOTE", "REPO", "SOUR", "SUBM")
ELEMS2Y = ("BIRT", "DEAT", "CHR", "MARR")

class GedcomImporter():
    def __init__(self, import_file):
        self.records_dict = {}
        for tag0 in ZERO_LEVEL_TAGS:
            self.records_dict[tag0] = {}
        current_file = get_current_file()[0]
        self.exceptions_dict = {}
        self.conn = sqlite3.connect(current_file)
        self.cur = self.conn.cursor()
        self.line_lists = []
        self.head = []
        self.head_dict = {
            'SOUR': {'NAME': '', 'VERS': '', 'CORP': ''}, 
            'FILE': '', 'GEDC': '', 'CHAR': ''}
        self.read_gedcom(import_file)
        self.import_file = import_file

    def read_gedcom(self, file):
        """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
            first line.
        """
        f = open(file, "r", encoding='utf-8-sig')
        for line_text in f.readlines():
            lst = line_text.strip("\n").split(" ", 2)
            lst[0] = int(lst[0])
            self.line_lists.append(lst)

    def validate_lines(self):
        """ Add a 4th element to bad lines. """
        for line in self.line_lists:
            length = len(line)
            tag = line[1]
            if length > 3:
                line.append("too_long")
            elif length > 2:
                if tag in ELEMS2Y:
                    if line[2] != "Y":
                        line.append("too_long_y")

    def delineate_records(self):
        tag0 = None
        h = 0
        for line in self.line_lists:
            if line[0] == 0:
                if line[1] in ("HEAD", "TRLR"):
                    tag0 = line[1]
                    h = self.add_subrecords(line, h, tag0)

                elif len(line) > 2:
                    tag0 = line[2]
                    h = self.add_subrecords(line, h, tag0)
                else:
                    print("line", looky(seeline()).lineno, "case not handled:")
            else:
                pass
        self.head = self.records_dict['HEAD']['HEAD']

    def add_subrecords(self, line, h, tag0):
        copy = self.records_dict
        pk = line[1]
        subrecords = []
        j = h + 1
        for lst in self.line_lists[j:]:
            if lst[0] > 0:
                subrecords.append(lst)
                j += 1
            else:
                break
        for k,v in copy.items():
            if k == tag0:
                self.records_dict[k][pk] = subrecords 
        return j

    def input_persons(self):
        for k,v in self.records_dict.items():
            if k != "INDI":
                continue
            record = v
            for kk, vv in record.items():
                person_id = kk
                person_data = vv
                z = 0
                for line in person_data:
                    self.parse_line(person_id, line, z)
                    z += 1

    def input_sources(self):
        for k,v in self.records_dict.items():
            if k != "SOUR":
                continue
            record = v
            for kk, vv in record.items():
                source_id = kk
                source_data = vv
                z = 0
                for line in source_data:
                    self.parse_line(source_id, line, z)
                    z += 1

    def input_families(self):
        for k,v in self.records_dict.items():
            if k != "FAM":
                continue
            record = v
            for kk, vv in record.items():
                family_id = kk
                family_data = vv
                z = 0
                for line in family_data:
                    self.parse_line(family_id, line, z, k=k)
                    z += 1


    def parse_line(self, pk, line, z, k=None):
        n = line[0]
        tag = line[1]
        if len(line) == 3:
            data = line[2]
        if n == 1:
            if tag == "NAME":
                self.add_person(pk, data)
            elif tag == "TITL":
                self.add_source(pk, data)
            elif k and k == "FAM":
                if tag in ("HUSB", "WIFE", "CHILD", "SOUR"):
                    self.add_family(pk, data, tag)
            self.parse_next_line(pk, z)

    def parse_next_line(self, person_id, z):
        # print("line", looky(seeline()).lineno, "person_id:", person_id)
        # print("line", looky(seeline()).lineno, "z:", z)
        pass

    def add_family(self, pk, data, tag):
        if tag == "SOUR":
            self.link_source_famtag(pk, data)
        elif tag == "CHILD":
            pass
        elif tag == "HUSB":
            pass
        elif tag == "WIFE":
            pass
        else:
            print("line", looky(seeline()).lineno, "tag not handled:", tag)

    def link_source_famtag(self, pk, data):
        fk = int(sub("\D", "", data))
        if self.exceptions_dict.get(no_fam_tag_sources) is None:
            self.exceptions_dict[no_fam_tag_sources] = [(pk, data)]
        else:
            self.exceptions_dict[no_fam_tag_sources].append((pk, data))  

    def add_source(self, source_id, title):
        source_id = int(sub("\D", "", source_id))
        self.cur.execute(insert_source, (source_id, title))
        self.conn.commit()    

    def add_person(self, person_id, name):
        person_id = int(sub("\D", "", person_id))
        name_list = name.split()
        for i in name_list:
            if i.startswith("/"):
                idx = name_list.index(i)
                x = name_list.pop(idx).strip("/")
                sorter = list(name_list)
                sorter.insert(0, "{},".format(x))
                sorter = " ".join(sorter).strip()
        name_list.insert(idx, x)
        name = " ".join(name_list)
        if person_id != 1:    
            self.cur.execute(insert_person, (person_id,))
            self.conn.commit()
            self.cur.execute(insert_name, (person_id, name, sorter))
            self.conn.commit()
            self.cur.execute(insert_finding_birth, (person_id,))
            self.conn.commit()
        else:
            self.cur.execute(update_name, (name, sorter))
            self.conn.commit()

    def make_unique_tag_lists(self):
        for lst in self.line_lists:
            elem_1 = lst[1]
            if elem_1.startswith("@") is False:
                if elem_1.startswith("_"):
                    custom_tags.append(elem_1.rstrip("\n"))
                else:
                    tags.append(elem_1.rstrip("\n"))
            else:
                if lst[2].startswith("_"):
                    custom_tags.append(lst[2].rstrip("\n"))
                else:
                    tags.append(lst[2].rstrip("\n"))
        tags = list(set(tags))
        custom_tags = list(set(custom_tags))

    def get_value(self, lst, x, tag):
        value = None
        w = x + 1
        for lst in self.head[w:]:
            if lst[1] == tag:
                value = lst[2]
                break
            w += 1
        return value

    def parse_head(self):
        x = 0
        for lst in self.head:
            n = lst[0] 
            if n != 1:
                x += 1
                continue
            else:
                tag = lst[1]
                if tag == 'SOUR':
                    for tagg in ('VERS', 'NAME', 'CORP'):
                        self.head_dict[tag][tagg] = self.get_value(lst, x, tagg)
                elif tag == 'GEDC':
                    self.head_dict[tag] = self.get_value(lst, x, 'VERS')
                elif tag in ('FILE', 'CHAR'):
                    self.head_dict[tag] = lst[2]
                x += 1

elements_dict = {"FAM": "family_id", "INDI": "person_id", "SOUR": "source_id"}

def get_id_type(tag):
    if tag in ("FAM", "INDI", "SOUR"):
        element = elements_dict[tag]
    return element 

# # # def reset_tree():
    # # # cur.execute(update_gender_default_person)
    # # # conn.commit()
    # # # cur.execute(delete_name_all)
    # # # conn.commit()
    # # # cur.execute(update_name_default_person)
    # # # conn.commit()
    # # # cur.execute(delete_finding_all)
    # # # conn.commit()
    # # # cur.execute(insert_finding_default_person)
    # # # conn.commit()
    # # # cur.execute(delete_source_all)
    # # # conn.commit()
    # # # cur.execute(delete_person_all)
    # # # conn.commit()
    # forgot places_places and remember to leave #1 in person, name, finding, place, and places_places

MESSAGES = (
    "", 
)

class GedcomExceptions(Toplevel):
    """ Open dialog without user's prompting when GEDCOM import is complete. """
    def __init__(self, master, treebard, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.master = master
        self.treebard = treebard

        self.formats = make_formats_dict()

        # self.rc_menu = RightClickMenu(self.master, treebard=self.treebard)

        self.make_widgets()

        self.importer = GedcomImporter(self.treebard.import_file)
        self.importer.read_gedcom(self.treebard.import_file)
        self.importer.validate_lines()
        self.importer.delineate_records()
        print("line", looky(seeline()).lineno, "self.importer.head:", self.importer.head)
        self.importer.parse_head()
        self.importer.input_persons()
        self.importer.input_sources()
        self.importer.input_families()
        self.write_exceptions_report()
        # self.infolab.config(text="GEDCOM input file: {}".format(self.treebard.import_file))

        # now = datetime.now()
        # stamp = now.strftime("%Y%m%d%H%M")
        # filename = "{}treebard_gps/etc/gedcom_import_exceptions_{}.txt".format(current_drive, stamp)
        # date, hour, minute = stamp[0:8], stamp[8:10], stamp[10:]

        # ff = open(filename, "a")
        # ff.write("Imported from <insert software> to Treebard GPS\n")
        # ff.write("GEDCOM Source File: {}".format(self.importer.import_file))
        # ff.write(" imported on {} at {}:{}.\n".format(date, hour, minute))
        # ff.write("This file: {}\n\n".format(filename))



        # replace = {
            # 'SOUR': 'Source of GEDCOM File', 'FILE': 'GEDCOM File Name', 
            # 'GEDC': 'GEDCOM Version', 'CHAR': 'Character Set Encoding'}
        # for k,v in self.importer.head_dict.items():
            # ff.write("\n{}: ".format(replace[k]))


            # if k == 'SOUR':
                # print("line", looky(seeline()).lineno, "v.values():", v.values())
                # ware, version, vendor = v.values()
                # # for val in v.values():
                    # # print("line", looky(seeline()).lineno, "val:", val)
                    # # ff.write("{}: ".format(val))
                # ff.write("{} version {} by {}".format(ware, version, vendor))
            # else:
                # ff.write("\n{}\n".format(v))




        # for k,v in self.importer.exceptions_dict.items():
            # self.textbox.text.insert("end", "\n{}\n\n".format(k))
            # ff.write("{}\n\n".format(k))
            # for tup in v:
                # text = "Family ID #{} linked to Source ID #{}".format(
                    # int(sub("\D", "", tup[0])), int(sub("\D", "", tup[1])))
                # self.textbox.text.insert("end", "{}\n".format(text))
                # ff.write("{}\n".format(text))
        # ff.close()

        self.importer.cur.close()
        self.importer.conn.close()

    def make_widgets(self):

        self.title('GEDCOM Import Exceptions')
        self.geometry('+100+20')

        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, self.master, self.formats)
        self.canvas.title_1.config(text="GEDCOM Import Exceptions")
        self.canvas.title_2.config(text=self.treebard.import_file)

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
        header.columnconfigure(0, weight=1)
        self.exceptions_dialog_heading = LabelH2(
            header, 
            text='Items Not Imported by GEDCOM')
        self.exceptions_dialog_heading.grid(column=0, row=0, pady=(24,0), sticky="ew")

        head_msg = "Items listed below can be input manually using Treebard's interface.\nInstructions are included for each category of failed import.\nThis document has been saved as a text file named\n`{drive}treebard_gps/etc/gedcom_import_exceptions_{timestamp}.txt`."
        instrux = Label(header, text=head_msg, justify="left")
        instrux.grid(column=0, row=1, padx=24, pady=(24,0), sticky="ew")

        self.info = Frame(self.window)
        self.info.grid(column=0, row=1, sticky='news', padx=48, pady=(24,0))

        self.infolab = Label(self.info)
        self.infolab.grid(pady=(0,12))

        self.textbox = ScrolledText(self.info)
        self.textbox.grid()

        # visited = (
            # (self.search_input, 
                # "Person Search Input", 
                # "Type any part of any name or ID number; table will fill "
                    # "with matches."),
            # (self.info, 
                # "Person Search Table", 
                # "Select highlighted row with Enter or Space key to change "
                    # "current person, or click any row."))   
     
        # run_statusbar_tooltips(
            # visited, 
            # self.canvas.statusbar.status_label, 
            # self.canvas.statusbar.tooltip_label)

        # rcm_widgets = (
            # self.search_input, self.exceptions_dialog_heading, self.info)
        # make_rc_menus(
            # rcm_widgets, 
            # self.rc_menu, 
            # search_person_help_msg) 

        resize_scrolled_content(self, self.canvas, self.window)

    def write_exceptions_report(self):

        self.infolab.config(text="GEDCOM input file: {}".format(self.treebard.import_file))

        now = datetime.now()
        stamp = now.strftime("%Y%m%d%H%M")
        filename = "{}treebard_gps/etc/gedcom_import_exceptions_{}.txt".format(current_drive, stamp)
        date, hour, minute = stamp[0:8], stamp[8:10], stamp[10:]
        date = "{}-{}-{}".format(date[0:4], date[4:6], date[6:])
        ff = open(filename, "a")
        ff.write("Imported to Treebard GPS on {} at {}:{}.\n".format(date, hour, minute))
        REPLACE = {
            'SOUR': 'Source of GEDCOM File', 'FILE': 'GEDCOM File Name', 
            'GEDC': 'GEDCOM Version', 'CHAR': 'Character Set Encoding'}
        for k,v in self.importer.head_dict.items():
            ff.write("\n{}: ".format(REPLACE[k]))

            if k == 'SOUR':
                ware, version, vendor = v.values()
                ff.write("{} version {} by {}".format(ware, version, vendor))
            else:
                print("line", looky(seeline()).lineno, "v:", v)
                ff.write("{}\n".format(v))

        ff.write("\nThis file: {}\n\n".format(filename))

        if self.importer.head_dict['FILE'] != self.treebard.import_file:
            msg = "The file actually imported...\n\t{}\nhas had its name changed from the file that was originally exported...\n\t{}.\n".format(
                self.treebard.import_file, self.importer.head_dict['FILE'])
            ff.write("{}\n".format(msg))

        ff.write("EXCEPTIONS\n\n")

        for k,v in self.importer.exceptions_dict.items():
            self.textbox.text.insert("end", "\n{}\n\n".format(k))
            ff.write("{}\n\n".format(k))
            for tup in v:
                text = "Family ID #{} linked to Source ID #{}".format(
                    int(sub("\D", "", tup[0])), int(sub("\D", "", tup[1])))
                self.textbox.text.insert("end", "{}\n".format(text))
                ff.write("\t{}\n".format(text))
        ff.close()

    def cancel(self):
        self.destroy()




# # # reset_tree() # DO NOT DELETE AND DO NOT RUN ACCIDENTALLY, ALL DATA WILL BE DELETED***********
# `_fixed` has had custom tags manually deleted






















