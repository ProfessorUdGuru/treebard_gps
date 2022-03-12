# names.py

import tkinter as tk
import sqlite3
from files import get_current_file
from styles import config_generic
from widgets import (
    Frame, Label, Button, LabelMovable, LabelH3, Entry, Toplevel)
from window_border import Border
from custom_combobox_widget import Combobox  
from scrolling import MousewheelScrolling, Scrollbar, resize_scrolled_content 
from autofill import EntryAutoPerson
from toykinter_widgets import run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from messages_context_help import person_add_help_msg
from messages import open_yes_no_message, names_msg, open_message
from images import get_all_pics    
from query_strings import (
    select_current_person, select_name_with_id, select_all_names_ids,
    select_all_person_ids, select_image_id, select_max_person_id,    
    insert_images_elements, select_name_type_id, insert_name, 
    select_all_images, select_all_name_types, insert_person_new,
    select_person_gender, select_max_name_type_id, insert_name_type_new,
    insert_image_new, select_name_with_id_any, select_birth_names_ids,
    insert_finding_birth_new_person, insert_finding_places_new,
    select_current_person_id, delete_name_person, delete_findings_roles_person,
    select_name_person, delete_links_links_person, delete_links_links_name,
    update_persons_persons_1_null, update_persons_persons_2_null,
    delete_finding_person, delete_claims_roles_person, delete_person,
    update_claims_persons_1_null, update_claims_persons_2_null,
    delete_images_elements_person, delete_claim_person, select_name_sorter,
    select_name_type_sorter_with_id, 
    )
import dev_tools as dt
from dev_tools import looky, seeline




GENDER_TYPES = ('unknown', 'female', 'male', 'other')

NAME_SUFFIXES = (
    'jr.', 'sr.', 'jr', 'sr', 'junior', 'senior', 
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 
    'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv')

NAME_TYPES_HIERARCHY = (
    'reference name', 'adoptive name', 'also known as', 'married name', 
    'legally changed name', 'pseudonym', 'pen name', 'stage name', 'nickname', 
    'call name', 'official name', 'anglicized name', 'religious order name', 
    'alternate spelling', 'mis-spelling', 'ID number', 'handle', 
    'other name type', 'given name', 'unknown name')

def get_current_person():
    current_person_id = 1
    current_person = ""
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person)
    result = cur.fetchone()
    return result

def get_name_types():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_name_types)
    name_types = cur.fetchall()
    cur.close()
    conn.close()
    name_types = [i[0] for i in name_types]

    return name_types

def get_name_with_id(iD):
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_name_with_id, (iD,))
    full_name = cur.fetchone()

    cur.close()
    conn.close()

    if full_name:
        return full_name[0]
    elif not full_name:
        return ''

def get_any_name_with_id(iD):
    """ Get any available name that Treebard considers a viable name type
        even if there is no birth name available. To be viable, the name type
        has to be in the hierarchy.

        Returns 'name unknown' if no name or if the only available name type
        is not considered viable.

        Since this viability hierarchy was applied, some names will not display
        at all, so the hierarchy should actually include all name types so one
        will display if it's all that's available.

        Currently dealing with this problem with a hard-coded tuple 
        NAME_TYPES_HIERARCHY which has to have each name type added to it. So if
        the user creates a new name type, it will not be viable (the name won't display
        if the person has no name type in the hierarchy.)

        The solution is to let the user prioritize any added name types, 
        by interfiling them in the tuple which will have to be a list. Birth 
        name will be priority 1. All other names will be priority 2 or 3 or maybe
        2 thru 5. This will be saved in the database for each type in a new column
        called `hierarchy`. Then the hard-coded list could be dispensed with.

        For now I'm just going to add non-viable name types to the end of the tuple
        so that no one goes without a display name.
    """

    # current_file = get_current_file()[0]
    # birth_name = get_name_with_id(iD)
    # if len(birth_name) == 0:
        # use_name = ""
        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_name_with_id_any, (iD,))
        # all_names_types = cur.fetchall()
        # for tup in all_names_types:
            # for name in NAME_TYPES_HIERARCHY:
                # if tup[1] == name:
                    # use_name = tup
                    # break
        # cur.close()
        # conn.close()

        # length = len(use_name)
        # if length == 2:
            # use_name = "{} ({})".format(
                # use_name[0], use_name[1])

        # return use_name
    # else:
        # return birth_name   


# keys1 = (12, 1, 6, 5599, 5, 9898, 9999)
# keys2 = ("birth name", "alt name", "alt name type", "sort order")
# values = [
    # ("James Norton", "James Woodland", "adopted name", "Woodland, James"),
    # ("Jeremiah Grimaldo", "G-Man", "nickname", "Grimaldo, Jeremiah"),
    # ("Ronnie Webb", "Miss Polly", "stage name", "Webb, Ronnie"),
    # ("", "Selina Savoy", "pseudonym", "Savoy, Selina"),
    # ("Donald Webb", "Donny Boxer", "nickname", "Webb, Donald"),
    # ("John Smith", "Smitty", "nickname", "Smith, John"),
    # ("John Smith", "Mack", "nickname", "Smith, John"),
# ]

# # inner_dict = list(zip(keys2, values))
# # print(inner_dict)
# inner_dict = []
# for tup in values:
    # indict = dict(zip(keys2, tup))
    # inner_dict.append(indict)
# # print(inner_dict)

# outer_dict = dict(zip(keys1, inner_dict))
# # print(outer_dict)
# # {12: {'birth name': 'James Norton', 'alt name': 'James Woodland', 'alt name type': 'adopted name', 'sort order': 'Woodland, James'}, 1: {'birth name': 'Jeremiah Grimaldo', 'alt name': 'G-Man', 'alt name type': 'nickname', 'sort order': 'Grimaldo, Jeremiah'}, 6: {'birth name': 'Ronnie Webb', 'alt name': 'Miss Polly', 'alt name type': 'stage name', 'sort order': 'Webb, Ronnie'}, 5599: {'birth name': '', 'alt name': 'Selina Savoy', 'alt name type': 'pseudonym', 'sort order': 'Savoy, Selina'}, 5: {'birth name': 'Donald Webb', 'alt name': 'Donny Boxer', 'alt name type': 'nickname', 'sort order': 'Webb, Donald'}}

# people = outer_dict

PERSON_DATA = ("birth name", "alt name", "alt name type", "sort order")
def make_all_names_dict_for_person_select():
    """ Make a name dict for global use in all name autofills.
    """

    # def get_any_name(iD, cur):
        # birth_name, sorter = ("", "")
        # cur.execute(select_name_sorter, (iD,))
        # result = cur.fetchone()
        # if result:
            # birth_name, sorter = result
        # if len(birth_name) == 0:
            # name_data = []
            # cur.execute(select_name_type_sorter_with_id, (iD,))
            # all_names_types = cur.fetchall()
            # for tup in all_names_types:
                # for alt_name_type in NAME_TYPES_HIERARCHY:
                    # if tup[1] == alt_name_type:
                        # name_data = list(tup)
                        # break
            # return [""] + name_data
        # else:
            # return birth_name, "", "", sorter

    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_person_ids)
    person_ids = [i[0] for i in cur.fetchall()]
    values = []
    for iD in person_ids:
        # birth_name, name_data, alt_name_type, sort_order = get_any_name(iD)
        values.append(get_any_name(iD, cur))
    # print("line", looky(seeline()).lineno, "values[1:5]:", values[1:5])

    inner_dict = []
    for tup in values:
        indict = dict(zip(PERSON_DATA, tup))
        inner_dict.append(indict)

    cur.close()
    conn.close()

    return dict(zip(person_ids, inner_dict))

def get_any_name(iD, cur):
    birth_name, sorter = ("", "")
    cur.execute(select_name_sorter, (iD,))
    result = cur.fetchone()
    if result:
        birth_name, sorter = result
    if len(birth_name) == 0:
        name_data = []
        cur.execute(select_name_type_sorter_with_id, (iD,))
        all_names_types = cur.fetchall()
        for tup in all_names_types:
            for alt_name_type in NAME_TYPES_HIERARCHY:
                if tup[1] == alt_name_type:
                    name_data = list(tup)
                    break
        return [""] + name_data
    else:
        return birth_name, "", "", sorter
    

def make_all_names_list_for_person_select(): # change to _dict_
    """ Make a name dict for global use in all name autofills.
    """
# COMMENTED GOOD STUFF GETTING READY TO DELETE THIS FUNCTION SO JUST COVERING UP ERRORS NOW
    people = []
    # current_file = get_current_file()[0]
    # conn = sqlite3.connect(current_file)
    # cur = conn.cursor()
    # cur.execute(select_all_names_ids)

    # peeps = cur.fetchall()

    # cur.close()
    # conn.close()

    # peeps = sorted(peeps, key=lambda i: i[2])
    # people = dict(peeps)
    # print("line", looky(seeline()).lineno, "people:", people)
    return people 

# people = {
    # 12: {
        # "birth name": "James Norton", "alt name": "James Woodland", 
        # "alt name type": "adopted name", "sort order": "Woodland, James"},
    # 1: {
        # "birth name": "Jeremiah Grimaldo", "alt name": "G-Man", 
        # "alt name type": "nickname", "sort order": "Grimaldo, Jeremiah"}, 
    # 6: {
        # "birth name": "Ronnie Webb", "alt name": "Miss Polly", 
        # "alt name type": "stage name", "sort order": "Webb, Ronnie"}, 
    # 5599: {
        # "birth name": "", "alt name": "Selina Savoy", 
        # "alt name type": "pseudonym", "sort order": "Savoy, Selina"}, 
    # 5: {
        # "birth name": "Donald Webb", "alt name": "Donny Boxer", 
        # "alt name type": "nickname", "sort order": "Webb, Donald"}} 

# def make_all_names_list_for_person_select():
    # ''' 
        # all name types, best for autofill values 
    # '''
    # current_file = get_current_file()[0]
    # conn = sqlite3.connect(current_file)
    # cur = conn.cursor()
    # cur.execute(select_all_names_ids)

    # peeps = cur.fetchall()
    # peeps = [list(i) for i in peeps]

    # cur.close()
    # conn.close()

    # combo_peeps = sorted(peeps, key=lambda i: i[2])
    # people = []
    # for tup in combo_peeps:
        # line = '{}  #{}'.format(tup[0], tup[1])
        # people.append(line)
    # print("line", looky(seeline()).lineno, "people:", people)
    # return people

def update_person_autofill_values():
    people = make_all_names_dict_for_person_select()
    # people = make_all_names_list_for_person_select()
    all_birth_names = EntryAutoPerson.create_lists(people)
    for ent in EntryAutoPerson.all_person_autofills:
        ent.values = all_birth_names

def get_all_persons():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_person_ids)
    person_ids = cur.fetchall()
    person_ids = [i[0] for i in person_ids]
    cur.close()
    conn.close()
    persons = []
    for iD in person_ids:
        name = get_any_name_with_id(iD)
        if type(name) is tuple:
            name = "{}  #{}".format(name[0], iD)
        elif len(name) != 0:
            name = '{}  #{}'.format(name, iD)
        persons.append(name)
    return persons

def open_new_person_dialog(master, inwidg, root, treebard, formats, inwidg2=None):
    person_add = PersonAdd(master, inwidg, root, treebard, inwidg2, formats)
    root.wait_window(person_add)
    new_person_id = person_add.show()
    return new_person_id

def delete_person_from_tree(person_id):
    """Remove all references to a person.""" 

    def delete_current_person_dialog():
        print("line", looky(seeline()).lineno, "open dialog to get new curr per user input:")
   
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    # current
    cur.execute(select_current_person_id)
    current_person = cur.fetchone()[0]
    if current_person == person_id:
        delete_current_person_dialog()
    # links_links.name_id
    cur.execute(select_name_person, (person_id,))
    names = [i[0] for i in cur.fetchall()]
    for name_id in names:    
        cur.execute(delete_links_links_name, (name_id,))
        conn.commit()
    # links_links.person_id
    cur.execute(delete_links_links_person, (person_id,))
    conn.commit()
    # name
    cur.execute(delete_name_person, (person_id,))
    conn.commit()
    # findings_roles
    cur.execute(delete_findings_roles_person, (person_id,))
    conn.commit()
    # findings_persons.person_id1
    cur.execute(update_persons_persons_1_null, (person_id,))
    conn.commit()
    # findings_persons.person_id2
    cur.execute(update_persons_persons_2_null, (person_id,))
    conn.commit()
    # finding
    cur.execute(delete_finding_person, (person_id,))
    conn.commit()
    # claims_roles 
    cur.execute(delete_claims_roles_person, (person_id,))
    conn.commit()
    # # # # # DO NOT DELETE; the db table doesn't exist yet
    # # # # claims_persons.person_id1
    # # # cur.execute(update_claims_persons_1_null, (person_id,))
    # # # conn.commit()
    # # # # claims_persons.person_id2
    # # # cur.execute(update_claims_persons_2_null, (person_id,))
    # # # conn.commit()
    # claim
    cur.execute(delete_claim_person, (person_id,))
    conn.commit()
    # images_elements
    cur.execute(delete_images_elements_person, (person_id,))
    conn.commit()
    # person (primary key)
    cur.execute(delete_person, (person_id,))
    conn.commit()

    people = make_all_names_list_for_person_select()
    all_birth_names = EntryAutoPerson.create_lists(people)
    for ent in EntryAutoPerson.all_person_autofills:
        ent.values = all_birth_names

    cur.close()
    conn.close()

class PersonAdd(Toplevel):
    def __init__(
            self, master, inwidg, root, treebard, inwidg2, 
            formats, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.inwidg = inwidg
        self.root = root
        self.inwidg2 = inwidg2
        self.formats = formats

        self.xfr = self.inwidg.get()
        self.role_person_edited = False
        self.rc_menu = RightClickMenu(self.root, treebard=treebard)

        self.new_person_id = None
        self.full_name = ""
        self.name_type_id = None

        self.make_dupe = False

        self.make_widgets()

    def make_widgets(self):

        self.geometry('+100+20')

        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, self.root, self.formats)
        self.canvas.title_1.config(text="Add Person Dialog")
        self.canvas.title_2.config(text="")

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

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
        self.b1 = Button(
            buttonbox, text="OK", width=8, command=self.prepare_to_add_person)
        b2 = Button(
            buttonbox, text="CANCEL", width=8, command=self.close_new_person)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1)
        buttonbox.grid(column=3, row=9, sticky='e', pady=6)

        self.b1.grid(column=0, row=0, padx=(0,12))
        b2.grid(column=1, row=0, padx=(2,0))

        self.make_inputs()
        self.maxsize(
            int(self.winfo_screenwidth() * 0.90),
            int(self.winfo_screenheight() * 0.90))
        self.grab_set()

    def make_inputs(self):

        all_pics = get_all_pics()

        lab1 = Label(self.window, text='Gender:')
        self.gender_input = Combobox(
            self.window, self.master, values=GENDER_TYPES)

        lab2 = Label(self.window, text='Main Image:')
        self.image_input = Combobox(self.window, self.master, values=all_pics)

        lab3 = Label(self.window, text='Name Type:')
        self.name_type_input = Combobox(
            self.window, self.master, values=get_name_types())

        lab4 = Label(self.window, text='Full Name:')
        self.name_input = Entry(self.window, width=65)
        self.name_input.bind("<FocusOut>", self.show_sort_order)

        self.how = LabelH3(
            self.window, 
            justify="left",
            text="Alphabetize name: with AUTOSORT or OK button in focus...\n"
                "...use arrow keys to enter auto-filled name fields to modify "
                "sort order or...\n...in case sort order is already "
                "correct, TAB goes directly to OK button.")
        autosort = Button(
            self.window, text='AUTOSORT', command=self.show_sort_order)
        autosort.bind("<Right>", self.go_to_movables)
        self.b1.bind("<Left>", self.go_to_movables)

        self.order_frm = Frame(self.window)

        s = 0
        for stg in range(20):
            mov = LabelMovable(self.order_frm)
            mov.grid(column=s, row=0, padx=3)
            s += 1 
        for child in self.order_frm.winfo_children():
            child.config(takefocus=0)
        lab1.grid(column=0, row=3)
        self.gender_input.grid(
            column=1, row=3, padx=12, pady=12, sticky='e')
        lab2.grid(column=2, row=3)
        self.image_input.grid(column=3, row=3, padx=12, pady=12, sticky='w')
        lab3.grid(column=0, row=4, padx=(18,0))
        self.name_type_input.grid(
            column=1, row=4,  padx=12, pady=12, sticky='e')
        lab4.grid(column=2, row=4)
        self.name_input.grid(column=3, row=4, padx=12, pady=12)

        self.how.grid(column=1, row=5, padx=6, pady=6, columnspan=4, sticky='w')
        autosort.grid(column=1, row=6, padx=6, pady=6, sticky='w')
        self.order_frm.grid(column=2, row=6, columnspan=4, pady=24, sticky='w')

        visited = (
            (self.gender_input, 
                "Gender Input", 
                "'Unknown' used if left blank."),
            (self.image_input, 
                "Image Input", 
                "Use an old photo of person's home town if no photo available."),
            (self.name_type_input, 
                "Name Type Input", 
                "Choose the name type."),
            (self.name_input, 
                "Name Input", 
                "Autofills but you can change it."),
            (autosort, 
                "Autosort Button", 
                "Click to auto-create a sortable name."),
            (self.order_frm, 
                "", 
                "Tab to focus name element. Arrow to change order.")
)        
        run_statusbar_tooltips(
            visited, 
            self.canvas.statusbar.status_label, 
            self.canvas.statusbar.tooltip_label)

        self.preset()

        rcm_widgets = (
            self.name_input, self.name_type_input.entry, self.gender_input.entry,
            self.image_input.entry, autosort, self.order_frm)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu, 
            person_add_help_msg)

        config_generic(self)
        resize_scrolled_content(self, self.canvas, self.window)
        self.gender_input.entry.focus_set()

    def show_sort_order(self, evt=None):

        if evt is not None and evt.type == "10":
            for child in self.order_frm.winfo_children():
                child.config(text='')

        self.got = self.name_input.get().split()
        if len(self.got) == 0:
            return
        else:
            length = len(self.got)-1
        word = self.got[length].lower()
        
        self.got.insert(0, ',')
        length += 1
        if word not in NAME_SUFFIXES:
            self.got.insert(0, self.got.pop())
        elif word in NAME_SUFFIXES and self.got[length].lower() == word:
            self.got.insert(0, self.got.pop())
            self.got.insert(0, self.got.pop())

        for child in self.order_frm.winfo_children():
            child.config(text='')

        v = 0
        for name in self.got:
            self.order_frm.winfo_children()[v].config(text=name)
            v += 1

    def go_to_movables(self, evt):
        labels = self.order_frm.winfo_children()
        for child in labels:
            child.config(takefocus=1)
        sym = evt.keysym
        if sym == "Right":
            labels[0].focus_set()
        elif sym == "Left":
            labels[19].focus_set()

    def preset(self):
        self.gender_input.entry.delete(0, 'end')
        self.gender_input.entry.insert(0, 'unknown')
        self.image_input.entry.delete(0, 'end')
        self.image_input.entry.insert(0, 'default_image_unisex.jpg')
        self.name_type_input.entry.config(state='normal')
        self.name_type_input.entry.delete(0, 'end')
        self.name_type_input.entry.insert(0, 'birth name')
        self.name_input.delete(0, 'end')
        get2 = self.inwidg2
        if get2 and len(get2.get()) != 0:
            self.name_input.insert(0, get2.get())
        elif get2 and len(get2.get()) == 0:
            self.name_input.insert(0, self.xfr)
        elif get2 is None:
            self.name_input.insert(0, self.xfr)

    def make_sort_order_to_store(self): 
        self.order = []

        for child in self.order_frm.winfo_children():
            text = child['text']
            self.order.append(text)

        self.order = ' '.join(self.order)
        self.order = self.order.replace(' , ', ', ')
        self.order = self.order.strip(', ')
        if len(self.order) == 0:
            order = self.full_name.split()
            order.insert(0, order.pop())
            order[0] = order[0] + ","
            self.order = " ".join(order)

    def prepare_to_add_person(self, findings_roles_id=None):

        def err_done():
            self.name_type_input.delete(0, 'end')
            msg[0].grab_release()
            msg[0].destroy()
            self.name_type_input.entry.focus_set()
    
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        self.get_entered_values(cur, conn)
        self.findings_roles_id = findings_roles_id
        # can these 2 queries be combined?
        cur.execute(select_image_id, (self.selected_image,))
        self.img_id = cur.fetchone()[0]
        cur.execute(select_name_type_id, (self.name_type,))
        name_type_id = cur.fetchone()
        if name_type_id:
            self.name_type_id = name_type_id[0]            
            self.check_for_dupes()
        else:
            msg = open_message(
                self, 
                names_msg[1], 
                "Unknown Name Type", 
                "OK")
            msg[0].grab_set()
            msg[2].config(command=err_done)
            return
        cur.close()
        conn.close()

    def ok_new_person(self):
        self.save_new_name()
        self.close_new_person() 

    def close_new_person(self):
        self.grab_release()
        self.inwidg.focus_set()
        self.destroy()        

    def get_entered_values(self, cur, conn):
        self.full_name = self.name_input.get()
        selected_image = self.image_input.entry.get()
        self.name_type = self.name_type_input.entry.get()
        gender = self.gender_input.get()
        if gender in GENDER_TYPES:
            self.gender = gender
        else:
            self.gender = 'unknown'
        all_images = [i[0] for i in get_all_pics()]
        if selected_image in all_images:
            self.selected_image = selected_image
        else:
            cur.execute(insert_image_new, (selected_image,))
            conn.commit()
            self.selected_image = selected_image 

    def save_new_name(self):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        conn.execute('PRAGMA foreign_keys = 1')
        cur.execute(insert_person_new, (self.new_person_id, self.gender))
        conn.commit()
        cur.execute(
            insert_name, 
            (self.new_person_id, self.full_name, self.name_type_id, self.order))
        conn.commit()

        cur.execute(insert_images_elements, (self.img_id, self.new_person_id))
        conn.commit()

        cur.execute(insert_finding_birth_new_person, (self.new_person_id,))
        conn.commit()
        cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "finding"')
        birth_id = cur.fetchone()[0]
        cur.execute(insert_finding_places_new, (birth_id,))
        conn.commit()

        new_name_string = "{}  #{}".format(self.full_name, self.new_person_id)
        self.inwidg.delete(0, 'end')
        self.inwidg.insert(0, new_name_string)
        cur.close()
        conn.close()

        self.image_input.delete(0, 'end')
        self.image_input.insert(0, 'default_image_unisex.jpg')

        for widg in (self.name_type_input, self.name_input):
            widg.delete(0, 'end')

        for child in self.order_frm.winfo_children():
            child.config(text='')
        self.gender_input.delete(0, 'end')

    def show(self):
        people = make_all_names_list_for_person_select()        
        all_birth_names = EntryAutoPerson.create_lists(people)

        return self.new_person_id

    def make_temp_person_id(self):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_max_person_id)
        self.new_person_id = cur.fetchone()[0] + 1
        if self.role_person_edited is True:
            cur.execute(
                update_findings_roles_person, 
                (self.new_person_id, self.findings_roles_id))
            conn.commit()
            self.role_person_edited = False 
        
        cur.close()
        conn.close()

    def check_for_dupes(self):

        def ok_new_name():
            self.make_dupe = True
            msg[0].destroy()
            self.name_input.insert(0, self.full_name)
            self.make_temp_person_id()
            self.make_sort_order_to_store()
            self.ok_new_person()

        def cancel_new_name():
            msg[0].destroy()
            self.reset()
            self.name_input.focus_set()
 
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_person_ids)
        all_people = cur.fetchall()
        cur.close()
        conn.close()
        
        all_people = [[i[0]] for i in all_people]

        names_only = []

        for iD in all_people:
            display_name = get_name_with_id(iD[0]) 
            names_only.append(display_name)
            iD.insert(0, display_name)

        people_vals = []
        for lst in all_people:
            if not lst[0]:
                lst[0] = ''
            people_vals.append(' #'.join([lst[0], str(lst[1])]))
        if self.full_name not in names_only:
            self.make_temp_person_id()
            self.make_sort_order_to_store()
            self.ok_new_person()
        else:
            msg = open_yes_no_message(
                self, 
                names_msg[0], 
                "Duplicate Name in Tree", 
                "OK", "CANCEL")
            msg[0].grab_set()
            msg[2].config(command=ok_new_name)
            msg[3].config(command=cancel_new_name)
            if self.make_dupe is True:  
                self.make_temp_person_id() 
                self.reset()
            else:
                self.reset() 

    def reset(self):
        self.preset()
        self.name_input.delete(0, 'end')
        for child in self.order_frm.winfo_children():
            child['text'] = ''
        self.make_dupe = True 

if __name__ == "__main__":

    def open_dialog():
        person_add = PersonAdd(root, person_input, root) 
    
    root = tk.Tk()

    person_input = Entry(root, width=40)
    person_input.grid()
    person_input.focus_set()

    addbutt = Button(
        root, 
        text="ADD NEW PERSON", 
        command=open_dialog)
    addbutt.grid()

    root.mainloop()






