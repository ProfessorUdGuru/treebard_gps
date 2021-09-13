# names

import tkinter as tk
import sqlite3
from files import get_current_file, current_file
from widgets import (
    Frame, Label, ClearableReadonlyCombobox, ClickAnywhereCombo, Button, 
    LabelMovable, LabelH3, Entry)
from autofill import EntryAuto
from toykinter_widgets import StatusbarTooltips, run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from message_strings import person_add_msg
from messages import open_yes_no_message, names_msg
from query_strings import (
    select_current_person, select_name_with_id, select_all_names_ids,
    select_all_person_ids, insert_person_null, select_image_id, 
    insert_images_entities, select_name_type_id, insert_name, 
    select_all_images, select_all_name_types)
import dev_tools as dt
from dev_tools import looky, seeline





GENDER_TYPES = ('unknown (default if left blank)', 'female', 'male', 'other')

NAME_SUFFIXES = (
    'jr.', 'sr.', 'jr', 'sr', 'junior', 'senior', 
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 
    'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv')

def get_current_person():

    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person)
    current_person = cur.fetchone()
    current_person_id = current_person[0]
    current_person = current_person[1]
    return current_person_id, current_person

def get_name_with_id(id):
    ''' 
        Get birth name of person with passed ID. 
    '''

    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_name_with_id, (id,))
    full_name = cur.fetchone()

    cur.close()
    conn.close()

    if full_name:
        return full_name[0]
    elif not full_name:
        return ''

def make_values_list_for_person_select():

    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_names_ids)

    peeps = cur.fetchall()
    peeps = [list(i) for i in peeps]

    cur.close()
    conn.close()

    combo_peeps = sorted(peeps, key=lambda i: i[2])
    people = []
    for tup in combo_peeps:
        line = '{}  #{}'.format(tup[0], tup[1])
        people.append(line)
    return people

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
    for id in person_ids:
        name = get_name_with_id(id)
        if len(name) != 0:
            name = '{}  #{}'.format(name, id)
            persons.append(name)
    return persons

class PersonAdd(Frame):
    '''
        The parameter `name_entry` used to be `autofill` so watch out for this
        till the refactoring is complete.
    '''
    def __init__(self, parent, name_entry, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.name_entry = name_entry
        self.root = root

        self.config(padx=24, pady=24)

        self.gender = 'unknown'

        self.new_person_id = None

        self.role_person_edited = False
        self.findings_roles_id = None
        self.make_dupe = False

        self.rc_menu = RightClickMenu(self.root)
        self.make_widgets()
        # self.show_sort_order()
        print("line", looky(seeline()).lineno, "self.master:", self.master)
        print("line", looky(seeline()).lineno, "self:", self)
        if self.master.winfo_class() == "Toplevel": # ADDED 20210913 save comment
            self.master.withdraw()

    def make_widgets(self):

        def go_beyond(evt):
            for child in self.order_frm.winfo_children():
                child.config(takefocus=0)

        all_pics = self.get_all_pics()

        lab1 = Label(self, text='Gender:')
        self.gender_input = ClearableReadonlyCombobox(self, values=GENDER_TYPES)

        lab2 = Label(self, text='Main Image:')
        self.image_input = ClickAnywhereCombo(self, values=all_pics)

        lab3 = Label(self, text='Name Type:')
        self.name_type_input = ClearableReadonlyCombobox(self, values=self.get_name_types())

        lab4 = Label(self, text='Full Name:')
        self.name_input = Entry(self, width=65)
        self.name_input.bind("<FocusOut>", self.show_sort_order)

        self.how = LabelH3(
            self, 
            text='Alphabetize name: after clicking auto-sort, tab into '
                  'auto-filled name fields to modify\nsort order with '
                  'arrow keys or if sort order is correct, just click ADD.')

        autosort = Button(
            self, text='AUTOSORT')
            # self, text='AUTOSORT', command=self.show_sort_order)
        autosort.bind("<Control-Tab>", go_beyond)#, add="+"

        self.order_frm = Frame(self)

        s = 0
        for stg in range(20):
            mov = LabelMovable(self.order_frm)
            mov.grid(column=s, row=0, padx=3)
            s += 1 

        self.buttonbox = Frame(self)
        self.add_butt = Button(self.buttonbox, text='ADD', width=8)

        lab1.grid(column=0, row=3)
        self.gender_input.grid(
            column=1, row=3, padx=12, pady=12, sticky='e')
        lab2.grid(column=2, row=3)
        self.image_input.grid(column=3, row=3, padx=12, pady=12)
        lab3.grid(column=0, row=4)
        self.name_type_input.grid(
            column=1, row=4,  padx=12, pady=12, sticky='e')
        lab4.grid(column=2, row=4)
        self.name_input.grid(column=3, row=4, padx=12, pady=12)

        self.how.grid(column=0, row=5, padx=6, pady=6, columnspan=4)
        autosort.grid(column=0, row=6, padx=6, pady=6)
        self.order_frm.grid(column=1, row=6, columnspan=4, pady=24)
        self.buttonbox.grid(column=1, row=7, sticky='e')
        self.add_butt.grid(column=0, row=0, padx=6, pady=6, sticky='e')

        self.new_person_statusbar = StatusbarTooltips(self.parent, resizer=False)
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
            self.new_person_statusbar.status_label, 
            self.new_person_statusbar.tooltip_label)

        self.preset()

        rcm_widgets = (self.name_input, self.name_type_input)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu, 
            person_add_msg)

    def preset(self):

        self.gender_input.config(state='normal')
        self.gender_input.delete(0, 'end')
        self.gender_input.config(state='readonly')
        self.image_input.delete(0, 'end')
        self.image_input.insert(0, 'no_photo_001.gif')
        self.name_type_input.config(state='normal')
        self.name_type_input.delete(0, 'end')
        self.name_type_input.insert(0, 'birth name')
        self.name_type_input.config(state='readonly')

    def reset(self):
        self.preset()
        self.name_input.delete(0, 'end')
        for child in self.order_frm.winfo_children():
            child['text'] = ''
        self.make_dupe = True  

    def add_person(self, findings_roles_id=None):
        self.get_entered_values()
        self.findings_roles_id = findings_roles_id
        self.check_for_dupes()

    def get_entered_values(self):
        if len(self.gender_input.get()) != 0:
            self.gender = self.gender_input.get()
        self.full_name = self.name_input.get()
        print("line", looky(seeline()).lineno, "self.full_name:", self.full_name)
        self.selected_image = self.image_input.get()
        self.name_type = self.name_type_input.get()

    def check_for_dupes(self):
        ''' 
            If birth name already exists in database, open dialog. 
        '''

        def ok_new_name():
            self.make_dupe = True
            msg[0].destroy()
            self.master.deiconify()
            self.master.grab_set() 
            # if self.make_dupe is True:  
            # self.make_new_person() 
            # self.make_sort_order()
            # self.save_new_name(self.new_person_id)  
            # self.reset()
            # else:
                # self.reset()

        def cancel_new_name():
            msg[0].destroy()
            self.master.destroy()
            self.master.master.grab_set()
            self.reset()
 
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_person_ids)
        all_people = cur.fetchall()
        cur.close()
        conn.close()
        
        all_people = [[i[0]] for i in all_people]

        names_only = []

        for id in all_people:
            display_name = get_name_with_id(id[0]) 
            names_only.append(display_name)
            id.insert(0, display_name)

        people_vals = []
        for lst in all_people:
            if not lst[0]:
                lst[0] = ''
            people_vals.append(' #'.join([lst[0], str(lst[1])]))

        if self.full_name not in names_only:
            print("line", looky(seeline()).lineno, "running:")
            self.make_new_person()
            self.make_sort_order()
            self.save_new_name(self.new_person_id)  
            self.reset()
        else:
            msg = open_yes_no_message(
                self, 
                names_msg[0], 
                "Duplicate Name in Tree", 
                "OK", "CANCEL")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(command=ok_new_name)
            msg[3].config(command=cancel_new_name) 
            print("line", looky(seeline()).lineno, "self.make_dupe:", self.make_dupe)
            if self.make_dupe is True:  
                self.make_new_person() 
                self.make_sort_order()
                self.save_new_name(self.new_person_id)  
                self.reset()
            else:
                self.reset() 

    def make_new_person(self): 
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(insert_person_null, (self.gender,))
        conn.commit()
        cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'person' ")
        new_person_id = cur.fetchone()
        if new_person_id:
            self.new_person_id = new_person_id[0]

        if self.role_person_edited is True:
            cur.execute(
                update_findings_roles_person, 
                (self.new_person_id, self.findings_roles_id))
            conn.commit()
            self.role_person_edited = False 
        
        cur.close()
        conn.close()

    def make_sort_order(self): 

        self.order = []

        for child in self.order_frm.winfo_children():
            text = child['text']
            self.order.append(text)

        self.order = ' '.join(self.order)
        self.order = self.order.replace(' , ', ', ')
        self.order = self.order.strip(', ') 

    def save_new_name(self, subject_id):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        conn.execute('PRAGMA foreign_keys = 1')
        cur.execute(select_image_id, (self.selected_image,))
        img_id = cur.fetchone()[0]
        cur.execute(insert_images_entities, (img_id, subject_id))
        conn.commit()
        cur.execute(select_name_type_id, (self.name_type,))
        name_type_id = cur.fetchone()
        name_type_id = name_type_id[0]

        print("line", looky(seeline()).lineno, "self.full_name:", self.full_name)
        cur.execute(
            insert_name, 
            (subject_id, self.full_name, name_type_id, self.order))
        conn.commit()

        # # new_list = make_values_list_for_person_select()
        # # self.name_entry.values = new_list
        people = make_values_list_for_person_select()        
        all_birth_names = EntryAuto.create_lists(people)
        self.name_entry.values = all_birth_names
        
        cur.close()
        conn.close()

        self.image_input.delete(0, 'end')
        self.image_input.insert(0, 'no_photo_001.gif')

        for widg in (self.name_type_input, self.name_input):
            widg.config(state='normal')
            widg.delete(0, 'end')
        self.name_type_input.config(state='readonly')

        for child in self.order_frm.winfo_children():
            child.config(text='')
        self.gender_input.config(state='normal')
        self.gender_input.delete(0, 'end')
        self.gender_input.config(state='readonly')
        self.gender_input.focus_set()

    def show_sort_order(self, evt=None):
        '''
            This has to be run in the instance as soon as the name input has a 
            name inserted into it by the program so that normally the user can 
            bypass manual sorting by pressing Ctrl+Tab when the AUTOFOCUS 
            button is in focus.
            But if the user changes what Treebard inserts to the name entry,
            then on focus out this function runs again.
        '''

        if evt is not None and evt.type == "10":
            for child in self.order_frm.winfo_children():
                child.config(text='')

        self.got = self.name_input.get()
        self.new_name = self.got
        self.got = self.got.split()
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

    def get_name_types(self):

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_name_types)
        name_types = cur.fetchall()
        cur.close()
        conn.close()
        name_types = [i[0] for i in name_types]

        return name_types

    def get_all_pics(self):

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_images)
        picvals = cur.fetchall()
        cur.close()
        conn.close()
        return picvals




