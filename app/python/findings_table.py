# events_table.py

import tkinter as tk
import sqlite3
from files import get_current_file, global_db_path
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, Radiobutton, configall,
    LabelH3, Button, Entry, LabelHeader, Separator, open_message, Scrollbar,
    LabelStay, make_formats_dict, EntryAuto, EntryAutoPlace, EntryAutoHilited, NEUTRAL_COLOR,
    redraw_person_tab)
from scrolling import resize_scrolled_content
from toykinter_widgets import run_statusbar_tooltips
from dates import validate_date, format_stored_date, OK_MONTHS, get_date_formats
from error_messages import  open_yes_no_message
from persons import (
    make_all_names_dict_for_person_select, check_name, 
    get_original)
from assertions import AssertionsDialog
from roles import RolesDialog
from notes import NotesDialog
from places import ValidatePlace
from messages import findings_msg
from utes import split_sorter
    
from query_strings import (
    select_finding_nested_place, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_type_ids_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple, select_findings_details_couple_generic,
    select_finding_id_birth, select_finding_couple_details_by_finding,
    select_person_id_birth, select_all_findings_notes_ids,
    select_all_findings_roles_ids_distinct, 
    select_count_finding_id_sources, select_finding_event_type,  
    update_finding_particulars, select_all_kin_ids_types_couple,
    update_finding_age, update_current_person, select_all_place_ids,
    select_all_event_types, select_event_type_id, insert_finding_new,
    insert_finding_new_couple, insert_finding_new_couple_details,
    update_finding_age1, insert_finding_new_couple_alt, 
    select_event_type_couple_bool, insert_kin_type_new, update_event_types, 
    insert_event_type_new, select_max_event_type_id, delete_finding,
    update_finding_ages_kintypes_null, select_finding_id_guardianship, 
    delete_findings_roles_finding, delete_findings_notes_finding,         
    select_findings_for_person, delete_assertions_findings, 
    select_event_type_after_death, select_event_type_after_death_bool,
    insert_finding_birth, update_finding_age2, select_person,   
    select_finding_persons, update_finding_date, 
    select_finding_id_adoption, select_finding_id_fosterage,
    select_finding_id_age1_alt_parents, select_finding_id_age2_alt_parents,
    select_person_id_alt_parentage, select_kin_type_string, 
    select_finding_couple_details_include_nulls, 
    select_finding_details_offspring_alt_parentage)

import dev_tools as dt
from dev_tools import looky, seeline




date_prefs = get_date_formats()

HEADS = (
    'event', 'date', 'place', 'particulars', 'age', 
    'roles', 'notes', 'sources')

def delete_generic_finding(finding_id, conn, cur):
    cur.execute(delete_findings_roles_finding, (finding_id,))
    conn.commit()
    cur.execute(delete_findings_notes_finding, (finding_id,))
    conn.commit()
    cur.execute(delete_assertions_findings, (finding_id,))
    conn.commit()
    cur.execute(delete_finding, (finding_id,))
    conn.commit()

def delete_couple_finding(finding_id):
    """ Used also in families.py. """
    current_file = get_current_file()
    if current_file is not None:
        current_file = get_current_file()[0]
    else:
        return
    conn = sqlite3.connect(current_file)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    delete_generic_finding(finding_id, conn, cur) 
    cur.execute(update_finding_ages_kintypes_null, (finding_id,)) 
    conn.commit()
    cur.close()
    conn.close()

formats = make_formats_dict() 

class FindingsTable(Frame):

    def __init__(
            self, master, root, treebard, main, current_person,
            person_autofill_values, place_data, 
            # person_autofill_values, place_data, nestings, existing_place_names, 
            *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.treebard = treebard
        self.main_window = main
        self.current_person = current_person
        self.person_autofill_values = person_autofill_values
        self.place_data = place_data
        # self.place_autofill_values = nestings
        # self.existing_place_names = existing_place_names

        self.main_canvas = main.master

        current_name = self.person_autofill_values[self.current_person][0]["name"]
        self.inwidg = None
        self.headers = []
        self.widths = [0, 0, 0, 0, 0]

        self.initial = None

        self.widget = None
        self.kintip = None
        self.kintip_text = None
        self.kin_widths = [0, 0, 0, 0, 0, 0]
        self.kintip_bindings = {"on_enter": [], "on_leave": []}
        self.hovered_kin_widg = None

        self.screen_height = self.winfo_screenheight()
        self.column_padding = 2
        self.new_row = 0
        event_types = self.get_all_event_types()
        self.event_autofill_values = EntryAuto.create_lists(event_types)
        self.couple_event_types = self.get_couple_event_types()
        self.after_death_events = self.get_after_death_event_types()
        if self.after_death_events is None:
            return
        self.events_only_even_without_dates = [
            "birth", "death"] + self.after_death_events
        self.root.bind(
            "<Control-F5>", 
            lambda evt, main_window=self.main_window: redraw_person_tab(
                evt, main_window))
        # self.root.bind(
            # "<Control-f5>", 
            # lambda evt, main_window=self.main_window: redraw_person_tab(
                # evt, main_window))

        self.is_couple_event = False
        self.new_alt_parent_event = False
        self.unknown_event_type = False

        self.make_header()
        self.make_table_cells()
        self.set_cell_content()
        self.show_table_cells()

    def get_initial(self, evt):
        self.initial = evt.widget.get()
        self.inwidg = evt.widget

    def get_final(self, evt):
        if self.initial is None:
            return
        widg = evt.widget
        final = widg.get()
        if final != self.initial:
            self.final = final
            for row in self.cell_pool:
                c = 0
                for col in row[1]:
                    if col == widg:
                        self.finding = row[0]
                        col_num = c
                    c += 1
        
            self.update_db(widg, col_num)

    def delete_finding(self, finding_id, widg, initial):

        def ok_delete_finding():
            msg[0].destroy()
            self.focus_set()
            proceed(initial_value)

        def cancel_delete_finding():
            msg[0].destroy()
            widg.insert(0, initial)
            widg.focus_set()

        def err_done1():
            msg1[0].grab_release()
            msg1[0].destroy()
            widg.focus_set()
            widg.delete(0, 'end')
            widg.insert(0, initial)

        def proceed(initial_value):
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(select_event_type_id, (initial_value,))
            result = cur.fetchone()
            if result:
                old_event_type_id, couple_event_old = result 
            if couple_event_old == 0:
                cur.execute(select_finding_event_type, (finding_id,))
                event_type = cur.fetchone()[0]
                delete_generic_finding(finding_id, conn, cur)
            elif couple_event_old == 1:
                delete_couple_finding(finding_id)
            redraw_person_tab(main_window=self.main_window)
            cur.close()
            conn.close()

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        cur.execute(select_finding_event_type, (finding_id,))
        event_type = cur.fetchone()[0]
        if event_type == 1:
            msg1 = open_message(
                self, 
                findings_msg[9], 
                "Birth Events Undeletable Error", 
                "OK")
            msg1[0].grab_set()
            msg1[2].config(command=err_done1)
            return

        msg = open_yes_no_message(
            self, 
            findings_msg[4], 
            "Delete Conclusion Confirmation", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[2].config(command=ok_delete_finding)
        msg[3].config(command=cancel_delete_finding)

        initial_value = self.initial
        cur.close()
        conn.close()

    def update_db(self, widg, col_num):

        def update_event_type():

            def err_done3():
                msg[0].destroy()
                widg.focus_set()
                widg.delete(0, 'end')
                widg.insert(0, initval)

            def err_done4():
                msg[0].destroy()
                self.focus_set()
                widg.delete(0, 'end')
                widg.insert(0, 'offspring')

            def err_done7():
                msg[0].destroy()
                self.focus_set()
                widg.delete(0, 'end')
                widg.insert(0, initval)

            def update_to_existing_type():

                def err_done5():
                    msg4[0].destroy()
                    self.focus_set()
                    widg.delete(0, 'end')
                    widg.insert(0, initial_value)

                initial_value = self.initial
                cur.execute(select_event_type_id, (initial_value,))
                result = cur.fetchone()
                if result:
                    old_event_type_id, couple_event_old = result 
                event_type_id = None
                couple_event_new = None
                cur.execute(select_event_type_id, (self.final,))
                result = cur.fetchone()
                if result:
                    event_type_id, couple_event_new = result 
                if couple_event_old != couple_event_new:
                    msg4 = open_message(
                        self, 
                        findings_msg[3], 
                        "Incompatible Event Type Error", 
                        "OK")
                    msg4[0].grab_set()
                    msg4[2].config(command=err_done5)
                    return

                if couple_event_new in (0, 1):
                    cur.execute(
                        update_event_types, (event_type_id, self.finding))
                    conn.commit() 
                else:
                    print("line", looky(seeline()).lineno, "case not handled:")
            initval = self.initial
            event_types = self.get_all_event_types()
            self.final = self.final.strip().lower()
            if (self.initial == 'offspring' and len(self.final) != 0):
                msg = open_message(
                    self, 
                    findings_msg[2], 
                    "Offspring Event Edit Error", 
                    "OK")
                msg[0].grab_set()
                msg[2].config(command=err_done4)
                return

            if self.final == 'offspring':
                msg = open_message(
                    self, 
                    findings_msg[6], 
                    "Change to Offspring Event Error", 
                    "OK")
                msg[0].grab_set()
                msg[2].config(command=err_done7)
                return
                
            if self.final in event_types:
                update_to_existing_type()
            elif len(self.final) == 0:
                initial = self.initial
                self.delete_finding(self.finding, widg, initial)
            else:
                msg = open_message(
                    self.root, 
                    findings_msg[8], 
                    "Unknown Event Type", 
                    "OK") 
                msg[0].grab_set()
                msg[2].config(command=err_done3)
                return 

        def update_date():
            self.final = validate_date(
                self.root, 
                self.inwidg,
                self.final)

            if not self.final:
                self.final = "-0000-00-00-------"
            sorter = self.make_date_sorter(self.final)

            if self.final == "----------":
                self.final = "-0000-00-00-------"

            cur.execute(
                update_finding_date, (self.final, sorter, self.finding))
            conn.commit()
            date_prefs = get_date_formats(tree_is_open=1)
            formatted_date = format_stored_date(
                self.final, date_prefs=date_prefs)
            widg.delete(0, 'end')
            widg.insert(0, formatted_date)
            redraw_person_tab(main_window=self.main_window)

        def update_place():
            self.final = ValidatePlace(
                self.root, 
                self.treebard,
                self.inwidg,
                self.initial,
                self.final,
                self.finding,
                self.place_data,
                # self.place_autofill_values,
                # self.existing_place_names
)

        def update_age(offspring_event, row):
            if (event_string == "birth" and 
                    self.final not in (0, "0", "0d 0m 0y")):
                return
            if couple is False and offspring_event is False:
                cur.execute(update_finding_age, (self.final, self.finding))
                conn.commit() 
            else:
                cur.execute(select_finding_persons, (self.finding,))
                right_person = cur.fetchone()
                if right_person[0] == self.current_person:
                    cur.execute(
                        update_finding_age1, 
                        (self.final, self.finding, right_person[2]))
                elif right_person[1] == self.current_person:
                    cur.execute(
                        update_finding_age2, 
                        (self.final, self.finding, right_person[2])) 
                conn.commit()

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        if col_num == 0:
            update_event_type()
        elif col_num == 1:
            update_date()
        elif col_num == 2:
            update_place()
        elif col_num == 3:
            self.update_particulars(self.final, self.finding)
        elif col_num == 4:
            couple = False
            offspring_event = False
            for row in self.cell_pool:
                if row[0] == self.finding:
                    event_string = self.findings_data[self.finding]["event"]
                    cur.execute(select_event_type_couple_bool, (event_string,))
                    couple_or_not = cur.fetchone()[0]
                    if couple_or_not == 1:
                        couple = True
                    else: 
                        couple = False
                    if event_string == "offspring":
                        offspring_event = True
                        row = row
                    break
            update_age(offspring_event, row)            

        cur.close()
        conn.close()

    def make_table_cells(self, qty=2000):
        '''
            EntryAuto is used for all the text columns to keep the code 
            symmetrical for all the text columns, with autofill defaulting to 
            False except for the places column.
        '''

        self.table_cells = []
        for i in range(int(qty/8)):
            row = []
            for j in range(8):
                if j < 5:
                    if j == 0:
                        cell = EntryAuto(
                            self, width=0,
                            autofill=True, 
                            values=self.event_autofill_values)
                    elif j == 2:
                        cell = EntryAutoPlace(
                            self, width=0, 
                            autofill=True,
                            values=EntryAutoPlace.place_autofill_values)
                    else:                        
                        cell = EntryAuto(self, width=0,)
                    cell.initial = ''
                    cell.final = ''
                    cell.finding = None
                    cell.bind('<FocusIn>', self.get_initial, add="+")
                    cell.bind('<FocusOut>', self.get_final, add="+")
                elif j == 5:
                    cell = LabelDots(
                        self, RolesDialog, self.treebard, 
                        person_autofill_values=self.person_autofill_values
)
                elif j == 6:
                    cell = LabelDots(
                        self, NotesDialog, self.treebard, 
                        person_autofill_values=self.person_autofill_values
)
                elif j == 7:
                    cell = LabelButtonText(
                        self,
                        width=8,
                        anchor='w',
                        font=formats['heading3'])
                row.append(cell)
            self.table_cells.append(row)
        self.new_finding_frame = Frame(self)
        self.finding_input = EntryAutoHilited(
            self.new_finding_frame,
            width=32, 
            autofill=True, 
            values=self.event_autofill_values)
        self.add_finding_button = Button(
            self.new_finding_frame, 
            text="NEW CONCLUSION", 
            command=self.make_new_conclusion)

    def set_cell_content(self):
        self.findings_data, current_roles, current_notes = self.get_findings()
        copy = dict(self.findings_data)
        self.attributes = {}
        finding_ids = list(self.findings_data.keys())
        table_size = len(self.findings_data)
        self.cell_pool = []

        i = 0
        for row in self.table_cells[0:table_size]:
            self.cell_pool.append([finding_ids[i], row])
            i += 1
            
        for row in self.cell_pool:
            widg = row[1][5]
            finding_id = row[0]
            widg.finding_id = finding_id
            widg.current_person = self.current_person
            widg.header = [
                self.findings_data[finding_id]["event"], 
                self.findings_data[finding_id]["date"], 
                self.findings_data[finding_id]["place"], 
                self.findings_data[finding_id]["particulars"]]

        for row in self.cell_pool:
            widg = row[1][6]
            finding_id = row[0]
            widg.finding_id = finding_id
            widg.current_person = self.current_person
            widg.header = [
                self.findings_data[finding_id]["event"], 
                self.findings_data[finding_id]["date"], 
                self.findings_data[finding_id]["place"], 
                self.findings_data[finding_id]["particulars"]]

    def sort_by_date(self):
        after_death = []
        for finding_id in self.findings_data:
            event_type = self.findings_data[finding_id]['event']
            sorter = self.findings_data[finding_id]['sorter']
            if event_type in self.after_death_events:
                after_death.append([finding_id, event_type, sorter])             

        after_death = sorted(after_death, key=lambda i: i[2])
        m = 0
        for lst in after_death:
            lst[2] = [20000 + m, 0, 0]
            m += 1

        undated = []
        row_order = []
        for finding_id in self.findings_data:
            event_type = self.findings_data[finding_id]['event']
            date = self.findings_data[finding_id]['date']
            if event_type == "birth":
                sorter = [-10000, 0, 0]
                row_order.append([finding_id, event_type, sorter])
            elif event_type == "death":
                sorter = [10000, 0, 0]
                row_order.append([finding_id, event_type, sorter])
            elif event_type in (self.after_death_events):
                pass
            elif len(date) == 0:
                undated.append([finding_id, event_type, sorter])
            else:
                sorter = self.findings_data[finding_id]['sorter']
                row_order.append([finding_id, event_type, sorter])

        undated = sorted(undated, key=lambda i: i[1])
        n = 0
        for lst in undated:
            lst[2] = [30000 + n, 0, 0]
            n += 1

        row_order = sorted(row_order, key = lambda i: i[2])
        all_sorted = row_order + after_death + undated
 
        new_order = []
        for lst in all_sorted:
            new_order.append(lst[0])
        return new_order

    def show_table_cells(self): 
        current_file = get_current_file()[0]
        row_order = self.sort_by_date()
       
        copy = []
        for finding_id in row_order:
            for row in self.cell_pool:
                if row[0] == finding_id:
                    copy.append(row)

        self.cell_pool = copy

        r = 2
        for row in self.cell_pool:
            finding_id = row[0]
            c = 0
            for cell in row[1]:
                widg = row[1][c]
                if c < 5:
                    text = self.findings_data[finding_id][HEADS[c]]
                elif c == 7:
                    text = self.findings_data[finding_id]["source_count"]
                    # print("line", looky(seeline()).lineno, "text:", text)
                    # print("line", looky(seeline()).lineno, "widg:", widg)
                    widg.bind("<Button-1>", lambda evt, finding=finding_id, text=text, widg=widg: self.open_assertions_dialog(finding, text, widg))
                else:
                    text = "     "
                    if c == 5 and self.findings_data[finding_id].get("roles"):
                        text = " ... "
                    elif c == 6 and self.findings_data[finding_id].get("notes"):
                        text = " ... "
                    
                if c in (5, 6, 7):
                    widg.config(text=text)
                    widg.grid(
                        column=c, row=r, sticky='w', pady=(3,0), padx=(2,0))
                else:
                    widg.grid(column=c, row=r, sticky='ew', pady=(3,0))
                if c < 5:
                    if len(text) > self.widths[c]:
                        self.widths[c] = len(text)
                    widg.insert(0, text) 
                if c == 0:
                    # kintips
                    dkt = self.findings_data[finding_id]
                    evtype = dkt["event"]
                    if evtype in ("adopted a child", "acted as guardian", 
                            "fostered a child", "offspring"):
                        name = dkt.get("child_name")
                        child_id = dkt["child_id"]
                        if len(name) == 0:
                            name = self.person_autofill_values[child_id][0]["name"]
                        offspring_in = widg.bind(
                            "<Enter>", lambda evt, 
                            kin="child", name=name: self.handle_enter(kin, name))
                        offspring_out = widg.bind("<Leave>", self.on_leave)
                        self.widget = widg
                        self.kintip_bindings["on_enter"].append([widg, offspring_in])
                        self.kintip_bindings["on_leave"].append([widg, offspring_out])
                    elif evtype in self.couple_event_types:
                        name = dkt.get("partner_name")
                        if name is None and dkt.get("partner_id"):
                            name = self.person_autofill_values[dkt["partner_id"]][0]["name"]
                        kin = "partner"
                        if (dkt.get("partner_kin_type") and 
                                dkt["partner_kin_type"] not in (
                                    "generic_partner1", "generic_partner2")):
                            kin = dkt["partner_kin_type"]
                        couple_in = widg.bind(
                            "<Enter>", lambda evt, 
                            kin=kin, 
                            name=name: self.handle_enter(kin, name))
                        couple_out = widg.bind("<Leave>", self.on_leave)
                        self.widget = widg
                        self.kintip_bindings["on_enter"].append([widg, couple_in])
                        self.kintip_bindings["on_leave"].append([widg, couple_out])
                    elif evtype in ("birth", "adoption", "guardianship", "fosterage"):
                        if evtype == "birth":
                            name1 = dkt.get("father_name")
                            name2 = dkt.get("mother_name")
                            names = "{}, {}".format(name1, name2)
                            parents_in = widg.bind(
                                "<Enter>", lambda evt, 
                                kin="parent(s)", names=names: self.handle_enter(
                                    kin, names))
                            parents_out = widg.bind("<Leave>", self.on_leave)
                            self.widget = widg
                            self.kintip_bindings["on_enter"].append([widg, parents_in])
                            self.kintip_bindings["on_leave"].append([widg, parents_out])
                        elif evtype == "adoption":
                            alts1 = (
                                "adoptive_parent_name1", "adoptive_father_name1", 
                                "adoptive_mother_name1")
                            alts2 = (
                                "adoptive_parent_name2", "adoptive_father_name2", 
                                "adoptive_mother_name2")
                            for key in alts1:
                                name1 = dkt.get(key)
                                if name1:
                                    break
                            for key in alts2:
                                name2 = dkt.get(key)
                                if name2:
                                    break
                            names = "{}, {}".format(name1, name2)
                            adoptive_parents_in = widg.bind(
                                "<Enter>", lambda evt, 
                                kin="adoptive parent(s)", names=names: self.handle_enter(
                                    kin, names))
                            adoptive_parents_out = widg.bind("<Leave>", self.on_leave)
                            self.widget = widg
                            self.kintip_bindings["on_enter"].append([widg, adoptive_parents_in])
                            self.kintip_bindings["on_leave"].append([widg, adoptive_parents_out])
                        elif evtype == "fosterage":
                            alts1 = (
                                "foster_parent_name1", "foster_father_name1", "foster_mother_name1")
                            alts2 = (
                                "foster_parent_name2", "foster_father_name2", "foster_mother_name2")
                            for key in alts1:
                                name1 = dkt.get(key)
                                if name1:
                                    break
                            for key in alts2:
                                name2 = dkt.get(key)
                                if name2:
                                    break
                            names = "{}, {}".format(name1, name2)
                            foster_parents_in = widg.bind(
                                "<Enter>", lambda evt, 
                                kin="foster parent(s)", names=names: self.handle_enter(
                                    kin, names)) 
                            foster_parents_out = widg.bind("<Leave>", self.on_leave)
                            self.widget = widg
                            self.kintip_bindings["on_enter"].append([widg, foster_parents_in])
                            self.kintip_bindings["on_leave"].append([widg, foster_parents_out])
                        elif evtype == "guardianship":
                            alts1 = ("guardian_name1", "legal_guardian_name1")
                            alts2 = ("guardian_name2", "legal_guardian_name2")
                            for key in alts1:
                                name1 = dkt.get(key)
                                if name1:
                                    break
                            for key in alts2:
                                name2 = dkt.get(key)
                                if name2:
                                    break
                            names = "{}, {}".format(name1, name2)
                            guardians_in = widg.bind(
                                "<Enter>", lambda evt, 
                                kin="guardian(s)", names=names: self.handle_enter(
                                    kin, names))
                            guardians_out = widg.bind("<Leave>", self.on_leave)
                            self.widget = widg
                            self.kintip_bindings["on_enter"].append([widg, guardians_in])
                            self.kintip_bindings["on_leave"].append([widg, guardians_out])
                c += 1
            r += 1
        z = 0
        for widg in self.headers[0:5]:
            if self.widths[z] < len(HEADS[z]):
                widg.config(width=len(HEADS[z]) + 2)
            else:
                widg.config(width=self.widths[z] + 2)
            z += 1

        self.fix_tab_traversal() 
        for row_num in range(self.grid_size()[1]):
            self.grid_rowconfigure(row_num, weight=0)
        self.new_row = row_num + 1

        self.new_finding_frame.grid(
            column=0, row=self.new_row, pady=6, columnspan=5, sticky='ew')
        self.finding_input.grid(column=0, row=0, padx=(0,12), sticky='w')
        self.add_finding_button.grid(
            column=1, row=0, sticky='w')

    def open_assertions_dialog(self, finding_id, text, widg):
        self.assertions_dialog = AssertionsDialog(
            self.master, self.treebard, finding_id, text, widg)

    def show_kintip(self, kin_type, name):
        """ Based on show_kintip() in search.py. """
        maxvert = self.winfo_screenheight()

        if self.kintip or not self.kintip_text:
            return
        x, y, cx, cy = self.widget.bbox('insert')        

        self.kintip = d_tip = Toplevel(self.widget)
        label = LabelStay(
            d_tip, 
            text=self.kintip_text, 
            justify='left',
            relief='solid', 
            bd=1,
            bg=NEUTRAL_COLOR, fg="white")
        label.pack(ipadx=6, ipady=3)

        mouse_at = self.winfo_pointerxy()

        tip_shift = 48 

        if mouse_at[1] < maxvert - tip_shift * 2:
            x = mouse_at[0] + tip_shift
            y = mouse_at[1] + tip_shift
        else:
            x = mouse_at[0] + tip_shift
            y = mouse_at[1] - tip_shift

        d_tip.wm_overrideredirect(1)
        d_tip.wm_geometry('+{}+{}'.format(x, y))

    def off(self):
        d_tip = self.kintip
        self.kintip = None
        if d_tip:
            d_tip.destroy()

    def handle_enter(self, kin_type, name):
        if name is None:
            name = "unknown person"
        elif len(name) == 2:
            name = list(name)
            name[1] = "({})".format(name[1])
            name = " ".join(name)
        self.kintip_text = "{}: {}".format(kin_type, name)

        if self.kintip_text:
            self.show_kintip(kin_type, name)

    def on_leave(self, evt):
        self.off()

    def make_header(self):
        y = 0
        for heading in HEADS:
            head = LabelH3(self, text=heading.upper(), anchor='w')
            head.grid(column=y, row=0, sticky='ew')
            self.headers.append(head)
            y += 1

        sep = Separator(self, height=3)
        sep.grid(column=0, row=1, columnspan=9, sticky='ew')

    def fix_tab_traversal(self):

        def third_and_second_items(pos):
            return pos[2], pos[1]

        row_fixer = []
        for lst in self.cell_pool:
            for child in lst[1]:           
                row_fixer.append((
                    child, 
                    child.grid_info()['column'], 
                    child.grid_info()['row']))
        row_fixer_2 = sorted(row_fixer, key=third_and_second_items) 

        widgets = []
        for tup in row_fixer_2:
            widgets.append(tup[0])

        for widg in widgets:
            widg.lift() 

    def make_date_sorter(self, storable_date):
        sorter = storable_date.split("-")
        sorter = sorter[1:4]
        i = 0
        for item in sorter:
            if i == 0:
                if len(item) == 0:
                    sorter[0] = "0"
            elif i == 1:
                if len(item) != 0:
                    a = 1
                    for abb in OK_MONTHS:
                        if abb == sorter[1]:
                            sorter[1] = str(a)
                            break
                        a += 1
                else:
                    sorter[1] = "0"
            elif i == 2:
                if len(item) == 0:
                    sorter[2] = "0"

            i += 1
        sorter = ",".join(sorter)
        return sorter

    def count_birth_death_events(self, new_conclusion):
        too_many = False
        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_findings_for_person, (self.current_person,))
        all_events = [i[0] for i in cur.fetchall()]
        if new_conclusion in all_events:
            too_many = True
        cur.close()
        conn.close()
        return too_many

    def make_new_conclusion(self):
        """ Disallow creation of second birth or death event or types 
            that don't exist yet.
        """

        def err_done6():
            self.finding_input.delete(0, 'end')
            msg[0].destroy()
            self.focus_set()

        too_many = False
        new_conclusion = self.finding_input.get().strip().lower()
        if new_conclusion in ("birth", "death"):
            too_many = self.count_birth_death_events(new_conclusion)
        if too_many is True: 
            msg = open_message(
                self, 
                findings_msg[5], 
                "Multiple Birth or Death Conclusions", 
                "OK")
            msg[0].grab_set()
            msg[2].config(command=err_done6)
            return

        self.new_conclusion = new_conclusion

        self.get_new_finding_data()
        if self.unknown_event_type is False:
            if self.is_couple_event is False:
                if self.new_conclusion == "offspring":
                    msg = open_message(
                        self.root, 
                        findings_msg[7], 
                        "Offspring Event Creation Error", 
                        "OK") 
                    msg[0].grab_set()
                    return 
                elif self.new_conclusion in ("adoption", "fosterage", "guardianship"):
                    self.new_alt_parent_event = True

        self.add_finding()
        self.finding_input.delete(0, 'end')

    def add_finding(self):
        """ Unlike parents in a birth event, it doesn't matter which
            partner in a couple event is person_id1 or person_id2 in
            the finding table of the database, because only one of the
            partners is displayed in the families table.
        """
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        if self.is_couple_event is False and self.new_alt_parent_event is False:
            cur.execute(
                insert_finding_new, (self.event_type_id, self.current_person))
            conn.commit() 
        elif self.is_couple_event is False and self.new_alt_parent_event is True:
            if self.event_type_id == 48:
                unisex_alt_parent = 130
            elif self.event_type_id == 83:
                unisex_alt_parent = 110
            elif self.event_type_id == 95:
                unisex_alt_parent = 120 
            cur.execute(
                insert_finding_new_couple_alt, 
                (self.current_person, self.event_type_id, unisex_alt_parent, unisex_alt_parent))
            conn.commit()            
            self.new_alt_parent_event = False 
        elif self.is_couple_event is True:
            cur.execute(
                insert_finding_new_couple, 
                (self.event_type_id, self.current_person))
            conn.commit()  
        else:
            print("line", looky(seeline()).lineno, "case not handled:")
# this if/else added 20220625, not finished, commented 20220629
        # if len(self.place_string) == 0:
            # cur.execute(insert_finding_places_new, (self.new_finding,))
            # conn.commit()
        # else:
            # self.update_db_place(conn, cur)

        cur.close()
        conn.close()
        current_name = self.person_autofill_values[self.current_person][0]["name"]
        redraw_person_tab(
            main_window=self.main_window, 
            current_person=self.current_person, 
            current_name=current_name)

    def get_new_finding_data(self):

        def err_done2():
            self.destroy()
            msg[0].destroy()
            self.finding_input.focus_set()
            self.finding_input.delete(0, 'end')

        tree = get_current_file()[0]
        conn =  sqlite3.connect(global_db_path)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_event_type_id, (self.new_conclusion,))
        result = cur.fetchone()
        if result is not None:
            self.event_type_id, is_couple_event = result
            if is_couple_event == 1:
                self.is_couple_event = True
            elif is_couple_event == 0:
                self.is_couple_event = False
        else:
            self.unknown_event_type = True
            msg = open_message(
                self.root, 
                findings_msg[8], 
                "Unknown Event Type", 
                "OK") 
            msg[0].grab_set()
            msg[2].config(command=err_done2)
            return 

        cur.execute("DETACH tree")
        cur.close()
        conn.close()

    def update_particulars(self, input_string, finding):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(
            update_finding_particulars, 
            (input_string, finding))
        conn.commit()
        cur.close()
        conn.close()

    def get_all_event_types(self):
        tree, current_dir = get_current_file()
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_all_event_types)
        event_types = [i[0] for i in cur.fetchall()]
        cur.execute("DETACH tree")
        cur.close()
        conn.close()
        return event_types

    def get_after_death_event_types(self):
        tree, current_dir = get_current_file()
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_event_type_after_death)
        after_death_event_types = [i[0] for i in cur.fetchall()]
        cur.execute("DETACH tree")
        cur.close()
        conn.close()
        return after_death_event_types 

    def get_couple_kin_types(self):
        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_all_kin_type_ids_couple)
        couple_kin_type_ids = [i[0] for i in cur.fetchall()]
        cur.execute("DETACH tree")
        cur.close()
        conn.close()
        return couple_kin_type_ids

    def get_couple_event_types(self):
        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_all_event_types_couple)
        couple_event_types = [i[0] for i in cur.fetchall()]
        cur.execute("DETACH tree")
        cur.close()
        conn.close()
        return couple_event_types

    def get_place_string(self, finding_id, cur):
        place_string = ""
        cur.execute(select_finding_nested_place, finding_id)
        result = cur.fetchone()
        if result:
            place_string = ", ".join([i for i in result if i != "unknown"])
        return place_string

    def get_generic_findings(
            self, dkt, cur, finding_id, findings_data, 
            non_empty_roles, non_empty_notes):
        cur.execute(select_findings_details_generic, finding_id)
        generic_details = [i for i in cur.fetchone()]
        date_prefs = get_date_formats(tree_is_open=1)
        dkt["date"] = format_stored_date(generic_details[3], date_prefs=date_prefs)
        dkt["event"], dkt["particulars"], dkt["age"] = generic_details[0:3]
        dkt["sorter"] = split_sorter(generic_details[4])

        place = self.get_place_string(finding_id, cur)
        dkt["place"] = place

        if finding_id[0] in non_empty_roles:
            self.get_role_findings(dkt, finding_id[0], cur)

        if finding_id[0] in non_empty_notes:
            self.get_note_findings(dkt, finding_id[0], cur)

        cur.execute(select_count_finding_id_sources, finding_id)
        source_count = cur.fetchone()[0]
        dkt["source_count"] = source_count

        findings_data[finding_id[0]] = dkt

    def get_couple_findings(
            self, cur, rowtotype, findings_data, 
            non_empty_roles, non_empty_notes, person_autofill_values):

        couple_kin_type_ids = self.get_couple_kin_types()
        curr_per_kin_types = tuple([self.current_person] + couple_kin_type_ids)

        sql =   '''
                    SELECT finding_id 
                    FROM finding
                    WHERE person_id1 = ?
                        AND kin_type_id1 in ({})
                '''.format(
                    ','.join('?' * (len(curr_per_kin_types) - 1)))
        cur.execute(sql, curr_per_kin_types)
        couple_findings1 = [i[0] for i in cur.fetchall()]
        sql =   '''
                    SELECT finding_id 
                    FROM finding
                    WHERE person_id2 = ?
                        AND kin_type_id2 in ({})
                '''.format(
                    ','.join('?' * (len(curr_per_kin_types) - 1)))
        cur.execute(sql, curr_per_kin_types)
        couple_findings2 = [i[0] for i in cur.fetchall()]
        couple_findings = couple_findings1 + couple_findings2
        for finding_id in couple_findings:
            finding_id = (finding_id,)
            dkt = dict(rowtotype)
            cur.execute(select_findings_details_couple, finding_id)
            gotgot = cur.fetchone()
            if gotgot:
                name = ""
                if gotgot[0] == self.current_person:
                    iD = gotgot[3]
                    if iD:
                        name = person_autofill_values[iD][0]["name"] 
                    dkt["age"] = gotgot[1]
                    dkt["kin_type"] = gotgot[2]
                    dkt["partner_id"] = iD
                    dkt["partner_kin_type"] = gotgot[5]
                    dkt["partner_name"] = name
                elif gotgot[3] == self.current_person:
                    iD = gotgot[0]
                    if iD:
                        name = person_autofill_values[iD][0]["name"] 
                    dkt["age"] = gotgot[4]
                    dkt["kin_type"] = gotgot[5]
                    dkt["partner_id"] = iD
                    dkt["partner_kin_type"] = gotgot[2]
                    dkt["partner_name"] = name

            cur.execute(select_findings_details_couple_generic, finding_id)
            couple_generics = list(cur.fetchone())
            date_prefs = get_date_formats(tree_is_open=1)
            couple_generics[1] = format_stored_date(
                couple_generics[1], date_prefs=date_prefs)
            place = self.get_place_string(finding_id, cur)
            dkt["place"] = place
            sorter = split_sorter(couple_generics[2])
            couple_generic_details = [
                couple_generics[0], 
                couple_generics[1], 
                sorter,  
                couple_generics[3]]

            if finding_id[0] in non_empty_roles:
                self.get_role_findings(dkt, finding_id[0], cur)

            if finding_id[0] in non_empty_notes:
                self.get_note_findings(dkt, finding_id[0], cur)

            cur.execute(select_count_finding_id_sources, finding_id)
            source_count = cur.fetchone()[0]
            dkt["source_count"] = source_count

            dkt["event"], dkt["date"], dkt["sorter"], dkt["particulars"] = couple_generic_details
            findings_data[finding_id[0]] = dkt 

    def make_parent_kintips(self, dkt, cur, person_autofill_values):
        cur.execute(select_finding_id_birth, (self.current_person,))
        birth_id = cur.fetchone()
        parents = (None, None)
        if birth_id:
            cur.execute(select_finding_couple_details_include_nulls, birth_id)
            parents = cur.fetchone()
        if parents is None:
            return
        else:
            parents = list(parents)
        pa_id = None
        ma_id = None
        pa_name = None
        ma_name = None
        if "father" in parents:
            if parents.index("father") == 3:
                parents = [parents[2], parents[3], parents[0], parents[1]]
        if "mother" in parents:
            if parents.index("mother") == 1:
                parents = [parents[2], parents[3], parents[0], parents[1]]
        pa_id = parents[0]
        if pa_id:
            pa_name = person_autofill_values[pa_id][0]["name"]
        ma_id = parents[2]
        if ma_id:
            ma_name = person_autofill_values[ma_id][0]["name"]
        dkt["father_id"] = pa_id
        dkt["mother_id"] = ma_id
        dkt["father_name"] = pa_name
        dkt["mother_name"] = ma_name

    def make_alt_parent_kintips(
            self, dkt, cur, finding_id, person_autofill_values,  
            adoption=None, fosterage=None, guardianship=None):

        if adoption:
            query = select_finding_id_adoption
        elif fosterage:
            query = select_finding_id_fosterage
        elif guardianship:
            query = select_finding_id_guardianship
        cur.execute(query, (self.current_person,))
        event_id = cur.fetchall()
        parents = None
        if event_id is None:
            return
        elif finding_id in event_id:
            cur.execute(select_finding_couple_details_by_finding, finding_id)
            parents = cur.fetchone()
        if not parents:
            pass
        else:
            key1 = parents[1].replace(" ", "_")
            key2 = parents[3].replace(" ", "_")
            key1a = "{}_id1".format(key1)
            key1b = "{}_name1".format(key1)
            key2a = "{}_id2".format(key2)
            key2b = "{}_name2".format(key2)
            parent1 = None
            parent2 = None
            parent1_id = parents[0]
            parent2_id = parents[2]
            if parent1_id:
                parent1 = person_autofill_values[parent1_id][0]["name"]
            if parent2_id:
                parent2 = person_autofill_values[parent2_id][0]["name"]

            dkt[key1a] = parent1_id
            dkt[key1b] = parent1
            dkt[key2a] = parent2_id
            dkt[key2b] = parent2

    def autocreate_parent_findings(
        self, dkt, cur, findings_data, finding_id, person_autofill_values):
        """ Get birth & alt_birth findings to autocreate rows when parent is current 
            person. """

        def get_event_type_string(iD):
            cur.execute(select_finding_event_type, (iD,))
            event_type_id = cur.fetchone()[0]
            conversion = {
                1: "offspring", 83: "adopted a child", 95: "fostered a child", 
                48: "acted as guardian"}
            for k,v in conversion.items():
                if event_type_id == k:
                    event_type = v
            return event_type

        cur.execute(select_finding_id_age1_alt_parents, (self.current_person,))
        offspring1 = [list(i) for i in cur.fetchall()]

        cur.execute(select_finding_id_age2_alt_parents, (self.current_person,))
        offspring2 = [list(i) for i in cur.fetchall()]

        offspring = offspring1 + offspring2

        for child in offspring:
            finding = child[0]
            cur.execute(select_person, (finding,))
            child_id = cur.fetchone()
            if child_id:
                child.append(child_id[0])

        for child in offspring:
            offspring_event_id, parent_age, child_id = child
            cur.execute(
                select_finding_details_offspring_alt_parentage, 
                (child_id, offspring_event_id))     
            offspring_details = cur.fetchone()
            event_type = get_event_type_string(offspring_event_id)

            child_name = person_autofill_values[child_id][0]["name"]

            sorter = split_sorter(offspring_details[1])
            date_prefs = get_date_formats(tree_is_open=1)
            date = format_stored_date(offspring_details[0], date_prefs=date_prefs)

            particulars = offspring_details[2]
            place = self.get_place_string((offspring_event_id,), cur)

            cur.execute(select_count_finding_id_sources, (offspring_event_id,))
            source_count = cur.fetchone()[0]      
            findings_data[offspring_event_id] = {}
            findings_data[offspring_event_id]["event"] = event_type
            findings_data[offspring_event_id]["date"] = date
            findings_data[offspring_event_id]["place"] = place
            findings_data[offspring_event_id]["particulars"] = particulars
            findings_data[offspring_event_id]["age"] = parent_age
            findings_data[offspring_event_id]["source_count"] = source_count
            findings_data[offspring_event_id]["child_id"] = child_id
            findings_data[offspring_event_id]["child_name"] = child_name
            findings_data[offspring_event_id]["sorter"] = sorter

        event_type = dkt["event"]
        if event_type == "birth":
            self.make_parent_kintips(dkt, cur, person_autofill_values)
        elif event_type == "adoption":
            self.make_alt_parent_kintips(dkt, cur, finding_id, person_autofill_values, adoption=True)
        elif event_type == "fosterage":
            self.make_alt_parent_kintips(dkt, cur, finding_id, person_autofill_values, fosterage=True)
        elif event_type == "guardianship":
            self.make_alt_parent_kintips(dkt, cur, finding_id, person_autofill_values, guardianship=True)

    def get_role_findings(
        self, dkt, finding_id, cur, findings_data=None):
        current_roles = []
        current_roles.append(finding_id)
        if findings_data is None:
            dkt["roles"] = current_roles
        else: 
            findings_data[finding_id]["roles"] = current_roles

    def get_note_findings(
        self, dkt, finding_id, cur, findings_data=None):
        current_notes = []
        current_notes.append(finding_id)
        if findings_data is None:
            dkt["notes"] = current_notes
        else:
            findings_data[finding_id]["notes"] = current_notes

    def get_findings(self):
        findings_data = {}
        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))

        rowtotype = {
            "event": "", "date": "", "place": "", "particulars": "", "age": ""}

        cur.execute(select_all_findings_current_person, (self.current_person,))
        generic_finding_ids = cur.fetchall()
        cur.execute(select_all_findings_roles_ids_distinct)
        non_empty_roles = [i[0] for i in cur.fetchall()]

        cur.execute(select_all_findings_notes_ids)
        non_empty_notes = [i[0] for i in cur.fetchall()]

        person_autofill_values = make_all_names_dict_for_person_select()  
        for finding_id in generic_finding_ids:
            dkt = dict(rowtotype)
            
            self.get_generic_findings(
                dkt, cur, finding_id, findings_data, 
                non_empty_roles, non_empty_notes)     

            if dkt["event"] == "birth":
                self.autocreate_parent_findings(
                    dkt, cur, findings_data, finding_id, 
                    person_autofill_values)
            elif dkt["event"] == "adoption":
                self.autocreate_parent_findings(
                    dkt, cur, findings_data, finding_id, 
                    person_autofill_values)
            elif dkt["event"] == "fosterage":
                self.autocreate_parent_findings(
                    dkt, cur, findings_data, finding_id, 
                    person_autofill_values)
            elif dkt["event"] == "guardianship":
                self.autocreate_parent_findings(
                    dkt, cur, findings_data, finding_id, 
                    person_autofill_values)

        self.get_couple_findings(
            cur, rowtotype, findings_data, 
            non_empty_roles, non_empty_notes, person_autofill_values)

        cur.execute("DETACH tree")
        cur.close()
        conn.close()  
        return findings_data, non_empty_roles, non_empty_notes 














