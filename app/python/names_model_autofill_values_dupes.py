# name_id|person_id|names|name_type_id|sort_order|used_by
# 1|1|Jeremiah Laurence Grimaldo|1|Grimaldo, Jeremiah Laurence|
# 4|1|8897652|4|8897652|
# 5|1|G-Man|12|G-Man|
# 6|1|Jerry Grimm|8|Grimm, Jerry|
# 1390|1|Gerry Grimaldi|9|Grimaldi, Gerry|
# 1391|1|Geronimo Gramaldo|9|Gramaldo, Geronimo|

import tkinter as tk
import sqlite3
from persons import EntryAutoPerson, EntryAutoPersonHilited, open_new_person_dialog
from widgets import Entry, Button, Frame, Label
from query_strings import select_name_type_hierarchy_by_id, select_all_names_all_details_order_hierarchy
from files import get_current_file
from styles import make_formats_dict, config_generic
from messages import open_message, persons_msg

import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()
treebard = None

# person_autofill_values = {
    # 1: [	
        # {
            # "name": "Jeremiah Laurence Grimaldo",
            # "name type": "birth name",
            # "name id": 11,
            # "sort order": "Grimaldo, Jeremiah Laurence",
            # "used by": "",	
            # "dupe name": False},
        # {
            # "name": "8897652",
            # "name type": "ID number",
            # "name id": 16,
            # "sort order": "8897652",
            # "used by": "Colorado Prison System",	
            # "dupe name": False,}
    # ],
    # 5: [	
        # {
            # "name": "Donald Wiley Webb",
            # "name type": "birth name",
            # "name id": 13,
            # "sort order": "Webb, Donald Wiley",
            # "used by": "",	
            # "dupe name": False,},	
        # {
            # "name": "Donny Boxer",
            # "name type": "nickname",
            # "name id": 166,
            # "sort order": "Boxer, Donny",
            # "used by": "local business associates",	
            # "dupe name": False,}
    # ],
    # 2297: [	
        # {
            # "name": "John Doe",
            # "name type": "birth name",
            # "name id": 233,
            # "sort order": "Smith, John",
            # "used by": "",	
            # "dupe name": False,}
    # ],	
    # 4288: [
        # {
            # "name": "Frank Jones",
            # "name type": "birth name",
            # "name id": 67,
            # "sort order": "Jones, Frank",
            # "used by": "",	
            # "dupe name": False,},
        # {
            # "name": "John Doe",
            # "name type": "also known as",
            # "name id": 45,
            # "sort order": "Doe, John",
            # "used by": "morgue",	
            # "dupe name": False,}
    # ]
# }

PERSON_DATA = ("name", "name type", "name id", "sort order", "used by", "dupe name")

def update_person_autofill_values():
    people = make_all_names_dict_for_person_select()
    new_values = EntryAutoPerson.create_lists(people)
    for ent in EntryAutoPerson.all_person_autofills:
        ent.values = new_values
    return new_values

def make_all_names_dict_for_person_select():
    """ Make a name dict for use in all name autofills.
    """
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    cur.execute(select_all_names_all_details_order_hierarchy)
    results = cur.fetchall()
    person_ids = [i[0] for i in results]
    values = [list(i[1:]) for i in results]
    values = [i + [False] for i in values]
    inner_dict = []
    for tup in values:
        indict = dict(zip(PERSON_DATA, tup))
        inner_dict.append(indict)
    cur.close()
    conn.close() 

    values = list(zip(person_ids, inner_dict))
    new_values = {}
    for tup in values:
        iD, name_dict = tup
        if new_values.get(iD):
            new_values[iD].append(name_dict)
        else:
            new_values[iD] = [name_dict]

    all_names = []
    dupes = []

    for lst in new_values.values():
        for dkt in lst:
            for k,v in dkt.items():
                if k == "name":
                    stg = v
                    if stg in all_names and stg not in dupes:                    
                        dupes.append(stg)
                    else:
                        all_names.append(stg)
    person_autofill_values = new_values

    a = 0
    for k,v in new_values.items():
        b = 0
        for dkt in v:
            c = 0
            for kk,vv in dkt.items():
                if dkt["name"] in dupes:
                    person_autofill_values[k][b]["dupe name"] = True
                c += 1
            b += 1
        a += 1

    return person_autofill_values

person_autofill_values = make_all_names_dict_for_person_select()

def validate_id(iD, entry):
    """ Get a name to fill in when ID is input. Unlike name autofill, the best
        name to fill in is determined by hierarchy column in name_type table so
        names are put into the dict in the right order so the first name
        found will be the most suitable one according to the name types hierarchy.
        E.G. birth name trumps pseudonym and pseudonym trumps nickname.
    """
        
    def err_done(entry, msg):
        entry.delete(0, 'end')
        msg[0].grab_release()
        msg[0].destroy()
        entry.focus_set()

    if iD not in person_autofill_values:
        msg = open_message(
            entry, 
            persons_msg[2], 
            "Unknown Person ID", 
            "OK")
        msg[0].grab_set()
        msg[2].config(
            command=lambda entry=entry, msg=msg: err_done(
                entry, msg))
    else:
        name_from_id = get_name_from_id(iD)
        return name_from_id   

def get_name_from_id(iD):
    name_from_id = None
    for k,v in person_autofill_values.items():
        if iD == k:
            name_from_id = (v[0], k)
            break 
    return name_from_id

def check_name(evt=None, ent=None):
    iD = None
    name_from_id = None
    if evt:
        ent = evt.widget
    elif ent:
        ent = ent
    else:
        return
    filled = ent.get().strip()
    if filled.startswith("#"):
        filled = filled
    elif filled.startswith("+"):
        filled = filled
    else:
        filled = ent.filled_name
    if filled == ent.original or filled is None:
        print("line", looky(seeline()).lineno, "ent.original:", ent.original)
        return
    elif filled.startswith("#"):
        name_from_id = validate_id(int(filled.lstrip("#").strip()), ent)
        if name_from_id is None:
            return 
        else:
            lab.config(text=name_from_id)
            ent.delete(0, 'end')
            return
    elif filled.startswith("+"):
        global person_autofill_values
        new_person_id = open_new_person_dialog(
            root, ent, root, treebard, formats, person_autofill_values=person_autofill_values)
        person_autofill_values = update_person_autofill_values()
        name_from_id = get_name_from_id(new_person_id)
        lab.config(text=name_from_id)
        ent.delete(0, 'end')
        return

    dupes = []
    for hit in ent.hits:
        the_one = hit[0]
        if the_one["dupe name"] is False or the_one["name"] != ent.filled_name:
            continue
        else:
            dupes.append(hit)
    if len(dupes) > 1:
        right_dupe = ent.open_dupe_dialog(dupes)
        lab.config(text=right_dupe)
    elif len(ent.hits) > 0:        
        lab.config(text=ent.hits[0])
        ent.delete(0, 'end')
    else:
        lab.config(text="")
        ent.delete(0, 'end')

def get_original(evt):
    widg=evt.widget
    widg.original = widg.get()    

root = tk.Tk()
root.title("Name Autofill Model March 25, 2022")

head = Label(
    root, 
    text="Top Input validates on focus out. Button input validates on button press.",
    wraplength=300)
head.grid()

lab = Label(root, wraplength=300)
lab.grid()

ent1 = EntryAutoPersonHilited(root, formats, autofill=True, values=person_autofill_values, width=40)
ent1.grid(pady=12, padx=12)
ent1.bind("<FocusOut>", check_name)

ent2 = EntryAutoPersonHilited(root, formats, autofill=True, values=person_autofill_values, width=40)
ent2.grid(pady=12, padx=12)

btn = Button(root, text="OK", command=lambda evt=None, ent=ent2: check_name(evt, ent))
btn.grid(pady=(0, 12), padx=12, sticky="e")

ent1.focus_set()

for ent in (ent1, ent2):
    ent.bind("<FocusIn>", get_original)

config_generic(root)

root.mainloop()











