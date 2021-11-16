# events_table

# previous version x7 canned because modifying the code is too hard due to the use of lists throughout the process of building a table from queried data results. I had once done this with dicts but changed to lists since the table columns are in a fixed order and the list can be in the same order, so making the table is faster from a list. But it's more important to make the code accessible so I'm going back to dictionaries which will make the code easier to read and understand. 

import tkinter as tk
import sqlite3
from files import get_current_file
from window_border import Border 
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, Radiobutton,
    LabelH3, Button, Entry, MessageHilited, EntryHilited1,
    LabelHilited)
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from dates import validate_date, format_stored_date, OK_MONTHS, get_date_formats
from nested_place_strings import make_all_nestings
from toykinter_widgets import Separator
from styles import make_formats_dict, config_generic
from names import (
    get_name_with_id, make_all_names_list_for_person_select,
    open_new_person_dialog)
from roles import RolesDialog
from notes import NotesDialog
# from places import place_strings, ValidatePlace, places_places
from places import ValidatePlace
from scrolling import Scrollbar, resize_scrolled_content
from messages import open_error_message, events_msg, open_yes_no_message
from query_strings import (
    select_finding_places_nesting, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_type_ids_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple, select_findings_details_couple_generic,
    select_finding_id_birth, select_person_id_kin_types_birth,
    select_person_id_birth, select_finding_ids_age1_parents,
    select_finding_ids_age2_parents, select_all_findings_notes_ids,
    select_findings_details_offspring, select_all_findings_roles_ids_distinct,     
    select_count_finding_id_sources, select_nesting_fk_finding,
    update_finding_particulars, select_all_kin_ids_types_couple,
    update_finding_age, update_current_person, select_all_place_ids,
    select_all_event_types, select_event_type_id, insert_finding_new,
    insert_finding_new_couple, insert_findings_persons_new_couple,    
    update_findings_persons_age1, select_max_finding_id, insert_place_new,
    select_event_type_couple_bool, insert_kin_type_new, update_event_types,    
    insert_places_places_new, insert_finding_places_new_event,
    insert_event_type_new, select_max_event_type_id, delete_finding,delete_claims_findings, delete_finding_places, delete_findings_persons,
    delete_findings_roles_finding, delete_findings_notes_finding,         
    select_findings_for_person, insert_finding_places_new,
    select_event_type_after_death, select_event_type_after_death_bool,
    select_findings_persons_parents, select_findings_persons_age,    
    insert_finding_birth, update_findings_persons_age2,
    select_finding_event_type, delete_findings_persons_offspring,
    select_findings_persons_person_id, update_finding_date,
    
)

import dev_tools as dt
from dev_tools import looky, seeline



date_prefs = get_date_formats()
formats = make_formats_dict()

HEADS = (
    'event', 'date', 'place', 'particulars', 'age', 
    'roles', 'notes', 'sources')

def get_current_person():
    current_file = get_current_file()
    if current_file is not None:
        current_file = get_current_file()[0]
    else:
        return
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person_id)
    current_person = cur.fetchone()[0]
    cur.close()
    conn.close()
    return current_person

def update_particulars(input_string, finding):
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

def get_all_event_types():
    current_file, current_dir = get_current_file()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_event_types)
    event_types = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return event_types

def get_after_death_event_types():
    current_file, current_dir = get_current_file()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_event_type_after_death)
    after_death_event_types = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return after_death_event_types 

def get_couple_kin_types():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_kin_type_ids_couple)
    couple_kin_type_ids = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return couple_kin_type_ids

def get_couple_event_types():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_event_types_couple)
    couple_event_types = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return couple_event_types

def get_place_string(finding_id, cur):
    cur.execute(select_finding_places_nesting, finding_id)
    place = cur.fetchone()
    place_string = ", ".join([i for i in place if i])
    if place_string == "unknown": place_string = ""
    return place_string

def split_sorter(date):
    sorter = date.split(",")
    date = [int(i) for i in sorter]
    return date

def get_generic_findings(
        dkt, cur, finding_id, findings_data, 
        current_person, non_empty_roles, non_empty_notes):
    cur.execute(select_findings_details_generic, finding_id)
    generic_details = [i for i in cur.fetchone()]
    dkt["date"] = format_stored_date(generic_details[3], date_prefs)
    # dkt["date"] = format_stored_date(generic_details[3])

    dkt["event"], dkt["particulars"], dkt["age"] = generic_details[0:3]
    dkt["sorter"] = split_sorter(generic_details[4])

    place = get_place_string(finding_id, cur)
    dkt["place"] = place

    if finding_id[0] in non_empty_roles:
        get_role_findings(dkt, finding_id[0], cur, current_person)

    if finding_id[0] in non_empty_notes:
        get_note_findings(dkt, finding_id[0], cur, current_person)

    cur.execute(select_count_finding_id_sources, finding_id)
    source_count = cur.fetchone()[0]
    dkt["source_count"] = source_count

    findings_data[finding_id[0]] = dkt

def get_couple_findings(
        cur, current_person, rowtotype, findings_data, 
        non_empty_roles, non_empty_notes):

    couple_kin_type_ids = get_couple_kin_types()
    curr_per_kin_types = tuple([current_person] + couple_kin_type_ids)
    sql =   '''
                SELECT finding_id 
                FROM findings_persons 
                WHERE person_id1 = ?
                    AND kin_type_id1 in ({})
            '''.format(
                ','.join('?' * (len(curr_per_kin_types) - 1)))
    cur.execute(sql, curr_per_kin_types)
    couple_findings1 = [i[0] for i in cur.fetchall()]
    sql =   '''
                SELECT finding_id 
                FROM findings_persons 
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
            if gotgot[0] == current_person:
                dkt["age"] = gotgot[1]
                dkt["kin_type"] = gotgot[2]
                dkt["partner_id"] = gotgot[3]
                dkt["partner_kin_type"] = gotgot[5]
                dkt["partner_name"] = get_name_with_id(gotgot[3])
            elif gotgot[3] == current_person:
                dkt["age"] = gotgot[4]
                dkt["kin_type"] = gotgot[5]
                dkt["partner_id"] = gotgot[0]
                dkt["partner_kin_type"] = gotgot[2]
                dkt["partner_name"] = get_name_with_id(gotgot[0])

        cur.execute(select_findings_details_couple_generic, finding_id)
        couple_generics = list(cur.fetchone())
        couple_generics[1] = format_stored_date(couple_generics[1], date_prefs)
        # couple_generics[1] = format_stored_date(couple_generics[1])
        place = get_place_string(finding_id, cur)
        dkt["place"] = place
        sorter = split_sorter(couple_generics[2])
        couple_generic_details = [
            couple_generics[0], 
            couple_generics[1], 
            sorter,  
            couple_generics[3]]

        if finding_id[0] in non_empty_roles:
            get_role_findings(dkt, finding_id[0], cur, current_person)

        if finding_id[0] in non_empty_notes:
            get_note_findings(dkt, finding_id[0], cur, current_person)

        cur.execute(select_count_finding_id_sources, finding_id)
        source_count = cur.fetchone()[0]
        dkt["source_count"] = source_count

        dkt["event"], dkt["date"], dkt["sorter"], dkt["particulars"] = couple_generic_details
        findings_data[finding_id[0]] = dkt

    return couple_findings

def get_birth_findings(
        dkt, cur, current_person, findings_data, non_empty_roles, non_empty_notes):
    cur.execute(select_finding_id_birth, (current_person,))
    birth_id = cur.fetchone()
    parents = (None, None)
    if birth_id:
        cur.execute(select_person_id_kin_types_birth, birth_id)
        parents = cur.fetchone()
    if not parents:
        pass
    elif parents[1] == "mother":
        dkt["mother_id"] = parents[0]
        dkt["mother_name"] = get_name_with_id(parents[0])
        dkt["father_id"] = parents[2]
        dkt["father_name"] = get_name_with_id(parents[2])
    elif parents[3] == "mother":
        dkt["father_id"] = parents[0]
        dkt["father_name"] = get_name_with_id(parents[0])
        dkt["mother_id"] = parents[2]
        dkt["mother_name"] = get_name_with_id(parents[2])

    cur.execute(select_finding_ids_age1_parents, (current_person,))
    children1 = [list(i) for i in cur.fetchall()]

    cur.execute(select_finding_ids_age2_parents, (current_person,))
    children2 = [list(i) for i in cur.fetchall()]

    children = children1 + children2
    for lst in children:
        offspring_event_id = lst[0]
        cur.execute(select_person_id_birth, (offspring_event_id,))
        offspring = cur.fetchone()
        if offspring:
            lst.append(offspring[0])

    for lst in children:
        offspring_event_id, parent_age, child_id = lst
        cur.execute(select_findings_details_offspring, (child_id,))       
        offspring_details = cur.fetchone()

        child_name = get_name_with_id(child_id)

        sorter = split_sorter(offspring_details[1])
        date = format_stored_date(offspring_details[0], date_prefs)
        # date = format_stored_date(offspring_details[0])

        particulars = offspring_details[2]
        place = get_place_string((offspring_event_id,), cur)

        cur.execute(select_count_finding_id_sources, (offspring_event_id,))
        source_count = cur.fetchone()[0]      
        findings_data[offspring_event_id] = {}
        findings_data[offspring_event_id]["event"] = "offspring"
        findings_data[offspring_event_id]["date"] = date
        findings_data[offspring_event_id]["place"] = place
        findings_data[offspring_event_id]["particulars"] = particulars
        findings_data[offspring_event_id]["age"] = parent_age
        findings_data[offspring_event_id]["source_count"] = source_count
        findings_data[offspring_event_id]["child_id"] = child_id
        findings_data[offspring_event_id]["child_name"] = child_name
        findings_data[offspring_event_id]["sorter"] = sorter

        if offspring_event_id in non_empty_roles:
            get_role_findings(
                dkt, offspring_event_id, cur, current_person, 
                findings_data=findings_data)

        if offspring_event_id in non_empty_notes:
            get_note_findings(
                dkt, offspring_event_id, cur, current_person, 
                findings_data=findings_data)

def get_role_findings(
    dkt, finding_id, cur, current_person, findings_data=None):
    current_roles = []
    current_roles.append(finding_id)
    if findings_data is None:
        dkt["roles"] = current_roles
    else: 
        findings_data[finding_id]["roles"] = current_roles

def get_note_findings(
    dkt, finding_id, cur, current_person, findings_data=None):
    current_notes = []
    current_notes.append(finding_id)
    if findings_data is None:
        dkt["notes"] = current_notes
    else:
        findings_data[finding_id]["notes"] = current_notes

def get_findings():
    
    findings_data = {}
    current_person = get_current_person()
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    rowtotype = {
        "event": "", "date": "", "place": "", "particulars": "", "age": ""}

    cur.execute(select_all_findings_current_person, (current_person,))
    generic_finding_ids = cur.fetchall()

    cur.execute(select_all_findings_roles_ids_distinct)
    non_empty_roles = [i[0] for i in cur.fetchall()]

    cur.execute(select_all_findings_notes_ids)
    non_empty_notes = [i[0] for i in cur.fetchall()]

    for finding_id in generic_finding_ids:
        dkt = dict(rowtotype)
        get_generic_findings(
            dkt, cur, finding_id, findings_data, 
            current_person, non_empty_roles, non_empty_notes)
        if dkt["event"] == "birth":
            get_birth_findings(
                dkt, cur, current_person, findings_data,
                non_empty_roles, non_empty_notes)

    couple_finding_ids = get_couple_findings(
        cur, current_person, rowtotype, findings_data, 
        non_empty_roles, non_empty_notes)

    cur.close()
    conn.close()  

    return findings_data, non_empty_roles, non_empty_notes

class EventsTable(Frame):

    instances = []

    def __init__(self, master, root, treebard, main, attrib=False, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.treebard = treebard
        self.main_window = main
        self.attrib = attrib

        self.main_canvas = main.master

        self.current_person = get_current_person()
        self.inwidg = None
        self.headers = []
        self.widths = [0, 0, 0, 0, 0]

        self.screen_height = self.winfo_screenheight()
        self.column_padding = 2
        self.new_row = 0
        event_types = get_all_event_types()
        self.event_autofill_values = EntryAuto.create_lists(event_types)
        self.after_death_events = get_after_death_event_types()
        if self.after_death_events is None:
            return
        self.events_only_even_without_dates = ["birth", "death"] + self.after_death_events

        self.root.bind(
            "<Control-S>", 
            lambda evt, curr_per=self.current_person: self.redraw(
                evt, current_person=curr_per))
        self.root.bind(
            "<Control-s>", 
            lambda evt, curr_per=self.current_person: self.redraw(
                evt, current_person=curr_per))

        self.place_strings = make_all_nestings(select_all_place_ids)

        self.make_header()
        self.make_table_cells()

    def get_initial(self, evt):
        self.initial = evt.widget.get()
        self.inwidg = evt.widget

    def get_final(self, evt):
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

    def delete_event(self, finding_id, widg, initial):

        def ok_delete_event():
            msg[0].destroy()
            self.focus_set()
            proceed(initial_value)

        def cancel_delete_event():
            msg[0].destroy()
            widg.insert(0, initial)
            widg.focus_set()

        def proceed(initial_value):

            def delete_generic_finding():
                cur.execute(delete_finding_places, (finding_id,))
                conn.commit()
                cur.execute(delete_findings_roles_finding, (finding_id,))
                conn.commit()
                cur.execute(delete_findings_notes_finding, (finding_id,))
                conn.commit()
                cur.execute(delete_claims_findings, (finding_id,))
                conn.commit()
                cur.execute(delete_finding, (finding_id,))
                conn.commit()

            def delete_couple_finding():
                cur.execute(delete_findings_persons, (finding_id,))
                conn.commit()
                delete_generic_finding()

            def delete_offspring_finding():
                cur.execute(select_findings_persons_parents, (finding_id,))
                parents = cur.fetchone()
                for person in parents:
                    cur.execute(delete_findings_persons_offspring, (finding_id,))
                conn.commit()       
                delete_generic_finding()

            current_person = self.current_person
            current_file = get_current_file()[0]
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
                if event_type == 1:
                    delete_offspring_finding()
                else:
                    delete_generic_finding()
            elif couple_event_old == 1:
                delete_couple_finding()
            self.redraw(current_person=current_person)
            cur.close()
            conn.close()

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        msg = open_yes_no_message(
            self, 
            events_msg[5], 
            "Delete Event Confirmation", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(command=ok_delete_event)
        msg[3].config(command=cancel_delete_event)

        initial_value = self.initial
        cur.close()
        conn.close()

    def update_db(self, widg, col_num):

        def update_event_type():

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

            def make_new_event_type():
                cur.execute(select_event_type_couple_bool, (self.initial,))
                couple = cur.fetchone()[0]

                cur.execute(
                    select_event_type_after_death_bool, (self.initial,))
                after_death = cur.fetchone()[0] 
                cur.execute(
                    insert_event_type_new, (
                        None, 
                        self.final, couple, after_death))
                conn.commit() 
                event_types = get_all_event_types()
                self.event_autofill_values = EntryAuto.create_lists(event_types)
                self.event_input.values = self.event_autofill_values

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
                    msg4 = open_error_message(
                        self, 
                        events_msg[4], 
                        "Incompatible Event Type Error", 
                        "OK")
                    msg4[0].grab_set()
                    msg4[1].config(aspect=400)
                    msg4[2].config(command=err_done5)
                    return

                if couple_event_new in (0, 1):
                    cur.execute(update_event_types, (event_type_id, self.finding))
                    conn.commit() 
                else:
                    print("line", looky(seeline()).lineno, "case not handled:")
            initval = self.initial
            event_types = get_all_event_types()
            self.final = self.final.strip().lower()
            if (self.initial == 'offspring' and len(self.final) != 0):
                msg = open_error_message(
                    self, 
                    events_msg[3], 
                    "Offspring Event Edit Error", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(command=err_done4)
                return

            if self.final == 'offspring':
                msg = open_error_message(
                    self, 
                    events_msg[7], 
                    "Change to Offspring Event Error", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(command=err_done7)
                return
                
            if self.final in event_types:
                update_to_existing_type()
            elif len(self.final) == 0:
                initial = self.initial
                self.delete_event(self.finding, widg, initial)
            else:
                make_new_event_type()
                update_to_existing_type()

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

            cur.execute(update_finding_date, (self.final, sorter, self.finding))
            conn.commit()
            formatted_date = format_stored_date(self.final, date_prefs)
            # formatted_date = format_stored_date(self.final)
            widg.delete(0, 'end')
            widg.insert(0, formatted_date)
            for instance in EventsTable.instances:
                instance.redraw()

        def update_place():
            cur.execute(select_nesting_fk_finding, (self.finding,))
            nested_place = cur.fetchone()[0]
            self.final = ValidatePlace(
                self.root, 
                self.treebard,
                self.inwidg,
                self.initial,
                self.final,
                self.finding)

        def update_age(offspring_event, row):
            if event_string == "birth" and self.final not in (0, "0", "0d 0m 0y"):
                return
            if couple is False and offspring_event is False:
                cur.execute(update_finding_age, (self.final, self.finding))
                conn.commit() 
            else:
                cur.execute(select_findings_persons_person_id, (self.finding,))
                right_person = cur.fetchone()
                if right_person[0] == self.current_person:
                    cur.execute(
                        update_findings_persons_age1, 
                        (self.final, self.finding, self.current_person))
                elif right_person[1] == self.current_person:
                    cur.execute(
                        update_findings_persons_age2, 
                        (self.final, self.finding, self.current_person))
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
            update_particulars(self.final, self.finding)
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
                    else: couple = False
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
        self.place_autofill_values = EntryAuto.create_lists(self.place_strings)
        self.table_cells = []
        for i in range(int(qty/8)):
            row = []
            for j in range(8):
                if j < 5:
                    if j == 0:
                        cell = EntryAuto(
                            self, width=0,
                            autofill=True, 
                            # too early
                            values=self.event_autofill_values
)
                    elif j == 2:
                        cell = EntryAuto(
                            self, width=0, 
                            autofill=True, 
                            # too early
                            values=self.place_autofill_values
)
                    else:                        
                        cell = EntryAuto(self, width=0,)
                    cell.initial = ''
                    cell.final = ''
                    cell.finding = None
                    cell.bind('<FocusIn>', self.get_initial, add="+")
                    cell.bind('<FocusOut>', self.get_final, add="+")
                elif j == 5:
                    cell = LabelDots(self, RolesDialog, self.treebard, finding_row=None)
                elif j == 6:
                    cell = LabelDots(self, NotesDialog, self.treebard, finding_row=None)
                elif j == 7:
                    cell = LabelButtonText(
                        self,
                        width=8,
                        anchor='w',
                        font=formats['heading3'])
                row.append(cell)
            self.table_cells.append(row)
        self.new_event_frame = Frame(self)
        self.event_input = EntryAutoHilited(
            self.new_event_frame, 
            width=32, 
            autofill=True, 
            values=self.event_autofill_values)
        self.add_event_button = Button(
            self.new_event_frame, 
            text="NEW EVENT OR ATTRIBUTE", 
            command=self.make_new_event)
        self.set_cell_content()

    def set_cell_content(self):

        self.findings_data, current_roles, current_notes = get_findings()

        copy = dict(self.findings_data)
        self.attributes = {}
        for k,v in copy.items():        
            if v["event"] in self.events_only_even_without_dates:
                pass
            elif len(v["date"]) == 0:
                self.attributes[k] = v
                del self.findings_data[k]

        if self.attrib is True:
            self.findings_data = self.attributes

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

        self.show_table_cells()

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

        row_order = []
        for finding_id in self.findings_data:
            event_type = self.findings_data[finding_id]['event']
            if event_type == "birth":
                sorter = [-10000, 0, 0]
                row_order.append([finding_id, event_type, sorter])
            elif event_type == "death":
                sorter = [10000, 0, 0]
                row_order.append([finding_id, event_type, sorter])
            elif event_type in (self.after_death_events):
                pass
            else:
                sorter = self.findings_data[finding_id]['sorter']
                row_order.append([finding_id, event_type, sorter])

        row_order = sorted(row_order, key = lambda i: i[2])
        all_sorted = row_order + after_death
 
        new_order = []
        for lst in all_sorted:
            new_order.append(lst[0])
        return new_order

    def show_table_cells(self): 

        couple_event_types = get_couple_event_types()

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
                c += 1
            r += 1
        z = 0
        for widg in self.headers:
            if self.widths[z] < len(HEADS[z]):
                widg.config(width=len(HEADS[z]) + 2)
            else:
                widg.config(width=self.widths[z] + 2)
            z += 1

        self.fix_tab_traversal()
        for row_num in range(self.grid_size()[1]):
            self.grid_rowconfigure(row_num, weight=0)
        self.new_row = row_num + 1

        self.new_event_frame.grid(
            column=0, row=self.new_row, pady=6, columnspan=5, sticky='ew')
        self.event_input.grid(column=0, row=0, padx=(0,12), sticky='w')
        self.add_event_button.grid(
            column=1, row=0, sticky='w')

    def redraw(self, evt=None, current_person=None):
        if evt:
            self.current_person = current_person

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_person, (self.current_person,))
        conn.commit()
        cur.close()
        conn.close()
        self.forget_cells()
        self.new_row = 0 
        self.widths = [0, 0, 0, 0, 0]
        self.set_cell_content()
        self.resize_scrollbar(self.root, self.main_canvas)

    def resize_scrollbar(self, root, canvas):
        root.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    def forget_cells(self):
        self.update_idletasks()
        for lst in self.cell_pool:
            for widg in lst[1]:
                if widg.winfo_subclass() == 'EntryAuto':
                    widg.delete(0, 'end')
                elif widg.winfo_subclass() == 'LabelButtonText':
                    widg.config(text='')
                widg.grid_forget()
        self.event_input.grid_forget()
        self.add_event_button.grid_forget()

    def make_header(self):
        y = 0
        for heading in HEADS:
            head = LabelH3(self, text=heading.upper(), anchor='w')
            head.grid(column=y, row=0, sticky='ew')
            if y in (5, 6, 7):
                head.grid(column=y, row=0, sticky='ew')
            else:
                head.grid(column=y, row=0, sticky='ew')
            if y < 5:
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
        # if self.final == "----------":
            # self.final = "-0000-00-00-------"
        sorter = ",".join(sorter)
        return sorter

    def count_birth_death_events(self, new_event):
        too_many = False
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_findings_for_person, (self.current_person,))
        all_events = [i[0] for i in cur.fetchall()]
        if new_event in all_events:
            too_many = True
        cur.close()
        conn.close()
        return too_many

    def make_new_event(self):
        '''
            Disallow creation of second birth or death event, and
            otherwise proceed.
        '''

        def err_done6():
            self.event_input.delete(0, 'end')
            msg[0].destroy()
            self.focus_set()

        too_many = False
        new_event = self.event_input.get().strip().lower()
        if new_event in ("birth", "death"):
            too_many = self.count_birth_death_events(new_event)
        if too_many is True: 
            msg = open_error_message(
                self, 
                events_msg[6], 
                "Multiple Birth or Death Events", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(command=err_done6)
            return
        self.new_event_dialog = NewEventDialog(
            self.root, 
            self.treebard,
            self,
            new_event,
            self.current_person,
            self.place_strings,
            self.place_autofill_values,   
            self.redraw)
        self.event_input.delete(0, 'end')

class NewEventDialog(Toplevel):
    def __init__(
            self, master, treebard, events_table, new_event, 
            current_person, place_strings, place_autofill_values, 
            redraw, finding=None, ma_pa=False, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.root = master
        self.treebard = treebard
        self.events_table = events_table
        self.new_event = new_event
        self.current_person = current_person
        self.place_strings = place_strings
        self.place_autofill_values = place_autofill_values
        self.redraw = redraw
        self.finding = finding
        self.ma_pa = ma_pa

        self.place_dicts = None
        self.new_event_type = False
        self.never_mind = False

        self.new_kin_type_codes = [None, None]

        self.current_name = get_name_with_id(self.current_person)
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        people = make_all_names_list_for_person_select()        
        self.all_names = EntryAuto.create_lists(people)

        cur.execute(select_all_kin_ids_types_couple)
        self.kintypes_and_ids = [i for i in cur.fetchall()]
        self.kintypes_and_ids = sorted(self.kintypes_and_ids, key=lambda i: i[1])
        self.kin_types = [i[1] for i in self.kintypes_and_ids]

        self.focus_new_event_dialog()
        self.get_some_info()
        if self.new_event_type is False:
            self.make_widgets()

        cur.close()
        conn.close()

    def get_some_info(self):
        current_file = get_current_file()[0]
        conn =  sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_max_finding_id)
        self.new_finding = cur.fetchone()[0] + 1
        cur.execute(select_event_type_id, (self.new_event,))
        result = cur.fetchone()
        if result is not None:
            self.event_type_id, self.couple_event = result
        else:
            self.new_event_type = True
            cur.execute(select_max_event_type_id)
            self.event_type_id = cur.fetchone()[0] + 1            
            self.input_new_event_type()
        cur.close()
        conn.close()

    def ask_if_after_death(self):

        def ok_new_evt_type(conn, cur):

            evt_is_after_death = posthumousvar.get()
            cur.execute(insert_event_type_new, (
                self.event_type_id, 
                self.new_event, 
                self.couple_event, 
                evt_is_after_death))
            conn.commit()

            event_types = get_all_event_types()
            more_event_types = EntryAuto.create_lists(event_types)
            self.events_table.event_input.values = more_event_types

            self.asker.grab_release()
            self.asker.destroy()
            self.deiconify()
            self.focus_set() 
            self.lift()
            self.grab_set()

        def cancel_new_evt_type():
            nonlocal never_mind
            self.asker.grab_release()
            self.asker.destroy()
            never_mind = True

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        never_mind = False

        text = ( 
            "Before-death event type: e.g. 'promotion', "
            "'business venture', 'graduation'.",
            "After-death event type: e.g. 'funeral', 'probate', "
            "'reading of the will', 'posthumous ______'.")
        posthumousvar = tk.IntVar(None, 0)
        self.asker = Toplevel(self)
        self.asker.title("Select Before- or After-Death Event Type")
        lab = LabelH3(
            self.asker, 
            text="Does the new event type occur after death?")
        
        for i in range(2):
            rad = Radiobutton(
                self.asker,  
                text=text[i],
                value=i,
                variable=posthumousvar,
                anchor='w')
            rad.grid(column=0, row=i+1)

        buttonframe = Frame(self.asker)
        butt1 = Button(
            buttonframe, text="OK", width=6, 
            command=lambda conn, cur: ok_new_evt_type(conn, cur))
        butt2 = Button(
            buttonframe, text="CANCEL", width=6, 
            command=cancel_new_evt_type)

        lab.grid(column=0, row=0, pady=12)
        buttonframe.grid(column=0, row=3, sticky='e', pady=(0,12))
        butt1.grid(column=0, row=0, sticky='e', padx=12, pady=6)
        butt2.grid(column=1, row=0, sticky='e', padx=12, pady=6)
        self.asker.grab_set()
        butt1.focus_set()
        
        self.wait_window(self.asker)
        if never_mind is False:
            self.make_widgets()
        else:
            self.destroy()
        cur.close()
        conn.close()        

    def input_new_event_type(self):  

        def ask_next_question():
            self.couple_event = couplevar.get()
            id_couple_event.grab_release()
            id_couple_event.destroy()

        def input_evt_type_now():
            current_file = get_current_file()[0]
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            self.couple_event = couplevar.get()
            cur.execute(insert_event_type_new, (
                self.event_type_id, self.new_event, self.couple_event, 0))
            conn.commit()

            event_types = get_all_event_types()
            more_event_types = EntryAuto.create_lists(event_types)
            self.events_table.event_input.values = more_event_types

            cur.close()
            conn.close()

            self.make_widgets()
            self.deiconify()

        def cancel_new_evt_type():
            nonlocal never_mind
            id_couple_event.grab_release()
            id_couple_event.destroy()
            never_mind = True

        never_mind = False

        text = ( 
            "Generic event type: one primary participant or a parent, e.g. "
                "'birth', 'career', 'adopted a child'.",
            "Couple event type: two equal participants, e.g. 'marriage', "
                "'wedding', 'engagement'.")
        couplevar = tk.IntVar(None, 0)
        id_couple_event = Toplevel(self.root)
        id_couple_event.title("Select Couple or Generic Event Type")
        self.withdraw()
        id_couple_event.grab_set()

        lab = LabelH3(
            id_couple_event, 
            text="Is the new event type a couple event?")
        
        for i in range(2):
            rad = Radiobutton(
                id_couple_event,  
                text=text[i],
                value=i,
                variable=couplevar,
                anchor='w')
            rad.grid(column=0, row=i+1)

        buttonframe = Frame(id_couple_event)
        butt1 = Button(
            buttonframe, text="OK", width=6, 
            command=ask_next_question)
        butt2 = Button(
            buttonframe, text="CANCEL", width=6, 
            command=cancel_new_evt_type)

        lab.grid(column=0, row=0, pady=12)
        buttonframe.grid(column=0, row=3, sticky='e', pady=(0,12))
        butt1.grid(column=0, row=0, sticky='e', padx=12, pady=6)
        butt2.grid(column=1, row=0, sticky='e', padx=12, pady=6)
        butt1.focus_set()
        
        self.wait_window(id_couple_event)
        if never_mind is False:
            if self.couple_event == 0:
                self.ask_if_after_death()
            else:
                input_evt_type_now()
        else:
            self.destroy()

    def make_widgets(self):

        def show_message():
            window.columnconfigure(1, weight=1)
            window.rowconfigure(1, weight=1)
            self.new_evt_msg = MessageHilited(
                window, 
                justify='left', 
                aspect=1200)
            self.new_evt_msg.grid(column=1, row=1, sticky='news', ipady=18)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        canvas = Border(self)

        canvas.title_1.config(text="New Event Dialog")
        canvas.title_2.config(text="Current Person: {}, id #{}".format(
            self.current_name, self.current_person))

        window = Frame(canvas)
        canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.treebard.scroll_mouse.append_to_list([canvas, window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        window.vsb = Scrollbar(
            self, 
            hideable=True, 
            command=canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            self, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        buttonbox = Frame(window)
        self.b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=self.cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        window.columnconfigure(2, weight=1)
        window.rowconfigure(1, minsize=60)
        buttonbox.grid(column=1, row=3, sticky='se', pady=6)

        self.b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.frm = Frame(window)
        self.frm.grid(column=1, row=2, sticky='news', pady=12)
        self.frm.columnconfigure(0, weight=1)
        show_message()
        self.make_inputs()

        resize_scrolled_content(self, canvas, window)

    def make_inputs(self):

        def err_done8():
            msg[0].destroy() 
            self.destroy()            

        self.offspring_input = None
        self.parent1_input = None
        self.kin_type_input1 = None
        self.other_person_input = None
        self.age2_input = None
        self.kin_type_input2 = None

        self.generic_data_inputs = Frame(self.frm)
        self.couple_data_inputs = Frame(self.frm)
        more = Label(
            self.frm, 
            text="Roles, Notes & Sources can be created and "
                "edited in the events table.")

        self.generic_data_inputs.grid(column=0, row=0, sticky="news")
        self.couple_data_inputs.grid(column=0, row=2, sticky='news')
        more.grid(column=0, row=4, columnspan=2, sticky="ew", pady=(12,0))
        
        self.lab0 = LabelH3(
            self.generic_data_inputs, text="Event Type: {}".format(
                self.new_event))
        lab1 = Label(self.generic_data_inputs, text="Date")
        self.date_input = EntryHilited1(self.generic_data_inputs)
        lab2 = Label(self.generic_data_inputs, text="Place")
        self.place_input = EntryAutoHilited(
            self.generic_data_inputs, 
            width=48, autofill=True, values=self.place_autofill_values)
        self.place_input.bind("<FocusOut>", self.validate_place)
        lab3 = Label(self.generic_data_inputs, text="Particulars")
        self.particulars_input = EntryHilited1(
            self.generic_data_inputs, width=60)

        self.lab0.grid(column=0, row=0, sticky="w", pady=6)
        lab1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.date_input.grid(column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        lab2.grid(column=0, row=2, sticky="e", pady=(0,1))
        self.place_input.grid(
            column=1, row=2, sticky="w", padx=(3,0), pady=(0,1))
        lab3.grid(column=0, row=3, sticky="e")
        self.particulars_input.grid(column=1, row=3, sticky="w", padx=(3,0))
        if self.couple_event == 0:
            self.b1.config(command=self.add_event)
            if self.ma_pa is True:
                self.show_other_person()
            elif self.new_event == "offspring":
                msg = open_error_message(
                    self, 
                    events_msg[8], 
                    "Offspring Event Creation Error", 
                    "OK") 
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(command=err_done8)
                return           
            else:
                self.show_one_person()
        elif self.couple_event == 1:
            self.show_other_person()
            self.b1.config(command=self.validate_kin_types)       

        self.focus_first_empty()

    def show_one_person(self):
        self.new_evt_msg.config(text="Information about the new event "
            "relating to the current person.")
        age1 = Label(self.generic_data_inputs, text="Age")
        self.age1_input = EntryHilited1(self.generic_data_inputs, width=6)

        self.generic_data_inputs.columnconfigure(0, weight=1)
        age1.grid(column=0, row=4, sticky="e", pady=(0,1))
        self.age1_input.grid(
            column=1, row=4, sticky="w", padx=(3,0), pady=(0,1))
        
        self.lab0.config(text="Event Type: {} ({})".format(
            self.new_event,
            self.current_name))
        self.lab0.grid_configure(columnspan=2)

    def show_other_person(self):

        def radio_reflex():
            parent_type = self.offspringvar.get()
            if parent_type == 1:
                self.mother_or_father.config(text="father")
            elif parent_type == 2:
                self.mother_or_father.config(text="mother")

        self.new_evt_msg.config(text="Information about the new event "
            "relating to the current person and other primary participants "
            "in the event.")
        sep1 = Separator(self.frm, width=3)
        sep2 = Separator(self.frm, width=3)
        sep1.grid(column=0, row=1, columnspan=2, sticky="ew", pady=(12,0))
        sep2.grid(column=0, row=3, columnspan=2, sticky="ew", pady=(12,0))

        name1 = Label(self.couple_data_inputs, text=self.current_name)
        parent1 = Label(self.couple_data_inputs, text="mother")
        offspring = Label(self.couple_data_inputs, text="Name of Child")
        self.parent1_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, 
            autofill=True, values=self.all_names)
        self.offspring_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, 
            autofill=True, values=self.all_names)
        self.offspring_input.bind(
            "<FocusOut>", 
            lambda evt, widg=self.offspring_input: self.catch_dupe_or_new_person(
                evt, widg))
        age1 = Label(self.couple_data_inputs, text="Age")
        self.age1_input = EntryHilited1(self.couple_data_inputs, width=6)
        kin_type1 = Label(self.couple_data_inputs, text="Kin Type")
        self.kin_type_input1 = Combobox(
            self.couple_data_inputs, self.root, values=self.kin_types)
        mother_is_it = LabelHilited(self.couple_data_inputs, text="mother")
        self.mother_or_father = LabelHilited(
            self.couple_data_inputs, text="(current person)")

        spacer = Frame(self.couple_data_inputs)

        name2 = Label(self.couple_data_inputs, text="Partner")
        self.other_person_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, autofill=True, 
            values=self.all_names)
        self.other_person_input.bind(
            "<FocusOut>", 
            lambda evt, widg=self.other_person_input: self.catch_dupe_or_new_person(
                evt, widg))

        age2 = Label(self.couple_data_inputs, text="Age")
        self.age2_input = EntryHilited1(self.couple_data_inputs, width=6)
        kintype2 = Label(self.couple_data_inputs, text="Kin Type")
        self.kin_type_input2 = Combobox(
            self.couple_data_inputs, self.root, values=self.kin_types)
        radframe = Frame(self.couple_data_inputs)
        father_is_it = LabelHilited(self.couple_data_inputs, text="father")

        if self.new_event == "offspring":
            self.ma_pa = True
            self.lab0.config(
                text="offspring (child of {})".format(self.current_name))
            age1.config(text="Current Person Age")
            offspring.grid(column=0, row=0, sticky='e', pady=(9,1))
            self.offspring_input.grid(
                column=1, row=0, sticky='w', padx=(3,0), pady=(9,1))
            self.mother_or_father.grid(
                column=1, row=2, sticky="w", padx=(2,0), ipadx=1)
            radframe.grid(column=4, row=2, sticky="w", padx=(2,0))
            self.offspringvar = tk.IntVar(None, 0)
            pardlabs = ("mother", "father")
            for i in range(2):
                rad = Radiobutton(
                    radframe,  
                    text=pardlabs[i],
                    value=i+1,
                    variable=self.offspringvar,
                    anchor='w',
                    command=radio_reflex)
                rad.grid(column=i, row=0)
        elif self.ma_pa is False:
            name1.grid(column=0, row=0, sticky="w", columnspan=2, pady=(9,1))
            self.kin_type_input1.grid(column=1, row=2, sticky="w", padx=(2,0))
            self.kin_type_input2.grid(column=4, row=2, sticky="w", padx=(2,0))
        else:
            parent1.grid(column=0, row=0, sticky='e', pady=(9,1))
            self.parent1_input.grid(
                column=1, row=0, sticky='w', padx=(3,0), pady=(9,1))
            name1.config(text="mother")
            name2.config(text="father")
            mother_is_it.grid(column=1, row=2, sticky="w", padx=(2,0), ipadx=1)
            father_is_it.grid(column=4, row=2, sticky="w", padx=(2,0), ipadx=1)
        age1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.age1_input.grid(
            column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        kin_type1.grid(column=0, row=2, sticky="e")

        self.couple_data_inputs.columnconfigure(2, weight=1)
        spacer.grid(column=2, row=0, sticky="news", rowspan=3)

        name2.grid(column=3, row=0, sticky="e", pady=(9,1))
        self.other_person_input.grid(
            column=4, row=0, sticky="w", padx=(3,0), pady=(9,1))
        age2.grid(column=3, row=1, sticky="e", pady=(0,1))
        self.age2_input.grid(column=4, row=1, sticky="w", padx=(3,0), pady=(0,1))
        kintype2.grid(column=3, row=2, sticky="e", padx=(9,0)) 

    def cancel(self):
        self.root.focus_set()
        self.root.lift()
        self.destroy()

    def add_event(self):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        self.age_1 = self.age1_input.get()
        if self.couple_event == 1:
            self.age_2 = self.age2_input.get()
            self.other_person = self.other_person_input.get()

        if self.couple_event == 0:
            cur.execute(
                insert_finding_new, (
                    self.new_finding, self.age_1, 
                    self.event_type_id, self.current_person))
            conn.commit()            
        else:
            cur.execute(
                insert_finding_new_couple, 
                (self.new_finding, self.event_type_id,))
            conn.commit()

            self.couple_ok(cur, conn) 
        if len(self.place_string) == 0:
            cur.execute(insert_finding_places_new, (self.new_finding,))
            conn.commit()
        else:
            self.update_db_place(conn, cur)

        new_event_date = validate_date(
            self.root,
            self.date_input,
            self.date_input.get())
        if not new_event_date:
            new_event_date = "-0000-00-00-------"

        sorter = self.events_table.make_date_sorter(new_event_date)

        if new_event_date == "----------":
            new_event_date = "-0000-00-00-------"

        cur.execute(update_finding_date, (new_event_date, sorter, self.new_finding))
        conn.commit()

        update_particulars(
            self.particulars_input.get().strip(), self.new_finding)        

        cur.close()
        conn.close()
        self.cancel()
        for instance in EventsTable.instances:
            instance.redraw(current_person=self.current_person)

    def couple_ok(self, cur, conn):                
        if len(self.other_person) != 0:
            other_person_all = self.other_person.split(" #")
            other_person_id = other_person_all[1]
        else:
            other_person_id = None

        self.talk_to_db(other_person_id, conn, cur)
        self.create_birth_event(other_person_id, cur, conn)


    def create_birth_event(self, child_id, cur, conn):

        cur.execute(select_max_finding_id)
        new_finding = cur.fetchone()[0] + 1
        cur.execute(insert_finding_birth, (new_finding, child_id))
        conn.commit()
        cur.execute(insert_finding_places_new, (new_finding,))
        conn.commit()
        return new_finding

    def focus_first_empty(self):
        for widg in (
                self.date_input, self.place_input, self.particulars_input, 
                self.offspring_input, self.parent1_input, self.age1_input, 
                self.kin_type_input1, self.other_person_input, self.age2_input, 
                self.kin_type_input2):
            if widg:
                filled_in = widg.get()
                if len(filled_in) == 0:
                    widg.focus_set()
                    break

    def talk_to_db(self, other_person_id, conn, cur):
        self.make_new_kin_type(cur, conn)
        cur.execute(
            insert_findings_persons_new_couple,
            (self.new_finding, self.current_person, self.age_1, 
                self.kin_type_list[0][0], other_person_id, self.age_2, 
                self.kin_type_list[1][0]))
        conn.commit()

    def make_new_kin_type(self, cur, conn):
        self.kin_type_list = list(
            zip(self.kin_type_list, self.new_kin_type_codes))
        self.kin_type_list = [list(i) for i in self.kin_type_list]
        for item in self.kin_type_list:
            if item[1] is None:
                continue
            else:
                cur.execute(
                    insert_kin_type_new, 
                    (item[0], item[1].get()))
                conn.commit()
                cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'kin_type'")
                new_id = cur.fetchone()[0]
                item[0] = new_id 

    def update_db_place(self, conn, cur):
        if self.place_dicts is None: return

        ids = []
        for dkt in self.place_dicts:            
            ids.append(dkt["id"])
        qty = len(self.place_dicts)
        nulls = 9 - qty
        ids = ids + [None] * nulls
        last = len(self.place_dicts) - 1
        q = 0
        for dkt in self.place_dicts:
            child = dkt["id"]
            if q < last:
                parent = self.place_dicts[q+1]["id"]
            else:
                parent = None
            if child == dkt["temp_id"]:
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

        ids.append(self.new_finding)

        cur.execute(insert_finding_places_new_event, tuple(ids))
        conn.commit()

        self.place_strings.insert(0, self.place_string)

        self.place_autofill_values = EntryAuto.create_lists(self.place_strings)

    def validate_kin_types(self):

        def err_done2(widg):
            msg[0].destroy() 
            self.grab_set()
            widg.focus_set()

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        self.kin_type_list = [
            self.kin_type_input1.get(), self.kin_type_input2.get()]

        new_kin_types = []
        for kin_type_input in [self.kin_type_input1, self.kin_type_input2]:
            if len(kin_type_input.get()) == 0:
                msg = open_error_message(
                    self, 
                    events_msg[1], 
                    "No Kin Type Selected", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(
                    command=lambda widg=kin_type_input: err_done2(widg))
                return
        v = 0
        for item in self.kin_type_list:
            if item in self.kin_types:
                k = 0
                for stg in self.kin_types:
                    if stg == item:
                        idx = k
                        self.kin_type_list[v] = self.kintypes_and_ids[idx][0]
                    k += 1
                new_kin_types.append(None)
            else:
                if type(item) is not int and len(item) != 0:
                    new_kin_types.append(item)            
            v += 1
        if new_kin_types != [None, None]:
            self.new_kin_type_codes = NewKinTypeDialog(
                self.root,
                new_kin_types,
                self).show()

        cur.close()
        conn.close()
        self.add_event()

    def catch_dupe_or_new_person(self, evt, input_widget):

        def err_done(): 
            input_widget.focus_set()
            input_widget.delete(0, 'end')
            self.grab_set()
            msg[0].destroy()
        person_and_id = input_widget.get().split("#")
        if len(person_and_id[0]) == 0: 
            return
        elif len(person_and_id) == 1:
            new_partner = open_new_person_dialog(self, input_widget, self.root)
            self.validate_kin_types()
        elif self.current_person == int(person_and_id[1]):
            msg = open_error_message(
                self, 
                events_msg[0], 
                "Duplicate Persons in Couple", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(command=err_done)  

    def validate_place(self, evt):
        inwidg = evt.widget
        self.place_string = inwidg.get().strip()
        if len(self.place_string) == 0:
            return
        place_validator = ValidatePlace(
            self.root, 
            self.treebard,
            inwidg,
            '',
            self.place_string,
            self.new_finding)
        self.place_dicts = place_validator.input_new_event()
        self.place_autofill_values.insert(0, inwidg.get())
        if place_validator.new_place_dialog is not None:
            self.place_validator = place_validator.new_place_dialog.new_places_dialog
            self.place_validator.bind("<Destroy>", self.focus_new_event_dialog)
            self.place_validator.grab_set()

    def focus_new_event_dialog(self, evt=None):
        self.grab_set()
        self.lift()

class NewKinTypeDialog(Toplevel):

    def __init__(
            self, master, new_kin_types,  
            new_event_dialog, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.root = master
        self.new_event_dialog = new_event_dialog

        self.kinradvars = [None, None]

        self.title("New Kin Types Dialog")
        self.columnconfigure('all', weight=1)
        self.make_widgets()
        column = 0
        for item in new_kin_types:
            self.make_widgets_for_one(item, column)            
            column += 1
        self.grab_set()

    def make_widgets(self):
        buttons = Frame(self)
        buttons.grid(column=0, row=1, columnspan=2, sticky='e')
        ok_rads = Button(buttons, text="OK", command=self.ok_new_kin_type)
        ok_rads.grid(column=0, row=0, padx=12, pady=12)
        cancel_rads = Button(buttons, text="CANCEL", command=self.cancel_new_kin_type)
        cancel_rads.grid(column=1, row=0, padx=12, pady=12)

    def make_widgets_for_one(self, item, column): 
        if item is None:
            return
        radframe = Frame(self)
        radframe.grid(column=column, row=0, sticky="news", padx=12, pady=(6,0))
        radios = []
        radvar = tk.StringVar(None, "B")
        self.kinradvars[column] = radvar
        head = LabelH3(radframe, text="Create new kin type: {}".format(item))
        head.grid(column=0, row=0, padx=12, pady=(6,0))
        instrux = Label(radframe, text="Describe this kin type's role:")
        instrux.grid(column=0, row=1, padx=12, pady=(6,0))
        kinrads = [
            ("parent", "B"), ("sibling", "C"), 
            ("partner", "D"), ("child", "E")]
        d = 2
        for tup in kinrads:
            rad = Radiobutton(
                radframe, 
                text=tup[0], 
                variable=radvar,
                value=tup[1],
                anchor="w")
            rad.grid(column=0, row=d, sticky='we', padx=12, pady=(6,0))
            radios.append(rad)  
            d += 1
        d = d
        radios[0].focus_set()

    def show(self):
        self.root.wait_window(self)
        return self.kinradvars        

    def ok_new_kin_type(self):
        self.destroy()
        self.cancel_new_kin_type()

    def cancel_new_kin_type(self):
        self.grab_release()
        self.new_event_dialog.focus_set()
        self.new_event_dialog.lift()
 
short_values = ['red', 'white', 'blue', 'black', 'rust', 'pink', 'steelblue']

if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('+800+300')

    strings = make_all_nestings(select_all_place_ids)
    place_autofill_values = EntryAuto.create_lists(strings)

    auto = EntryAuto(root, width=50, autofill=True, values=place_autofill_values)


    auto.focus_set()   

    move = tk.Entry(root)

    auto.grid()
    move.grid()

    root.mainloop()


# DO LIST

# BRANCH: front_page
# Then split get_current_tree into 4 procedures and stop with the if/else confusion.
# 1) done
# 2) done except to open the dlg at the bottom of files.py which shd be finished/improved
# 3) when opening a file with the dialog, who cares what the prior file was? My reason for running get_current_file was probably not very good back when I wrote this code. A missing file will not be available in the dialog.
# 4) when creating a new file, again the prior file and missing file are irrelevant.
# THE ONLY WAY TO PROCEED IS TO FOCUS ON ONE PROCEDURE AT A TIME AND KEEP THE CODE SEPARATE FOR THE FOUR PROCEDURES ABOVE. START WITH THE SIMPLEST. don't mix these 4 procedures together and then try to tease them apart with if/else.

# rolled back to last night's version since everything I did today was wrong. First thing to do is delete the section that deals with missing files since it doesn't work right and introduces bugs that are hard to find. Then get rid of the global. Then create a new tree and delete it manually and follow the error messages. Create one line of code at a time and test after each change. The goal is to just open a message when a file doesn't exist and tell the user the right way to delete files. The other goal is to rethink this and keep it simple.
# test the feature which creates a new tree from the default tree if the user has deleted a file outside of treebard's controls see files.py valid_dummy THIS WORKS which you can test by making a change to the tree. But close and reopen it, and the change (I tried changing current person) doesn't show. But close and reopen it a second time, and it does. OR SOMETHING LIKE THAT. It is flaky and instead of patching it up I have to rethink it and come up with a better solution. Auto-replace it? And open a dlg telling the user to delete it correctly? And giving a button to do so right on the dlg? As a CONFIRM button; not telling the user what/why/how but by auto-replace I mean putting a copy of the default tree in its place with the same name. This is OK for now but has to be fixed right away. The main idea is that if the absence of a needed filename is ever detected, flaky patches go into effect and that should be cut off at the pass.
# retest click pick to open prior tree
# when you press Open button then Cancel, sample tree opens (or is this bec I deleted some files manually?)
# add a parameter to pass current_person to Main on instantiation, it shd never be None
# try to move open_input_message() from files.py to messages.py by making if a parameter of new_tree() where it's called in opening.py
# remove stuff from default tree both copies same so it's a real default tree for starting new trees with, and start a real new tree
# get the file commands to work from the opening window except gedcom which shd open a standard message "this feature is not complete. Please visit proboards if you would like to assist in creating this feature."
# get rid of globals in files.py
# fix the same menu and icon commands that already work from the opening dialog as well as Recent Files which could be columns in closing_state?
# make big pic change or something so user knows when it's in focus so spacebar will be easy to use for non mousers when opening last used file? and/or just start with the pic in focus so spacebar is ready
# change all dialogs to Border class
# I think in names.py the StatusBar is being imported and instantiated redundantly or is it that the Border class hasn't been used there yet?
# TEST every functionality due to recent restructuring
# possibly the need for a 2nd db was mistaken as I have been turning off the new stuff and everything still works so find all references to global_db_path and see what happens if they're turned off one by one APPARENTLY IT'S ONLY NEEDED FOR CLOSING STATE AND NOT AT ALL FOR FORMATS. But what if it works different when I'm not just opening the last-opened file? In that case, SOLUTION IS TO ACCESS THE DEFAULTS IN opening.py AND PUT EVERYTHING ELSE BACK THE WAY IT WAS. 
# delete columns openpic_dir, default_openpic_dir from setting in .tbd, it has to be in treebard.db
# have to keep a global copy of place tables or just move them to treebard.tbd. Maybe better to have a function that imports places from any given tree but both techniques have their drawbacks. Wait till make_new_tree is working so this can be tested while it's being written.
# dates prefs tab, get rid of ttk comboboxes
# Test ALL COLOR SCHEMES AND DELETE THE COLOR SCHEMES THAT ARE NO GOOD--THE BORDER around a dialog HAS TO MAKE THE DISTINCTION BETWEEN MAIN APP AND A DIALOG--HAVE TO SET built_in TO 0 before delete will work
# get all main tabs back into working order
# add Border/scrollbar to roles/notes dlg & other dlg in case someone is using big fonts on small screen
# in main.py make_widgets() shd be broken up into smaller funx eg make_family_table() etc.
# statustips and rcm in search dialog and new person dialog and other recent dialogs; tooltip in attributes table says that adding a date will move the attrib to evts table
# fix Border so that title bar changes color when not on top or in focus

# BRANCH: pedigree
# INSTEAD OF MAKING kintips for event column only to say child, spouse name not parents bec we have only 2 parents and it's redundant info (on the same page) but since there can be more than one spouse or child, it is important to make kintips for event rows re: child or spouse only DO THIS INSTEAD: since it's still redundant info, with the same info in a table up top (not even started), just highlight the spouse or child in the top table as the mouse hovers over them. Don't make it like gbx. The spouse should be WITH the relevant children and both families in the case of 2 spouses shd be visible at the same time with the 2 spouses also visible at the same time. ALSO if the highlighted row is not visible on the screen, it appears as a tooltip instead so user can always see it.

# BRANCH: names_images
# redo names tab so it's not about making new person
# in save_new_name() in names.py, how to indicate whether the image is supposed to be main_image (1) vs (0) which is now the default in the insert query to images_entities; if already a main_image it has to be changed to 0 programmatically
# don't let a default image be entered (see NEW PERSON DLG) if a non-default image already exists for that person; if the person already has a default image, it can be changed to a different default image, a real image, or to no image; think of other cases to handle
# If user selects his own photo as default, prepend "default_image_" to user's file name.
# If no main_image has been input to db, tbard will use no image or default image selected by user. User can make settings in images/prefs tab so that one photo is used as default for all when no pic or can select one for F and one for M, one for places, one for sources. tbard will provide defaults which user can change. There's no reason to input a default_image_ placeholder image as anything but a main_image so make it impossible.

# BRANCH: fonts
# when changing font, window/scrollbar don't resize till reloaded; see notes in fonts_picker; when fixed get rid of the message
# on change of font size: dropdown font doesn't resize instantly; font size on roles/notes dialogs esp headers doesn't resize instantly

# BRANCH: sources
# IDEA for copy/pasting citations. This is still tedious and uncertain bec you never know what's in a clipboard, really. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, maybe a C for Copy, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys. If this idea isn't practical, it still leads to the notion of a tabular display of citations which would make copy & paste very easy instead of showing citations a click apart from each other, and seeing them all together might be useful for the sake of comparison?
# edit ReadMe
# figure out how to dump db as a text file so it can be pushed to github, first delete any unused tables
# post new screenshots
# edit official do list
# website: change "units of genealogy" to "elements of genealogy"
# write blog post "refactor finished"

# BRANCH: post_refactor
# add to main do list
# make sure there's a way to make new person, new name, new place
# add functionality to place tab & source tab for alias and edit/delete 
# refactor date calculator
# menu: add functionality to obvious menu choices incl. add new person, add/edit name, and others 
# combobox: when scrolling if the mouse strays off the scrollbar the dropdown undrops, I've seen a way to fix that but what was it?
# add to main do list re: all dialogs: run the same code when clicking X on title bar
# add to do list for new_event dialog: add person search button 
# events_table:
# add tooltips/status bar messages
# get rid of ttk combobox in new person dialog 
# incorporate config_generic all dialogs
# replace windows border on all dialogs see new event dialog for example
# notes dialog:
# get all error messages from messages.py
# rc_menu--need access to the referenced widgets but they're made inside of functions.
# add statusbar messages




# ADD TO DEV DOCS FOR EVENTS TABLE.PY: is it possible to get rid of persons_persons table? There seems to be a one-to-one relationship between the finding_id in a couple event and the persons_persons_id in that event. So look at what persons_persons is being used for. Can the finding_id be used instead? Seems like they aren't exactly the same thing because finding_id has 2 records in findings_persons for each event where the two people are related, but 1 record in persons_persons. Try to remember why I created this table to begin with. Something to do with ??? I have no idea but it's very recent so shd have left a trail of blather in some rollback with the rationale behind this annoying data item. Look at August rollbacks for a hint. For ex on aug 28 I wrote "But let's say you want to search how many 2 people are linked to each other. This would be a very simple search if each event in which the 2 are coupled is a separate persons_persons_id.) Another question: have I put the fk in the wrong table? Now I'm putting persons_persons_id in findings_persons table. Should I instead be putting finding_id in persons_persons table? Then there's a directly discernible reason for each row in the p_P table to exist instead of just these 2 mysterious columns. But it would be a drastic redesign to move finding_id to persons_persons out of findings_persons where it is now and it seems like I'm very close to making the code work, since it already works for same-name couple (spouse/spouse), all I need is to make the code work for diff-name couples (wife/husband) and since it's already close, I shd resist the temptation to rip the building down to the foundations, change the foundations, and start over completely because that's what I'd have to do, I'd have to refactor the events_table code again and I kinda refuse." But what was the original reason to make the table? Here it is, same day: "select_findings_details_couple is inadequate since it looks for pairs of matched kin_type_id but wife & husband have different ids whereas spouse & spouse have the same. Need a better way to select partnerships eg maybe a new table called couples so that each coupling will have a separate couple_id (persons_persons_id). It should be a table called persons_persons because it is many to many, each person can have any number of links to each other person including more than one link to the same person in case the same couple gets married twice etc. Then put fk persons_persons_id in findings_persons. The persons_persons table might be useful for other relationship problems later on such as people with real parents, foster parents, and adoptive parents for example." So in short, the problem I was having was that I was doing something by searching for matching kin type to find spouses, but this didn't work eg with "wife" and "husband" because the kin types didn't match. So I had to register the relationship as a single record in a table to easily detect the relationship.









