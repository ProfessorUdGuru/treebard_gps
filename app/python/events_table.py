# events_table.py

import tkinter as tk
import sqlite3
from files import get_current_file
from window_border import Border, Dialogue 
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, Radiobutton,
    LabelH3, Button, Entry, EntryHilited1, LabelHeader, LabelHilited,
    LabelNegative)
from autofill import EntryAuto, EntryAutoHilited
from dates import validate_date, format_stored_date, OK_MONTHS, get_date_formats
from nested_place_strings import make_all_nestings
from toykinter_widgets import Separator, run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from messages_context_help import new_event_dlg_help_msg
from styles import config_generic, make_formats_dict
from persons import (
    make_all_names_dict_for_person_select, EntryAutoPersonHilited, check_name, 
    get_original, open_new_person_dialog, update_person_autofill_values,
    EntryAutoPerson)
from roles import RolesDialog
from notes import NotesDialog
from places import ValidatePlace, get_all_places_places
from scrolling import Scrollbar, resize_scrolled_content
from messages import open_message, events_msg, open_yes_no_message
from utes import split_sorter
    
from query_strings import (
    select_finding_places_nesting, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_type_ids_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple, select_findings_details_couple_generic,
    select_finding_id_birth, select_person_ids_kin_types,
    select_person_id_birth, select_finding_ids_age1_parents,
    select_finding_ids_age2_parents, select_all_findings_notes_ids,
    select_all_findings_roles_ids_distinct,     
    select_count_finding_id_sources, select_nesting_fk_finding,
    update_finding_particulars, select_all_kin_ids_types_couple,
    update_finding_age, update_current_person, select_all_place_ids,
    select_all_event_types, select_event_type_id, insert_finding_new,
    insert_finding_new_couple, insert_findings_persons_new_couple,    
    update_findings_persons_age1, select_max_finding_id, insert_place_new,
    select_event_type_couple_bool, insert_kin_type_new, update_event_types,    
    insert_places_places_new, insert_finding_places_new_event,
    insert_event_type_new, select_max_event_type_id, delete_finding,
    delete_finding_places, delete_findings_persons, insert_persons_persons,
    delete_findings_roles_finding, delete_findings_notes_finding,         
    select_findings_for_person, insert_finding_places_new, delete_claims_findings, 
    select_event_type_after_death, select_event_type_after_death_bool,
    select_findings_persons_parents, select_findings_persons_age2,    
    insert_finding_birth, update_findings_persons_age2, select_person,
    select_finding_event_type, select_findings_persons_ppid,
    select_findings_persons_person_id, update_finding_date, delete_persons_persons,
    select_findings_persons_alt_parents, select_event_type_via_event_string,
    insert_persons_persons_null, insert_findings_persons_null_couple,
    select_finding_id_adoption, select_finding_id_fosterage, 
    select_finding_id_guardianship, select_event_type_id_only,
    select_finding_ids_age1_alt_parents, select_finding_ids_age2_alt_parents,
    select_person_id_alt_parentage, select_kin_type_string, 
    select_person_ids_kin_types_include_nulls, select_findings_persons_id,
    select_findings_details_offspring_alt_parentage,
    )

import dev_tools as dt
from dev_tools import looky, seeline





date_prefs = get_date_formats()

HEADS = (
    'event', 'date', 'place', 'particulars', 'age', 
    'roles', 'notes', 'sources')

def delete_generic_finding(finding_id, fpid, conn, cur):
    ppid = None
    cur.execute(delete_finding_places, (finding_id,))
    conn.commit()
    cur.execute(delete_findings_roles_finding, (finding_id,))
    conn.commit()
    cur.execute(delete_findings_notes_finding, (finding_id,))
    conn.commit()
    cur.execute(delete_claims_findings, (finding_id,))
    conn.commit()
    if fpid is not None:
        cur.execute(select_findings_persons_ppid, (fpid,))
        ppid = cur.fetchone()
    cur.execute(delete_findings_persons, (finding_id,))
    conn.commit()
    if ppid is not None:
        cur.execute(delete_persons_persons, ppid)
        conn.commit()
    cur.execute(delete_finding, (finding_id,))
    conn.commit()

def delete_couple_finding(finding_id, fpid=None):
    """ Used also in families.py. """
    current_file = get_current_file()
    if current_file is not None:
        current_file = get_current_file()[0]
    else:
        return
    conn = sqlite3.connect(current_file)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    delete_generic_finding(finding_id, fpid, conn, cur) #1
    cur.execute(delete_findings_persons, (finding_id,)) #2
    conn.commit()
    cur.close()
    conn.close()

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

def get_generic_findings(
        dkt, cur, finding_id, findings_data, 
        current_person, non_empty_roles, non_empty_notes):
    cur.execute(select_findings_details_generic, finding_id)
    generic_details = [i for i in cur.fetchone()]
    date_prefs = get_date_formats(tree_is_open=1)
    dkt["date"] = format_stored_date(generic_details[3], date_prefs=date_prefs)

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
        non_empty_roles, non_empty_notes, person_autofill_values):

    couple_kin_type_ids = get_couple_kin_types()
    curr_per_kin_types = tuple([current_person] + couple_kin_type_ids)
    sql =   '''
                SELECT finding_id 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id1 = ?
                    AND kin_type_id1 in ({})
            '''.format(
                ','.join('?' * (len(curr_per_kin_types) - 1)))
    cur.execute(sql, curr_per_kin_types)
    couple_findings1 = [i[0] for i in cur.fetchall()]
    sql =   '''
                SELECT finding_id 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
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
            if gotgot[0] == current_person:
                iD = gotgot[3]
                if iD:
                    name = person_autofill_values[iD][0]["name"] 
                dkt["age"] = gotgot[1]
                dkt["kin_type"] = gotgot[2]
                dkt["partner_id"] = iD
                dkt["partner_kin_type"] = gotgot[5]
                dkt["partner_name"] = name
                dkt["partner_age"] = gotgot[4]
            elif gotgot[3] == current_person:
                iD = gotgot[0]
                if iD:
                    name = person_autofill_values[iD][0]["name"] 
                dkt["age"] = gotgot[4]
                dkt["kin_type"] = gotgot[5]
                dkt["partner_id"] = iD
                dkt["partner_kin_type"] = gotgot[2]
                dkt["partner_name"] = name
                dkt["partner_age"] = gotgot[1]

        cur.execute(select_findings_details_couple_generic, finding_id)
        couple_generics = list(cur.fetchone())
        date_prefs = get_date_formats(tree_is_open=1)
        couple_generics[1] = format_stored_date(
            couple_generics[1], date_prefs=date_prefs)
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

def make_parent_kintips(dkt, current_person, cur, person_autofill_values):
    cur.execute(select_finding_id_birth, (current_person,))
    birth_id = cur.fetchone()
    parents = (None, None)
    if birth_id:
        cur.execute(select_person_ids_kin_types_include_nulls, birth_id)
        parents = cur.fetchone()
    if not parents:
        pass
    elif parents[1] == "father" or  parents[3] == "mother":
        dad = parents[0]
        mom = parents[2]
        dad_name = None
        mom_name = None
        dkt["father_id"] = dad
        if dad:
            
            dad_name = person_autofill_values[dad][0]["name"]         
        dkt["father_name"] = dad_name
        dkt["mother_id"] = mom
        if mom:
            mom_name = person_autofill_values[mom][0]["name"]
            dkt["mother_name"] = mom_name

def make_alt_parent_kintips(
        dkt, current_person, cur, finding_id, person_autofill_values,  
        adoption=None, fosterage=None, guardianship=None):

    if adoption:
        query = select_finding_id_adoption
    elif fosterage:
        query = select_finding_id_fosterage
    elif guardianship:
        query = select_finding_id_guardianship
    cur.execute(query, (current_person,))
    event_id = cur.fetchall()
    parents = None
    if event_id is None:
        return
    elif finding_id in event_id:
        cur.execute(select_person_ids_kin_types, finding_id)
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
    dkt, cur, current_person, findings_data, finding_id, person_autofill_values):
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

    cur.execute(select_finding_ids_age1_alt_parents, (current_person,))
    offspring1 = [list(i) for i in cur.fetchall()]

    cur.execute(select_finding_ids_age2_alt_parents, (current_person,))
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
        cur.execute(select_findings_details_offspring_alt_parentage, (child_id, offspring_event_id))     
        offspring_details = cur.fetchone()
        event_type = get_event_type_string(offspring_event_id)
        child_name = person_autofill_values[child_id][0]["name"]

        sorter = split_sorter(offspring_details[1])
        date_prefs = get_date_formats(tree_is_open=1)
        date = format_stored_date(offspring_details[0], date_prefs=date_prefs)

        particulars = offspring_details[2]
        place = get_place_string((offspring_event_id,), cur)

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
        make_parent_kintips(dkt, current_person, cur, person_autofill_values)
    elif event_type == "adoption":
        make_alt_parent_kintips(dkt, current_person, cur, finding_id, person_autofill_values, adoption=True)
    elif event_type == "fosterage":
        make_alt_parent_kintips(dkt, current_person, cur, finding_id, person_autofill_values, fosterage=True)
    elif event_type == "guardianship":
        make_alt_parent_kintips(dkt, current_person, cur, finding_id, person_autofill_values, guardianship=True)

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

    person_autofill_values = make_all_names_dict_for_person_select()  
    for finding_id in generic_finding_ids:
        dkt = dict(rowtotype)
        
        get_generic_findings(
            dkt, cur, finding_id, findings_data, 
            current_person, non_empty_roles, non_empty_notes)     

        if dkt["event"] == "birth":
            autocreate_parent_findings(
                dkt, cur, current_person, findings_data, finding_id, 
                person_autofill_values)
        elif dkt["event"] == "adoption":
            autocreate_parent_findings(
                dkt, cur, current_person, findings_data, finding_id, 
                person_autofill_values)
        elif dkt["event"] == "fosterage":
            autocreate_parent_findings(
                dkt, cur, current_person, findings_data, finding_id, 
                person_autofill_values)
        elif dkt["event"] == "guardianship":
            autocreate_parent_findings(
                dkt, cur, current_person, findings_data, finding_id, 
                person_autofill_values)

    get_couple_findings(
        cur, current_person, rowtotype, findings_data, 
        non_empty_roles, non_empty_notes, person_autofill_values)

    cur.close()
    conn.close()  
    return findings_data, non_empty_roles, non_empty_notes  

class EventsTable(Frame):

    def __init__(
            self, master, root, treebard, main, formats, person_autofill_values, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.treebard = treebard
        self.main_window = main
        self.formats = formats
        self.person_autofill_values = person_autofill_values

        self.main_canvas = main.master

        self.current_person = get_current_person()
        self.inwidg = None
        self.headers = []
        self.widths = [0, 0, 0, 0, 0]

        self.widget = None
        self.kintip = None
        self.kintip_text = None
        self.kin_widths = [0, 0, 0, 0, 0, 0]
        self.kintip_bindings = {"on_enter": [], "on_leave": []}

        self.screen_height = self.winfo_screenheight()
        self.column_padding = 2
        self.new_row = 0
        self.event_types = get_all_event_types()
        self.event_autofill_values = EntryAuto.create_lists(self.event_types)
        self.couple_event_types = get_couple_event_types()
        self.after_death_events = get_after_death_event_types()
        if self.after_death_events is None:
            return
        self.events_only_even_without_dates = [
            "birth", "death"] + self.after_death_events
        # without the parameter passed by lambda, running this
        #   function creates a null current person
        self.root.bind(
            "<Control-S>", 
            lambda evt, curr_per=self.current_person: self.redraw(
                evt, curr_per))
        self.root.bind(
            "<Control-s>", 
            lambda evt, curr_per=self.current_person: self.redraw(
                evt, curr_per))

        self.place_strings = make_all_nestings(select_all_place_ids)

        self.make_header()
        self.make_table_cells()
        self.set_cell_content()
        self.show_table_cells()

    def get_initial(self, evt):
        self.initial = evt.widget.get()
        self.inwidg = evt.widget

    def get_final(self, evt):
        if not self.initial:
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

    def delete_event(self, finding_id, widg, initial):

        def ok_delete_event():
            msg[0].destroy()
            self.focus_set()
            proceed(initial_value)

        def cancel_delete_event():
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
            current_person = self.current_person
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
                delete_generic_finding(finding_id, None, conn, cur)
            elif couple_event_old == 1:
                cur.execute(select_findings_persons_id, (finding_id,))
                fpid = cur.fetchone()[0]
                delete_couple_finding(finding_id, fpid=fpid)
            self.redraw()
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
                events_msg[9], 
                "Birth Events Undeletable Error", 
                "OK")
            msg1[0].grab_set()
            msg1[2].config(command=err_done1)
            return

        msg = open_yes_no_message(
            self, 
            events_msg[4], 
            "Delete Event Confirmation", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[2].config(command=ok_delete_event)
        msg[3].config(command=cancel_delete_event)

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
                        events_msg[3], 
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
            self.event_types = get_all_event_types()
            self.final = self.final.strip().lower()
            if (self.initial == 'offspring' and len(self.final) != 0):
                msg = open_message(
                    self, 
                    events_msg[2], 
                    "Offspring Event Edit Error", 
                    "OK")
                msg[0].grab_set()
                msg[2].config(command=err_done4)
                return

            if self.final == 'offspring':
                msg = open_message(
                    self, 
                    events_msg[6], 
                    "Change to Offspring Event Error", 
                    "OK")
                msg[0].grab_set()
                msg[2].config(command=err_done7)
                return
            if self.final in self.event_types:
                update_to_existing_type()
            elif len(self.final) == 0:
                initial = self.initial
                self.delete_event(self.finding, widg, initial)
            else:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
                msg = open_message(
                    self.root, 
                    events_msg[8], 
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
            self.redraw()

        def update_place():
            cur.execute(select_nesting_fk_finding, (self.finding,))
            nested_place = cur.fetchone()[0]
            self.final = ValidatePlace(
                self.root, 
                self.treebard,
                self.inwidg,
                self.initial,
                self.final,
                self.finding,
                self.formats)

        def update_age(offspring_event, row):
            if (event_string == "birth" and 
                    self.final not in (0, "0", "0d 0m 0y")):
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
                        (self.final, self.finding, right_person[2]))
                elif right_person[1] == self.current_person:
                    cur.execute(
                        update_findings_persons_age2, 
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
                            values=self.event_autofill_values)
                        cell.bind("<Double-Button-1>", self.open_edit_event_dialog)
                    elif j == 2:
                        cell = EntryAuto(
                            self, width=0, 
                            autofill=True, 
                            values=self.place_autofill_values)
                    else:                        
                        cell = EntryAuto(self, width=0,)
                    cell.initial = ''
                    cell.final = ''
                    cell.finding = None
                    cell.bind('<FocusIn>', self.get_initial, add="+")
                    cell.bind('<FocusOut>', self.get_final, add="+")
                elif j == 5:
                    cell = LabelDots(
                        self, RolesDialog, self.treebard, self.formats, 
                        person_autofill_values=self.person_autofill_values
)
                elif j == 6:
                    cell = LabelDots(
                        self, NotesDialog, self.treebard, self.formats, 
                        person_autofill_values=self.person_autofill_values
)
                elif j == 7:
                    cell = LabelButtonText(
                        self,
                        width=8,
                        anchor='w',
                        font=self.formats['heading3'])
                row.append(cell)
            self.table_cells.append(row)
        self.new_event_frame = Frame(self)
        self.event_input = EntryAutoHilited(
            self.new_event_frame,
            self.formats,
            width=32, 
            autofill=True, 
            values=self.event_autofill_values)
        self.add_event_button = Button(
            self.new_event_frame, 
            text="NEW EVENT OR ATTRIBUTE", 
            command=self.make_new_event)

    def set_cell_content(self):
        self.findings_data, current_roles, current_notes = get_findings()
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
                        if name is None:
                            name = self.person_autofill_values[dkt["partner_id"]][0]["name"]
                        couple_in = widg.bind(
                            "<Enter>", lambda evt, 
                            kin=dkt["partner_kin_type"], 
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
                                kin="parent(s)", names=names: self.handle_enter(kin, names))
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
                                kin="adoptive parent(s)", names=names: self.handle_enter(kin, names))
                            adoptive_parents_out = widg.bind("<Leave>", self.on_leave)
                            self.widget = widg
                            self.kintip_bindings["on_enter"].append([widg, adoptive_parents_in])
                            self.kintip_bindings["on_leave"].append([widg, adoptive_parents_out])
                        elif evtype == "fosterage":
                            alts1 = ("foster_parent_name1", "foster_father_name1", "foster_mother_name1")
                            alts2 = ("foster_parent_name2", "foster_father_name2", "foster_mother_name2")
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
                                kin="foster parent(s)", names=names: self.handle_enter(kin, names))
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
                                kin="guardian(s)", names=names: self.handle_enter(kin, names))
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

        self.fix_tab_traversal() # DO NOT DELETE THIS IS NEEDED
        for row_num in range(self.grid_size()[1]):
            self.grid_rowconfigure(row_num, weight=0)
        self.new_row = row_num + 1

        self.new_event_frame.grid(
            column=0, row=self.new_row, pady=6, columnspan=5, sticky='ew')
        self.event_input.grid(column=0, row=0, padx=(0,12), sticky='w')
        self.add_event_button.grid(
            column=1, row=0, sticky='w')

    def show_kintip(self, kin_type, name):
        ''' 
            Based on show_kintip() in search.py.
        '''

        maxvert = self.winfo_screenheight()

        if self.kintip or not self.kintip_text:
            return
        x, y, cx, cy = self.widget.bbox('insert')        

        self.kintip = d_tip = tk.Toplevel(self.widget)
        label = LabelNegative(
            d_tip, 
            text=self.kintip_text, 
            justify='left',
            relief='solid', 
            bd=1,
            bg=self.formats['highlight_bg'])
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
        if len(name) == 2:
            name = list(name)
            name[1] = "({})".format(name[1])
            name = " ".join(name)
        self.kintip_text = "{}: {}".format(kin_type, name)

        if self.kintip_text:
            self.show_kintip(kin_type, name)

    def on_leave(self, evt):
        self.off()

    def redraw(self, evt=None, current_person=None):
        self.formats = make_formats_dict()
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
        self.kin_widths = [0, 0, 0, 0, 0, 0]
        self.set_cell_content()
        self.show_table_cells()
        if evt: # user pressed CTRL+S for example
            self.main_window.nuke_table.make_nuke_inputs(
                current_person=self.current_person)
        else: # user pressed OK to change current person for example   
            self.main_window.nuke_table.make_nuke_inputs()

        self.resize_scrollbar(self.root, self.main_canvas)

    def resize_scrollbar(self, root, canvas):
        root.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    def forget_cells(self):
        self.update_idletasks()
        for k,v in self.kintip_bindings.items():
            if k == "on_enter":
                for lst in v:
                    lst[0].unbind("<Enter>", lst[1])                    
            elif k == "on_leave":
                for lst in v:
                    lst[0].unbind("<Leave>", lst[1])
            self.kintip_bindings = {"on_enter": [], "on_leave": []}

        for lst in self.cell_pool:
            for widg in lst[1]:
                if widg.winfo_subclass() == 'EntryAuto':
                    widg.delete(0, 'end')
                elif widg.winfo_subclass() == 'LabelButtonText':
                    widg.config(text='')
                widg.grid_forget()
        self.event_input.grid_forget()
        self.add_event_button.grid_forget()

        self.main_window.person_entry.current_id = None

        for ent in self.main_window.nuke_table.nuke_inputs:
            ent.delete(0, "end")
        self.main_window.nuke_table.ma_input.delete(0, "end")
        self.main_window.nuke_table.pa_input.delete(0, "end")
        self.main_window.nuke_table.new_kin_frame.grid_forget()
        self.main_window.nuke_table.current_person_alt_parents = []
        self.main_window.nuke_table.compound_parent_type = "Children's"        
        for widg in self.main_window.nuke_table.nuke_containers: 
            # pardframe, prodigy_frame, alt parent entries & labels
            widg.destroy() 

        self.main_window.nuke_table.nuke_containers = []

        self.main_window.nuke_table.family_data = [
            [
                [
                    {'fpid': None, 'ppid': None, 'finding': None, 
                        'sorter': [0, 0, 0]}, 
                    {'id': None, 'name': '', 'kin_type_id': 2, 
                        'kin_type': 'father', 'labwidg': None, 'inwidg': None}, 
                    {'id': None, 'name': '', 'kin_type_id': 1, 
                        'kin_type': 'mother', 'labwidg': None, 'inwidg': None}
                ],
            ],
            {},
        ]

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
            Disallow creation of second birth or death event or types 
            that don't exist yet.
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
            msg = open_message(
                self, 
                events_msg[5], 
                "Multiple Birth or Death Events", 
                "OK")
            msg[0].grab_set()
            msg[2].config(command=err_done6)
            return
        self.new_event_dialog = NewEventDialog(
            self.root, 
            self.treebard,
            self,
            self.formats,
            self.current_person,
            self.place_strings,
            self.place_autofill_values,   
            self.redraw,
            self.person_autofill_values,
            new_event=new_event)
        self.event_input.delete(0, 'end')

    def open_edit_event_dialog (self, evt):
        inwidg = evt.widget
        for lst in self.cell_pool:
            if lst[1][0] == inwidg:
                finding = lst[0]
                break

        for k,v in self.findings_data.items():
            if k == finding:
                edit_event = v["event"]

        if edit_event in self.couple_event_types:
            is_couple_event = 1
        elif edit_event in self.event_types:
            is_couple_event = 0
            
        
        data = self.findings_data[finding]

        edit_event_dialog = NewEventDialog(
            self.root, 
            self.treebard,
            self,
            self.formats,
            self.current_person,
            self.place_strings,
            self.place_autofill_values,   
            self.redraw,
            self.person_autofill_values,
            finding=finding, 
            inwidg=inwidg,
            is_couple_event=is_couple_event,
            data=data,
            from_edit=True)

class NewEventDialog(Toplevel):
    def __init__(
            self, master, treebard, events_table, formats,
            current_person, place_strings, place_autofill_values, 
            redraw, person_autofill_values, finding=None, new_event=None, 
            inwidg=None, is_couple_event=None, data=None, from_edit=False, 
            *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.withdraw()

        self.root = master
        self.treebard = treebard
        self.events_table = events_table
        self.formats = formats
        self.current_person = current_person
        self.place_strings = place_strings
        self.place_autofill_values = place_autofill_values
        self.redraw = redraw
        self.finding = finding
        self.person_autofill_values = person_autofill_values
        self.new_event = new_event
        self.inwidg = inwidg
        self.is_couple_event = is_couple_event
        self.data = data
        self.from_edit = from_edit
        self.visited = []
        self.new_alt_parent_event = False
        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        self.place_dicts = None
        self.unknown_event_type = False  

        self.other_person_id = None

        self.current_name = self.person_autofill_values[self.current_person][0]["name"]
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        people = make_all_names_dict_for_person_select()        
        self.person_autofill_values = EntryAutoPersonHilited.create_lists(people)

        self.focus_new_event_dialog()
        self.get_some_info()
        if self.unknown_event_type is False:
            self.make_widgets(cur)

        cur.close()
        conn.close()
        self.deiconify()

    def get_some_info(self):
        """ `self.new_finding` ID is predicted reluctantly, see `maxx`. It's 
            used in `validate_place()` before OK is pressed and in `couple_ok()` 
            and `update_db_place()` after OK is pressed. Between these two uses
            another finding ID is created in 
                persons.py `PersonAdd.save_new_person()`.
            Then `self.new_finding` has already been used. So it has to be +1
            twice in case of a new person being added here. This is hard to 
            debug in case of unforeseen changes so it should be refactored. The
            reason for doing it is so that the place input is validated first,
            which prevents more than one dialog from opening on pressing OK, in
            a case where the user inputs both a new person and a place that 
            needs a validation dialog to open. I don't want two dialogs to open
            when the new event dialog closes.
        """

        def err_done2():
            self.destroy()
            msg[0].destroy()
            self.events_table.event_input.focus_set()
            self.events_table.event_input.delete(0, 'end')

        current_file = get_current_file()[0]
        conn =  sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_max_finding_id)  
        maxx = cur.fetchone()
        if maxx is None:
            self.new_finding = 1 # first event recorded to database
        else:
            self.new_finding = maxx[0] + 1 # see docstring
        cur.execute(select_event_type_id, (self.new_event,))
        result = cur.fetchone()
        if result is not None:
            self.event_type_id, self.is_couple_event = result
        elif result is None:
            pass # eg when opening edit event dialog
        else:
            print("line", looky(seeline()).lineno, "result:", result)
            self.unknown_event_type = True
            msg = open_message(
                self.root, 
                events_msg[8], 
                "Unknown Event Type", 
                "OK") 
            msg[0].grab_set()
            msg[2].config(command=err_done2)
            return 
        cur.close()
        conn.close()

    def make_widgets(self, cur):

        def show_message():
            window.columnconfigure(1, weight=1)
            window.rowconfigure(1, weight=1)
            self.new_evt_msg = LabelHeader(window, justify='left')
            self.new_evt_msg.grid(
                column=1, row=1, sticky='news', ipady=18, ipadx=6)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        self.new_event_canvas = Border(self, self.root, self.formats)

        if self.from_edit == 0:
            self.new_event_canvas.title_1.config(text="New Event Dialog")
        elif self.from_edit == 1:
            self.new_event_canvas.title_1.config(text="Edit Event Dialog")
        self.new_event_canvas.title_2.config(
            text="Current Person: {}, id #{}".format(
                self.current_name, self.current_person))

        window = Frame(self.new_event_canvas)
        self.new_event_canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.treebard.scroll_mouse.append_to_list(
            [self.new_event_canvas, window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        window.vsb = Scrollbar(
            self, 
            hideable=True, 
            command=self.new_event_canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            self, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.new_event_canvas.xview)
        self.new_event_canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        buttonbox = Frame(window)
        self.b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(
            buttonbox, text="CANCEL", width=7, 
            command=self.close_new_event_dialog)

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

        self.make_inputs(cur)
        resize_scrolled_content(self, self.new_event_canvas, window)

    def make_inputs(self, cur):

        def err_done8():
            msg[0].destroy() 
            self.destroy()  

        self.other_person_input = None
        self.age2_input = None        

        self.generic_data_inputs = Frame(self.frm)
        self.couple_data_inputs = Frame(self.frm)
        more = Label(
            self.frm, 
            text="Roles, Notes & Sources can be created and "
                "edited in the events table.")

        self.generic_data_inputs.grid(column=0, row=0, sticky="news")
        self.couple_data_inputs.grid(column=0, row=2, sticky='news')
        more.grid(column=0, row=4, columnspan=2, sticky="ew", pady=(12,0))

        self.lab0 = LabelH3(self.generic_data_inputs)
        if self.from_edit:
            self.lab0.config(text="Event Type: {}".format(self.data["event"]))            
        else:
            self.lab0.config(text="Event Type: {}".format(self.new_event))
        lab1 = Label(self.generic_data_inputs, text="Date")
        self.date_input = EntryHilited1(self.generic_data_inputs)
        lab2 = Label(self.generic_data_inputs, text="Place")
        self.place_input = EntryAutoHilited(
            self.generic_data_inputs, self.formats, 
            width=48, autofill=True, values=self.place_autofill_values)
        self.place_input.bind("<FocusOut>", self.validate_place)
        lab3 = Label(self.generic_data_inputs, text="Particulars")
        self.particulars_input = EntryHilited1(
            self.generic_data_inputs, width=60)

        self.lab0.grid(column=0, row=0, sticky="w", pady=6)
        lab1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.date_input.grid(
            column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        lab2.grid(column=0, row=2, sticky="e", pady=(0,1))
        self.place_input.grid(
            column=1, row=2, sticky="w", padx=(3,0), pady=(0,1))
        lab3.grid(column=0, row=3, sticky="e")
        self.particulars_input.grid(column=1, row=3, sticky="w", padx=(3,0))

        print("line", looky(seeline()).lineno, "self.is_couple_event:", self.is_couple_event)
        if self.is_couple_event == 0:
            if self.new_event == "offspring":
                self.withdraw()
                msg = open_message(
                    self.root, 
                    events_msg[7], 
                    "Offspring Event Creation Error", 
                    "OK") 
                msg[0].grab_set()
                msg[2].config(command=err_done8)
                return 
            elif self.new_event in ("adoption", "fosterage", "guardianship"):
                self.new_alt_parent_event = True
                self.show_one_person()
            else:
                self.show_one_person()
        elif self.is_couple_event == 1:
            self.show_other_person()
        else:
            print("line", looky(seeline()).lineno, "self.is_couple_event:", self.is_couple_event)
            print("line", looky(seeline()).lineno, "case not handled:")
        self.b1.config(command=self.add_event)

        if self.from_edit is True:
            self.fill_inputs(cur)

        self.visited.extend([
            (self.date_input,
                "Date Input",
                "The date of the event."),
            (self.place_input,
                "Place Input",
                "The location of the event."),
            (self.particulars_input,
                "Particulars Input",
                "A few words of detail. Use Notes for more."),
            (self.age1_input,
                "Age Input",
                "Current person's age at time of event.")])

        run_statusbar_tooltips(
            self.visited, 
            self.new_event_canvas.statusbar.status_label, 
            self.new_event_canvas.statusbar.tooltip_label)  

        rcm_widgets = (
            self.date_input, self.place_input, self.particulars_input, 
            self.age1_input, self.new_evt_msg)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            new_event_dlg_help_msg) 

        config_generic(self)
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
        self.lab0.grid_configure(columnspan=2)

    def show_other_person(self):

        def radio_reflex():
            parent_type = self.offspringvar.get()
            if parent_type == 1:
                self.mother_or_father.config(text="father")
            elif parent_type == 2:
                self.mother_or_father.config(text="mother")

        self.new_evt_msg.config(text="Information about the event "
            "relating to the current person and other primary participants "
            "in the event.")
        sep1 = Separator(self.frm, width=3)
        sep1.grid(column=0, row=1, columnspan=2, sticky="ew", pady=(12,0))

        name1 = Label(self.couple_data_inputs, text=self.current_name)
        age1 = Label(self.couple_data_inputs, text="Age")
        self.age1_input = EntryHilited1(self.couple_data_inputs, width=6)

        spacer = Frame(self.couple_data_inputs)

        name2 = Label(self.couple_data_inputs, text="Partner")
        self.other_person_input = EntryAutoPersonHilited(
            self.couple_data_inputs, self.formats, width=48, autofill=True, 
            values=self.person_autofill_values)
        self.other_person_input.bind(
            "<FocusIn>", lambda evt: get_original(evt))
        EntryAutoPerson.all_person_autofills.append(self.other_person_input)

        age2 = Label(self.couple_data_inputs, text="Age")
        self.age2_input = EntryHilited1(self.couple_data_inputs, width=6)
        father_is_it = LabelHilited(self.couple_data_inputs, text="father")
        name1.grid(column=0, row=0, sticky="w", columnspan=2, pady=(9,1))

        age1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.age1_input.grid(
            column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))

        self.couple_data_inputs.columnconfigure(2, weight=1)
        spacer.grid(column=2, row=0, sticky="news", rowspan=3)

        name2.grid(column=3, row=0, sticky="e", pady=(9,1))
        self.other_person_input.grid(
            column=4, row=0, sticky="w", padx=(3,0), pady=(9,1))
        age2.grid(column=3, row=1, sticky="e", pady=(0,1))
        self.age2_input.grid(
            column=4, row=1, sticky="w", padx=(3,0), pady=(0,1))
        self.visited.extend(
            [(self.age2_input,
                "Age Input 2",
                "Other person's age at time of event."),
            (self.other_person_input,
                "Other Person Input",
                "Birth name of the other person.")])

    def close_new_event_dialog(self):
        self.events_table.event_input.focus_set()
        self.root.lift()
        self.grab_release()
        self.destroy()

    def update_event(self):
    
        def change_stored_value(widg, key, final):
            print("line", looky(seeline()).lineno, "widg, key, final:", widg, key, final)
            self.changes[key] = final

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        keys = ("date", "place", "particulars", "age", "partner_name", "partner_age")
        widgets = [
            self.date_input, self.place_input, self.particulars_input, 
            self.age1_input]
        widgets_couple = [self.other_person_input, self.age2_input]
        if self.is_couple_event:
            widgets = widgets + widgets_couple  

        u = 0
        for key in keys:
            final = widgets[u].get()
            print("line", looky(seeline()).lineno, "self.data[key], final:", self.data[key], final)
            if final != self.data[key]:
                self.changes[key] = final
                widg = widgets[u]
                row = self.inwidg.grid_info()["row"]
                column = None
                if u < 5:
                    column = u + 1
                if column:
                    table_cell = row, column
                    for child in self.events_table.winfo_children():
                        if child.grid_info().get("row") is None:
                            continue
                        cell_row, cell_column = (child.grid_info()["row"], child.grid_info()["column"])
                        if cell_row == row and cell_column == column:
                            right_widget = child
                            break
                right_widget.delete(0, "end")
                right_widget.insert(0, final)
                change_stored_value(widg, key, final)
            u += 1
        print("line", looky(seeline()).lineno, "self.changes:", self.changes)






        # data = check_name(ent=self.other_person_input)
        # print("line", looky(seeline()).lineno, "data:", data)
        # if data == "add_new_person":
            # self.other_person_id = open_new_person_dialog(
                # self, self.other_person_input, self.root, self.treebard, self.formats, 
                # person_autofill_values=self.person_autofill_values)
            # self.person_autofill_values = update_person_autofill_values()
            # self.new_finding += 1 # see get_some_info() docstring
        # elif self.is_couple_event == 1:
            # self.other_person_id = data[1]
            # print("line", looky(seeline()).lineno, "self.other_person_id:", self.other_person_id)
        # self.age_1 = self.age1_input.get()
        # if self.is_couple_event == 1:
            # self.age_2 = self.age2_input.get()
            # self.other_person = data[0]["name"]
        # if self.is_couple_event == 0:
            # cur.execute(
                # insert_finding_new, (
                    # self.new_finding, self.age_1, 
                    # self.event_type_id, self.current_person))
            # conn.commit()            
        # else:
            # cur.execute(
                # insert_finding_new_couple, 
                # (self.new_finding, self.event_type_id,))
            # conn.commit()
            # self.couple_ok(cur, conn)

        # if len(self.place_string) == 0:
            # cur.execute(insert_finding_places_new, (self.new_finding,))
            # conn.commit()
        # else:
            # self.update_db_place(conn, cur)

        # new_event_date = validate_date(
            # self.root,
            # self.date_input,
            # self.date_input.get())
        # if not new_event_date:
            # new_event_date = "-0000-00-00-------"

        # sorter = self.events_table.make_date_sorter(new_event_date)

        # if new_event_date == "----------":
            # new_event_date = "-0000-00-00-------"

        # cur.execute(update_finding_date, (new_event_date, sorter, self.new_finding))
        # conn.commit()

        # update_particulars(
            # self.particulars_input.get().strip(), self.new_finding) 

        # if self.new_alt_parent_event is True:
            # self.make_alt_parent_event(conn, cur, self.event_type_id)
            # self.new_alt_parent_event = False

        # self.close_new_event_dialog()
        # self.events_table.redraw()

        cur.close()
        conn.close()
    def add_event(self):
        if self.from_edit:
            self.update_event()
            return

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        data = check_name(ent=self.other_person_input)
        print("line", looky(seeline()).lineno, "data:", data)
        if data == "add_new_person":
            self.other_person_id = open_new_person_dialog(
                self, self.other_person_input, self.root, self.treebard, self.formats, 
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
            self.new_finding += 1 # see get_some_info() docstring
        elif self.is_couple_event == 1:
            self.other_person_id = data[1]
        self.age_1 = self.age1_input.get()
        if self.is_couple_event == 1:
            self.age_2 = self.age2_input.get()
            self.other_person = data[0]["name"]
        if self.is_couple_event == 0:
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

        if self.new_alt_parent_event is True:
            self.make_alt_parent_event(conn, cur, self.event_type_id)
            self.new_alt_parent_event = False         

        cur.close()
        conn.close()
        self.close_new_event_dialog()
        self.events_table.redraw()

    def couple_ok(self, cur, conn): 
        if len(self.other_person) != 0:
            other_person_id = self.other_person_id 
        else:
            other_person_id = None

        cur.execute(insert_persons_persons, (self.current_person, other_person_id))
        conn.commit()        
        cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "persons_persons"')
        ppid = cur.fetchone()[0]
        cur.execute(insert_findings_persons_new_couple, (
            self.new_finding, self.age_1, self.age_2, ppid))
        conn.commit()
        if self.event_type_id == 1:
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
                self.age1_input, self.other_person_input, self.age2_input):
            if widg:
                filled_in = widg.get()
                if len(filled_in) == 0:
                    widg.focus_set()
                    break

    def fill_inputs(self, cur):

        def change_event_type(evt):
            print("line", looky(seeline()).lineno, "self.lab0.cget('text'):", self.lab0.cget('text'))

        def get_final_text(widg):
            print("line", looky(seeline()).lineno, "self.data:", self.data)

        self.lab0.bind("<Double-Button-1>", change_event_type)

        date = self.data["date"]
        place = self.data["place"]
        particulars = self.data["particulars"]
        age1 = self.data["age"]

        self.date_input.insert(0, date)
        self.place_input.insert(0, place)
        self.particulars_input.insert(0, particulars)
        self.age1_input.insert(0, age1)
        if self.is_couple_event:
            age2 = self.data["partner_age"]
            partner_name = self.data["partner_name"]
            self.age2_input.insert(0, age2)
            self.other_person_input.insert(0, partner_name)

        self.changes = self.data

    def update_db_place(self, conn, cur):
        if self.place_dicts is None: 
            return

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
                places_places = get_all_places_places()
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
            self.new_finding,
            self.formats)
        self.place_dicts = place_validator.input_new_event()
        self.place_autofill_values.insert(0, inwidg.get())
        if place_validator.new_place_dialog is not None:
            self.place_validator = place_validator.new_place_dialog.new_places_dialog
            self.place_validator.bind("<Destroy>", self.focus_new_event_dialog)
            self.place_validator.grab_set()

    def focus_new_event_dialog(self, evt=None):
        self.grab_set()
        self.lift()

    def make_alt_parent_event(self, conn, cur, event_type_id):
        """ Auto-create the database rows needed to store alt parents. 
            In module-level namespace for reasons maybe no longer relevant?
            
        """
        if event_type_id == 48:
            unisex_alt_parent = 130
        elif event_type_id == 83:
            unisex_alt_parent = 110
        elif event_type_id == 95:
            unisex_alt_parent = 120
        cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "finding"')
        event_id = cur.fetchone()[0]
        cur.execute(insert_persons_persons_null)
        conn.commit()
        cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "persons_persons"')
        ppid = cur.fetchone()[0]
        cur.execute(insert_findings_persons_null_couple, (event_id, unisex_alt_parent, unisex_alt_parent, ppid))
        conn.commit() 

short_values = ['red', 'white', 'blue', 'black', 'rust', 'pink', 'steelblue']

if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('+800+300')

    strings = make_all_nestings(select_all_place_ids)
    place_autofill_values = EntryAuto.create_lists(strings)

    auto = EntryAuto(
        root, width=50, autofill=True, values=place_autofill_values)

    auto.focus_set()   

    move = tk.Entry(root)

    auto.grid()
    move.grid()

    root.mainloop()














