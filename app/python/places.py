# places.py

import tkinter as tk
import sqlite3
from widgets import (
    Toplevel, Frame, Button, Label, Radiobutton, LabelHeader, 
    Entry, ButtonQuiet, configall, Border, Scrollbar, open_message,
    EntryAuto, Separator, make_formats_dict)
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
    select_place_id_hint, insert_place_new, update_finding_places_null,     
    select_place_hint, select_all_places, update_nested_place,
    update_place_hint, select_place_id2, select_all_place_strings,
    select_max_place_id, select_place_id1, update_finding_places,
    insert_places_places_new, select_all_place_ids, insert_nested_place,
    select_all_nested_places, select_place_id, insert_place_name,
    select_all_place_names, select_nested_place_inclusion,
    select_finding_nested_place_id, update_finding_nested_place)
import dev_tools as dt
from dev_tools import looky, seeline






def get_all_place_strings():
    all_place_strings = []
    conn = sqlite3.connect(global_db_path)
    cur = conn.cursor()
    cur.execute(select_all_place_strings)
    tups = cur.fetchall()
    for tup in tups:
        all_place_strings.append(", ".join([i for i in tup if i]))
    cur.close()
    conn.close()
    return all_place_strings

def update_place_autofill_values():
    places = get_all_place_strings()
    for ent in EntryAuto.place_autofills:
        ent.values = places
    return places

class ValidatePlace():
    """ Duplicate places have to be checked by user dialog. Existing places
        go into a list. New places go straight into database and into a list.
        On OK the new places have already been input so just input the places
        that already exist. On CANCEL delete the new places.
    """

    def __init__(
            self, root, treebard, inwidg, initial, final, finding): 
        self.root = root
        self.treebard = treebard
        self.inwidg = inwidg
        self.initial = initial
        self.final = final
        self.finding = finding

        self.formats = make_formats_dict()

        self.place_list = []
        self.dupe_names = set()

        self.new_nesting = []
        self.cancelled = True
        self.new_places = []

        self.validate_place()

    def validate_place(self):

        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        if len(self.final) == 0 and len(self.initial) != 0:
            cur.execute(update_finding_places_null, (self.finding,))
            conn.commit()
            return

        cur.execute(select_all_place_names)
        all_place_names = [i[0] for i in cur.fetchall()]
        for name in all_place_names:
            if all_place_names.count(name) > 1:
                self.dupe_names.add(name)
        self.place_list = self.final.split(",")
        self.place_list = [self.place_list[i].strip() for i in range(
            len(self.place_list))]

        new_nesting = []
        for idx, name in enumerate(self.place_list):
            if name in self.dupe_names and self.inwidg.autofilled != self.final:
                choice = self.open_dupe_place_dlg(name, idx, cur)
                place_id = self.dupe_ids[choice]
                new_nesting.append((name, place_id, idx))
            else:
                cur.execute(select_place_id, (name,))
                place_id = cur.fetchone()
                if place_id is None:
                    name, place_id = self.make_new_place(name)
                    new_nesting.append((name, place_id, idx))
                else:
                    new_nesting.append((name, place_id[0], idx))
        self.new_nesting = sorted(new_nesting, key=lambda u: u[2])
        if self.cancelled is False: 
            self.update_place(cur, conn)
        else:
            pass
        cur.execute("DETACH tree")
        cur.close()
        conn.close()

    def make_new_place(self, name):
        conn = sqlite3.connect(global_db_path)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_max_place_id)
        self.max_id = cur.fetchone()[0] # ******revert on CANCEL by deleting > this
        cur.execute(insert_place_name, (name,))
        conn.commit()
        cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'place'")
        temp_id = cur.fetchone()[0] 
        self.new_places.append(temp_id)
        cur.close()
        conn.close()
        return name, temp_id

    def open_dupe_place_dlg(self, name, idx, cur):
        self.duplicate_places_dlg = Toplevel(self.root)
        self.duplicate_places_dlg.geometry("+120+24")
        self.duplicate_places_dlg.columnconfigure(1, weight=1)
        self.duplicate_places_dlg.rowconfigure(4, weight=1)
        self.dupe_nest = name
        cur.execute(select_place_id, (name,))
        self.dupe_ids = [i[0] for i in cur.fetchall()]
        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)
        self.make_widgets()
        self.make_inputs(name, idx, cur)
        self.root.wait_window(self.duplicate_places_dlg)
        return self.dupevar.get()

    def make_inputs(self, name, idx, cur):

        def show_examples(num, frm):
            cur.execute(select_nested_place_inclusion, tuple([num]*9,))
            inclusions = [list(i) for i in cur.fetchall()]
            copy = inclusions
            for indx, lst in enumerate(copy):
                lst = [i for i in lst if i]
                inclusions[indx] = lst
                lab = Label(frm, text=", ".join(inclusions[indx]), anchor="w")
                lab.grid(column=0, row=indx+1, sticky="ew", padx=(24,0))

        self.dupevar = tk.IntVar()
        row = 0
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
            if row == 0:
                rad.select()
            row += 1
        self.resize_window()

    def make_widgets(self):

        def ok():
            self.cancelled = False
            self.duplicate_places_dlg.destroy()
            self.inwidg.delete(0, 'end')
            self.inwidg.insert(0, self.final)

        def cancel():
            for num in self.new_places:
                self.delete_temp_ids(num)
            self.duplicate_places_dlg.destroy()
            self.inwidg.delete(0, 'end')
            self.inwidg.insert(0, self.initial)

        self.canvas = Border(self.duplicate_places_dlg, self.root)            
        self.canvas.title_1.config(text="Duplicate Place Dialog")
        self.canvas.title_2.config(text="input: {}".format(self.final))

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        lab = LabelHeader(
            self.window, text="Which {}?".format(self.dupe_nest), 
            justify='left', wraplength=600)
        self.radframe = Frame(self.window)

        buttonbox = Frame(self.window)
        b1 = Button(buttonbox, text="OK", width=7, command=ok)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=cancel)

        # children of self.window
        lab.grid(
            column=0, row=0, sticky='news', ipady=6, ipadx=6, 
            columnspan=2, padx=12, pady=12)
        self.radframe.grid(column=0, row=1, sticky="news")
        buttonbox.grid(column=1, row=2, sticky='se', padx=12, pady=12)
        # children of buttonbox
        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))
        configall(self.duplicate_places_dlg, self.formats)

    def resize_window(self):
        """ Added to requested width and height 
            are allowances for widgets not in self.window such as borders, 
            title bar, and status bar.
        """
        self.root.update_idletasks()    
        width = self.window.winfo_reqwidth() + 6
        height = self.window.winfo_reqheight() + 42
        self.duplicate_places_dlg.geometry("{}x{}".format(width, height))
        center_dialog(self.duplicate_places_dlg)

    def update_place(self, cur, conn):
        nested_ids = [i[1] for i in self.new_nesting]
        cur.execute(select_finding_nested_place_id, (self.finding,))
        nested_place_id = cur.fetchone()
        length = len(self.new_nesting)
        self.new_nesting = nested_ids + [None] * (9 - length) + [nested_place_id[0]] 

        if nested_place_id and nested_place_id[0] != 1:
            cur.execute(update_nested_place, tuple(self.new_nesting))
            conn.commit()
        else:
            cur.execute(insert_nested_place, tuple(self.new_nesting[0:9]))
            conn.commit()
            cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'nested_place'")
            new_nesting_id = cur.fetchone()[0]
            cur.execute(update_finding_nested_place, (new_nesting_id, self.finding))
            conn.commit()

        place_autofill_values = update_place_autofill_values()     

    def delete_temp_ids(self, num):
        print("line", looky(seeline()).lineno, "num:", num)








 


