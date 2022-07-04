# families.py

""" It took six months to write this module. Don't rewrite it for fun. 
    It's not fun. Its worst defect now (20220612) is that tab traversal
    correction after changing something in the families table is a huge
    hassle, due to the fact that some of the widgets are permanent and 
    some of the widgets are only created as needed. A whole day was 
    wasted trying to chase this problem into code hell, but for now
    the simple solution is to use the mouse to put the cursor back where
    it's wanted after the obligatory redraw which follows every change to
    the table. A possible solution is to use a cell pool as in
    the findings table and never destroy anything, just grid_forget() any
    field that's no longer needed. BEST SOLUTION might be to redesign the
    feature so that all the inputs including the parent inputs are equally
    destroyed on redraw. That way things should work symmetrically and it
    should be easy to get a simple tab traversal that remains stable.
"""

import tkinter as tk
import sqlite3
from widgets import (
    Frame, LabelH3, Label, Button, Canvas, LabelEntry, Radiobutton, LabelFrame,
    FrameHilited, LabelHeader, Checkbutton, LabelStay, Dialogue, Combobox,
    Scrollbar, EntryAutoPerson, EntryAutoPersonHilited, open_message, 
    make_formats_dict, Toplevel, NEUTRAL_COLOR, configall,
    initialize_parents_data, redraw_person_tab)
from files import get_current_file, global_db_path
from persons import (
    open_new_person_dialog, make_all_names_dict_for_person_select, check_name,
    delete_person_from_tree, update_person_autofill_values)
from messages import families_msg
from dates import format_stored_date, get_date_formats, OK_MONTHS, validate_date
from findings_table import delete_couple_finding
from query_strings import (
    select_finding_id_birth, update_finding_ages_kintypes_null,
    select_person_gender_by_id, select_finding_date, update_finding_kin_type_1,
    select_finding_id_death, select_finding_date_and_sorter,
    update_finding_person_1, update_finding_person_2, select_kin_type_string,   
    update_finding_person_1_null_by_id, update_finding_person_2_null_by_id,
    select_finding_details, update_current_person, update_finding_mother, 
    update_finding_kin_type_2, select_all_event_type_ids_marital,
    update_person_gender, update_finding_parents, update_finding_father,
    update_finding_date, insert_finding_death, select_kin_types_parental,
    select_finding_couple_details, select_finding_details_sorter,
    select_finding_kin_types, select_finding_couple_person1_details,
    select_finding_couple_person2_details, select_kin_types,
    select_finding_couple_details_alt_parent1, select_finding_death_by_person,
    select_finding_couple_details_alt_parent2, select_finding_event_type,
    select_finding_id_by_person_and_event, select_finding_death_date,
    select_finding_person_date_by_finding_and_type, update_finding_partner2,
    select_finding_person_date_alt_parent_event, update_finding_partner1,
    update_finding_parent1_null, update_finding_parent2_null,
    update_finding_parents_new, select_finding_persons,
    update_finding_parents_null)
import dev_tools as dt
from dev_tools import looky, seeline



def make_parent_types_dict():
    tree = get_current_file()[0]
    # conn = sqlite3.connect(current_file)
    conn = sqlite3.connect(global_db_path)
    cur = conn.cursor()
    cur.execute("ATTACH ? AS tree", (tree,))
    cur.execute(select_kin_types_parental)
    parentTypes = cur.fetchall()    
    PARENT_TYPES = {}
    for tup in parentTypes:
        PARENT_TYPES[tup[0]] = tup[1]
    cur.execute("DETACH tree")
    cur.close()
    conn.close()
    return PARENT_TYPES

PARENT_TYPES = make_parent_types_dict()

def get_all_marital_event_types(conn, cur):
    cur.execute(select_all_event_type_ids_marital)
    marital_event_types = [i[0] for i in cur.fetchall()]
    return marital_event_types

class NuclearFamiliesTable(Frame):
    """ `...alt...` refers to alternate parents such as relationships 
        created by adoption, fosterage, and guardianship.
    """
    def __init__( 
            self, master, root, treebard, current_person, findings_table, 
            right_panel, person_autofill_values,
            *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.root = root
        self.treebard = treebard
        self.current_person = current_person
        self.findings_table = findings_table
        self.right_panel = right_panel
        self.person_autofill_values = person_autofill_values

        self.date_prefs = get_date_formats(tree_is_open=1)
        self.unlink_partners = {"marital_findings": [], "children": []}
        self.link_partners = {"marital_findings": [], "children": []}
        self.parent_types = [] # See docstring in `make_pard_dict()`

        self.parents_data = initialize_parents_data()
        self.progeny_data = {}
        self.nukefam_inputs = []

        self.widget = None
        self.idtip = None
        self.idtip_text = None
        self.idtip_bindings = {"on_enter": [], "on_leave": []}
        self.person_inputs = []

        self.original = ""
        self.no_error = False

        self.nukefam_containers = []

        self.cancel_unlink_partner_pressed = False
        self.cancel_link_partner_pressed = False
        self.cancel_unlink_child_pressed = False
        self.new_partner_id = None

        self.parents_of_child_to_unlink = [0, 0]

        self.newkidvar = tk.IntVar()

        self.current_person_name = ""
        self.current_widget = None

        self.make_widgets()

    def bind_autofill(self, ent):
        ent.bind("<FocusIn>", self.get_original, add="+")
        ent.bind("<FocusOut>", self.get_final)
        ent.bind("<Double-Button-1>", self.change_current_person) 

    def make_widgets(self):

        self.nukefam_canvas = Canvas(self)
        self.nukefam_window = Frame(self.nukefam_canvas)
        self.nukefam_canvas.create_window(
            0, 0, anchor="nw", window=self.nukefam_window)
        nukefam_sbv = Scrollbar(
            self, command=self.nukefam_canvas.yview, hideable=True)
        self.nukefam_canvas.config(yscrollcommand=nukefam_sbv.set)
        nukefam_sbh = Scrollbar(
            self, orient='horizontal', 
            command=self.nukefam_canvas.xview, hideable=True)
        self.nukefam_canvas.config(xscrollcommand=nukefam_sbh.set)

        # children of self
        self.nukefam_canvas.grid(column=0, row=0, sticky="news")
        nukefam_sbv.grid(column=1, row=0, sticky="ns")
        nukefam_sbh.grid(column=0, row=1, sticky="ew")

    def make_nukefam_widgets_perm(self):
        
        self.pardlabs = []
        self.parents_area = LabelFrame(self.nukefam_window) 
        labelwidget = LabelH3(self.parents_area, text="Parents of the Current Person")
        self.pardlabs.append(labelwidget)
        self.parents_area.config(labelwidget=labelwidget)
        palab = Label(self.parents_area, text="Father", anchor="e")
        self.pa_input = EntryAutoPerson(
            self.parents_area, width=30, autofill=True, cursor="hand2", 
            values=self.person_autofill_values, name="pa")
        malab = Label(self.parents_area, text="Mother", anchor="e")
        self.ma_input = EntryAutoPerson(
            self.parents_area, width=30, autofill=True, cursor="hand2",
            values=self.person_autofill_values, name="ma")

        # children of self.nukefam_window
        self.parents_area.grid(column=0, row=0, sticky="w")

        # children of self.parents_area
        palab.grid(column=0, row=0, sticky="ew", pady=(6,12), padx=12)
        self.pa_input.grid(column=1, row=0, pady=(6,12), padx=(0,0))
        malab.grid(column=2, row=0, sticky="ew", pady=(6,12), padx=12)
        self.ma_input.grid(column=3, row=0, pady=(6,12), padx=(0,0))

        for ent in (self.pa_input, self.ma_input):
            self.bind_autofill(ent)
            EntryAutoPerson.person_autofills.append(ent)

    def make_new_kin_inputs(self):
        """ Get `self.new_kid_frame` into the correct row by ungridding it and 
            regridding it in `self.make_nukefam_inputs()` which runs in 
            `redraw_families_table()` which is in widgets.py.
        """
        self.new_kid_frame = Frame(self.nukefam_window)
        self.new_kid_input = EntryAutoPersonHilited(
            self.new_kid_frame, width=48, 
            autofill=True, 
            values=self.person_autofill_values)
        EntryAutoPerson.person_autofills.append(self.new_kid_input)
        self.childmaker = Button(
            self.new_kid_frame, 
            text="ADD CHILD TO SELECTED PARTNER", 
            command=self.add_child)
        self.new_kid_input.grid(column=0, row=0)
        self.childmaker.grid(column=1, row=0, padx=(6,0), pady=(12,0))    

    def add_child(self):

        def err_done7(entry, msg):
            entry.delete(0, 'end')
            msg7[0].grab_release()
            msg7[0].destroy()
            entry.focus_set()
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        for k,v in self.progeny_data.items():
            row = v["inwidg"].grid_info()["row"]
            if self.newkidvar.get() == row:
                other_parent_id = k
                break
        name_data = check_name(ent=self.new_kid_input)
        if not name_data:
            msg7 = open_message(
                self, 
                families_msg[1], 
                "Person Name Unknown", 
                "OK")
            msg7[0].grab_set()
            msg7[2].config(command=lambda entry=self.new_kid_input, msg=msg7: err_done7(
                entry, msg))
            return

        if name_data == "add_new_person":
            new_child_id = open_new_person_dialog(
                self, self.new_kid_input, self.root, self.treebard, 
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
        else:
            new_child_id = name_data[1]

        pa_id = None
        ma_id = None
        cur.execute(select_finding_id_birth, (new_child_id,))
        birth_id = cur.fetchone()[0] 
        if "father" in self.progeny_data[other_parent_id]["parent_type"]:
            ma_id = self.current_person
            pa_id = other_parent_id
        elif "mother" in self.progeny_data[other_parent_id]["parent_type"]:
            pa_id = self.current_person
            ma_id = other_parent_id
        else:
            for pard in (other_parent_id, self.current_person):
                cur.execute(select_person_gender_by_id, (pard,))
                gender = cur.fetchone()[0]
                if gender in ("male", "female"):
                    if gender == "male":
                        if pard == other_parent_id:
                            pa_id = other_parent_id
                            ma_id = self.current_person
                        elif pard == self.current_person:
                            pa_id = self.current_person
                            ma_id = other_parent_id
                    elif gender == "female":
                        if pard == other_parent_id:
                            pa_id = self.current_person
                            ma_id = other_parent_id
                        elif pard == self.current_person:
                            pa_id = other_parent_id
                            ma_id = self.current_person                            
                    break
                else:
                    name1 = self.person_autofill_values[self.current_person][0]["name"]
                    name2 = self.person_autofill_values[other_parent_id][0]["name"]
                    pa_id, ma_id = self.open_assign_gender_dialog(
                        (self.current_person, name1), (other_parent_id, name2))  
                    break

        cur.execute(update_finding_parents, (pa_id, ma_id, birth_id))
        conn.commit()

        cur.close()
        conn.close()
        redraw_person_tab(main_window=self.treebard.main, current_person=self.current_person)

    def open_assign_gender_dialog(self, pard1, pard2):

        def ok_assign_gender():
            self.new_kid_input.delete(0, "end")
            assign_gender_dlg.destroy()

        def cancel_assign_gender():
            nonlocal assign_gender_dlg_cancelled
            assign_gender_dlg_cancelled = True
            self.new_kid_input.delete(0, "end")
            assign_gender_dlg.destroy()

        assign_gender_dlg_cancelled = False
        self.right_id = tk.IntVar()
        assign_gender_dlg = Dialogue(self)

        lab = LabelHeader(
            assign_gender_dlg.window, text="Which partner is which biological parent? If you press CANCEL, parent roles will be assigned randomly.", 
            justify='left', wraplength=450)
        lab.grid(column=0, row=0, padx=12, pady=12, ipadx=6, ipady=6)

        radfrm = Frame(assign_gender_dlg.window)
        radfrm.grid(column=0, row=1)
        
        choices = (pard1[0], pard2[0])

        rdo1 = Radiobutton(
            radfrm, text="{} is father and {} is mother.".format(pard1[1], pard2[1]), 
            variable=self.right_id, value=pard1[0], anchor="w")
        rdo1.grid(column=0, row=0, sticky="ew")
        rdo2 = Radiobutton(
            radfrm, text="{} is father and {} is mother.".format(pard2[1], pard1[1]), 
            variable=self.right_id, value=pard2[0], anchor="w")
        rdo2.grid(column=0, row=1, sticky="ew")

        rdo1.select()
     
        buttons = Frame(assign_gender_dlg.window)
        buttons.grid(column=0, row=2, pady=12, padx=12)
        assign_gender_ok = Button(buttons, text="OK", command=ok_assign_gender, width=7)
        assign_gender_ok.grid(column=0, row=0, sticky="e", padx=(0,12))
        assign_gender_ok.focus_set()
        assign_gender_cancel = Button(
            buttons, text="CANCEL", command=cancel_assign_gender, width=7)
        assign_gender_cancel.grid(column=2, row=0, sticky="e", padx=0)

        assign_gender_dlg.canvas.title_1.config(text="Assign Father or Mother to Partner")
        assign_gender_dlg.canvas.title_2.config(text="")

        assign_gender_dlg.resize_window()
        self.wait_window(assign_gender_dlg)
        if assign_gender_dlg_cancelled is False:
            pa_id = self.right_id.get()
            if pa_id == choices[0]:
                ma_id = choices[1]
            elif pa_id == choices[1]:
                ma_id = choices[0]
            return pa_id, ma_id

    def get_marital_event_types(self, conn, cur):

        marital_event_types = get_all_marital_event_types(conn, cur)
        qlen = len(marital_event_types)
        marital_event_types.insert(0, self.current_person)
        marital_event_types.insert(0, self.current_person)

        sql = '''
                SELECT finding_id, person_id1, kin_type_id1,
                    person_id2, kin_type_id2, date
                FROM finding
                WHERE (person_id1 = ? OR person_id2 = ?) 
                    AND event_type_id in ({})
            '''.format(",".join(["?"] * qlen))

        cur.execute(sql, marital_event_types)
        marital_findings_current_person = [list(i) for i in cur.fetchall()]
        return marital_findings_current_person

    def make_nukefam_inputs(self, on_load=False):
        """ Run in main.py on_load=True and in redraw_families_table() 
            on_load=False.
        """
        self.nukefam_inputs = []

        if on_load:
            self.make_nukefam_widgets_perm()
        self.make_nukefam_dicts()
        self.populate_nuke_tables()
        for widg in self.nukefam_inputs:
            widg.bind("<FocusIn>", self.get_original, add="+")
            widg.bind("<FocusOut>", self.get_final)
        if on_load:
            self.make_new_kin_inputs()
        self.new_kid_frame.grid(column=0, row=self.last_row, sticky="ew")
        for row in range(self.nukefam_window.grid_size()[1]):
            self.nukefam_window.rowconfigure(row, weight=1)
        if on_load is False:
            formats = make_formats_dict()
            configall(self.nukefam_window, formats)

        self.update_idletasks()
        wd = self.nukefam_window.winfo_reqwidth()
        ht = self.right_panel.winfo_reqheight()
        self.nukefam_canvas.config(width=wd, height=ht)        
        self.nukefam_canvas.config(scrollregion=self.nukefam_canvas.bbox('all'))
        self.make_idtips()

    def make_progeny_frames(self, v, progeny_frame):
        r = 0
        for dkt in v["children"]:
            c = 0
            for i in range(6):
                if c == 0:
                    spacer = Frame(progeny_frame, width=48)
                    spacer.grid(column=c, row=r)
                elif c == 1:
                    text = dkt["name"]
                    ent = EntryAutoPerson(
                        progeny_frame, width=0, autofill=True, cursor="hand2", 
                        values=self.person_autofill_values)
                    if len(text) > self.findings_table.kin_widths[c]:
                        self.findings_table.kin_widths[c] = len(text)
                    ent.insert(0, text)
                    ent.grid(column=c, row=r, sticky="w")
                    self.nukefam_inputs.append(ent)
                    EntryAutoPerson.person_autofills.append(ent)
                    dkt["name_widg"] = ent
                    self.bind_autofill(ent)
                elif c == 2:
                    text = dkt["gender"]
                    ent = EntryAutoPerson(progeny_frame, width=0)
                    if len(text) > self.findings_table.kin_widths[c]:
                        self.findings_table.kin_widths[c] = len(text)
                    ent.insert(0, text)
                    ent.grid(column=c, row=r, sticky="w")
                    self.nukefam_inputs.append(ent)
                    dkt["gender_widg"] = ent
                elif c == 3:
                    text = dkt["birth"]
                    if text in ("", "unknown"):
                        text = "(birth date)"
                    ent = EntryAutoPerson(progeny_frame, width=0)
                    if len(text) > self.findings_table.kin_widths[c]:
                        self.findings_table.kin_widths[c] = len(text)
                    ent.insert(0, text)
                    ent.grid(column=c, row=r, sticky="w")
                    self.nukefam_inputs.append(ent)
                    dkt["birth_widg"] = ent
                elif c == 4:
                    text = "to"
                    if len(text) > self.findings_table.kin_widths[c]:
                        self.findings_table.kin_widths[c] = len(text)
                    lab = LabelEntry(progeny_frame, text=text, anchor="w")
                    lab.grid(column=c, row=r, sticky="w")
                elif c == 5:
                    text = dkt["death"]
                    if text in ("", "unknown"):
                        text = "(death date)"
                    ent = EntryAutoPerson(progeny_frame, width=0)
                    if len(text) > self.findings_table.kin_widths[c]:
                        self.findings_table.kin_widths[c] = len(text)
                    ent.insert(0, text)
                    ent.grid(column=c, row=r, sticky="w")
                    self.nukefam_inputs.append(ent)
                    dkt["death_widg"] = ent 
                c += 1
            r += 1

    def populate_nuke_tables(self):
        lst = [            
            self.parents_data[0][1]["name"],
            self.parents_data[0][2]["name"]]  
        for name in lst:
            if name == "name unknown":
                idx = lst.index(name)
                lst[idx] = ""
        a = 0
        for name in lst:
            if name and a == 0:
                self.pa_input.insert(0, name)
            elif name and a == 1:
                self.ma_input.insert(0, name)
            a += 1
        top_child_rows = []
        self.pardrads = []
        n = 0
        for i, (k,v) in enumerate(self.progeny_data.items(), start=1):
            n = (i * 2) - 1
            pard_kin_text = ""
            name = v["partner_name"]
            partner_kin_type = v["partner_kin_type"]

            if partner_kin_type is None:
                pard_kin_text = "Partner:"
            elif len(partner_kin_type) != 0:
                pard_kin_text = "{}:".format(v["partner_kin_type"].title()) 
            
            pard_id = k
            pard = "pard_{}_{}".format(pard_id, n)
            pardframe = Frame(self.nukefam_window)
            pardframe.grid(column=0, row=n, sticky="ew")
            self.nukefam_containers.append(pardframe)
            pardrad = Radiobutton(
                pardframe, variable=self.newkidvar, 
                value=n, anchor="w")
            self.pardrads.append(pardrad)
            pardrad.grid(column=0, row=n)
            if n == 1:
                pardrad.select()

            if partner_kin_type is None:
                pardlab = LabelH3(pardframe, text=pard_kin_text, anchor="w")
            if len(v["children"]) != 0 and len(partner_kin_type) == 0:
                ma_pa = "{}:".format(v["parent_type"])
                pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            elif len(v["children"]) != 0 and len(partner_kin_type) != 0:
                ma_pa = "{} ({}):".format(partner_kin_type.title(), v["parent_type"])
                pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            else:
                pardlab = LabelH3(pardframe, text=pard_kin_text, anchor="w")

            self.pardlabs.append(pardlab)
            pardlab.grid(column=1, row=n)
            pardent = EntryAutoPerson(
                pardframe, width=48, autofill=True, cursor="hand2", 
                values=self.person_autofill_values, name=pard)
            pardent.insert(0, name)
            pardent.grid(column=2, row=n, padx=(12,0))
            self.bind_autofill(pardent)
            EntryAutoPerson.person_autofills.append(pardent)

            v["inwidg"] = pardent
            self.nukefam_inputs.append(pardent)
            progeny_frame = Frame(self.nukefam_window)
            progeny_frame.grid(column=0, row=n+1)
            self.nukefam_containers.append(progeny_frame)
            top_child_rows.append(progeny_frame)

            self.make_progeny_frames(v, progeny_frame)

        self.last_row = n + 2

        for frm in top_child_rows:            
            top_row = frm.grid_slaves(row=0)            
            top_row.reverse()  
            z = 1
            for widg in top_row[1:]:
                widg.config(width=self.findings_table.kin_widths[z] + 2)
                z += 1

    def make_parents_dict(self, ma_id=None, pa_id=None):

        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        cur.execute(select_finding_id_birth, (self.current_person,))
        birth_id = cur.fetchone()[0]
        cur.execute(select_finding_couple_details, (birth_id,))
        parent_record = cur.fetchall()
        if len(parent_record) != 0:
            self.parent_record = parent_record[0]
        else:
            self.parent_record = None
        pa_name = ""
        ma_name = ""
        dad = None
        mom = None
        if self.parent_record:
            dad = self.parent_record[1:3]
            mom = self.parent_record[3:]
            pa_id = dad[0]
            ma_id = mom[0]
            self.parents_data[0][0]["birth_id"] = self.parent_record[0]
        else:
            self.parents_data[0][0]["birth_id"] = None

        for person in self.person_autofill_values:
            if person == pa_id:
                pa_name = self.person_autofill_values[pa_id][0]["name"]

        for person in self.person_autofill_values:
            if person == ma_id:
                ma_name = self.person_autofill_values[ma_id][0]["name"]
        parents = self.parents_data[0]
        parents[1]["id"] = pa_id
        parents[2]["id"] = ma_id
        parents[1]["name"] = pa_name
        parents[2]["name"] = ma_name
        parents[1]["inwidg"] = self.pa_input
        parents[2]["inwidg"] = self.ma_input
        self.get_alt_parents(cur)
        self.grid_alt_parents()

        cur.execute("DETACH tree")
        cur.close()
        conn.close()

    def make_nukefam_dicts(self):        
        tree = get_current_file()[0]
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute("ATTACH ? AS tree", (tree,))
        self.make_parents_dict()

        partners1, births = self.query_nukefams_data(conn, cur)
        alt_parentage_findings = self.query_alt_nukefams_data(conn, cur)
        self.arrange_partners_progeny(
            partners1, births, alt_parentage_findings, conn, cur)

        main_sorter = [0, 0, 0]
        for k,v in self.progeny_data.items():
            kids = v["children"]
            kids = sorted(kids, key=lambda i: i["sorter"])
            v["children"] = kids
            if len(v["children"]) != 0:
                main_sorter = v["children"][0]["sorter"]
            if len(v.get("sorter")) == 0:
                v["sorter"] = main_sorter
        self.progeny_data = dict(
            sorted(
                self.progeny_data.items(), key=lambda i: i[1]["sorter"]))
        cur.execute("DETACH tree")
        cur.close()
        conn.close()

    def arrange_partners_progeny(
            self, partners1, births, alt_parentage_findings, conn, cur):
        """ Updating person_autofill_values is necessary since 
            `redraw_families_table()` destroys partner and child frames
            and alt parent inputs.
        """
        births = births + alt_parentage_findings
        progeny = {}
        all_partners = [] 
        marital_finding_pards = []
        offspring_pards = []
        if partners1:
            partners = [tup for tup in partners1 if self.current_person in tup]
            for tup in partners:
                for num in tup:
                    if num != self.current_person:
                        marital_finding_pards.append(num)
                        all_partners.append(num)
            marital_finding_pards = list(set(marital_finding_pards))
        for tup in births:
            if tup[1] != self.current_person:
                pard_id = tup[1]              
            elif tup[3] != self.current_person:
                pard_id = tup[3]
            offspring_pards.append(pard_id)
            all_partners.append(pard_id)
        for pard_id in all_partners:
            compound_parent_type = False
            if pard_id in offspring_pards:
                if offspring_pards.count(pard_id) > 1:
                    compound_parent_type = True
                if pard_id in marital_finding_pards:
                    nested = {'offspring': True, 'marital_findings': True}
                elif pard_id not in marital_finding_pards:
                    nested = {'offspring': True, 'marital_findings': False}
            elif pard_id not in offspring_pards and pard_id in marital_finding_pards:
                nested = {'offspring': False, 'marital_findings': True}
            progeny[pard_id] = nested
        for pard_id in progeny:
            progeny_blank = {
                "sorter": [], "partner_name": "", "parent_type": None,
                "partner_kin_type": "", "inwidg": None, "children": [],
                "marital_findings": []}
            self.progeny_data[pard_id] = progeny_blank
        self.collect_couple_events(cur, conn)
        for k,v in progeny.items():
            pardner = k
            if v["offspring"] is True:
                for tup in births:
                    order = "{}-{}".format(str(tup[2]), str(tup[4]))                
                    if tup[3] == pardner:  
                        parent_type = tup[4]
                        pard_id = tup[3]
                        self.make_pard_dict(
                            pard_id, parent_type, cur, 
                            compound_parent_type=compound_parent_type)
                        if pard_id == pardner:
                            self.progeny_data[pardner]["children"].append(
                                {"birth_id": tup[0], "order": order})
                    elif tup[1] == pardner:
                        parent_type = tup[2]
                        pard_id = tup[1]
                        self.make_pard_dict(
                            pard_id, parent_type, cur, 
                            compound_parent_type=compound_parent_type) 
                        if pard_id == pardner:
                            self.progeny_data[pardner]["children"].append(
                                {"birth_id": tup[0], "order": order})
            elif v["marital_findings"] is True and v["offspring"] is False:
                self.make_pard_dict(pardner, "", cur)

        for pard_id in progeny:
            for k,v in self.progeny_data.items():
                if k == pard_id:
                    for dkt in v["children"]:
                        self.finish_progeny_dict(dkt, cur)

    def make_pard_dict(self, pard_id, parent_type, cur, compound_parent_type=None): 
        """ When a partner of the current person is BOTH alt parent and parent 
            of some of the current person's children (depending on which child), 
            `self.parent_types` gets the label text `compound_parent_text` right, 
            e.g. "Children's mother or foster mother". When a partner is EITHER 
            alt parent or parent of the current person's child(ren), 
            `parent_types` gets the label right, e.g. "Children's mother".
        """
        if not compound_parent_type or compound_parent_type is False:
            parent_types = []
        elif compound_parent_type is True:
            parent_types = self.parent_types
        if parent_type:
            parent_types.append(parent_type)
        p = 0
        for partype in parent_types:
            for k,v in PARENT_TYPES.items():
                if k == partype:
                    p_type = v
                    parent_types[p] = p_type
                    break
            p += 1
        parent_types = list(set(parent_types))
        stg = " or ".join(parent_types)
        if pard_id is None:
            partner_name = ""
            stg = "parent"
        else:
            partner_name = self.person_autofill_values[pard_id][0]["name"]
        compound_parent_text = "Children's {}".format(stg)

        self.progeny_data[pard_id]["parent_type"] = compound_parent_text
        self.progeny_data[pard_id]["partner_name"] = partner_name 

    def collect_couple_events(self, cur, conn):
        marital_findings = self.get_marital_event_types(conn, cur) 
        for lst in marital_findings:
            if lst[1] == self.current_person:
                del lst[1:3]
            elif lst[3] == self.current_person:
                del lst[3:5]            

        self.sorters = []
        for lst in marital_findings:
            self.save_marital_events(lst, cur)

        self.sorters = sorted(self.sorters, key=lambda i: i[1])
        for k,v in self.progeny_data.items():
            for sorter in self.sorters:
                if sorter[0] == k:
                    v["sorter"] = sorter[1]

    def save_marital_events(self, lst, cur):
        partner_id = lst[1]
        for k,v in self.progeny_data.items():
            if partner_id == k:
                cur.execute(select_kin_types, (lst[2],))
                kin_type = cur.fetchone()
                if kin_type:
                    kin_type = kin_type[0]
                sorter = self.make_sorter(lst[3])
                self.sorters.append((k, sorter))
                if kin_type in ("generic_partner1", "generic_partner2"):
                    kin_type = "Partner"
                v["partner_kin_type"] = kin_type
                v["marital_findings"].append({"finding": lst[0]})

    def make_sorter(self, date):
        sorter = [0,0,0]
        if date != "-0000-00-00-------":
            sorter = date.split("-")[1:4] 
            h = 0
            for stg in sorter:
                if len(stg) == 0:
                    sorter[h] = '0'
                h += 1
            num = sorter[1]
            if sorter[1] != '0':
                num = OK_MONTHS.index(sorter[1]) + 1
            else:
                num = 0
            sorter = [int(sorter[0]), num, int(sorter[2])]
        return sorter

    def finish_progeny_dict(self, dkt, cur):
        cur.execute(
            select_finding_person_date_by_finding_and_type, 
            (dkt["birth_id"],))
        result = cur.fetchone()
        if result is None:
            return self.finish_alt_progeny_dict(dkt, cur)
        else:
            born_id, birth_date = result
        cur.execute(select_finding_death_date, (born_id,))
        death_date = cur.fetchone()
        if death_date:
            death_date, death_id = death_date
        else:
            death_date = "-0000-00-00-------"
            death_id = None

        cur.execute(select_person_gender_by_id, (born_id,))
        gender = cur.fetchone()[0]

        sorter = self.make_sorter(birth_date)
        name = self.person_autofill_values[born_id][0]["name"]
        birth_date = format_stored_date(
            birth_date, date_prefs=self.date_prefs)
        death_date = format_stored_date(
            death_date, date_prefs=self.date_prefs)                

        dkt["gender"] = gender
        dkt["birth"] = birth_date
        dkt["sorter"] = sorter
        dkt["death"] = death_date
        dkt["name"] = name
        dkt["id"] = born_id
        dkt["death_id"] = death_id

    def finish_alt_progeny_dict(self, dkt, cur):
        cur.execute(select_finding_person_date_alt_parent_event, (dkt["birth_id"],))

        born_id, birth_date = cur.fetchone()
        cur.execute(select_finding_death_by_person, (born_id,))
        death_date = cur.fetchone()
        if death_date:
            death_date = death_date[0]
        else:
            death_date = "-0000-00-00-------"

        cur.execute(select_person_gender_by_id, (born_id,))
        gender = cur.fetchone()[0]

        sorter = self.make_sorter(birth_date)
        name = self.person_autofill_values[born_id][0]["name"]

        birth_date = format_stored_date(
            birth_date, date_prefs=self.date_prefs)
        death_date = format_stored_date(
            death_date, date_prefs=self.date_prefs)                

        dkt["gender"] = gender
        dkt["birth"] = birth_date
        dkt["sorter"] = sorter
        dkt["death"] = death_date
        dkt["name"] = name
        dkt["id"] = born_id 

    def query_nukefams_data(self, conn, cur):
        cur.execute(select_finding_couple_person1_details, (self.current_person,))
        result1 = cur.fetchall()
        cur.execute(select_finding_couple_person2_details, (self.current_person,))
        result2 = cur.fetchall()
        births = []
        births = [tup for q in (result1, result2) for tup in q]
        marital_event_types = get_all_marital_event_types(conn, cur)
        qlen = len(marital_event_types)

        sql = '''
                SELECT person_id1, person_id2
                FROM finding
                WHERE event_type_id in ({})                    
            '''.format(",".join("?" * qlen))
        cur.execute(sql, marital_event_types)
        partners1 = cur.fetchall()
        return partners1, births

    def query_alt_nukefams_data(self, conn, cur):
        cur.execute(
            select_finding_couple_details_alt_parent1, (self.current_person,))
        result1 = cur.fetchall()
        cur.execute(
            select_finding_couple_details_alt_parent2, (self.current_person,))
        result2 = cur.fetchall()
        alt_births = []
        alt_births = [tup for q in (result1, result2) for tup in q]
        alt_births = [list(i) for i in alt_births]
        for lst in alt_births:
            cur.execute(select_finding_id_by_person_and_event, (lst[0],))
            birth_evt_id = cur.fetchone()[0]
            lst[0] = birth_evt_id
        return alt_births

    def get_alt_parents(self, cur):
        """ Get adoptive parents, foster parents & guardians. """
        cur.execute(select_finding_details_sorter, (self.current_person,))
        alt_parent_findings = cur.fetchall()
        if alt_parent_findings is None:
            return
        r = 0
        for finding in alt_parent_findings:
            finding = list(finding)
            finding[1] = [int(i) for i in finding[1].split(",")]
            alt_parent_findings[r] = finding
            r += 1
        self.alt_parent_findings = sorted(alt_parent_findings, key=lambda i: i[1])

        self.make_alt_parents_dict(cur)
        alt_parent_details = self.parents_data[1:]
        j = 0
        for lst in alt_parent_details:
            lab_l = Label(self.parents_area, anchor="e")
            ent_l = EntryAutoPerson(
                self.parents_area, width=30, autofill=True, cursor="hand2", 
                values=self.person_autofill_values,
                name="altparent_l{}".format(str(j)))
            if lst[1]["kin_type"]:
                ent_l.insert(0, lst[1]["name"])
            lst[1]["inwidg"] = ent_l
            lst[1]["labwidg"] = lab_l
            if lst[1]["kin_type"]:
                lab_l.config(text=lst[1]["kin_type"].title())

            lab_r = Label(self.parents_area, anchor="e")
            ent_r = EntryAutoPerson(
                self.parents_area, width=30, autofill=True, cursor="hand2", 
                values=self.person_autofill_values,
                name="altparent_r{}".format(str(j)))
            if lst[2]["kin_type"]:
                ent_r.insert(0, lst[2]["name"]) 
            lst[2]["inwidg"] = ent_r
            lst[2]["labwidg"] = lab_r
            if lst[2]["kin_type"]:
                lab_r.config(text=lst[2]["kin_type"].title())

            for ent in (ent_l, ent_r):
                self.bind_autofill(ent)
                self.nukefam_containers.append(ent)
                EntryAutoPerson.person_autofills.append(ent)
            for lab in (lab_l, lab_r):
                lab.bind("<Double-Button-1>", self.change_alt_parent_type)
            self.nukefam_containers.extend([lab_l, lab_r])          
            j += 1

    def grid_alt_parents(self):
        """ Grid widgets as children of self.parents_area. """
        alt_parents = self.parents_data[1:]
        x = 1
        for lst in alt_parents:
            z = 0
            for person in lst[1:]:
                label = person["labwidg"]
                widget = person["inwidg"]
                label.grid(column=z, row=x, sticky="ew", padx=12, pady=(6,12))
                widget.grid(column=z+1, row=x, pady=(6,12))
                z += 2 
            x += 1

    def make_alt_parents_dict(self, cur):
        for finding in self.alt_parent_findings:
            parent_couple = [ 
                {'birth_id': finding[0], 'sorter': finding[1]}, 
                {'id': None, 'name': '', 'kin_type_id': None, 'kin_type': '', 
                    'labwidg': None, 'inwidg': None}, 
                {'id': None, 'name': '', 'kin_type_id': None, 'kin_type': '', 
                    'labwidg': None, 'inwidg': None}]
            common, alt_parent1, alt_parent2 = parent_couple
            cur.execute(select_finding_kin_types, (common["birth_id"],))
            alt_parent1["kin_type_id"], alt_parent2["kin_type_id"] = cur.fetchone()
            h = 1
            for kintype in (alt_parent1["kin_type_id"], alt_parent2["kin_type_id"]):    
                if kintype:
                    cur.execute(select_kin_type_string, (kintype,))
                    parent_couple[h]["kin_type"] = cur.fetchone()[0]
                h += 1
            self.parents_data.append(parent_couple)
        alt_parents = self.parents_data[1:] 
        for lst in alt_parents:
            finding_id = lst[0]["birth_id"]
            cur.execute(select_finding_persons, (finding_id,))
            lst[1]["id"], lst[2]["id"] = cur.fetchone()

        w = 0
        for lst in alt_parents:
            id1 = lst[1]["id"]
            id2 = lst[2]["id"]
            if id1:
                lst[1]["name"] = self.person_autofill_values[id1][0]["name"]
            if id2:
                lst[2]["name"] = self.person_autofill_values[id2][0]["name"]
            w += 1

    def get_original(self, evt):
        """ Make sure that everything works right when making new conclusion. At
            one time I had to not bind to FocusOut event till FocusIn event
            had taken place, but I think I did away with that assuming the 
            problem had been solved somewhere along the way. """
        self.original = evt.widget.get()

    def get_final(self, evt):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        widg = evt.widget
        self.final = widg.get()
        if self.final == self.original:
            return
        gridinfo = widg.grid_info()
        column, row = gridinfo["column"], gridinfo["row"]
        widgname = widg.winfo_name()
        if widgname == "pa":
            self.update_parent(self.final, conn, cur, widg, column=column, kin_type=1)
        elif widgname == "ma":
            self.update_parent(self.final, conn, cur, widg, column=column, kin_type=2)
        elif widgname.startswith("altparent"):
            labcol = column - 1
            for child in self.parents_area.winfo_children():
                if child.winfo_class() == "Label" and child.winfo_subclass() == "Label":
                    childgridinfo = child.grid_info()
                    if childgridinfo["column"] == labcol and childgridinfo["row"] == row:
                        text = child.cget("text")
                        break
            kin_type = None
            if text.startswith("A"):
                kin_type = 83
            elif text.startswith("F"):
                kin_type = 95
            elif text.startswith("G"):
                kin_type = 48                    
            self.update_parent(self.final, conn, cur, widg, column, kin_type=kin_type)
        elif widgname.startswith("pard"):
            if column == 2:
                if len(widg.get()) == 0:
                    self.unlink_partners_dialog(cur, conn, widg)
                else:
                    self.link_partners_dialog(cur, conn, widg)                
            else:
                print(
                    "line", 
                    looky(seeline()).lineno, 
                    "case not handled for column", column)
        else:
            if column == 1:
                self.update_child(widg, conn, cur)
            elif column == 2:
                self.update_child_gender(widg, conn, cur)
            elif column == 3:
                self.update_child_birth(widg, conn, cur)
            elif column == 5:
                self.update_child_death(widg, conn, cur)
            else:
                print("line", looky(seeline()).lineno, "get_final() case not handled:")    

        cur.close()
        conn.close()
        current_name = self.person_autofill_values[self.current_person][0]["name"]
        redraw_person_tab(
            main_window=self.treebard.main, 
            current_person=self.current_person, 
            current_name=current_name)

    def update_parent(self, final, conn, cur, inwidg, column=None, 
            kin_type=None, alt_parent=None):

        def delete_parent(column):
            if column == 1:
                cur.execute(update_finding_person_1, (None, None, finding_id))
            elif column == 3:
                cur.execute(update_finding_person_2, (None, None, finding_id))
            conn.commit()
            inwidg.focus_set()
        
        for lst in self.parents_data:    
            for dkt in lst[1:]:
                if inwidg == dkt["inwidg"]:
                    finding_id = lst[0]["birth_id"]
                    break
            
        if len(self.final) != 0 or len(self.original) == 0:
            self.make_parent(column, finding_id, inwidg, conn, cur)
        elif len(self.final) == 0:
            column = inwidg.grid_info()["column"]
            delete_parent(column)
            inwidg.focus_set()
        else:
            print("line", looky(seeline()).lineno, "case not handled:")

    def make_parent(self, column, finding_id, widg, conn, cur):

        def err_done4(entry, msg):
            entry.delete(0, 'end')
            msg4[0].grab_release()
            msg4[0].destroy()
            entry.focus_set()

        name_data = check_name(ent=widg)
        if name_data is None:
            if self.no_error is True:
                self.no_error = False
                return
            else:
                msg4 = open_message(
                    self, 
                    families_msg[1], 
                    "Person Name Unknown", 
                    "OK")
                msg4[0].grab_set()
                msg4[2].config(command=lambda entry=widg, msg=msg4: err_done4(
                    entry, msg))
                return
        elif name_data == "add_new_person":
            new_parent_id = open_new_person_dialog(
                self, widg, self.root, self.treebard, 
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
        else:
            new_parent_id = name_data[1]

        cur.execute(select_finding_event_type, (finding_id,))
        event_type = cur.fetchone()[0]
        kin_type_id = None

        if event_type == 1:
            if column == 1:
                kin_type_id = 1
            elif column == 3:
                kin_type_id = 2
        elif event_type == 83:
            kin_type_id = 110 
        elif event_type == 95:
            kin_type_id = 120
        elif event_type == 48:
            kin_type_id = 130
        else:
            print("line", looky(seeline()).lineno, "case not handled:")

        if column == 1:
            cur.execute(update_finding_person_1, (new_parent_id, kin_type_id, finding_id))
        elif column == 3:
            cur.execute(update_finding_person_2, (new_parent_id, kin_type_id, finding_id))
        else:
            print("line", looky(seeline()).lineno, "case not handled:")
        conn.commit()

    def link_partners_dialog(self, cur, conn, inwidg):
        def ok_link_partner(checks):
            copy = checks
            i = 0
            for dkt in copy["marital_findings"]:
                checks["marital_findings"][i]["vars"] = dkt["vars"].get()
                i += 1            
            self.link_partners["marital_findings"] = checks["marital_findings"]

            copy = checks
            j = 0
            for dkt in copy["children"]:
                checks["children"][j]["vars"] = dkt["vars"].get()
                j += 1            
            self.link_partners["children"] = checks["children"]
            self.null_partner_replacer.destroy()          
        def cancel_link_partner():
            self.cancel_link_partner_pressed = True
            self.null_partner_replacer.destroy()
            self.cancel_link_partner_pressed = False
        def update_partners_link(inwidg, conn, cur):
            """ Run after user selects which marital_findings & children to link
                to the new partner and the dialog closes. 
            """
            if self.cancel_link_partner_pressed is True:
                return

            name_data = check_name(ent=inwidg)
            if name_data is None:
                msg5 = open_message(
                    self, 
                    families_msg[1], 
                    "Person Name Unknown", 
                    "OK")
                msg5[0].grab_set()
                return
            elif name_data == "add_new_person":
                self.new_partner_id = open_new_person_dialog(
                    self, inwidg, self.root, self.treebard, 
                    person_autofill_values=self.person_autofill_values)
                self.person_autofill_values = update_person_autofill_values()
                
            else:
                self.new_partner_id = name_data[1]

            for dkt in self.link_partners["marital_findings"]:
                if dkt["vars"] == 0:
                    continue
                elif dkt["vars"] == 1:
                    link_partner(dkt["finding"], inwidg)
            for dkt in self.link_partners["children"]:
                if dkt["vars"] == 0:
                    continue
                elif dkt["vars"] == 1:
                    link_offspring(dkt["birth_id"])

        def link_partner(finding_id, inwidg):

            cur.execute(select_finding_persons, (finding_id,))
            person_id1, person_id2 = cur.fetchone()
            if self.current_person == person_id1:
                cur.execute(update_finding_partner2, (self.new_partner_id, finding_id))
            elif self.current_person == person_id2:
                cur.execute(update_finding_partner1, (self.new_partner_id, finding_id))
            conn.commit()

        def link_offspring(finding_id):
            cur.execute(select_finding_persons, (finding_id,))
            person_id1, person_id2 = cur.fetchone()
            if self.current_person == person_id1:
                cur.execute(update_finding_mother, (self.new_partner_id, finding_id))
            elif self.current_person == person_id2:
                cur.execute(update_finding_father, (self.new_partner_id, finding_id))
            conn.commit()

        partner_id = None
        checks = {"marital_findings": [], "children": []}
        for k,v in self.progeny_data.items():
            if v["inwidg"] == inwidg:
                partner_id = k
                break

        for finding in self.progeny_data[partner_id]["marital_findings"]:
            checks["marital_findings"].append(finding)
        for child in self.progeny_data[partner_id]["children"]:
            checks["children"].append(child)

        message = "Select which marital_findings & children to link to added partner:"
        self.null_partner_replacer = Dialogue(self.root)
        
        head = LabelHeader(
            self.null_partner_replacer.window, text=message, justify='left', wraplength=650)
        inputs = Frame(self.null_partner_replacer.window)

        s = 1
        for finding in checks["marital_findings"]: 
            cur.execute(select_finding_details, (finding["finding"],))
            finding_id, finding_date, event_type = cur.fetchone()
            finding_date = format_stored_date(
                finding_date, date_prefs=self.date_prefs)
            text = "{} {} (Conclusion #{})".format(
                finding_date, event_type, finding_id)
            var = tk.IntVar()
            chk = Checkbutton(inputs, variable=var)
            chk.grid(column=0, row=s)
            finding["vars"] = var
            evtlab = Label(inputs, text=text, anchor="w")
            evtlab.grid(column=1, row=s, sticky="we")
            s += 1

        m = s
        for child in checks["children"]:
            var = tk.IntVar()
            chk = Checkbutton(
                inputs,
                variable=var)
            chk.grid(column=0, row=m)
            child["vars"] = var
            lab = Label(
                inputs, text="{}  #{}".format(
                    child["name"], child["id"]),
                anchor="w")
            lab.grid(column=1, row=m, sticky="we")
            m += 1

        buttons = Frame(self.null_partner_replacer.window)
        b1 = Button(
            buttons, text="OK", 
            command=lambda checks=checks: ok_link_partner(checks))
        b2 = Button(
            buttons, text="CANCEL", command=cancel_link_partner) 

        self.null_partner_replacer.canvas.title_1.config(
            text="Select Children & Marital Conclusions to Link to Added Partner")
        self.null_partner_replacer.canvas.title_2.config(text="") 
        
        head.grid(
            column=0, row=0, sticky='news', padx=12, pady=12,  
            columnspan=2, ipady=6, ipadx=6)
        inputs.grid(column=1, row=1, sticky="news", padx=12)

        buttons.grid(
            column=1, row=6, sticky="e", padx=12, pady=12, columnspan=2)
        b1.grid(column=0, row=0, sticky='e', ipadx=3)
        b2.grid(column=1, row=0, padx=(6,0), sticky='e', ipadx=3)

        self.null_partner_replacer.resize_window()
        # Find the first input in the dialog and give it focus, otherwise the
        #   root dialog will be on top.
        for child in inputs.winfo_children():
            child.focus_set()
            break

        self.root.wait_window(self.null_partner_replacer)
        update_partners_link(inwidg, conn, cur)

    def unlink_partners_dialog(self, cur, conn, widg):
        def ok_unlink_partner(checks):
            copy = checks
            i = 0
            for dkt in copy["marital_findings"]:
                h = 0
                for var in dkt["vars"]:
                    got = var.get()
                    checks["marital_findings"][i]["vars"][h] = got
                    h += 1
                i += 1            
            self.unlink_partners["marital_findings"] = checks["marital_findings"]

            copy = checks
            j = 0
            for dkt in copy["children"]:
                h = 0
                for var in dkt["vars"]:
                    got = var.get()
                    checks["children"][j]["vars"][h] = got
                    h += 1
                j += 1            
            self.unlink_partners["children"] = checks["children"]

            self.partner_unlinker.destroy()
            
        def cancel_unlink_partner():
            self.cancel_unlink_partner_pressed = True
            self.partner_unlinker.destroy()
            self.cancel_unlink_partner_pressed = False

        def update_partners_unlink(conn, cur):
            """ Run after dialog closes. """
            if self.cancel_unlink_partner_pressed is True:
                return
            for dkt in self.unlink_partners["marital_findings"]:
                finding = dkt["finding"]
                if dkt["vars"] == [0, 0]:
                    continue
                elif dkt["vars"] == [1, 1]:
                    delete_couple_finding(finding)
                elif dkt["vars"] == [0, 1]:
                    unlink_partner(finding, [0, 1])
                elif dkt["vars"] == [1, 0]:
                    unlink_partner(finding, [1, 0])
            for dkt in self.unlink_partners["children"]:
                finding = dkt["birth_id"]
                if dkt["vars"] == [0, 0]:
                    continue
                elif dkt["vars"] == [1, 1]:
                    delete_offspring(conn, cur, finding)
                elif dkt["vars"] == [0, 1]:
                    unlink_offspring(finding, [0, 1])
                elif dkt["vars"] == [1, 0]:
                    unlink_offspring(finding, [1, 0])

        def delete_offspring(conn, cur, finding_id):
            cur.execute(update_finding_ages_kintypes_null, (finding_id,))
            conn.commit()

        def unlink_partner(finding_id, order):
            cur.execute(select_finding_persons, (finding_id,))
            person_id1, person_id2 = cur.fetchone()
            currper = self.current_person
            if currper == person_id1:
                if order == [0, 1]:
                    cur.execute(update_finding_person_2_null_by_id, (finding_id,))
                elif order == [1, 0]:
                    cur.execute(update_finding_person_1_null_by_id, (finding_id,))                
            elif currper == person_id2:
                if order == [0, 1]:
                    cur.execute(update_finding_person_1_null_by_id, (finding_id,))
                elif order == [1, 0]:
                    cur.execute(update_finding_person_2_null_by_id, (finding_id,))
            conn.commit()

        def unlink_offspring(finding_id, order):
            cur.execute(select_finding_persons, (finding_id,))
            person_id1, person_id2 = cur.fetchone()
            currper = self.current_person
            if currper == person_id1:
                if order == [0, 1]:
                    cur.execute(update_finding_person_2_null_by_id, (finding_id,))
                elif order == [1, 0]:
                    cur.execute(update_finding_person_1_null_by_id, (finding_id,))
            elif currper == person_id2:
                if order == [0, 1]:
                    cur.execute(update_finding_person_1_null_by_id, (finding_id,))
                elif order == [1, 0]:
                    cur.execute(update_finding_person_2_null_by_id, (finding_id,))
            conn.commit()

        partner_id = None
        checks = {"marital_findings": [], "children": []}
        for k,v in self.progeny_data.items():
            if v["inwidg"] == widg:
                partner_id = k
                break

        for finding in self.progeny_data[partner_id]["marital_findings"]:
            checks["marital_findings"].append(finding)
        for child in self.progeny_data[partner_id]["children"]:
            checks["children"].append(child)
            
        message = "Select which marital_findings/children to unlink from whom:"
        self.partner_unlinker = Dialogue(self.root)
        head = LabelHeader(
            self.partner_unlinker.window, text=message, justify='left', wraplength=650)
        inputs = Frame(self.partner_unlinker.window)
        self.current_person_name = self.person_autofill_values[self.current_person][0]["name"]
        currperlab = LabelH3(inputs, text=self.current_person_name)
        currperlab.grid(column=1, row=0)
        spacer0 = Label(inputs, width=3)
        spacer0.grid(column=2, row=0)
        pardlab = LabelH3(inputs, text=self.original.split("(")[0])
        pardlab.grid(column=3, row=0)
        f = 1
        for finding in checks["marital_findings"]: 
            cur.execute(select_finding_details, (finding["finding"],))
            finding_id, finding_date, event_type = cur.fetchone()
            finding_date = format_stored_date(finding_date, date_prefs=self.date_prefs)
            text = "{} {} (Conclusion #{}):".format(finding_date, event_type, finding_id)
            evtlab = Label(inputs, text=text, anchor="e")
            evtlab.grid(column=0, row=f, sticky="e")
            var0 = tk.IntVar()
            var1 = tk.IntVar()
            chk0 = Checkbutton(inputs, variable=var0)
            chk0.grid(column=1, row=f)
            chk1 = Checkbutton(inputs, variable=var1)
            finding["vars"] = [var0, var1]
            chk1.grid(column=3, row=f)
            chk1.select()
            f += 1

        g = f
        for child in checks["children"]: 
            text = "{}  #{}:".format(child["name"], child["id"])
            kidlab = Label(inputs, text=text, anchor="e")
            kidlab.grid(column=0, row=g, sticky="e")
            var0 = tk.IntVar()
            var1 = tk.IntVar()
            chk0 = Checkbutton(inputs, variable=var0)
            chk0.grid(column=1, row=g)
            chk1 = Checkbutton(inputs, variable=var1)
            child["vars"] = [var0, var1]
            chk1.grid(column=3, row=g)
            chk1.select()
            g += 1

        buttons = Frame(self.partner_unlinker.window)
        b1 = Button(
            buttons, text="OK", command=lambda checks=checks: ok_unlink_partner(checks))
        b2 = Button(
            buttons, text="CANCEL", command=cancel_unlink_partner)            

        self.partner_unlinker.canvas.title_1.config(
            text="Unlink Partner from Current Person's Marital Conclusions")
        self.partner_unlinker.canvas.title_2.config(text="")            

        head.grid(
            column=0, row=4, sticky='news', padx=12, pady=12,  
            columnspan=2, ipady=6)
        inputs.grid(column=1, row=5, sticky="news", padx=12)
        buttons.grid(
            column=1, row=6, sticky="e", padx=12, pady=12, columnspan=2)
        b1.grid(column=0, row=0, sticky='e', ipadx=3)
        b2.grid(column=1, row=0, padx=(6,0), sticky='e', ipadx=3)

        self.partner_unlinker.resize_window()
        self.partner_unlinker.focus_set()

        self.root.wait_window(self.partner_unlinker)
        update_partners_unlink(conn, cur)

    def unlink_child(self, orig_child_id, parent_id, conn, cur):

        def ok_unlink_child():
            self.parents_of_child_to_unlink = [i.get() for i in (var0, var1)]
            self.child_unlinker.destroy()
            
        def cancel_unlink_child():
            self.cancel_unlink_child_pressed = True
            self.child_unlinker.destroy()
            self.cancel_unlink_child_pressed = False

        def update_child_unlink(conn, cur):
            """ Run after dialog closes. """
            if self.cancel_unlink_child_pressed is True:
                return
            if self.parents_of_child_to_unlink == [0, 0]:
                return
            else:
                unlink_parents_of_child(conn, cur, birth_id)
        
        def unlink_parents_of_child(conn, cur, birth_id):
            if self.parents_of_child_to_unlink == [1, 1]:
                cur.execute(update_finding_parents_null, (birth_id,))
                conn.commit()
            elif self.parents_of_child_to_unlink == [1, 0]:
                cur.execute(update_finding_parent1_null, (birth_id,))
                conn.commit()
            elif self.parents_of_child_to_unlink == [0, 1]:
                cur.execute(update_finding_parent2_null, (birth_id,))
                conn.commit()
            else:
                print("line", looky(seeline()).lineno, "case not handled:")

        cur.execute(select_finding_id_birth, (orig_child_id,))
        birth_id = cur.fetchone()[0]

        message = "Unlink child from whom:"
        self.child_unlinker = Dialogue(self.root)
        head = LabelHeader(
            self.child_unlinker.window, text=message, wraplength=650)
        self.current_person_name = self.person_autofill_values[self.current_person][0]["name"]
        partner_name = "null partner"
        if parent_id:
            partner_name = self.person_autofill_values[parent_id][0]["name"]

        currperlab = LabelH3(
            self.child_unlinker.window, text=self.current_person_name)
        currperlab.grid(column=1, row=5, padx=(12,0))
        spacer0 = Label(self.child_unlinker.window, width=3)
        spacer0.grid(column=2, row=5)
        pardlab = LabelH3(self.child_unlinker.window, text=partner_name)
        pardlab.grid(column=3, row=5)

        var0 = tk.IntVar()
        var1 = tk.IntVar()
        chk0 = Checkbutton(self.child_unlinker.window, variable=var0)
        chk0.grid(column=1, row=6)
        chk1 = Checkbutton(self.child_unlinker.window, variable=var1)
        chk1.grid(column=3, row=6)
        chk1.select()

        buttons = Frame(self.child_unlinker.window)
        b1 = Button(buttons, text="OK", command=ok_unlink_child)
        b2 = Button(buttons, text="CANCEL", command=cancel_unlink_child)            

        self.child_unlinker.canvas.title_1.config(
            text="Unlink Child from Current Person, Partner, or Both")
        self.child_unlinker.canvas.title_2.config(text="")            

        head.grid(
            column=0, row=4, sticky='ew', padx=12, pady=12,  
            columnspan=5, ipady=6)
        buttons.grid(
            column=3, row=7, sticky="e", padx=12, pady=12, columnspan=2)
        b1.grid(column=0, row=0, sticky='e', ipadx=3)
        b2.grid(column=1, row=0, padx=(6,0), sticky='e', ipadx=3)

        self.child_unlinker.resize_window()
        self.child_unlinker.focus_set()

        self.root.wait_window(self.child_unlinker)
        update_child_unlink(conn, cur)

    def update_child(self, widg, conn, cur):

        def do_update(widg, parent_id, child, cur, conn):
            orig_child_id = child["id"]
            new_child_id = None 
            birth_id = None
            orig_birth_id = None
            death_date = "-0000-00-00-------"
            birth_date = "-0000-00-00-------"
            sorter = (0,0,0)
            if len(self.final) == 0:
                self.unlink_child(orig_child_id, parent_id, conn, cur)
                return

            name_data = check_name(ent=widg)
            if not name_data:
                msg6 = open_message(
                    self, 
                    families_msg[1], 
                    "Person Name Unknown", 
                    "OK")
                msg6[0].grab_set()
                return

            if name_data == "add_new_person":
                new_child_id = open_new_person_dialog(
                    self, widg, self.root, self.treebard, 
                    person_autofill_values=self.person_autofill_values)
                self.person_autofill_values = update_person_autofill_values()
            else:
                new_child_id = name_data[1]

            cur.execute(select_finding_id_birth, (new_child_id,))
            birth_id = cur.fetchone()[0]
            cur.execute(select_finding_id_death, (new_child_id,))
            death_id = cur.fetchone()
            cur.execute(select_finding_date_and_sorter, (birth_id,))
            birth_date, sorter = cur.fetchone()
            sorter = self.make_sorter(birth_date)
            if death_id:
                death_id = death_id[0]
                cur.execute(select_finding_date, (death_id,))
                death_date = cur.fetchone()[0] 

            partner_parent_type = self.progeny_data[parent_id]["parent_type"]
            if partner_parent_type == "Children's mother":
                father_id, mother_id = self.current_person, parent_id
            else:
                father_id, mother_id = parent_id, self.current_person                
            cur.execute(update_finding_parents_new, (father_id, mother_id, birth_id))
            conn.commit()
            cur.execute(select_finding_id_birth, (orig_child_id,))
            orig_birth_id = cur.fetchone()[0]
            cur.execute(update_finding_parents_null, (orig_birth_id,))
            conn.commit()

        for k,v in self.progeny_data.items():
            for child in v["children"]:
                if widg != child["name_widg"]:
                    continue
                else:
                    parent_id = k
                    do_update(widg, parent_id, child, cur, conn)
                    break

    def update_child_gender(self, widg, conn, cur):
        new_gender = widg.get().strip()
        if new_gender not in ("male", "female", "unknown", "other"):
            return  
        for k,v in self.progeny_data.items():
            s = 0
            for child in v["children"]:
                if widg != child["gender_widg"]:
                    continue
                else:
                    child_id = child["id"]
                    cur.execute(update_person_gender, (new_gender, child_id))
                    conn.commit()
                    break
                s += 1

    def update_child_birth(self, widg, conn, cur):
        new_date = validate_date(self, widg, widg.get().strip())
        sorter = self.make_sorter(new_date)
        sorter = [str(i) for i in sorter]
        sorter = ",".join(sorter)
        for k,v in self.progeny_data.items():
            s = 0
            for child in v["children"]:
                if widg != child["birth_widg"]:
                    continue
                else:
                    birth_id = child["birth_id"]
                    cur.execute(update_finding_date, (new_date, sorter, birth_id))
                    conn.commit()
                    break
                s += 1

    def update_child_death(self, widg, conn, cur):
        new_date = validate_date(self, widg, widg.get().strip())
        sorter = self.make_sorter(new_date)
        sorter = [str(i) for i in sorter]
        sorter = ",".join(sorter)
        for k,v in self.progeny_data.items():
            s = 0
            for child in v["children"]:
                if widg != child["death_widg"]:
                    continue
                else:
                    death_id = child["death_id"]
                    if death_id is None:
                        cur.execute(insert_finding_death, (new_date, child["id"], sorter))
                        conn.commit()
                    else:
                        cur.execute(update_finding_date, (new_date, sorter, death_id))
                        conn.commit()
                    break
                s += 1

    def change_current_person(self, evt): 
        """ `self.no_error` prevents an error message from opening due to a 
            parent input appearing to be empty at a bad time.
        """
        self.no_error = True
        current_name = evt.widget.get()
        for tup in self.person_inputs:
            if evt.widget == tup[0]:
                current_person = tup[1]
                break
        
        self.current_person = self.treebard.main.current_person = current_person
        self.root.focus_set()
        redraw_person_tab(
            main_window=self.treebard.main,
            current_person=current_person, 
            current_name=current_name)

    def show_idtip(self, iD, name_type):
        """ Based on show_kintip() in findings table.py. """
        maxvert = self.winfo_screenheight()
        if self.idtip or not self.idtip_text:
            return
        x, y, cx, cy = self.widget.bbox('insert')        

        self.idtip = d_tip = Toplevel(self.widget)
        label = LabelStay(
            d_tip, 
            text=self.idtip_text, 
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
        d_tip = self.idtip
        self.idtip = None
        if d_tip:
            d_tip.destroy()

    def handle_enter(self, iD, name_type):
        if name_type is None:
            return
        
        if len(name_type) == 2:
            name_type = list(name_type)
            name_type[1] = "({})".format(name_type[1])
            name_type = " ".join(name_type)
        self.idtip_text = "ID #{}: {}".format(iD, name_type)

        if self.idtip_text:
            self.show_idtip(iD, name_type)

    def on_leave(self, evt):
        self.off()        

    def make_idtips(self):
        self.person_inputs = []

        for lst in self.parents_data:
            pa_name_type = None
            ma_name_type = None
            pa, ma = lst[1:]
            pa_id = pa["id"]
            if pa_id:
                pa_name_type = self.person_autofill_values[pa_id][0]["name type"]
            pa_widg = pa["inwidg"]
            ma_id = ma["id"]
            if ma_id:
                ma_name_type = self.person_autofill_values[ma_id][0]["name type"]
            ma_widg = ma["inwidg"]
            self.person_inputs.append((pa_widg, pa_id, pa_name_type))
            self.person_inputs.append((ma_widg, ma_id, ma_name_type))

        for k,v in self.progeny_data.items():
            name_type = None
            iD = k
            if iD:
                name_type = self.person_autofill_values[iD][0]["name type"]
            widg = v["inwidg"]
            self.person_inputs.append((widg, iD, name_type))
            children = v["children"]
            for dkt in children:
                kid_id = dkt["id"]
                if kid_id:
                    kid_name_type = self.person_autofill_values[kid_id][0]["name type"]
                kid_widg = dkt["name_widg"]
                self.person_inputs.append((kid_widg, kid_id, kid_name_type))
        for tup in self.person_inputs:
            widg, iD, name_type = tup
            
            name_in = widg.bind(
                "<Enter>", lambda evt, 
                iD=iD, name_type=name_type: self.handle_enter(iD, name_type))
            name_out = widg.bind("<Leave>", self.on_leave)
            self.widget = widg
            self.idtip_bindings["on_enter"].append([widg, name_in])
            self.idtip_bindings["on_leave"].append([widg, name_out])  

    def change_alt_parent_type(self, evt):
        """ Change alt parent kin type on double-click of label such as 
            "Guardian", "Foster Parent" etc.
        """
        def ok_change():
            current_file = get_current_file()[0]
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            new_kin_type = combo.entry.get()
            widg.config(text=new_kin_type.title())
            gridinfo = widg.grid_info()
            col = gridinfo["column"]
            row = gridinfo["row"]

            for tup in names_ids:
                if tup[0] == new_kin_type:
                    new_id = tup[1]
                    break
            finding_id = self.parents_data[1:][row - 1][0]["birth_id"]
            if col == 0:
                cur.execute(update_finding_kin_type_1, (new_id, finding_id))
            elif col == 2:
                cur.execute(update_finding_kin_type_2, (new_id, finding_id))                
            conn.commit()
            cancel_change()
            cur.close()
            conn.close()

        def cancel_change():
            frm.destroy()
            widg.config(width=orig_width)

        OK_ALT_PARENT_TYPES = {
            "adoptive": 
                [("Adoptive Parent", 110), ("Adoptive Father", 111), ("Adoptive Mother", 112)], 
            "Foster": 
                [("Foster Parent", 120), ("Foster Father", 121), ("Foster Mother", 122)], 
            "Guardian": 
                [("Guardian", 130), ("Legal Guardian", 131)]}

        widg = evt.widget
        orig_width = len(widg.cget("text"))
        original_text = widg.cget("text")
        for lst in OK_ALT_PARENT_TYPES.values():
            for tup in lst:
                if original_text == tup[0]:
                    alt_parent_types = [i[0] for i in lst]
                    names_ids = lst
                    break

        frm = FrameHilited(widg)
        combo = Combobox(frm, self.root, values=alt_parent_types)
        ok_butt = Button(frm, text="OK", command=ok_change, width=7)
        cancel_butt = Button(frm, text="CANCEL", command=cancel_change, width=7)
        frm.grid(column=0, row=0, sticky="ew")
        combo.grid(column=0, row=0) 
        ok_butt.grid(column=1, row=0)
        cancel_butt.grid(column=2, row=0)

