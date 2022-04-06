# families.py

import tkinter as tk
import sqlite3
from widgets import (
    Frame, LabelH3, Label, Button, Canvas, LabelEntry, Radiobutton, LabelFrame,
    FrameHilited, LabelHeader, Checkbutton)
from window_border import Dialogue
from custom_combobox_widget import Combobox
from files import get_current_file
from scrolling import Scrollbar
from persons import (
    open_new_person_dialog, make_all_names_dict_for_person_select, check_name,
    delete_person_from_tree, update_person_autofill_values, EntryAutoPerson, 
    EntryAutoPersonHilited)
from messages import InputMessage, open_message, families_msg
from dates import format_stored_date, get_date_formats, OK_MONTHS
from events_table import (
    get_current_person, delete_generic_finding, delete_couple_finding)
from query_strings import (
    select_finding_id_birth, delete_findings_persons, select_persons_persons,
    select_person_id_gender, select_finding_date, select_finding_id_birth,
    select_finding_id_death, select_finding_date_and_sorter,
    update_findings_persons_finding, insert_persons_persons_father,
    insert_findings_persons_new_father, select_findings_persons_birth,
    update_persons_persons_1, update_persons_persons_2, select_kin_type_string,
    update_persons_persons1_by_finding, update_persons_persons2_by_finding,
    select_kin_type_alt_parent, update_findings_persons_kin_type1,
    update_findings_persons_kin_type2, insert_persons_persons_mother,
    insert_findings_persons_new_mother, select_findings_persons_ppid,
    update_findings_persons_age2_blank, update_findings_persons_age1_blank,
    update_persons_persons_1_null_by_id, update_persons_persons_2_null_by_id,
    select_finding_details, delete_findings_persons_by_id, 
    delete_persons_persons, select_all_event_type_ids_marital
)
import dev_tools as dt
from dev_tools import looky, seeline




PARENT_TYPES = {
    1: "Mother", 2: "Father", 110: "Adoptive Parent", 111: "Adoptive Mother", 
    112: "Adoptive Father", 120: "Foster Parent", 121: "Foster Mother", 
    122: "Foster Father", 130: "Guardian", 131: "Legal Guardian"}

def get_all_marital_event_types(conn, cur):
    cur.execute(select_all_event_type_ids_marital)
    marital_event_types = [i[0] for i in cur.fetchall()]
    return marital_event_types

class NuclearFamiliesTable(Frame):
    """ In general, `...alt...` in this class refers to alternate parents and
        families such as relationships created by adoption, fosterage, and
        guardianship.

        `fpid` refers to findings_persons_id` in the database table 
        `findings_persons`, and `ppid` refers to persons_perons_id in the
        database table `persons_persons`.
    """
    def __init__(
            self, master, root, treebard, current_person, findings_table, 
            right_panel, formats, person_autofill_values=[], 
            *args, **kwargs):
        """ self.family_data[0] is for parents and alt parents of current person.
            self.family_data[0][0] is for biological parents.
            self.family_data[0][1] is for alt parents.
            self.family_data[0][x][0] is for data that's true for both parents.
            self.family_data[0][x][1] is for only the father or alt parent 1.
            self.family_data[0][x][2] is for only the mother or alt parent 2.
            self.family_data[1] is for partners & children of current person.
            self.family_data[1] has a partner's person ids as its keys.
            For its values see: 
                `progeny = { 
                    "sorter": [], "partner_name": "", "parent_type": "",
                    "partner_kin_type": "", "inwidg": None, "children": [],
                    "marital_events": []}
                self.family_data[1][pard_id] = progeny`
        """
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.root = root
        self.treebard = treebard
        self.current_person = current_person
        self.findings_table = findings_table
        self.right_panel = right_panel
        self.formats = formats
        self.person_autofill_values = person_autofill_values

        self.date_prefs = get_date_formats(tree_is_open=1)
        self.compound_parent_type = "Children's"
        self.unlink_partners = {"events": [], "children": []}
        self.link_partners = {"events": [], "children": []}

        # There's an exact copy of this blank collection in forget_cells() in events_table.py
        #   so it has to be changed if this is changed. Initial attempt to not repeat
        #   the code didn't work.
        self.family_data = [
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

        self.original = ""

        self.nukefam_containers = []

        self.cancel_unlink_partner_pressed = False
        self.cancel_link_partner_pressed = False

        self.newkidvar = tk.IntVar()

        self.current_person_name = ""

        self.make_widgets()

    def make_widgets(self):

        self.nukefam_canvas = Canvas(self)
        self.nukefam_window = Frame(self.nukefam_canvas)
        self.nukefam_canvas.create_window(0, 0, anchor="nw", window=self.nukefam_window)
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
        self.parentslab = LabelFrame(self.nukefam_window) 
        labelwidget = LabelH3(self.parentslab, text="Parents of the Current Person")
        self.pardlabs.append(labelwidget)
        self.parentslab.config(labelwidget=labelwidget)
        palab = Label(self.parentslab, text="Father", anchor="e")
        self.pa_input = EntryAutoPerson(
            self.parentslab, width=30, autofill=True, cursor="hand2", 
            values=self.person_autofill_values, name="pa")
        malab = Label(self.parentslab, text="Mother", anchor="e")
        self.ma_input = EntryAutoPerson(
            self.parentslab, width=30, autofill=True, cursor="hand2",
            values=self.person_autofill_values, name="ma")

        # children of self.nukefam_window
        self.parentslab.grid(column=0, row=0, sticky="w")

        # children of self.parentslab
        palab.grid(column=0, row=0, sticky="ew", padx=(12,12), pady=(6,12))
        self.pa_input.grid(column=1, row=0, pady=(6,12), padx=(0,0))
        malab.grid(column=2, row=0, sticky="ew", padx=(12,12), pady=(6,12))
        self.ma_input.grid(column=3, row=0, pady=(6,12), padx=(0,0))

        EntryAutoPerson.all_person_autofills.extend([self.ma_input, self.pa_input])
        for ent in (self.pa_input, self.ma_input):
            ent.bind("<FocusIn>", self.get_original, add="+")
            ent.bind("<Double-Button-1>", self.change_current_person) 

    def make_new_kin_inputs(self):
        """ Get self.new_kid_frame into the correct row by ungridding it in 
            self.findings_table.forget_cells() and regridding it in 
            self.make_nukefam_inputs().
        """
        self.new_kid_frame = Frame(self.nukefam_window)
        new_kid_input = EntryAutoPersonHilited(
            self.new_kid_frame, self.formats, width=48, 
            autofill=True, 
            values=self.person_autofill_values)
        childmaker = Button(
            self.new_kid_frame, 
            text="ADD CHILD TO SELECTED PARTNER", 
            command=self.add_child)
        new_kid_input.grid(column=0, row=0)
        childmaker.grid(column=1, row=0, padx=(6,0), pady=(12,0))        

        EntryAutoPerson.all_person_autofills.append(new_kid_input)

    def get_marital_event_types(self, conn, cur):

        marital_event_types = get_all_marital_event_types(conn, cur)
        qlen = len(marital_event_types)
        marital_event_types.insert(0, self.current_person)
        marital_event_types.insert(0, self.current_person)

        sql = '''
                SELECT findings_persons_id, person_id1, kin_type_id1,
                    person_id2, kin_type_id2, findings_persons.finding_id, 
                    date
                FROM findings_persons
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                JOIN finding
                    ON finding.finding_id = findings_persons.finding_id
                WHERE (person_id1 = ? OR person_id2 = ?) 
                    AND event_type_id in ({})
            '''.format(",".join(["?"] * qlen))

        cur.execute(sql, marital_event_types)
        marital_events_current_person = [list(i) for i in cur.fetchall()]
        return marital_events_current_person

    def make_nukefam_inputs(self, current_person=None, on_load=False):
        '''
            Run in main.py on_load=True and in events_table.redraw() 
            on_load=False.
        '''
        self.nukefam_inputs = []
        if current_person:
            self.current_person = current_person
        else:
            self.current_person = get_current_person()
        if on_load:
            self.make_nukefam_widgets_perm()
        self.make_nukefam_dicts()
        self.populate_nuke_tables()
        for widg in self.nukefam_inputs:
            widg.bind("<FocusIn>", self.get_original, add="+")
        if on_load:
            self.make_new_kin_inputs()
        self.new_kid_frame.grid(column=0, row=self.last_row, sticky="ew")
        for row in range(self.nukefam_window.grid_size()[1]):
            self.nukefam_window.rowconfigure(row, weight=1)
            
        self.update_idletasks()
        wd = self.nukefam_window.winfo_reqwidth()
        ht = self.right_panel.winfo_reqheight()
        self.nukefam_canvas.config(width=wd, height=ht)        
        self.nukefam_canvas.config(scrollregion=self.nukefam_canvas.bbox('all'))

        if len(self.family_data[1]) != 0:
            self.newkidvar.set(100)
        else:
            # set to non-existent value so no Radiobutton will be selected
            self.newkidvar.set(999)
        # self.fix_button_state()

    def populate_nuke_tables(self):
        lst = [            
            self.family_data[0][0][1]["name"],
            self.family_data[0][0][2]["name"]]
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
        for i, (k,v) in enumerate(self.family_data[1].items(), start=1):
            n = (i * 2) - 1
            pard_kin_type = ""
            name = v["partner_name"]
            if len(v["partner_kin_type"]) != 0:
                pard_kin_type = "{}:".format(v["partner_kin_type"].title()) 
            pard_id = k
            pard = "pard_{}_{}".format(pard_id, n)
            pardframe = Frame(self.nukefam_window)
            pardframe.grid(column=0, row=n, sticky="ew")
            self.nukefam_containers.append(pardframe)
            pardrad = Radiobutton(
                pardframe, variable=self.newkidvar, 
                value=n, anchor="w")
                # value=n, anchor="w", command=self.fix_button_state)
            self.pardrads.append(pardrad)
            pardrad.grid(column=0, row=n)

            if len(v["children"]) != 0 and len(v["partner_kin_type"]) == 0:
                ma_pa = "{}:".format(v["parent_type"])
                pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            elif len(v["children"]) != 0 and len(v["partner_kin_type"]) != 0:
                ma_pa = "{} ({}):".format(v["partner_kin_type"], v["parent_type"])
                pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            else:
                pardlab = LabelH3(
                    pardframe, text=pard_kin_type, anchor="w")

            self.pardlabs.append(pardlab)
            pardlab.grid(column=1, row=n)
            pardent = EntryAutoPerson(
                pardframe, width=48, autofill=True, cursor="hand2", 
                values=self.person_autofill_values, name=pard)
            pardent.insert(0, name)
            pardent.grid(column=2, row=n)
            EntryAutoPerson.all_person_autofills.append(pardent)
            pardent.bind("<Double-Button-1>", self.change_current_person)

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
                    dkt["name_widg"] = ent
                    EntryAutoPerson.all_person_autofills.append(ent)
                    ent.bind("<Double-Button-1>", self.change_current_person)
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

    def make_parents_dict(self, ma_id=None, pa_id=None):
        '''
            Treebard assumes that if someone exists, then they were born 
            exactly once, had one mother and one father, and we can base 
            application design decisions on these assumptions. I am finding it 
            unsymmetrical and odd to have some persons in the tree not have a 
            birth event while others do. I'm going to try auto-creating a birth 
            event for every person as the user creates the person. It will make
            updates to the parents section at the top of the nukefams table easy
            and symmetrical since there will be no special case to deal with--
            the person who exists but hasn't been born. This will also 
            save the user time; they won't have to create a birth event for 
            anyone. Then when the user inputs an alternate parent event 
            (guardianship, fosterage, adoption), the same process will create
            inputs for the alternate parents. All symmetrical procedures except
            that the person's birth is assumed so inputs are automatically
            created for biological parents.
        '''

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute(select_finding_id_birth, (self.current_person,))
        birth_id = cur.fetchone()[0]
        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, 
                    person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE finding_id = ?
            ''',
            (birth_id,))
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
            dad = self.parent_record[2:4]
            mom = self.parent_record[4:]
            pa_id = dad[0]
            ma_id = mom[0]
            ids = self.family_data[0][0][0]
            ids["fpid"], ids["finding"] = self.parent_record[0:2]
        else:
            # This only runs when there are no parents recorded.
            self.family_data[0][0][0]["finding"] = birth_id

        for person in self.person_autofill_values:
            if person == pa_id:
                pa_name = self.person_autofill_values[pa_id][0]["name"]

        for person in self.person_autofill_values:
            if person == ma_id:
                ma_name = self.person_autofill_values[ma_id][0]["name"]
        
        parents = self.family_data[0][0]
        parents[1]["id"] = pa_id
        parents[2]["id"] = ma_id
        parents[1]["name"] = pa_name
        parents[2]["name"] = ma_name
        parents[1]["inwidg"] = self.pa_input
        parents[2]["inwidg"] = self.ma_input
        self.get_alt_parents(cur)
        self.grid_alt_parents()

        cur.close()
        conn.close()

    def get_alt_parents(self, cur):
        """ Get adoptive parents, foster parents & guardians. """
        cur.execute(
        '''
            SELECT finding_id, date_sorter, event_type_id 
            FROM finding 
            WHERE person_id = ? 
                AND event_type_id in (48, 83, 95)
        ''',
        (self.current_person,))
        alt_parent_events = cur.fetchall()
        if alt_parent_events is None:
            return
        # Get data about alt parent events and sort events by date.
        r = 0
        for event in alt_parent_events:
            event = list(event)
            event[1] = [int(i) for i in event[1].split(",")]
            alt_parent_events[r] = event
            r += 1
        alt_parent_events = sorted(alt_parent_events, key=lambda i: i[1])

        self.make_alt_parents_dict(alt_parent_events, cur)
        alt_parent_details = self.family_data[0][1:]
        j = 0
        for lst in alt_parent_details:
            lab_l = Label(self.parentslab, anchor="e")
            ent_l = EntryAutoPerson(
                self.parentslab, width=30, autofill=True, cursor="hand2", 
                values=self.person_autofill_values,
                name="altparent_l{}".format(str(j)))
            if lst[1]["kin_type"]:
                ent_l.insert(0, lst[1]["name"])
            lst[1]["inwidg"] = ent_l
            lst[1]["labwidg"] = lab_l
            if lst[1]["kin_type"]:
                lab_l.config(text=lst[1]["kin_type"].title())

            lab_r = Label(self.parentslab, anchor="e")
            ent_r = EntryAutoPerson(
                self.parentslab, width=30, autofill=True, cursor="hand2", 
                values=self.person_autofill_values,
                name="altparent_r{}".format(str(j)))
            if lst[2]["kin_type"]:
                ent_r.insert(0, lst[2]["name"]) 
            lst[2]["inwidg"] = ent_r
            lst[2]["labwidg"] = lab_r
            if lst[2]["kin_type"]:
                lab_r.config(text=lst[2]["kin_type"].title())

            EntryAutoPerson.all_person_autofills.extend([ent_l, ent_r])
            for ent in (ent_l, ent_r):
                ent.bind("<FocusIn>", self.get_original, add="+")
                ent.bind("<Double-Button-1>", self.change_current_person) 
                self.nukefam_containers.append(ent)
            for lab in (lab_l, lab_r):
                lab.bind("<Double-Button-1>", self.change_kin_type)

            self.nukefam_containers.extend([lab_l, lab_r])           
            j += 1

    def make_alt_parents_dict(self, alt_parent_events, cur):
     
        for finding in alt_parent_events:
            parent_couple = [ 
                {'fpid': None, 'ppid': None, 'finding': finding[0], 
                    'sorter': finding[1]}, 
                {'id': None, 'name': '', 'kin_type_id': None, 'kin_type': '', 
                    'labwidg': None, 'inwidg': None}, 
                {'id': None, 'name': '', 'kin_type_id': None, 'kin_type': '', 
                    'labwidg': None, 'inwidg': None}]
            ids, alt_parent1, alt_parent2 = parent_couple
            cur.execute(
            '''
                SELECT persons_persons_id, kin_type_id1, kin_type_id2, findings_persons_id
                FROM findings_persons
                WHERE finding_id = ?
            ''',
            (ids["finding"],))
            ids["ppid"], alt_parent1["kin_type_id"], alt_parent2["kin_type_id"], ids["fpid"] = cur.fetchone()
            h = 1
            for kintype in (alt_parent1["kin_type_id"], alt_parent2["kin_type_id"]):
                cur.execute(select_kin_type_string, (kintype,))
                parent_couple[h]["kin_type"] = cur.fetchone()[0]
                h += 1
            self.family_data[0].append(parent_couple)
        alt_parents = self.family_data[0][1:] 
        for lst in alt_parents:
            ppid = lst[0]["ppid"]
            cur.execute(
            '''
                SELECT person_id1, person_id2
                FROM persons_persons
                WHERE persons_persons_id = ?
            ''',
            (ppid,))
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

    def grid_alt_parents(self):
        """ Grid widgets as children of self.parentslab. """
        alt_parents = self.family_data[0][1:]
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

    def make_nukefam_dicts(self):
        
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.make_parents_dict()

        partners1, births = self.query_nukefams_data(conn, cur)
        alt_parentage_events = self.query_alt_nukefams_data(conn, cur)
        self.arrange_partners_progenies(partners1, births, alt_parentage_events, conn, cur)

        main_sorter = [0, 0, 0]
        for k,v in self.family_data[1].items():
            kids = v["children"]
            kids = sorted(kids, key=lambda i: i["sorter"])
            v["children"] = kids
            if len(v["children"]) != 0:
                main_sorter = v["children"][0]["sorter"]
            if len(v.get("sorter")) == 0:
                v["sorter"] = main_sorter
        self.family_data[1] = dict(
            sorted(
                self.family_data[1].items(), key=lambda i: i[1]["sorter"]))
        cur.close()
        conn.close()

    def arrange_partners_progenies(
            self, partners1, births, alt_parentage_events, conn, cur):
        """ Updating person_autofill_values is necessary since 
            `events_table.redraw()` destroys partner and child frames
            and alt parent inputs.
        """
        self.person_autofill_values = update_person_autofill_values()
        births = births + alt_parentage_events
        progenies = {}
        all_partners = [] 
        event_pards = []
        offspring_pards = []
        if partners1:
            partners = [tup for tup in partners1 if self.current_person in tup]
            for tup in partners:
                for num in tup:
                    if num != self.current_person:
                        event_pards.append(num)
                        all_partners.append(num)
            event_pards = list(set(event_pards))
        for tup in births:
            if tup[2] != self.current_person:
                pard_id = tup[2]              
            elif tup[4] != self.current_person:
                pard_id = tup[4]
            offspring_pards.append(pard_id)
            all_partners.append(pard_id)
            all_partners = list(set(all_partners))

        for pard_id in all_partners:
            if pard_id in offspring_pards and pard_id in event_pards:
                nested = {'offspring': True, 'events': True}
            elif pard_id in offspring_pards and pard_id not in event_pards:
                nested = {'offspring': True, 'events': False}
            elif pard_id not in offspring_pards and pard_id in event_pards:
                nested = {'offspring': False, 'events': True}
            progenies[pard_id] = nested
        for pard_id in progenies:
            progeny = {
                "sorter": [], "partner_name": "", "parent_type": "",
                "partner_kin_type": "", "inwidg": None, "children": [],
                "marital_events": []}
            self.family_data[1][pard_id] = progeny

        self.collect_couple_events(cur, conn)
        for k,v in progenies.items():
            pardner = k
            if v["offspring"] is True:
                for tup in births:
                    order = "{}-{}".format(str(tup[3]), str(tup[5]))                
                    if tup[4] == pardner:                        
                        parent_type = tup[5]
                        pard_id = tup[4]
                        self.make_pard_dict(pard_id, parent_type, cur)
                        if pard_id == pardner:
                            self.family_data[1][pardner]["children"].append(
                                {"fpid": tup[0], 
                                    "birth_id": tup[1], "order": order})
                    elif tup[2] == pardner:
                        parent_type = tup[3]
                        pard_id = tup[2]
                        self.make_pard_dict(pard_id, parent_type, cur) 
                        if pard_id == pardner:
                            self.family_data[1][pardner]["children"].append(
                                {"fpid": tup[0], 
                                    "birth_id": tup[1], "order": order})      

            if v["events"] is True and v["offspring"] is False:
                self.make_pard_dict(pardner, "", cur)
        for pard_id in progenies:
            for k,v in self.family_data[1].items():
                if k == pard_id:
                    for dkt in v["children"]:
                        self.finish_progeny_dict(dkt, cur)

    def query_nukefams_data(self, conn, cur):

        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, 
                    person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id1 = ? AND kin_type_id1 IN (1, 2)
            ''',
            (self.current_person,))
        result1 = cur.fetchall()
        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, 
                    person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id2 = ? AND kin_type_id2 IN (1, 2)
            ''',
            (self.current_person,))
        result2 = cur.fetchall()
        births = []
        births = [tup for q in (result1, result2) for tup in q]

        marital_event_types = get_all_marital_event_types(conn, cur)
        qlen = len(marital_event_types)
        sql = '''
                SELECT person_id1, person_id2
                FROM findings_persons
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                JOIN finding
                    ON finding.finding_id = findings_persons.finding_id
                WHERE event_type_id in ({})                    
            '''.format(",".join("?" * qlen))
        cur.execute(sql, marital_event_types)
        partners1 = cur.fetchall()

        return partners1, births

    def query_alt_nukefams_data(self, conn, cur):

        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, 
                    person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id1 = ? AND kin_type_id1 IN (110, 111, 112, 120, 121, 122, 130, 131)
            ''',
            (self.current_person,))
        result1 = cur.fetchall()
        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, 
                    person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id2 = ? AND kin_type_id2 IN (110, 111, 112, 120, 121, 122, 130, 131)
            ''',
            (self.current_person,))
        result2 = cur.fetchall()
        alt_births = []
        alt_births = [tup for q in (result1, result2) for tup in q]
        alt_births = [list(i) for i in alt_births]
        for lst in alt_births:
            cur.execute(
                '''
                SELECT finding_id
                FROM finding
                WHERE person_id = (SELECT person_id FROM finding WHERE finding_id = ?)
                    AND event_type_id = 1
                ''',
                (lst[1],))
            birth_evt_id = cur.fetchone()[0]
            lst[1] = birth_evt_id

        return alt_births

    def make_pard_dict(self, pard_id, parent_type, cur):
        
        for k,v in PARENT_TYPES.items():
            if k == parent_type:
                parent_type = v
                break
        if self.compound_parent_type.lstrip("Children's ") != parent_type:
            self.compound_parent_type = "{} or {}".format(self.compound_parent_type, parent_type)
        if self.compound_parent_type.startswith("Children's or"):
            self.compound_parent_type = self.compound_parent_type.replace("Children's or", "Children's")
        if pard_id is None:
            partner_name = ""
        else:
            partner_name = self.person_autofill_values[pard_id][0]["name"]
            
        self.family_data[1][pard_id]["parent_type"] = self.compound_parent_type
        self.family_data[1][pard_id]["partner_name"] = partner_name 
        self.compound_parent_type = "Children's"

    def collect_couple_events(self, cur, conn):
        marital_events = self.get_marital_event_types(conn, cur) 
        for lst in marital_events:
            if lst[1] == self.current_person:
                del lst[1:3]
            elif lst[3] == self.current_person:
                del lst[3:5]            

        self.sorters = []
        for lst in marital_events:
            self.save_marital_events(lst, cur)

        self.sorters = sorted(self.sorters, key=lambda i: i[1])
        for k,v in self.family_data[1].items():
            for sorter in self.sorters:
                if sorter[0] == k:
                    v["sorter"] = sorter[1]

    def save_marital_events(self, lst, cur):
        partner_id = lst[1]
        for k,v in self.family_data[1].items():
            if partner_id == k:
                cur.execute(
                    '''
                        SELECT kin_types
                        FROM kin_type
                        WHERE kin_type_id = ?
                    ''',
                    (lst[2],))
                kin_type = cur.fetchone()[0]
                sorter = self.make_sorter(lst[4])
                self.sorters.append((k, sorter))
                if kin_type in ("generic_partner1", "generic_partner2"):
                    kin_type = "Partner"
                v["partner_kin_type"] = kin_type
                v["marital_events"].append(
                    {"fpid": lst[0], "finding": lst[3]})

    def finish_progeny_dict(self, dkt, cur):
        cur.execute(
            '''
                SELECT person_id, date
                FROM finding
                WHERE finding_id = ?
                    AND event_type_id = 1                    
            ''',
            (dkt["birth_id"],)) 
        result = cur.fetchone()
        if result is None:
            return self.finish_alt_progeny_dict(dkt, cur)
        else:
            born_id, birth_date = result
        cur.execute(
            '''
                SELECT date
                FROM finding
                WHERE person_id = ?
                    AND event_type_id = 4
            ''',
            (born_id,))
        death_date = cur.fetchone()
        if death_date:
            death_date = death_date[0]
        else:
            death_date = "-0000-00-00-------"

        cur.execute(
            '''
                SELECT gender
                FROM person
                WHERE person_id = ?
            ''',
            (born_id,))
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

    def finish_alt_progeny_dict(self, dkt, cur):
        cur.execute(
            '''
                SELECT person_id, date
                FROM finding
                WHERE finding_id = ?
                AND event_type_id in (48, 83, 95)                   
            ''',
            (dkt["birth_id"],)) 

        born_id, birth_date = cur.fetchone()
        cur.execute(
            '''
                SELECT date
                FROM finding
                WHERE person_id = ?
                    AND event_type_id = 4
            ''',
            (born_id,))
        death_date = cur.fetchone()
        if death_date:
            death_date = death_date[0]
        else:
            death_date = "-0000-00-00-------"

        cur.execute(
            '''
                SELECT gender
                FROM person
                WHERE person_id = ?
            ''',
            (born_id,))
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

    def add_child(self):
        print("hey kid")

    def get_original(self, evt):
        """ The binding to FocusOut can't be done till a FocusIn event has
            taken place because for some reason a FocusOut event was being
            triggered when making a new event. This caused a mismatch between
            self.original and self.final on one of the partner inputs, which 
            opened the PersonAdd dialog when it wasn't wanted. This seems to 
            have solved the problem but the cause of the problem was not found. 
        """
        evt.widget.bind("<FocusOut>", self.get_final, add="+")
        self.original = evt.widget.get()
    def change_current_person(self, evt):
        widg = evt.widget
        widgname = widg.winfo_name()
        if len(widg.get()) == 0:
            return
        if widgname in ("pa", "ma"):
            col = widg.grid_info()["column"]
            if col == 1:
                print("line", looky(seeline()).lineno, "update_parent(pa):")
            elif col == 3:
                print("line", looky(seeline()).lineno, "update_parent(ma):")
        elif widgname.startswith("altparent"):
            update_parent(alt_parent)
        elif widgname.startswith("pard"):
            print("line", looky(seeline()).lineno, "update_partner:")
        else:
            for k,v in self.family_data[1].items():
                if v["inwidg"] == widg:
                    break
            col = widg.grid_info()["column"]
            if col == 1:
                print("line", looky(seeline()).lineno, "update_child_name:")
            elif col == 2:
                print("line", looky(seeline()).lineno, "update_child_gender:")
            elif col == 3:
                print("line", looky(seeline()).lineno, "update_child_birth:")
            elif col == 4:
                print("line", looky(seeline()).lineno, "update_child_death:")
    def make_parent(self, inwidg, conn, cur, got):
        """ Add a parent from an input on the nukefams table. """

        def err_done1(entry, msg):
            entry.delete(0, 'end')
            msg[0].grab_release()
            msg[0].destroy()
            entry.focus_set()

        name_data = check_name(ent=inwidg)
        if not name_data:
            msg1 = open_message(
                self, 
                families_msg[1], 
                "Person Name Unknown", 
                "OK")
            msg1[0].grab_set()
            msg1[2].config(command=lambda entry=inwidg, msg=msg1: err_done1(
                entry, msg))
            return

        if name_data == "add_new_person":
            new_parent_id = open_new_person_dialog(
                self, inwidg, self.root, self.treebard, self.formats, 
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
        else:
            new_parent_id = name_data[1]

        if inwidg.winfo_name() == "pa":
            parent_type = 2
        elif inwidg.winfo_name() == "ma":
            parent_type = 1
        birth_id = self.family_data[0][0][0]["finding"]
        cur.execute(select_findings_persons_birth, (birth_id,))
        fpid = cur.fetchone()
        if fpid:
            fpid, ppid = fpid
            if parent_type == 2:
                cur.execute(update_persons_persons_1, (new_parent_id, ppid))
                conn.commit()
                cur.execute(update_findings_persons_kin_type1, (2, fpid,))
                conn.commit()    
            elif parent_type == 1:
                cur.execute(update_persons_persons_2, (new_parent_id, ppid))
                conn.commit()
                cur.execute(update_findings_persons_kin_type2, (1, fpid,))
                conn.commit()
        else:
            # if there's no row yet for persons_persons, make one
            if parent_type == 2:
                cur.execute(insert_persons_persons_father, (new_parent_id,))
                conn.commit()
                cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "persons_persons"')
                ppid = cur.fetchone()[0]
                cur.execute(insert_findings_persons_new_father, (birth_id, ppid))
                conn.commit()

            elif parent_type == 1:
                cur.execute(insert_persons_persons_mother, (new_parent_id,))
                conn.commit()
                cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "persons_persons"')
                ppid = cur.fetchone()[0]
                cur.execute(insert_findings_persons_new_mother, (birth_id, ppid))
                conn.commit()

    def update_partner(self, final, conn, cur, inwidg):

        def get_new_partner_id(inwidg):
            name_data = check_name(ent=inwidg)

            if name_data == "add_new_person":
                new_partner_id = open_new_person_dialog(
                    self, inwidg, self.root, self.treebard, self.formats, 
                    person_autofill_values=self.person_autofill_values)
                self.person_autofill_values = update_person_autofill_values()
            elif not name_data:
                new_partner_id = None # added to stop an error
                # Keep unlink dlg from opening when replacing 
                #   existing partner with new person:
                if len(new_string) == 0:
                    self.unlink_partners_dialog(cur, conn, inwidg)
                else:
                    msg5 = open_message(
                        self, 
                        families_msg[1], 
                        "Person Name Unknown", 
                        "OK")
                    msg5[0].grab_set()
                    return
            else:
                new_partner_id = name_data[1]

            return new_partner_id

        new_string = inwidg.get()
        orig = self.original
        self.new_partner_id = get_new_partner_id(inwidg)
        if self.new_partner_id is None:
            inwidg.delete(0, 'end')
            inwidg.insert(0, orig)
            return
        else:
            for k,v in self.family_data[1].items():
                if inwidg != v["inwidg"]:
                    continue
                elif inwidg == v["inwidg"]:
                    if k is None and (k != self.new_partner_id or
                            len(v["partner_name"]) == 0):
                        self.link_partners_dialog(cur, conn, inwidg)
                    else:
                        for event in v["marital_events"]:                            
                            cur.execute(select_findings_persons_ppid, (event["fpid"],))
                            ppid = cur.fetchone()[0]
                            cur.execute(select_persons_persons, (ppid,))
                            both = cur.fetchone()
                            if self.current_person == both[0]:
                                cur.execute(update_persons_persons_2, (self.new_partner_id, ppid,))
                            elif self.current_person == both[1]:
                                cur.execute(update_persons_persons_1, (self.new_partner_id, ppid,))
                            conn.commit()
                else: 
                    print("line", looky(seeline()).lineno, "case not handled:")

    def link_partners_dialog(self, cur, conn, inwidg):
        def ok_link_partner(checks):
            copy = checks
            i = 0
            for dkt in copy["events"]:
                checks["events"][i]["vars"] = dkt["vars"].get()
                i += 1            
            self.link_partners["events"] = checks["events"]

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
            """ Run after dialog closes. """
            def update_partners_child(birth_fpid, order, parent_type):
                cur.execute(select_findings_persons_ppid, (birth_fpid,))
                ppid = cur.fetchone()[0]
                if parent_type == "Children's Father":
                    if order == "1-2":   
                        cur.execute(update_findings_persons_age2_blank, (birth_fpid,))
                        conn.commit()
                        cur.execute(update_persons_persons_2, (self.new_partner_id, ppid))
                        conn.commit()
                    elif order == "2-1":      
                        cur.execute(update_findings_persons_age1_blank, (birth_fpid,))
                        conn.commit()
                        cur.execute(update_persons_persons_1, (self.new_partner_id, ppid))
                        conn.commit()                    
                elif parent_type == "Children's Mother":
                    if order == "1-2":
                        cur.execute(update_findings_persons_age1_blank, (birth_fpid,))
                        conn.commit()
                        cur.execute(update_persons_persons_1, (self.new_partner_id, ppid))
                        conn.commit()
                    elif order == "2-1":   
                        cur.execute(update_findings_persons_age2_blank, (birth_fpid,))
                        conn.commit()
                        cur.execute(update_persons_persons_2, (self.new_partner_id, ppid))
                        conn.commit()

            if self.cancel_link_partner_pressed is True:
                return

            for dkt in self.link_partners["events"]:
                if dkt["vars"] == 0:
                    continue
                elif dkt["vars"] == 1:
                    link_partner(dkt["fpid"])
            for dkt in self.link_partners["children"]:
                if dkt["vars"] == 0:
                    continue
                elif dkt["vars"] == 1:
                    link_offspring(dkt["fpid"])

        def link_partner(fpid):
            cur.execute(select_findings_persons_ppid, (fpid,))
            ppid = cur.fetchone()[0]
            cur.execute(select_persons_persons, (ppid,))
            person_id1, person_id2 = cur.fetchone()
            currper = self.current_person
            if currper == person_id1:
                cur.execute(update_persons_persons_2, (self.new_partner_id, ppid))
            elif currper == person_id2:
                cur.execute(update_persons_persons_1, (self.new_partner_id, ppid))
            conn.commit()

        def link_offspring(fpid):
            cur.execute(select_findings_persons_ppid, (fpid,))
            ppid = cur.fetchone()[0]
            cur.execute(select_persons_persons, (ppid,))
            person_id1, person_id2 = cur.fetchone()
            currper = self.current_person
            if currper == person_id1:
                cur.execute(update_persons_persons_2, (self.new_partner_id, ppid))
            elif currper == person_id2:
                cur.execute(update_persons_persons_1, (self.new_partner_id, ppid))
            conn.commit()

        partner_id = None
        checks = {"events": [], "children": []}
        for k,v in self.family_data[1].items():
            if v["inwidg"] == inwidg:
                partner_id = k
                break

        for event in self.family_data[1][partner_id]["marital_events"]:
            checks["events"].append(event)
        for child in self.family_data[1][partner_id]["children"]:
            checks["children"].append(child)

        new_string = inwidg.get()
        message = "Select which events & children to link to\n{}:".format(new_string)
        self.null_partner_replacer = Dialogue(self.root)
        
        head = LabelHeader(
            self.null_partner_replacer.window, text=message, justify='left', wraplength=650)
        inputs = Frame(self.null_partner_replacer.window)

        s = 1
        for event in checks["events"]: 
            cur.execute(select_finding_details, (event["finding"],))
            event_id, event_date, event_type = cur.fetchone()
            event_date = format_stored_date(
                event_date, date_prefs=self.date_prefs)
            text = "{} {} (Conclusion #{})".format(
                event_date, event_type, event_id)
            var = tk.IntVar()
            chk = Checkbutton(inputs, variable=var)
            chk.grid(column=0, row=s)
            event["vars"] = var
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
            command=lambda checks=checks: ok_link_partner(
                checks))
        b2 = Button(
            buttons, text="CANCEL", command=cancel_link_partner) 

        self.null_partner_replacer.canvas.title_1.config(
            text="Select Children & Marital Events to Link to Added Partner")
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
            for dkt in copy["events"]:
                h = 0
                for var in dkt["vars"]:
                    got = var.get()
                    checks["events"][i]["vars"][h] = got
                    h += 1
                i += 1            
            self.unlink_partners["events"] = checks["events"]

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
            for dkt in self.unlink_partners["events"]:
                if dkt["vars"] == [0, 0]:
                    continue
                elif dkt["vars"] == [1, 1]:
                    delete_couple_finding(dkt["finding"], fpid=dkt["fpid"])
                elif dkt["vars"] == [0, 1]:
                    unlink_partner(dkt["fpid"], [0, 1])
                elif dkt["vars"] == [1, 0]:
                    unlink_partner(dkt["fpid"], [1, 0])
            for dkt in self.unlink_partners["children"]:
                if dkt["vars"] == [0, 0]:
                    continue
                elif dkt["vars"] == [1, 1]:
                    delete_offspring(conn, cur, fpid=dkt["fpid"])
                elif dkt["vars"] == [0, 1]:
                    unlink_offspring(dkt["fpid"], [0, 1])
                elif dkt["vars"] == [1, 0]:
                    unlink_offspring(dkt["fpid"], [1, 0])

        def delete_offspring(conn, cur, fpid):
            cur.execute(select_findings_persons_ppid, (fpid,))
            ppid = cur.fetchone()[0]
            cur.execute(delete_findings_persons_by_id, (fpid,))
            conn.commit()
            cur.execute(delete_persons_persons, (ppid,))
            conn.commit()

        def unlink_partner(fpid, order):
            cur.execute(select_findings_persons_ppid, (fpid,))
            ppid = cur.fetchone()[0]
            cur.execute(select_persons_persons, (ppid,))
            person_id1, person_id2 = cur.fetchone()
            currper = self.current_person
            if currper == person_id1:
                if order == [0, 1]:
                    cur.execute(update_persons_persons_2_null_by_id, (ppid,))
                elif order == [1, 0]:
                    cur.execute(update_persons_persons_1_null_by_id, (ppid,))                
            elif currper == person_id2:
                if order == [0, 1]:
                    cur.execute(update_persons_persons_1_null_by_id, (ppid,))
                elif order == [1, 0]:
                    cur.execute(update_persons_persons_2_null_by_id, (ppid,))
            conn.commit()

        def unlink_offspring(fpid, order):
            cur.execute(select_findings_persons_ppid, (fpid,))
            ppid = cur.fetchone()[0]
            cur.execute(select_persons_persons, (ppid,))
            person_id1, person_id2 = cur.fetchone()
            currper = self.current_person
            if currper == person_id1:
                if order == [0, 1]:
                    cur.execute(update_persons_persons_2_null_by_id, (ppid,))
                elif order == [1, 0]:
                    cur.execute(update_persons_persons_1_null_by_id, (ppid,))                
            elif currper == person_id2:
                if order == [0, 1]:
                    cur.execute(update_persons_persons_1_null_by_id, (ppid,))
                elif order == [1, 0]:
                    cur.execute(update_persons_persons_2_null_by_id, (ppid,))
            conn.commit()

        partner_id = None
        checks = {"events": [], "children": []}
        for k,v in self.family_data[1].items():
            if v["inwidg"] == widg:
                partner_id = k
                break

        for event in self.family_data[1][partner_id]["marital_events"]:
            checks["events"].append(event)
        for child in self.family_data[1][partner_id]["children"]:
            checks["children"].append(child)
            
        message = "Select which events/children to unlink from whom:"
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
        for event in checks["events"]: 
            cur.execute(select_finding_details, (event["finding"],))
            event_id, event_date, event_type = cur.fetchone()
            event_date = format_stored_date(event_date, date_prefs=self.date_prefs)
            text = "{} {} (Conclusion #{}):".format(event_date, event_type, event_id)
            evtlab = Label(inputs, text=text, anchor="e")
            evtlab.grid(column=0, row=f, sticky="e")
            var0 = tk.IntVar()
            var1 = tk.IntVar()
            chk0 = Checkbutton(inputs, variable=var0)
            chk0.grid(column=1, row=f)
            chk1 = Checkbutton(inputs, variable=var1)
            event["vars"] = [var0, var1]
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
            text="Unlink Partner from Current Person's Marital Events")
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

    def update_child_name(self, widg, conn, cur):

        def update_child(widg, parent_id, child, cur, conn):
            orig_child_id = child["id"]
            child_id = None 
            birth_id = None
            gender = "unknown"
            fpid = child["fpid"]
            orig_child = child["id"] # need this & widg in case user presses CANCEL etc.
            death_date = "-0000-00-00-------"
            birth_date = "-0000-00-00-------"
            sorter = (0,0,0)
            if "  #" in self.final:
                child_id = self.final.split("  #")[1]
                cur.execute(select_finding_id_birth, (child_id,))
                birth_id = cur.fetchone()[0]
                cur.execute(select_person_id_gender, (child_id,))
                gender = cur.fetchone()[0]
                cur.execute(select_finding_id_death, (child_id,))
                death_id = cur.fetchone()
                cur.execute(select_finding_date_and_sorter, (birth_id,))
                birth_date, sorter = cur.fetchone()
                sorter = self.make_sorter(birth_date)
                if death_id:
                    death_id = death_id[0]
                    cur.execute(select_finding_date, (death_id,))
                    death_date = cur.fetchone()[0] 
            elif len(self.final) == 0:
                # user unlinks child from both parents 
                #   by deleting existing name in entry; what about unlinking
                #   child only from current person? Try it this way first
                #   since the nukefams tables does allow changes to partners
                #   and children of the current person.
                cur.execute(select_finding_id_birth, (orig_child_id,))
                birth_id = cur.fetchone()[0]
                cur.execute(delete_findings_persons, (birth_id,))
                conn.commit()
                # HAVE TO BLANK OUT GENDER, BIRTH, DEATH TOO
            else:
                child_id = open_new_person_dialog(
                    self, widg, self.root, self.treebard, self.formats,
                    self.person_autofill_values)
                cur.execute(select_finding_id_birth, (child_id,))
                birth_id = cur.fetchone()[0] # CANCEL THROWS ERROR HERE
                cur.execute(select_person_id_gender, (child_id,))
                gender = cur.fetchone()[0]

            child["id"] = child_id
            child["name"] = self.final
            child["gender"] = gender
            child["birth"] = birth_date
            child["sorter"] = sorter
            child["death"] = death_date  

            if birth_id:
                cur.execute(update_findings_persons_finding, (birth_id, fpid))
                conn.commit()

        for k,v in self.family_data[1].items():
            for child in v["children"]:
                if widg != child["name_widg"]:
                    continue
                else:
                    parent_id = k
                    update_child(widg, parent_id, child, cur, conn)

    def update_child_gender(self):
        print("line", looky(seeline()).lineno, "self.family_data[1]:", self.family_data[1])

    def update_child_birth(self):
        print("line", looky(seeline()).lineno, "self.family_data[1]:", self.family_data[1])

    def update_child_death(self):
        print("line", looky(seeline()).lineno, "self.family_data[1]:", self.family_data[1])

    def update_parent(self, final, conn, cur, widg, kin_type=None):
        """ If the field is not blank, simulate a disabled field for any input that tries to
            change the contents to a different person (to change a parent, partner, or child,
            make that person the current person first? UPDATE THIS DOCSTRING)
        """
        def delete_parent(column):
            finding_id = self.family_data[0][0][0]["finding"]
            if column == 1:
                cur.execute(update_persons_persons1_by_finding, (None, finding_id))
            elif column == 3:
                cur.execute(update_persons_persons2_by_finding, (None, finding_id))
            conn.commit()
            widg.focus_set()

        def err_done2(entry, msg):
            """ It was thought necessary, with existing procedures, to delete a
                parent first, tab out, focus back in, and input a new parent. 
                All that, including this error message, was eliminated by
                programatically returning focus to the empty field after the
                parent is deleted. See `widg.focus_set()` at bottom of 
                `delete_parent`. Keeping this for now but shouldn't need it.
            """
            msg[0].grab_release()
            msg[0].destroy()
            entry.focus_set()

        for dkt in self.family_data[0][0][1:]:
            if widg == dkt["inwidg"]:
                iD = dkt["id"]
                name = dkt["name"]
                break

        ok_content = (name, "", "#{}".format(iD))
        if len(self.original) != 0 and self.final not in ok_content:
            widg.delete(0, "end")
            widg.insert(0, self.original)

            msg2 = open_message(
                self, 
                families_msg[2], 
                "Change Parent Workaround", 
                "OK")
            msg2[0].grab_set()
            msg2[2].config(command=lambda entry=widg, msg=msg2: err_done2(
                entry, msg))
            return

        elif len(self.final) == 0:
            column = widg.grid_info()["column"]
            delete_parent(column)
        elif len(self.original) == 0:
            self.make_parent(widg, conn, cur, self.final)

    def update_altparent(self, final, conn, cur, widg, column, kin_type=None):

        def err_done4(entry, msg):
            """ See docstring in err_done2. The good fluke mentioned there
                doesn't work here for alt parent. This msg still needed till I
                figure out how to set focus correctly after making a change in
                an alt parent field then tabbing out.
            """
            msg4[0].grab_release()
            msg4[0].destroy()
            entry.focus_set()

        def err_done3(entry, msg):
            entry.delete(0, 'end')
            msg[0].grab_release()
            msg[0].destroy()
            entry.focus_set()

        def delete_parent(column):
            if column == 1:
                cur.execute(update_persons_persons1_by_finding, (None, finding_id))
            elif column == 3:
                cur.execute(update_persons_persons2_by_finding, (None, finding_id))
            conn.commit()
            widg.focus_set()

        y = 1
        for lst in self.family_data[0][1:]:
            for dkt in lst[1:]:
                if widg == dkt["inwidg"]:
                    finding_id = lst[0]["finding"]
                    iD = dkt["id"]
                    name = dkt["name"]
                    break
            y += 1 

        ok_content = (name, "", "#{}".format(iD))
        if len(self.original) != 0 and self.final not in ok_content:
            widg.delete(0, "end")
            widg.insert(0, self.original)

            msg4 = open_message(
                self, 
                families_msg[2], 
                "Change Parent Workaround", 
                "OK")
            msg4[0].grab_set()
            msg4[2].config(command=lambda entry=widg, msg=msg4: err_done4(
                entry, msg))
            return

        elif len(self.final) == 0:
            column = widg.grid_info()["column"]
            delete_parent(column)
        elif len(self.original) == 0:
            self.make_alt_parent(column, finding_id, widg, conn, cur)

    def make_alt_parent(self, column, finding_id, widg, conn, cur):

        def err_done4(entry, msg):
            entry.delete(0, 'end')
            msg4[0].grab_release()
            msg4[0].destroy()
            entry.focus_set()

        name_data = check_name(ent=widg)
        if not name_data:
            msg4 = open_message(
                self, 
                families_msg[1], 
                "Person Name Unknown", 
                "OK")
            msg4[0].grab_set()
            msg4[2].config(command=lambda entry=widg, msg=msg4: err_done4(
                entry, msg))
            return

        if name_data == "add_new_person":
            alt_parent_id = open_new_person_dialog(
                self, widg, self.root, self.treebard, self.formats, 
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
        else:
            alt_parent_id = name_data[1]

        if column == 1:
            cur.execute(update_persons_persons1_by_finding, (alt_parent_id, finding_id))
        elif column == 3:
            cur.execute(update_persons_persons2_by_finding, (alt_parent_id, finding_id))
        conn.commit()

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
            self.update_parent(self.final, conn, cur, widg, kin_type=2)
        elif widgname == "ma":
            self.update_parent(self.final, conn, cur, widg, kin_type=1)
        elif widgname.startswith("altparent"):
            labcol = column - 1
            for child in self.parentslab.winfo_children():
                if child.winfo_class() == "Label" and child.winfo_subclass() == "Label":
                    childgridinfo = child.grid_info()
                    if childgridinfo["column"] == labcol and childgridinfo["row"] == row:
                        text = child.cget("text")
                        break
            if text.startswith("A"):
                kin_type = 83
            elif text.startswith("F"):
                kin_type = 95
            elif text.startswith("G"):
                kin_type = 48                    
            self.update_altparent(self.final, conn, cur, widg, column, kin_type=kin_type)
        elif widgname.startswith("pard"):
            if column == 2:
                self.update_partner(self.final, conn, cur, widg)                
            else:
                print(
                    "line", 
                    looky(seeline()).lineno, 
                    "case not handled for column", column)
        else:
            if column == 1:
                self.update_child_name(widg, conn, cur)
            elif column == 2:
                self.update_child_gender()
            elif column == 3:
                self.update_child_birth()
            elif column == 5:
                self.update_child_death()
            else:
                print("line", looky(seeline()).lineno, "case not handled:")    

        cur.close()
        conn.close()
        self.treebard.main.findings_table.redraw()

    def change_kin_type(self, evt):
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
            fpid = self.family_data[0][1:][row - 1][0]["fpid"]
            if col == 0:
                cur.execute(update_findings_persons_kin_type1, (new_id, fpid))
            elif col == 2:
                cur.execute(update_findings_persons_kin_type2, (new_id, fpid))                
            conn.commit()
            cancel_change()
            cur.close()
            conn.close()

        def cancel_change():
            frm.destroy()

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_kin_type_alt_parent)
        names_ids = cur.fetchall()
        alt_parent_types = [i[0] for i in names_ids]
        widg = evt.widget
        frm = FrameHilited(widg)
        combo = Combobox(frm, self.root, values=alt_parent_types)
        ok_butt = Button(frm, text="OK", command=ok_change, width=7)
        cancel_butt = Button(frm, text="CANCEL", command=cancel_change, width=7)
        frm.grid(column=0, row=0, sticky="ew")
        combo.grid(column=0, row=0) 
        ok_butt.grid(column=1, row=0)
        cancel_butt.grid(column=2, row=0)

        cur.close()
        conn.close()

