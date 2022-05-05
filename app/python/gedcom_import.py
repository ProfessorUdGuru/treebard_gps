# gedcom_import.py
import tkinter as tk
import sqlite3
from re import sub
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




conn = sqlite3.connect("d:/treebard_gps/data/gedcom_import_001/gedcom_import_001.tbd")
cur = conn.cursor()

# tags which can occur at level 0
ZERO_LEVEL_TAGS = ("HEAD", "TRLR", "FAM", "INDI", "OBJE", "NOTE", "REPO", "SOUR", "SUBM")
records_dict = {}
for tag0 in ZERO_LEVEL_TAGS:
    records_dict[tag0] = {}
# tags whose lines should always have exactly 2 elements
ELEMS2 = ("HEAD", "GEDC", "PLAC")
# tags whose lines should have only 2 elements, unless the 3rd element is "Y":
ELEMS2Y = ("BIRT", "DEAT", "CHR", "MARR")

# line_lists = []
# def read_gedcom(file):
    # """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
        # first line.
    # """
    # # print("line", looky(seeline()).lineno, "file:", file)
    # f = open(file, "r", encoding='utf-8-sig')
    # for line_text in f.readlines():
        # lst = line_text.strip("\n").split(" ", 2)
        # lst[0] = int(lst[0])
        # line_lists.append(lst)

# def validate_lines():
    # """ Add a 4th element to bad lines. """
    # for line in line_lists:
        # length = len(line)
        # tag = line[1]
        # if length > 3:
            # line.append("too_long")
        # elif length > 2:
            # if tag in ELEMS2Y:
                # if line[2] != "Y":
                    # line.append("too_long_y")

# def delineate_records():
    # tag0 = None
    # h = 0
    # for line in line_lists:
        # if line[0] == 0:
            # if line[1] in ("HEAD", "TRLR"):
                # tag0 = line[1]
                # h = add_subrecords(line, h, tag0)
            # elif len(line) > 2:
                # tag0 = line[2]
                # h = add_subrecords(line, h, tag0)
            # else:
                # print("line", looky(seeline()).lineno, "case not handled:")
        # else:
            # pass
    # # print("line", looky(seeline()).lineno, "records_dict:", records_dict)
      
# def add_subrecords(line, h, tag0):
    # copy = records_dict
    # pk = line[1]
    # subrecords = []
    # j = h + 1
    # for lst in line_lists[j:]:
        # if lst[0] > 0:
            # subrecords.append(lst)
            # j += 1
        # else:
            # break
    # for k,v in copy.items():
        # if k == tag0:
            # records_dict[k][pk] = subrecords            
    # return j

# def input_persons():
    # for k,v in records_dict.items():
        # if k != "INDI":
            # continue
        # record = v
        # for kk, vv in record.items():
            # person_id = kk
            # person_data = vv
            # z = 0
            # for line in person_data:
                # parse_line(person_id, line, z)
                # z += 1

# def input_sources():
    # for k,v in records_dict.items():
        # if k != "SOUR":
            # continue
        # record = v
        # for kk, vv in record.items():
            # source_id = kk
            # source_data = vv
            # z = 0
            # for line in source_data:
                # parse_line(source_id, line, z)
                # z += 1

# def input_families():
    # for k,v in records_dict.items():
        # if k != "FAM":
            # continue
        # record = v
        # for kk, vv in record.items():
            # family_id = kk
            # family_data = vv
            # z = 0
            # for line in family_data:
                # parse_line(family_id, line, z)
                # z += 1


# def parse_line(pk, line, z):
    # n = line[0]
    # tag = line[1]
    # if len(line) == 3:
        # data = line[2]
    # if n == 1:
        # if tag == "NAME":
            # add_person(pk, data)
        # elif tag == "TITL":
            # add_source(pk, data)
        # elif tag in ("HUSB", "WIFE", "CHILD", "SOUR"):
            # add_family(pk, data, tag)
        # parse_next_line(pk, z)

# def parse_next_line(person_id, z):
    # # print("line", looky(seeline()).lineno, "person_id:", person_id)
    # # print("line", looky(seeline()).lineno, "z:", z)
    # pass

# def add_family(pk, data, tag):
    # if tag == "SOUR":
        # link_source_famtag(pk, data)
    # elif tag == "CHILD":
        # pass
    # elif tag == "HUSB":
        # pass
    # elif tag == "WIFE":
        # pass
    # else:
        # print("line", looky(seeline()).lineno, "tag not handled:", tag)

# def link_source_famtag(pk, data):
    # fk = int(sub("\D", "", data))
    # print("line", looky(seeline()).lineno, "pk, data:", pk, data)
    

# def add_source(source_id, title):
    # source_id = int(sub("\D", "", source_id))
    # cur.execute(insert_source, (source_id, title))
    # conn.commit()    

# def add_person(person_id, name):
    # person_id = int(sub("\D", "", person_id))
    # name_list = name.split()
    # for i in name_list:
        # if i.startswith("/"):
            # idx = name_list.index(i)
            # x = name_list.pop(idx).strip("/")
            # sorter = list(name_list)
            # sorter.insert(0, "{},".format(x))
            # sorter = " ".join(sorter).strip()
    # if person_id != 1:    
        # cur.execute(insert_person, (person_id,))
        # conn.commit()
        # cur.execute(insert_name, (person_id, name, sorter))
        # conn.commit()
        # cur.execute(insert_finding_birth, (person_id,))
        # conn.commit()
    # else:
        # cur.execute(update_name, (name, sorter))
        # conn.commit()

class GedcomImporter():
    def __init__(self, import_file):
        self.line_lists = []
        self.read_gedcom(import_file)

    def read_gedcom(self, file):
        """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
            first line.
        """
        # print("line", looky(seeline()).lineno, "file:", file)
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
        # print("line", looky(seeline()).lineno, "records_dict:", records_dict)
          
    def add_subrecords(self, line, h, tag0):
        copy = records_dict
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
                records_dict[k][pk] = subrecords            
        return j

    def input_persons(self):
        for k,v in records_dict.items():
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
        for k,v in records_dict.items():
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
        for k,v in records_dict.items():
            if k != "FAM":
                continue
            record = v
            for kk, vv in record.items():
                family_id = kk
                family_data = vv
                z = 0
                for line in family_data:
                    self.parse_line(family_id, line, z)
                    z += 1


    def parse_line(self, pk, line, z):
        n = line[0]
        tag = line[1]
        if len(line) == 3:
            data = line[2]
        if n == 1:
            if tag == "NAME":
                self.add_person(pk, data)
            elif tag == "TITL":
                self.add_source(pk, data)
            elif tag in ("HUSB", "WIFE", "CHILD", "SOUR"):
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
        print("line", looky(seeline()).lineno, "pk, data:", pk, data)
        

    def add_source(self, source_id, title):
        source_id = int(sub("\D", "", source_id))
        cur.execute(insert_source, (source_id, title))
        conn.commit()    

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
        if person_id != 1:    
            cur.execute(insert_person, (person_id,))
            conn.commit()
            cur.execute(insert_name, (person_id, name, sorter))
            conn.commit()
            cur.execute(insert_finding_birth, (person_id,))
            conn.commit()
        else:
            cur.execute(update_name, (name, sorter))
            conn.commit()

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
             
# def make_unique_tag_lists():
    # for lst in line_lists:
        # elem_1 = lst[1]
        # if elem_1.startswith("@") is False:
            # if elem_1.startswith("_"):
                # custom_tags.append(elem_1.rstrip("\n"))
            # else:
                # tags.append(elem_1.rstrip("\n"))
        # else:
            # if lst[2].startswith("_"):
                # custom_tags.append(lst[2].rstrip("\n"))
            # else:
                # tags.append(lst[2].rstrip("\n"))
    # tags = list(set(tags))
    # custom_tags = list(set(custom_tags))
# line 50 tags: ['CONC', 'DATE', 'BAPM', 'NCHI', 'PLAC', 'NAME', 'STAE', 'SOUR', 'RESI', 'TIME', 'WILL', 'VERS', 'RELI', 'NATU', 'SSN', 'OCCU', 'GEDC', 'ADDR', 'BIRT', 'HUSB', 'PROB', 'CHIL', 'NMR', 'DSCR', 'MARL', 'CONF', 'CHAN', 'FAMS', 'PAGE', 'PUBL', 'TYPE', 'AUTH', 'MARR', 'HEAD', 'FILE', 'FORM', 'FAM', 'NICK', 'TRLR', 'CHAR', 'CONT', 'DEAT', 'DIV', 'BURI', 'CORP', 'NOTE', 'INDI', 'IMMI', 'CENS', 'WIFE', 'SEX', 'FAMC', 'EVEN', 'TITL']
# line 51 custom_tags: ['_ADDR', '_FLAG', '_PREF', '_PUBLISHER', '_TYPE', '_LEVEL', '_NAME', '_QUAL', '_PUBDATE', '_DETAIL']

elements_dict = {"FAM": "family_id", "INDI": "person_id", "SOUR": "source_id"}

def get_id_type(tag):
    if tag in ("FAM", "INDI", "SOUR"):
        element = elements_dict[tag]
    return element 

def reset_tree():
    cur.execute(update_gender_default_person)
    conn.commit()
    cur.execute(delete_name_all)
    conn.commit()
    cur.execute(update_name_default_person)
    conn.commit()
    cur.execute(delete_finding_all)
    conn.commit()
    cur.execute(insert_finding_default_person)
    conn.commit()
    cur.execute(delete_source_all)
    conn.commit()
    cur.execute(delete_person_all)
    conn.commit()

cur.close()
conn.close()

# from gedcom_exceptions



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

        self.make_text_file()
        self.importer = GedcomImporter(self.treebard.import_file)
        self.importer.read_gedcom(self.treebard.import_file)
        self.importer.validate_lines()
        self.importer.delineate_records()
        # self.importer.input_persons() # DO NOT DELETE **********************
        # self.importer.input_sources() # DO NOT DELETE **********************
        self.importer.input_families() # DO NOT DELETE **********************
        self.infolab.config(text="GEDCOM input file: {}".format(self.treebard.import_file))

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

        self.search_dlg_heading = LabelH2(
            header, 
            text='Items Not Imported by GEDCOM')
        self.search_dlg_heading.grid(column=0, row=0, pady=(24,0))

        head_msg = "Items listed below can be input manually using Treebard's interface.\nInstructions are included for each category of failed import.\nThis document has been saved as a text file with the same name as the GEDCOM file you imported."
        instrux = Label(header, text=head_msg)
        instrux.grid(column=0, row=1, sticky='e', padx=24, pady=12)

        self.info = Frame(self.window)
        self.info.grid(column=0, row=1, sticky='news', padx=48, pady=48)

        self.infolab = Label(self.info)
        self.infolab.grid()

        self.textbox = ScrolledText(self.info)

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
            # self.search_input, self.search_dlg_heading, self.info)
        # make_rc_menus(
            # rcm_widgets, 
            # self.rc_menu, 
            # search_person_help_msg) 

        resize_scrolled_content(self, self.canvas, self.window)

    def make_text_file(self):
        pass

    def cancel(self):
        self.destroy()



if __name__ == "__main__":
    # # # reset_tree() # DO NOT DELETE AND DO NOT RUN ACCIDENTALLY, ALL DATA WILL BE DELETED***********
    # `_fixed` has had custom tags manually deleted
    read_gedcom("D:/treebard_gps/app/python/todd_boyett_connections_fixed.ged")
    # read_gedcom("D:/treebard_gps/app/python/todd_boyett_connections.ged")
    # read_gedcom("D:/treebard_gps/app/python/robertson_rathbun_family_tree_export_by_gb.ged")
    validate_lines()
    delineate_records()
    # input_persons() # DO NOT DELETE **********************
    # input_sources() # DO NOT DELETE **********************
    input_families() # DO NOT DELETE **********************





















# DO LIST:
# there are now 3 things called "import_gedcom" which has to be fixed because I'm confused. 1) in SplashScreen there's a method, 2) in gedcom_import.py there WAS a module-level function which is now commented out but before I started making the new class importer which is not a widget, this worked and was run inside __init__ of the exceptions dialog class, 3) there's a instance level version of the comment function. The reason I started making a class is so that the functions in the module namespace could get access to the ScrolledText widget in the dialog by making the text an attribute of self.treebard which I had no access to in the module namespace.
# Make the module-level functions into instance-level methods of GedomExceptions class so that adding text to the ScrolledText widget each time something needs to be added is a simple matter of accessing self.
# When encountering a SOUR tag subordinate to a FAM tag, invoke the GedcomExceptions class which I need to create right now. This will be a dialog that opens up without the user's permission when a GEDCOM finishes loading. The gedcom_exceptions module will have messages such as this one: "The GEDCOM `FAM` tag is used during import to Treebard only to determine relationships of persons within the family. Chances are that if you linked a source to a family in the genealogy software that wrote the imported GEDCOM, you could look at the source again now and manually link it in Treebard to only those persons in the family that are actually elucidated by the source. But it's also probably that you originally linked the source to something other than a family unit when originally inputing the source, and then the software decided to add it to a family unit that was created by the software to match the expectations of GEDCOM's structure. If you know you didn't link sources to family units in the original, then there is nothing for you to do, since the software that created the GEDCOM probably did not delete your original link when creating the family unit expected by GEDCOM."
# what does the FAM tag accomplish that I also need to accomplish? It provides foreign key references for people related to each other.
# First get FAM, INDI & SOUR level 1 creation lines into the db then the ones in INDI that I forgot, before trying to get level 2+ in, because these levels will include FK refs that won't be valid till the data is in. FAMC and FAMS have to check whether the FK has already been put in and if so they can be ignored. MAKE/POST GEDCOM VIDEO SEE DO LIST. Add a `changed` table to db and a module to the app, or put the code in utes.py. Then write input_changed(). The only right time to handle subordinate lines is nested inside the for loops that handle the level 1 tags see parse_next_line
# After it becomes possible to input subordinate lines, change to a larger db that has SUBM, NOTE etc level 0 tags
# Replace switch statements with dicts
# Fix the names input code to handle multiple names. Put alt names back in that I stripped out earlier (see Jimmy, Grace, Lora in unfixed .ged file). From the docs:
# ! Multiple Names:
    # GEDCOM 5.x requires listing different names in different NAME structures, with the preferred
    # instance first, followed by less preferred names. However, Personal Ancestral File and other products
    # that only handle one name may use only the last instance of a name from a GEDCOM transmission.
    # This causes the preferred name to be dropped when more than one name is present. The same thing
    # often happens with other multiple-instance tags when only one instance was expected by the receiving
    # system.
