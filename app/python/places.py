# places.py
'''
Validation and input to database has been tested for these cases:
    ALL KNOWN PLACES, NO DUPES: dialog doesn't open;
    ALL KNOWN, SOME OUTER DUPES
    ALL KNOWN, SOME INNER DUPES
    ALL KNOWN, SOME INNER & SOME OUTER DUPES
    SOME NEW & SOME KNOWN, NO DUPES
    SOME NEW & SOME KNOWN, SOME OUTER DUPES
    SOME NEW & SOME KNOWN, SOME INNER DUPES
    SOME NEW & SOME KNOWN, SOME INNER & SOME OUTER DUPES
    ALL NEW, NO DUPES
    ALL NEW, SOME OUTER DUPES
    ALL NEW, SOME INNER DUPES
    ALL NEW, SOME INNER & SOME OUTER DUPES
    insert final parent (end of nesting)
    insert first child (start of nesting)
    insert intermediate child (mid-nesting)
'''                    

import tkinter as tk
import sqlite3
from widgets import (
    Toplevel, Frame, Button, Label, RadiobuttonBig, LabelHeader, 
    Entry, ButtonQuiet, configall, Border, Scrollbar, open_message,
    EntryAuto, Separator, make_formats_dict)
from right_click_menu import RightClickMenu, make_rc_menus
from toykinter_widgets import run_statusbar_tooltips
from scrolling import resize_scrolled_content
from files import get_current_file
from messages_context_help import (
    places_dialog_label_help_msg, places_dlg_help_msg, 
    places_dialog_radio_help_msg, places_dialog_hint_help_msg)
from nested_place_strings import make_all_nestings, ManyManyRecursiveQuery
from messages import places_err
from query_strings import (
    select_place_id_hint, insert_place_new, update_finding_places_null,     
    select_place_hint, select_all_places, select_all_places_places, 
    update_place_hint, select_place_id2, 
    select_max_place_id, select_place_id1, update_finding_places,
    insert_places_places_new, select_all_place_ids, 
    select_places_places_id, select_all_finding_places_findings)
import dev_tools as dt
from dev_tools import looky, seeline





def get_all_places_places():
    
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_places_places)
    places_places = cur.fetchall()
    cur.close()
    conn.close()
    return places_places

def get_all_unique_place_names():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_places)
    all_place_names = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()

    unique_place_names = set(all_place_names)

    return unique_place_names

class NewPlaceDialog():
    def __init__(
            self,
            master, 
            place_dicts,
            message, 
            title,
            button_labels,
            inwidg,
            initial,
            place_input,
            treebard,
            do_on_ok=None,
            selection=None):

        self.master = master # root
        self.place_dicts = place_dicts
        self.message = message
        self.title = title
        self.button_labels = button_labels
        self.inwidg = inwidg
        self.initial = initial
        self.place_input = place_input
        self.treebard = treebard
        self.do_on_ok = do_on_ok

        self.formats = make_formats_dict()

        self.got_row = 0
        self.got_nest = None
        self.edit_hint_id = 0
        self.hint_to_edit = None
        self.edit_rows = {}
        self.rc_menu = RightClickMenu(self.master, treebard=self.treebard)
        self.make_widgets()
        self.add_new_place_option = False
        self.error = False

    def make_widgets(self):

        def show_message():

            window.columnconfigure(1, weight=1)
            window.rowconfigure(1, weight=1)
            lab = LabelHeader(
                window, text=self.message, justify='left', wraplength=600)
            lab.grid(column=1, row=1, sticky='news', ipady=6, ipadx=6)

        def ok():
            print("line", looky(seeline()).lineno, "self.do_on_ok:", self.do_on_ok)
            print("line", looky(seeline()).lineno, "self.error:", self.error)
            print("line", looky(seeline()).lineno, "self.place_input:", self.place_input)
            if self.do_on_ok:
                self.do_on_ok()
            if self.error is False:
                self.new_places_dialog.destroy()
                self.inwidg.delete(0, 'end')
                self.inwidg.insert(0, self.place_input)

        def cancel():
            self.new_places_dialog.destroy()
            self.inwidg.delete(0, 'end')
            self.inwidg.insert(0, self.initial)
        size = (
            self.master.winfo_screenwidth(), self.master.winfo_screenheight())
        self.new_places_dialog = Toplevel(self.master)
        self.new_places_dialog.geometry("+120+24")
        self.new_places_dialog.maxsize(
            width=int(size[0] * 0.85), height=int(size[1] * 0.95))
        self.new_places_dialog.columnconfigure(1, weight=1)
        self.new_places_dialog.rowconfigure(4, weight=1)
        self.canvas = Border(self.new_places_dialog, self.master)            
        self.canvas.title_1.config(text=self.title)
        self.canvas.title_2.config(text="input: {}".format(self.place_input))

        window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.treebard.scroll_mouse.append_to_list([self.canvas, window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        window.vsb = Scrollbar(
            self.new_places_dialog, 
            hideable=True, 
            command=self.canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            self.new_places_dialog, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        buttonbox = Frame(window)
        b1 = Button(buttonbox, text=self.button_labels[0], width=7, command=ok)
        b2 = Button(buttonbox, text=self.button_labels[1], width=7, command=cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        window.columnconfigure(2, weight=1)
        window.rowconfigure(1, minsize=60)
        buttonbox.grid(column=1, row=3, sticky='se', pady=6)

        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.frm = Frame(window)
        self.frm.grid(column=1, row=2, sticky='news', pady=12)
        show_message()
        self.lay_out_radios()
        configall(self.new_places_dialog, self.formats)
        resize_scrolled_content(self.new_places_dialog, self.canvas, window)

        self.new_places_dialog.focus_set()

    def ok_hint(self):
        current_file = get_current_file()[0]
        edit_row = self.edit_rows[self.got_nest]
        new_hint = edit_row.ent.get()
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_place_hint, ((new_hint, self.edit_hint_id)))
        conn.commit()
        cur.close()
        conn.close()        
        self.hint_to_edit.config(text="hint: {}".format(new_hint))
        edit_row.remove_edit_row()

    def make_edit_row(self, parent, row=None):
        edit_row = EditRow(parent, self.ok_hint)
        self.edit_rows[parent] = edit_row

    def grid_edit_row(self, hint):
        edit_row = self.edit_rows[self.got_nest]
        edit_row.grid(column=0, row=self.got_row, sticky='ew', columnspan=2)
        edit_row.lift()
        for child in self.got_nest.winfo_children():
            if child.grid_info()['column'] == 0:
                if child.grid_info()['row'] == self.got_row - 1:
                    self.edit_hint_id = int(child.cget('text').split(': ')[0])
            elif child.grid_info()['column'] == 1:
                if child.grid_info()['row'] == self.got_row:
                    if child.winfo_class() == 'Label':
                        self.hint_to_edit = child
        edit_row.ent.delete(0, 'end')
        edit_row.ent.insert(0, hint)
        edit_row.ent.focus_set()

    def get_clicked_row(self, evt):
        self.got_row = evt.widget.grid_info()['row'] 
        self.got_nest = evt.widget.master

    def on_hover(self, evt):
        evt.widget.config(text='Edit') 

    def on_unhover(self, evt):
        evt.widget.config(text='')

    def lay_out_radios(self):
        '''
            Make a new place dialog the same way for every place, then for
            certain qualifying (unambiguous) cases, don't open the dialog.
        '''
        self.radvars = []
        i = 0
        for dd in self.place_dicts:
            self.var = tk.IntVar()
            self.radvars.append(self.var)
            i += 1

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
            
        cur.close()
        conn.close()

        self.bullet = len(self.place_dicts) - 1
        self.rowdx = 0
        self.vardx = 0
        for dkt in self.place_dicts:
            self.make_radiobuttons(dkt)

    def make_radiobuttons(self, dkt):
        if len(dkt["id"]) > 0:
            nest_ids =  dkt["id"]
        else:
            nest_ids = dkt["temp_id"]
        place_string = '{}: {}, place ID #{}'.format(
            self.bullet, dkt["input"], nest_ids)

        lab = Label(self.frm, text=place_string)
        lab.grid(column=0, row=self.rowdx, sticky='w')
        self.rc_menu.loop_made[lab] = places_dialog_label_help_msg
            
        self.nest_level = Frame(self.frm)
        self.nest_level.grid(column=0, row=self.rowdx+1, sticky='w', padx=(0,3), columnspan=2)
        self.nest_level.columnconfigure(0, minsize=48)

        self.make_edit_row(self.nest_level)
        self.radx = 0
        row = 0
        for hint in dkt["hint"]:
            if len(dkt["id"]) > 0:
                new_id = dkt["temp_id"]
                last_idx = len(dkt["id"])
                if self.radx == last_idx:
                    self.current_id = new_id
                    self.select_first_radio()
                    rad_string = "{}: {} (new place and new place ID)".format(
                        self.current_id, dkt["input"])
                else:
                    self.current_id = dkt["id"][self.radx]
                    self.select_first_radio()
                    nesting = ManyManyRecursiveQuery(
                        initial_id=self.current_id).radio_text
                    rad_string = "{}: {}".format(self.current_id, nesting)
            elif len(dkt["id"]) == 0:
                self.current_id = dkt["temp_id"]
                self.select_first_radio()
                rad_string = "{}: {} (new place and new place ID)".format(
                    self.current_id, dkt["input"])
            else:
                print("line", looky(seeline()).lineno, "case not handled")

            rad = RadiobuttonBig(
                self.nest_level, 
                variable=self.radvars[self.vardx],
                value=self.current_id,
                text=rad_string, 
                anchor="w")
            self.rc_menu.loop_made[rad] = places_dialog_radio_help_msg

            lab2 = Label(
                self.nest_level, 
                text="hint: {}".format(hint),
                anchor='w', bg='red')

            editx = ButtonQuiet(
                self.nest_level, 
                width=2, 
                command=lambda hint=hint: self.grid_edit_row(hint))
            self.rc_menu.loop_made[editx] = places_dialog_hint_help_msg

            self.nest_level.columnconfigure(1, weight=1)
            rad.grid(column=0, row=row, sticky='we', columnspan=2)
            lab2.grid(column=1, row=row+1, sticky='w', padx=6)
            editx.grid(column=0, row=row+1, pady=(0,3), sticky='e')

            editx.bind('<Enter>', self.on_hover)
            editx.bind('<Leave>', self.on_unhover)
            editx.bind('<Button-1>', self.get_clicked_row)
            editx.bind('<space>', self.get_clicked_row)
            editx.bind('<FocusIn>', self.on_hover)
            editx.bind('<FocusOut>', self.on_unhover)
            self.radx += 1

            visited = (
                (lab,
                    "",
                    "Name and ID of place."),
                (rad,
                    "Place Select",
                    "Select this option if it is correct."),
                (editx,
                    "Hint Edit Button",
                    "Optionally create/edit place hints (for duplicate "
                        "place names or ?)."))
            run_statusbar_tooltips(
                visited, 
                self.canvas.statusbar.status_label, 
                self.canvas.statusbar.tooltip_label) 

            rcm_widgets = ()
            make_rc_menus(
                rcm_widgets, 
                self.rc_menu,
                places_dlg_help_msg)

            row += 2

        sep = Separator(self.frm, width=3)
        sep.grid(column=0, row=self.rowdx+2, sticky='ew', 
            columnspan=3, pady=(3,0))
        self.rowdx += 3
        self.vardx += 1
        self.bullet -= 1

    def select_first_radio(self):
        if self.radx == 0:
            self.radvars[self.vardx].set(self.current_id)

class EditRow(Frame):
    def __init__(self, master, command, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.ent = Entry(self, width=36)
        spacer = Label(self, width=3)

        ok_butt = Button(
            self,
            text='OK',
            command=command)

        cancel_butt = Button(
            self,
            text='CANCEL',
            command=self.remove_edit_row)
        
        spacer.grid(column=0, row=0)
        self.ent.grid(column=1, row=0, padx=3, pady=3)
        ok_butt.grid(column=2, row=0, padx=6, pady=6)
        cancel_butt.grid(column=3, row=0, padx=6, pady=6)

    def remove_edit_row(self):
        self.grid_forget()

class ValidatePlace():

    def __init__(
            self, root, treebard, inwidg, initial, 
            place_input, finding): 
        self.root = root
        self.treebard = treebard
        self.inwidg = inwidg
        self.initial = initial
        self.place_input = place_input
        self.finding = finding

        self.place_list = []
        self.place_dicts = []
        self.new = False
        self.dupes = False

        self.new_place_dialog = None

        self.see_whats_needed()

    def see_whats_needed(self):

        def get_matching_ids_hints(nest):
            cur.execute(select_place_id_hint, (nest,))
            ids_hints = cur.fetchall()
            if len(ids_hints) == 0: self.new = True
            elif len(ids_hints) > 1: self.dupes = True
            return ids_hints

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        if len(self.place_input) == 0:
            cur.execute(update_finding_places_null, (self.finding,))
            conn.commit()
            return

        self.place_list = self.place_input.split(",")
        self.place_list = [self.place_list[i].strip() for i in range(len(self.place_list))]
        self.length = len(self.place_list)

        for nest in self.place_list:
            ids_hints = [list(i) for i in get_matching_ids_hints(nest)]
            ids = []
            hints = []
            for tup in ids_hints:
                ids.append(tup[0])
                hints.append(tup[1])        
            hints.append("")
            self.place_dicts.append({
                "id" : ids,
                "input" : nest,
                "hint" : hints})

        cur.close()
        conn.close()

        self.make_new_places()
        if self.new is True or self.dupes is True:
            self.new_place_dialog = NewPlaceDialog(
                self.root,
                self.place_dicts,
                "Clarify place selections where there is not exactly one ID "
                "number. Press the EDIT button to add or edit hints for "
                "duplicate place names or any place name. When entering "
                "new place names, ID numbers have been assigned which you can "
                "just OK. If the right options are not listed, press CANCEL "
                "and use the Places Tab to create or edit the place.", 
                "New and Duplicate Places Dialog",
                ("OK", "CANCEL"),
                self.inwidg,
                self.initial,
                self.place_input,
                self.treebard,
                do_on_ok=self.collect_place_ids)
        else:
            for dkt in self.place_dicts:
                dkt["id"] = dkt["id"][0]
            self.input_to_db()

    def make_new_places(self):
        '''
            A temp_id is assigned to each nest in case the user needs to make
            a new place by the name input, even if some place(s) by that name
            already exist in the database.

            The temp_ids all have to be assigned at the same time so that each
            number is unique, then entry to the database has to be done all
            at the same time while this information is still correct. After
            the max ID is obtained from the database, no db transactions can
            occur which insert to any of the place tables till these temp IDs
            are either used or discarded.
        '''
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_max_place_id)
        temp_id = cur.fetchone()[0] + 1
        for dkt in self.place_dicts:
            dkt["temp_id"] = temp_id
            temp_id += 1
        cur.close()
        conn.close()

    def collect_place_ids(self):

        def reset_error(evt):
            self.new_place_dialog.error = False

        r = 0
        for dkt in self.place_dicts:
            dkt["id"] = self.new_place_dialog.radvars[r].get()
            r += 1

        seen = set()
        for dkt in self.place_dicts:
            val = dkt['id']
            if val in seen:
                msg = open_message(
                    self.root, 
                    places_err[0], 
                    "Duplicate Place IDs", 
                    "OK")
                msg[1].config(aspect=400)
                msg[0].bind("<Destroy>", reset_error)
                self.new_place_dialog.error = True
                return
            seen.add(val)
        print("line", looky(seeline()).lineno, "RUNNING:")
        self.input_to_db()

    def input_new_finding(self):
        """ DON'T DELETE: This appeared 20220615 but I have no clue where it
        came from or what it's supposed to do or how or why. The ability to add
        a new place to a finding no longer exists.
        """
        print("line", looky(seeline()).lineno, "self.place_dicts:", self.place_dicts)
        return self.place_dicts

    def input_to_db(self):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
# FIRST CLUE: "...finding_places..."
        cur.execute(select_all_finding_places_findings) # HERE'S THE PROBLEM
        all_finding_ids = [i[0] for i in cur.fetchall()]
        print("line", looky(seeline()).lineno, "self.finding:", self.finding)
        print("line", looky(seeline()).lineno, "all_finding_ids:", all_finding_ids)
        if self.finding not in all_finding_ids:
            # If it's a new finding, there's no finding_id yet, all the
            #   database input is handled in the new findings procedure.
            self.input_new_finding()
            return

        ids = []
        for dkt in self.place_dicts:            
            ids.append(dkt["id"])
        qty = len(self.place_dicts)
        nulls = 9 - qty
        ids = ids + [None] * nulls
        ids.append(self.finding)

        places_places = get_all_places_places()
        print("line", looky(seeline()).lineno, "places_places:", places_places)
        last = len(self.place_dicts) - 1
        print("line", looky(seeline()).lineno, "self.place_dicts:", self.place_dicts)
        q = 0
        for dkt in self.place_dicts:
            child = dkt["id"]
            if q < last:
                parent = self.place_dicts[q+1]["id"]
            else:
                parent = None
            if child == dkt["temp_id"]:
                print("line", looky(seeline()).lineno, "RUNNING:", RUNNING)
                cur.execute(insert_place_new, (child, dkt["input"]))
                conn.commit()
                cur.execute(insert_places_places_new, (child, parent))
                conn.commit()
            else:
                if (child, parent) not in places_places:
                    places_places.append((child, parent))
                    cur.execute(insert_places_places_new, (child, parent))
                    conn.commit()
            q += 1

        place_strings = make_all_nestings(select_all_place_ids)

        cur.execute(update_finding_places, tuple(ids))
        conn.commit()   
        place_strings.insert(0, self.place_input)
            
        cur.close()
        conn.close()

if __name__ == "__main__":
    
    from widgets import make_formats_dict

    trials = {
        'a' : "114 Main Street, Paris, Precinct 5, Lamar County, Texas, USA",
        'b' : "114 Main Street, Paris, Bear Lake County, Idaho, USA",
        'c' : "Paris, Tennessee, USA",
        'd' : "Paris, Texas, USA",
        'e' : "Paris",
        'f' : "Maine, Maine, USA",
        'g' : "Glenwood Springs, Garfield County, Colorado, USA",
        'h' : "Paris, France",
        'i' : "Glenwood Springs, USA",
        'j' : "Paris, USA",
        'k' : "Paris",
        'l' : "Seadrift, Calhoun County, Texas, USA",
        'm' : "Hawaii, USA",
        'n' : "Jakarta, Java, Indonesia",
        'o' : "Old Town, Sacramento, California, New Spain, USA",
        'p' : "Blossom, Lamar County, Texas, USA",
        'q' : "Blossom, Precinct 1, Lamar County, Texas, USA",
        'r' : "Maine, Aroostook County, Maine, USA",
        's' : "Maine, Iowa, USA",
        't' : "Sassari, Sassari, Sardegna, Italy",
        'u' : "Elks Lodge, Paris, Precinct 5, Lamar County, Texas, USA",
        'v' : "Elks Lodge, Paris, Bear Lake County, Idaho, USA",
        'w' : "Elks Lodge, Sacramento, Sacramento County, California, USA",
        'x' : "Elks Lodge, Blossom, Lamar County, Texas, USA",
        'y' : "Jerusalem, Israel",
        'z' : "Masada, Israel",
        'aaa' : "Israel",
        'bbb' : "USA",
        'ccc' : "Dupes, Dupes, Dupes",
        'ddd' : "table 5, Elks Lodge, Paris, Precinct 5, Lamar County, Texas, USA",
        'eee' : "table 5, Elks Lodge, Paris, Bear Lake County, Idaho, USA",
        'fff' : "table 5, Elks Lodge, Paris, Precinct 5, Lamar County, Texas, USA",
        'ggg' : "Elks Lodge, Gee Whiz Mall, Maine, Arizona, USA",
        'hhh' : "Paris, Precinct 5, Lamar County, Texas, USA",
        'iii' : "Precinct 5, Lamar County, Texas, USA",
        'jjj' : "Dupe, Dupe, Dupe",
        'kkk' : "Transylvania",
        'lll' : "Blossom, Elma, Erie County, New York, USA",
        'mmm' : "Calhoun County, Texas, USA",
    }

    finding = 1
    initial = ''

    def get_final(evt):
        widg = evt.widget
        update_db(widg) # will need (widg, col_num) in real one

    def update_db(widg):
        final = widg.get()
        for child in frame.winfo_children():
            child.destroy()
        final = ValidatePlace(root, treebard, initial, final, finding)
        j = 0
        for dkt in final.place_dicts:
            lab = Label(
                frame,
                text='{} id#{}'.format(
                    final.place_list[j], final.place_list[j]))
            lab.grid()
            j += 1

    root = tk.Tk()
    treebard = root # mockup; this isn't what really happens

    place_values = EntryAuto.create_lists(place_strings)

    entry = EntryAuto(root, width=50, autofill=True, values=place_values)
    entry.grid()
    entry.focus_set()
    entry.bind("<FocusOut>", get_final, add="+")

    traverse = Entry(root)
    traverse.grid()
    frame = Frame(root)
    frame.grid()
    
    root.mainloop()






 


