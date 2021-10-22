# names

import tkinter as tk
import sqlite3
from files import get_current_file, current_file
from styles import config_generic
from widgets import (
    Frame, Label, Button, LabelMovable, LabelH3, Entry, Toplevel)
from window_border import Border
from custom_combobox_widget import Combobox  
from scrolling import MousewheelScrolling, Scrollbar, resize_scrolled_content 
from autofill import EntryAuto
from toykinter_widgets import StatusbarTooltips, run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from message_strings import person_add_msg
from messages import open_yes_no_message, names_msg, open_error_message
from images import get_all_pics    
from query_strings import (
    select_current_person, select_name_with_id, select_all_names_ids,
    select_all_person_ids, select_image_id, select_max_person_id,    
    insert_images_entities, select_name_type_id, insert_name, 
    select_all_images, select_all_name_types, insert_person_new,
    select_person_gender, select_max_name_type_id, insert_name_type_new,
    insert_image_new)
import dev_tools as dt
from dev_tools import looky, seeline





GENDER_TYPES = ('unknown', 'female', 'male', 'other')

NAME_SUFFIXES = (
    'jr.', 'sr.', 'jr', 'sr', 'junior', 'senior', 
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 
    'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv')

def get_current_person():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person)
    current_person = cur.fetchone()
    current_person_id = current_person[0]
    current_person = current_person[1]
    return current_person_id, current_person

def get_name_types():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_name_types)
    name_types = cur.fetchall()
    cur.close()
    conn.close()
    name_types = [i[0] for i in name_types]

    return name_types

def get_name_with_id(iD):
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
    name = get_name_with_id(iD)
    if len(name) == 0:
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_name_with_id_any, (iD,))
        all_names_types = cur.fetchall()
        print("line", looky(seeline()).lineno, "all_names_types:", all_names_types)


        cur.close()
        conn.close()
        

    

def make_values_list_for_person_select():
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

# class PersonAdd(Frame):
    # '''
        # The parameter `name_entry` used to be `autofill` so watch out for this
        # till the refactoring is complete.
    # '''
    # def __init__(self, master, name_entry, root, treebard, *args, **kwargs):
        # Frame.__init__(self, master, *args, **kwargs)

        # self.master = master
        # self.name_entry = name_entry
        # self.root = root
        # self.treebard = treebard

        # self.config(padx=24, pady=24)

        # self.gender = 'unknown'

        # self.new_person_id = None

        # self.role_person_edited = False
        # self.findings_roles_id = None
        # self.make_dupe = False

        # self.rc_menu = RightClickMenu(self.root)
        # self.make_widgets()
        # if self.master.winfo_class() == "Toplevel":
            # self.master.withdraw()

    # def make_widgets(self):

        # def go_beyond(evt):
            # for child in self.order_frm.winfo_children():
                # child.config(takefocus=0)

        # all_pics = self.get_all_pics()

        # lab1 = Label(self, text='Gender:')
        # self.gender_input = ClearableReadonlyCombobox(self, values=GENDER_TYPES)

        # lab2 = Label(self, text='Main Image:')
        # self.image_input = ClickAnywhereCombo(self, values=all_pics)

        # lab3 = Label(self, text='Name Type:')
        # self.name_type_input = ClearableReadonlyCombobox(self, values=self.get_name_types())

        # lab4 = Label(self, text='Full Name:')
        # self.name_input = Entry(self, width=65)
        # self.name_input.bind("<FocusOut>", self.show_sort_order)

        # self.how = LabelH3(
            # self, 
            # text='Alphabetize name: after clicking auto-sort, tab into '
                  # 'auto-filled name fields to modify\nsort order with '
                  # 'arrow keys or if sort order is correct, just click ADD.')

        # autosort = Button(self, text='AUTOSORT')
        # autosort.bind("<Control-Tab>", go_beyond)

        # self.order_frm = Frame(self)

        # s = 0
        # for stg in range(20):
            # mov = LabelMovable(self.order_frm)
            # mov.grid(column=s, row=0, padx=3)
            # s += 1 

        # self.buttonbox = Frame(self)
        # self.add_butt = Button(
            # self.buttonbox, 
            # text='ADD', 
            # width=6, 
            # command=self.ok_new_person)
        # self.cancel_butt = Button(
            # self.buttonbox, 
            # text='CANCEL', 
            # width=6, 
            # command=self.cancel_new_person)

        # lab1.grid(column=0, row=3)
        # self.gender_input.grid(
            # column=1, row=3, padx=12, pady=12, sticky='e')
        # lab2.grid(column=2, row=3)
        # self.image_input.grid(column=3, row=3, padx=12, pady=12)
        # lab3.grid(column=0, row=4)
        # self.name_type_input.grid(
            # column=1, row=4,  padx=12, pady=12, sticky='e')
        # lab4.grid(column=2, row=4)
        # self.name_input.grid(column=3, row=4, padx=12, pady=12)

        # self.how.grid(column=0, row=5, padx=6, pady=6, columnspan=4)
        # autosort.grid(column=0, row=6, padx=6, pady=6)
        # self.order_frm.grid(column=1, row=6, columnspan=4, pady=24)
        # self.buttonbox.grid(column=3, row=7, sticky='e', pady=(12,0))
        # self.add_butt.grid(column=0, row=0, padx=(0,12))
        # self.cancel_butt.grid(column=1, row=0)

        # self.new_person_statusbar = StatusbarTooltips(
            # self.master, resizer=False)
        # visited = (
            # (self.gender_input, 
                # "Gender Input", 
                # "'Unknown' used if left blank."),
            # (self.image_input, 
                # "Image Input", 
                # "Use an old photo of person's home town if no photo available."),
            # (self.name_type_input, 
                # "Name Type Input", 
                # "Choose the name type."),
            # (self.name_input, 
                # "Name Input", 
                # "Autofills but you can change it."),
            # (autosort, 
                # "Autosort Button", 
                # "Click to auto-create a sortable name."),
            # (self.order_frm, 
                # "", 
                # "Tab to focus name element. Arrow to change order.")
# )        
        # run_statusbar_tooltips(
            # visited, 
            # self.new_person_statusbar.status_label, 
            # self.new_person_statusbar.tooltip_label)

        # self.preset()

        # rcm_widgets = (self.name_input, self.name_type_input)
        # make_rc_menus(
            # rcm_widgets, 
            # self.rc_menu, 
            # person_add_msg)

    # def ok_new_person(self):
        # self.save_new_name()
        # self.cancel_new_person()

    # def cancel_new_person(self):
        # if self.master.winfo_class() == "Toplevel":
            # self.master.destroy()

    # def preset(self):

        # self.gender_input.config(state='normal')
        # self.gender_input.delete(0, 'end')
        # self.gender_input.config(state='readonly')
        # self.image_input.delete(0, 'end')
        # self.image_input.insert(0, 'no_photo_001.gif')
        # self.name_type_input.config(state='normal')
        # self.name_type_input.delete(0, 'end')
        # self.name_type_input.insert(0, 'birth name')
        # self.name_type_input.config(state='readonly')

    # def reset(self):
        # self.preset()
        # self.name_input.delete(0, 'end')
        # for child in self.order_frm.winfo_children():
            # child['text'] = ''
        # self.make_dupe = True  

    # def prepare_to_add_person(self, findings_roles_id=None):
        # self.get_entered_values()
        # self.findings_roles_id = findings_roles_id
        # self.check_for_dupes()

    # def get_entered_values(self):
        # if len(self.gender_input.get()) != 0:
            # self.gender = self.gender_input.get()
        # self.full_name = self.name_input.get()
        # self.selected_image = self.image_input.get()
        # self.name_type = self.name_type_input.get()

    # def check_for_dupes(self):
        # ''' 
            # If birth name already exists in database, open dialog. 
        # '''

        # def ok_new_name():
            # self.make_dupe = True
            # msg[0].destroy()
            # self.master.grab_set()
            # self.name_input.insert(0, self.full_name)
            # self.make_temp_person_id()
            # self.make_sort_order_to_store()
            # self.show_sort_order()

        # def cancel_new_name():
            # msg[0].destroy()
            # if self.master.winfo_class() == "Toplevel":
                # self.master.destroy()
                # self.master.master.grab_set()
            # self.reset()
 
        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_all_person_ids)
        # all_people = cur.fetchall()
        # cur.close()
        # conn.close()
        
        # all_people = [[i[0]] for i in all_people]

        # names_only = []

        # for id in all_people:
            # display_name = get_name_with_id(id[0]) 
            # names_only.append(display_name)
            # id.insert(0, display_name)

        # people_vals = []
        # for lst in all_people:
            # if not lst[0]:
                # lst[0] = ''
            # people_vals.append(' #'.join([lst[0], str(lst[1])]))
        # if self.full_name not in names_only:
            # self.make_temp_person_id()
            # self.make_sort_order_to_store()
            # self.master.grab_set()
        # else:
            # msg = open_yes_no_message(
                # self, 
                # names_msg[0], 
                # "Duplicate Name in Tree", 
                # "OK", "CANCEL")
            # msg[0].grab_set()
            # msg[1].config(aspect=400)
            # msg[2].config(command=ok_new_name)
            # msg[3].config(command=cancel_new_name)
            # if self.make_dupe is True:  
                # self.make_temp_person_id() 
                # self.make_sort_order_to_store()
                # self.reset()
            # else:
                # self.reset() 

    # def make_temp_person_id(self): 
        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_max_person_id)
        # self.new_person_id = cur.fetchone()[0] + 1

        # if self.role_person_edited is True:
            # cur.execute(
                # update_findings_roles_person, 
                # (self.new_person_id, self.findings_roles_id))
            # conn.commit()
            # self.role_person_edited = False 
        
        # cur.close()
        # conn.close()

    # def make_sort_order_to_store(self): 

        # self.order = []

        # for child in self.order_frm.winfo_children():
            # text = child['text']
            # self.order.append(text)

        # self.order = ' '.join(self.order)
        # self.order = self.order.replace(' , ', ', ')
        # self.order = self.order.strip(', ') 

    # def save_new_name(self):
        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # conn.execute('PRAGMA foreign_keys = 1')
        # cur.execute(select_image_id, (self.selected_image,))
        # img_id = cur.fetchone()[0]
        # cur.execute(select_name_type_id, (self.name_type,))
        # name_type_id = cur.fetchone()
        # name_type_id = name_type_id[0]

        # cur.execute(insert_person_new, (self.new_person_id, self.gender))
        # conn.commit()
        # cur.execute(
            # insert_name, 
            # (self.new_person_id, self.full_name, name_type_id, self.order))
        # conn.commit()

        # cur.execute(insert_images_entities, (img_id, self.new_person_id))
        # conn.commit()

        # new_name_string = "{}  #{}".format(self.full_name, self.new_person_id)
        # self.name_entry.delete(0, 'end')
        # self.name_entry.insert(0, new_name_string)
        # people = make_values_list_for_person_select()        
        # all_birth_names = EntryAuto.create_lists(people)
        # self.name_entry.values = all_birth_names
        
        # cur.close()
        # conn.close()

        # self.image_input.delete(0, 'end')
        # self.image_input.insert(0, 'no_photo_001.gif')

        # for widg in (self.name_type_input, self.name_input):
            # widg.config(state='normal')
            # widg.delete(0, 'end')
        # self.name_type_input.config(state='readonly')

        # for child in self.order_frm.winfo_children():
            # child.config(text='')
        # self.gender_input.config(state='normal')
        # self.gender_input.delete(0, 'end')
        # self.gender_input.config(state='readonly')
        # self.gender_input.focus_set()

    # def show_sort_order(self, evt=None):
        # '''
            # This has to be run in the instance as soon as the name input has a 
            # name inserted into it by the program so that normally the user can 
            # bypass manual sorting by pressing Ctrl+Tab when the AUTOFOCUS 
            # button is in focus. But if the user changes what Treebard inserts 
            # to the name entry, then on focus out this function runs again.
        # '''

        # if evt is not None and evt.type == "10":
            # for child in self.order_frm.winfo_children():
                # child.config(text='')

        # self.got = self.name_input.get()
        # self.new_name = self.got
        # self.got = self.got.split()
        # if len(self.got) == 0:
            # return
        # else:
            # length = len(self.got)-1
        # word = self.got[length].lower()
        
        # self.got.insert(0, ',')
        # length += 1
        # if word not in NAME_SUFFIXES:
            # self.got.insert(0, self.got.pop())
        # elif word in NAME_SUFFIXES and self.got[length].lower() == word:
            # self.got.insert(0, self.got.pop())
            # self.got.insert(0, self.got.pop())

        # for child in self.order_frm.winfo_children():
            # child.config(text='')

        # v = 0
        # for name in self.got:
            # self.order_frm.winfo_children()[v].config(text=name)
            # v += 1

    # def get_name_types(self):

        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_all_name_types)
        # name_types = cur.fetchall()
        # cur.close()
        # conn.close()
        # name_types = [i[0] for i in name_types]

        # return name_types

    # def get_all_pics(self):

        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_all_images)
        # picvals = cur.fetchall()
        # cur.close()
        # conn.close()
        # return picvals

def open_new_person_dialog(master, inwidg, root, inwidg2=None):
    person_add = PersonAdd(master, inwidg, root, inwidg2)
    root.wait_window(person_add)
    new_person_id = person_add.show()
    return new_person_id

class PersonAdd(Toplevel):
    def __init__(
            self, master, inwidg, root, inwidg2, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.inwidg = inwidg
        self.root = root
        self.inwidg2 = inwidg2
       

        self.xfr = self.inwidg.get()
        self.role_person_edited = False
        self.rc_menu = RightClickMenu(self.root)

        self.new_person_id = None
        self.full_name = ""
        self.name_type_id = None

        self.make_dupe = False

        self.make_widgets()

    def make_widgets(self):

        self.geometry('+100+20')

        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, size=3) # don't hard-code size
        self.canvas.title_1.config(text="Add Person Dialog")
        self.canvas.title_2.config(text="")

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        # DO NOT DELETE THESE LINES, UNCOMMENT IN REAL APP
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
        self.b1 = Button(
            buttonbox, text="OK", width=6, command=self.prepare_to_add_person)
        b2 = Button(
            buttonbox, text="CANCEL", width=6, command=self.cancel_new_person)

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

        self.new_person_statusbar = StatusbarTooltips(
            self.master, resizer=False)
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

        config_generic(self)
        resize_scrolled_content(self, self.canvas, self.window)
        self.gender_input.entry.focus_set()

    def show_sort_order(self, evt=None):

        if evt is not None and evt.type == "10":
            for child in self.order_frm.winfo_children():
                child.config(text='')

        self.got = self.name_input.get().split()
        if len(self.got) == 0:
            print("line", looky(seeline()).lineno, "self.got:", self.got)
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
        self.image_input.entry.insert(0, 'no_photo_001.gif')
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
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        self.get_entered_values(cur, conn)
        self.findings_roles_id = findings_roles_id

        cur.execute(select_image_id, (self.selected_image,))
        self.img_id = cur.fetchone()[0]
        cur.execute(select_name_type_id, (self.name_type,))
        name_type_id = cur.fetchone()
        if name_type_id:
            self.name_type_id = name_type_id[0]            
            self.check_for_dupes()
        else:
            self.create_new_name_type(
                self.name_type_input.entry.get(), cur, conn)
        cur.close()
        conn.close()

    def ok_new_person(self):
        self.save_new_name()
        self.cancel_new_person()

    def cancel_new_person(self):
        self.grab_release()
        self.inwidg.focus_set()
        if self.master.winfo_class() == "Toplevel":
            self.master.destroy()
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
            print("line", looky(seeline()).lineno, "selected_image:", selected_image)
            cur.execute(insert_image_new, (selected_image,))
            conn.commit()
            self.selected_image = selected_image
    

    def create_new_name_type(self, new_name_type, cur, conn):
        def ok_new_name_type():
            cur.execute(insert_name_type_new, (self.name_type_id, new_name_type))
            conn.commit()
            msg[0].destroy()
            self.lift()
            self.name_type_input.entry.focus_set()

        def cancel_new_name_type():
            go = False
            msg[0].destroy()
            self.lift()
            self.name_type_input.entry.focus_set()

        def show_choice(evt):
            button_text = evt.widget.cget["text"]
            if button_text == "OK":
                go = True
            elif button_text == "CANCEL":
                go = False
            show(go)

        def show():            
            self.wait_window(msg[0])
            if go is True:
                self.check_for_dupes()
        
        msg = open_yes_no_message(
            self, 
            names_msg[1], 
            "Unknown Name Type", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(command=ok_new_name_type)
        msg[3].config(command=cancel_new_name_type)
        msg[2].bind("<Button-1>", show_choice)

        cur.execute(select_max_name_type_id)
        self.name_type_id = cur.fetchone()[0] + 1

    def save_new_name(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        conn.execute('PRAGMA foreign_keys = 1')
        cur.execute(insert_person_new, (self.new_person_id, self.gender))
        conn.commit()
        cur.execute(
            insert_name, 
            (self.new_person_id, self.full_name, self.name_type_id, self.order))
        conn.commit()

        cur.execute(insert_images_entities, (self.img_id, self.new_person_id))
        conn.commit()

        new_name_string = "{}  #{}".format(self.full_name, self.new_person_id)
        
        self.inwidg.delete(0, 'end')
        self.inwidg.insert(0, new_name_string)
        people = make_values_list_for_person_select()        
        all_birth_names = EntryAuto.create_lists(people)
        self.inwidg.values = all_birth_names
        
        cur.close()
        conn.close()

        self.image_input.delete(0, 'end')
        self.image_input.insert(0, 'no_photo_001.gif')

        for widg in (self.name_type_input, self.name_input):
            widg.delete(0, 'end')

        for child in self.order_frm.winfo_children():
            child.config(text='')
        self.gender_input.delete(0, 'end')

    def show(self):
        people = make_values_list_for_person_select()        
        all_birth_names = EntryAuto.create_lists(people)
        self.inwidg.values = all_birth_names
        return self.new_person_id

    def make_temp_person_id(self): 
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
            msg[1].config(aspect=400)
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




