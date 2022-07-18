# places.py

import tkinter as tk
import sqlite3
from widgets import (
    Toplevel, Frame, Button, Label, Radiobutton, LabelHeader, 
    Entry, ButtonQuiet, configall, Border, Scrollbar, open_message,
    EntryAutoPlace, Separator, make_formats_dict)
from right_click_menu import RightClickMenu, make_rc_menus
from toykinter_widgets import run_statusbar_tooltips
from scrolling import resize_scrolled_content
from files import get_current_file, global_db_path
from messages_context_help import (
    places_dialog_label_help_msg, places_dlg_help_msg, 
    places_dialog_radio_help_msg, places_dialog_hint_help_msg)
from messages import places_err
from utes import center_dialog
from query_strings import (
    update_finding_nested_place_unknown, update_nested_place,
    select_all_nested_place_strings, select_all_place_ids, insert_nested_place,
    select_max_place_id, select_place_id_with_name, insert_place_new,     
    select_all_place_names, select_nested_place_inclusion, insert_place_name,
    select_finding_nested_place_id, update_finding_nested_place,
    select_nested_place_ids, delete_place, delete_place_name)
import dev_tools as dt
from dev_tools import looky, seeline






class ValidatePlace():
    """ Duplicate places have to be checked by user dialog. Existing places
        go into a list. New places go straight into database and into a list.
        On OK the new places have already been input so just input the places
        that already exist. On CANCEL delete the new places.
    """

    def __init__(
            self, root, treebard, inwidg, initial, final, finding,
            place_data): 
        self.root = root
        self.treebard = treebard
        self.inwidg = inwidg
        self.initial = initial
        self.final = final
        self.finding = finding
        self.place_data = place_data 

        self.formats = make_formats_dict()

        self.place_list = []

        self.new_nesting = []
        self.cancelled = False
        self.new_places = []

        self.validate_place()

    def make_widgets(self):

        def ok():
            self.duplicate_places_dlg.destroy()
            self.inwidg.delete(0, 'end')
            self.inwidg.insert(0, self.final)

        def cancel():
            self.cancelled = True
            self.duplicate_places_dlg.destroy()
            self.inwidg.delete(0, 'end')
            self.inwidg.insert(0, self.initial)

        self.duplicate_places_dlg.columnconfigure(1, weight=1)
        self.canvas = Border(self.duplicate_places_dlg, self.root)            
        self.canvas.title_1.config(text="Duplicate Place Dialog")
        self.canvas.title_2.config(text="input: {}".format(self.final))
        self.canvas.quitt.bind("<Button-1>", self.delete_temp_ids, add="+")        

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)

        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.window.vsb = Scrollbar(
            self.duplicate_places_dlg, 
            hideable=True, 
            command=self.canvas.yview,
            width=scridth)
        self.window.hsb = Scrollbar(
            self.duplicate_places_dlg, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=self.window.hsb.set, 
            yscrollcommand=self.window.vsb.set)

        lab = LabelHeader(
            self.window, text="Which {}?".format(self.dupe_nest), 
            justify='left', wraplength=600)
        self.radframe = Frame(self.window)

        buttonbox = Frame(self.window)
        b1 = Button(buttonbox, text="OK", width=7, command=ok)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=cancel)
        b1.focus_set()

        # children of self.duplicate_places_dlg
        self.window.vsb.grid(column=2, row=4, sticky='ns')
        self.window.hsb.grid(column=1, row=5, sticky='ew')

        # children of self.window
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        lab.grid(
            column=0, row=0, sticky='news', ipady=6, ipadx=6, 
            columnspan=2, padx=12, pady=12)
        self.radframe.grid(column=0, row=1, sticky="news")
        buttonbox.grid(column=1, row=2, sticky='se', padx=12, pady=12)

        # children of buttonbox
        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        configall(self.duplicate_places_dlg, self.formats)

        self.duplicate_places_dlg.maxsize(
            int(self.duplicate_places_dlg.winfo_screenwidth() * 0.90),
            int(self.duplicate_places_dlg.winfo_screenheight() * 0.90))

    def make_inputs(self, name, cur):

        def show_examples(num, frm):
            cur.execute(select_nested_place_inclusion, tuple([num]*9,))
            inclusions = [list(i) for i in cur.fetchall()]
            copy = inclusions
            for indx, lst in enumerate(copy):
                lst = [i for i in lst if i != "unknown"]
                inclusions[indx] = lst
                lab = Label(frm, text=", ".join(inclusions[indx]), anchor="w")
                lab.grid(column=0, row=indx+1, sticky="ew", padx=(24,0))

        self.dupevar = tk.IntVar()
        radnew = Radiobutton(
            self.radframe,
            text="New place named {}".format(name),
            variable=self.dupevar,
            value=0)
        radnew.grid(column=0, row=0, sticky="w", padx=12, pady=(0,12))
        radnew.select()
        row = 1
        for num in self.dupe_ids:
            frm = Frame(self.radframe)
            rad = Radiobutton(
                frm, 
                text="{} (place ID #{})".format(name, num),
                variable=self.dupevar,
                value=row)
            frm.grid(column=0, row=row, padx=12, pady=(0,12), sticky="ew")
            rad.grid(column=0, row=0, sticky="w")
            show_examples(num, frm)
            row += 1
        resize_scrolled_content(self.canvas.master, self.canvas, self.window)

    def validate_place(self):
        tree = get_current_file()[0]
        conn = sqlite3.connect(tree)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        lenstart = len(self.initial)
        lenfinal = len(self.final)
        if lenstart != 0 and lenfinal == 0:
            cur.execute(update_finding_nested_place_unknown, (self.finding,))
            conn.commit()
            return
        elif lenstart > 0 and lenfinal > 0:
            if self.final != self.initial:
                self.dispatch_tasks(cur, conn)
        elif lenstart == 0 and lenfinal > 0:
            self.dispatch_tasks(cur, conn)

        cur.close()
        conn.close() 

    def dispatch_tasks(self, cur, conn):

        if self.final in EntryAutoPlace.place_autofill_values:
            for dkt in EntryAutoPlace.place_data:
                for k,v in dkt.items():
                    if k == self.final: 
                        autofill_nested_place_id = v["nested_place_id"]
                        cur.execute(select_nested_place_ids, (autofill_nested_place_id,))
                        nesting = cur.fetchone()[0]
                        break
            self.update_place(cur, conn, autofill_nested_place_id=autofill_nested_place_id)
            EntryAutoPlace.place_data = EntryAutoPlace.get_place_values(new_place=True)
            self.prepend_match(self.inwidg)
            return
        new_nesting = []
        self.place_list = self.final.split(",")
        self.place_list = [self.place_list[i].strip() for i in range(
            len(self.place_list))]
        for idx, name in enumerate(self.place_list, 1):
            if name not in EntryAutoPlace.existing_place_names:
                name, place_id = self.make_new_place(name)
                print("line", looky(seeline()).lineno, "name, place_id:", name, place_id)
                new_nesting.append((name, place_id, idx))
            else:
                cur.execute(select_place_id_with_name, (name,))
                place_id = [i[0] for i in cur.fetchall()]
                if len(place_id) > 0:
                    choice = self.open_dupe_place_dlg(name, cur)
                    if choice > 0:
                        place_id = self.dupe_ids[choice-1]
                    else:
                        name, place_id = self.make_new_place(name)
                    new_nesting.append((name, place_id, idx))
 
        self.new_nesting = sorted(new_nesting, key=lambda u: u[2])
        if self.cancelled is False:
            self.update_place(cur, conn) 
        else:
            self.cancelled = True
            self.delete_temp_ids()

        EntryAutoPlace.place_data = EntryAutoPlace.get_place_values(new_place=True)
        self.prepend_match(self.inwidg)

    def prepend_match(self, widg):
        content = widg.get().strip()
        if content in EntryAutoPlace.place_autofill_values:
            idx = EntryAutoPlace.place_autofill_values.index(content)
            x = EntryAutoPlace.place_autofill_values.pop(idx)
            EntryAutoPlace.place_autofill_values.insert(0, x)

    def make_new_place(self, name):
        tree = get_current_file()[0]
        conn = sqlite3.connect(tree)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(insert_place_new)
        conn.commit()
        # cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'place'")
        # temp_id = cur.fetchone()[0] 
        temp_id = cur.lastrowid
        cur.execute(insert_place_name, (name, temp_id))
        conn.commit()
        self.new_places.append(temp_id)
        cur.close()
        conn.close()
        return name, temp_id

    def open_dupe_place_dlg(self, name, cur):
        self.duplicate_places_dlg = Toplevel(self.root)
        self.duplicate_places_dlg.geometry("+120+24")
        self.dupe_nest = name
        cur.execute(select_place_id_with_name, (name,))
        self.dupe_ids = [i[0] for i in cur.fetchall()]
        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)
        self.make_widgets()
        self.make_inputs(name, cur)
        self.root.wait_window(self.duplicate_places_dlg)
        return self.dupevar.get()

    def update_place(self, cur, conn, autofill_nested_place_id=None):
        nested_ids = [i[1] for i in self.new_nesting]
        cur.execute(select_finding_nested_place_id, (self.finding,))
        nested_place_id = cur.fetchone()
        length = len(self.new_nesting)
        self.new_nesting = nested_ids + [1] * (9 - length) + [nested_place_id[0]]
        if autofill_nested_place_id and nested_place_id:
            cur.execute(update_finding_nested_place, (
                autofill_nested_place_id, self.finding))
            conn.commit()
        else: 
            cur.execute(insert_nested_place, tuple(self.new_nesting[0:9]))
            conn.commit()
            new_nesting_id = cur.lastrowid
            if new_nesting_id:
                cur.execute(update_finding_nested_place, (new_nesting_id, self.finding))
                conn.commit()

    def delete_temp_ids(self, evt=None):
        if len(self.new_places) > 0:                
            for num in self.new_places:
                tree = get_current_file()[0]
                conn = sqlite3.connect(tree)
                conn.execute('PRAGMA foreign_keys = 1')
                cur = conn.cursor()
                cur.execute(delete_place_name, (num,))
                conn.commit()
                cur.execute(delete_place, (num,))
                conn.commit()
            cur.close()
            conn.close()
            self.duplicate_places_dlg.destroy()
            self.inwidg.delete(0, 'end')
            self.inwidg.insert(0, self.initial)











 


