# families.py

import tkinter as tk
import sqlite3
from widgets import (
    Frame, LabelH3, Label, Button, Canvas, LabelEntry, Radiobutton, LabelFrame)
from files import get_current_file
from autofill import EntryAutoHilited, EntryAuto    
from scrolling import Scrollbar
from names import (open_new_person_dialog, make_all_names_list_for_person_select,
    get_any_name_with_id, )
from messages import InputMessage
from dates import format_stored_date, get_date_formats, OK_MONTHS
from events_table import get_current_person    
from query_strings import (
    select_finding_id_birth, delete_findings_persons,
    update_findings_persons_by_id1, update_findings_persons_by_id2,
    select_person_id_gender, select_finding_date, select_finding_id_birth,
    select_finding_id_death, select_finding_date_and_sorter,
    update_findings_persons_finding,
)
import dev_tools as dt
from dev_tools import looky, seeline




def get_all_marital_event_types():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    cur.execute(
    '''
        SELECT event_type_id 
        FROM event_type
        WHERE marital = 1
    ''')

    marital_event_types = [i[0] for i in cur.fetchall()]

    return marital_event_types

class NuclearFamiliesTable(Frame):
    def __init__(
            self, master, root, treebard, current_person, findings_table, 
            right_panel, formats, person_autofill_values=[], *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        print("line", looky(seeline()).lineno, "self.master:", self.master)
        self.root = root
        self.treebard = treebard
        self.current_person = current_person
        self.person_autofill_values = person_autofill_values
        self.date_prefs = get_date_formats(tree_is_open=1)
        self.findings_table = findings_table
        self.right_panel = right_panel
        self.formats = formats

        self.current_person_parents = [
            [None, None], 
            {"id": None, "name": None, "widget": None}, 
            {"id": None, "name": None, "widget": None}]

        self.newkinvar = tk.IntVar()

        self.make_widgets()

    def make_widgets(self):

        self.nuke_canvas = Canvas(self)
        self.nuke_window = Frame(self.nuke_canvas)
        self.nuke_canvas.create_window(0, 0, anchor="nw", window=self.nuke_window)
        nuke_sbv = Scrollbar(
            self, command=self.nuke_canvas.yview, hideable=True)
        self.nuke_canvas.config(yscrollcommand=nuke_sbv.set)
        nuke_sbh = Scrollbar(
            self, orient='horizontal', 
            command=self.nuke_canvas.xview, hideable=True)
        self.nuke_canvas.config(xscrollcommand=nuke_sbh.set)

        # children of self
        self.nuke_canvas.grid(column=0, row=0, sticky="news")
        nuke_sbv.grid(column=1, row=0, sticky="ns")
        nuke_sbh.grid(column=0, row=1, sticky="ew")

    def make_nuke_frames(self):
        self.pardlabs = []
        parentslab = LabelFrame(self.nuke_window) 
        labelwidget = LabelH3(parentslab, text="Parents of the Current Person")
        self.pardlabs.append(labelwidget)
        parentslab.config(labelwidget=labelwidget)
        parentslab.grid(column=0, row=0, sticky="w")
        malab = Label(parentslab, text="Mother")
        malab.grid(column=0, row=0, sticky="w", padx=(12,0), pady=(6,12))
        self.ma_input = EntryAuto(
            parentslab, width=30, autofill=True, 
            values=self.person_autofill_values, name="ma")
        self.ma_input.grid(column=1, row=0, pady=(6,12), padx=(6,0))
        palab = Label(parentslab, text="Father")
        palab.grid(column=2, row=0, sticky="w", padx=(18,0), pady=(6,12))
        self.pa_input = EntryAuto(
            parentslab, width=30, autofill=True, 
            values=self.person_autofill_values, name="pa")
        self.pa_input.grid(column=3, row=0, pady=(6,12), padx=(6,12))
        self.nuke_inputs.append(self.ma_input)
        self.nuke_inputs.append(self.pa_input)
        EntryAuto.all_person_autofills.extend([self.ma_input, self.pa_input])
        for ent in (self.ma_input, self.pa_input):
            ent.bind("<KeyRelease-Delete>", self.open_input_message)
            ent.bind("<KeyRelease-BackSpace>", self.open_input_message)

    def fix_buttons(self):
        
        if self.newkinvar.get() == 100:
            self.childmaker.config(state="disabled")
            self.pardmaker.config(state="normal")
            if len(self.pardrads) == 0:
                self.kinradnew.config(state="normal")
        elif self.newkinvar.get() == 999:
            self.pardmaker.config(state="normal")
            self.childmaker.config(state="normal")
            if len(self.pardrads) == 0:
                self.kinradnew.config(state="disabled")
        else:
            self.pardmaker.config(state="disabled")
            self.childmaker.config(state="normal")
            if len(self.pardrads) == 0:
                self.kinradnew.config(state="normal") 

    def make_new_kin_inputs(self):
        new_kin_frame = Frame(self.nuke_window)
        new_kin_frame.grid(column=0, row=self.last_row, sticky="ew")
        self.kinradnew = Radiobutton(
            new_kin_frame, variable=self.newkinvar,
            value=100, anchor="w", 
            command=self.fix_buttons)
        self.kinradnew.grid(column=0, row=0)
        self.new_kin_input = EntryAutoHilited(
            new_kin_frame, self.formats, width=48, 
            autofill=True, 
            values=self.person_autofill_values)
        self.new_kin_input.grid(column=1, row=0)
        self.pardmaker = Button(
            new_kin_frame, 
            text="ADD PARTNER", width=12, 
            command=self.add_partner)
        self.pardmaker.grid(column=2, row=0, padx=(6,0), pady=(12,0))
        self.childmaker = Button(
            new_kin_frame, 
            text="ADD CHILD", width=12, 
            command=self.add_child)
        self.childmaker.grid(column=3, row=0, padx=(6,0), pady=(12,0))
        EntryAuto.all_person_autofills.append(self.new_kin_input)

    def get_marital_event_types(self):

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        marital_event_types = get_all_marital_event_types()
        qlen = len(marital_event_types)
        marital_event_types.insert(0, self.current_person)
        marital_event_types.insert(0, self.current_person)
        
        sql = '''
                SELECT findings_persons_id, person_id1, kin_type_id1,
                    person_id2, kin_type_id2, findings_persons.finding_id, 
                    date
                FROM findings_persons
                JOIN finding
                    ON finding.finding_id = findings_persons.finding_id
                WHERE (person_id1 = ? OR person_id2 = ?) 
                    AND event_type_id in ({})
            '''.format(",".join(["?"] * qlen))
        cur.execute(sql, marital_event_types)
        marital_events_current_person = [list(i) for i in cur.fetchall()]
        cur.close()
        conn.close()
        return marital_events_current_person
        
    def add_partner(self):
        print("howdy pardner")

    def add_child(self):
        print("hey kid")

    def bind_inputs(self):
        for widg in self.nuke_inputs:
            widg.bind("<FocusIn>", self.get_original, add="+")
            widg.bind("<FocusOut>", self.get_final, add="+")

    def get_original(self, evt):
        self.original = evt.widget.get()

    def edit_parent(self, final, widg):
        unlink = False
        if "#" in final:
            print("line", looky(seeline()).lineno, "# in final:")
            new_parent_id = final.split("#")[1]
        elif len(final) == 0:
            print("line", looky(seeline()).lineno, "len(final) == 0:")
            new_parent_id = None
            unlink = True
        else:
            print("line", looky(seeline()).lineno, "making new person:")
            new_parent_id = open_new_person_dialog(
                self, widg, self.root, self.treebard, self.formats)
            people = make_all_names_list_for_person_select()
            all_birth_names = EntryAuto.create_lists(people)
            for ent in EntryAuto.all_person_autofills:
                ent.values = all_birth_names

        return new_parent_id, unlink 

    def update_mother(self, final, conn, cur, widg):
        new_parent_id, unlink = self.edit_parent(final, widg)
        birth_id = self.current_person_parents[0][1]
        birth_fpid = self.current_person_parents[0][0]

        self.make_parents_dict(ma_id=new_parent_id)

        if self.birth_record[3] == 1:
            which = 1
        elif self.birth_record[5] == 1:
            which = 2  
        if unlink is False:
            if which == 1:
                query = update_findings_persons_by_id1
            elif which == 2:
                query = update_findings_persons_by_id2 
        elif unlink is True:
            if which == 1:
                query = update_findings_persons_by_id1_unlink
            elif which == 2:
                query = update_findings_persons_by_id2_unlink
        cur.execute(query, (new_parent_id, birth_fpid))
        conn.commit()

    def update_father(self, final, conn, cur, widg):
        new_parent_id, unlink = self.edit_parent(final, widg)
        birth_id = self.current_person_parents[0][1]
        birth_fpid = self.current_person_parents[0][0]

        self.make_parents_dict(pa_id=new_parent_id)

        if self.birth_record[3] == 2:
            which = 1
        elif self.birth_record[5] == 2:
            which = 2  
        if unlink is False:
            if which == 1:
                query = update_findings_persons_by_id1
            elif which == 2:
                query = update_findings_persons_by_id2 
            cur.execute(query, (new_parent_id, birth_fpid))
            conn.commit()
        elif unlink is True:
            if which == 1:
                self.query = update_findings_persons_by_id1
            elif which == 2:
                self.query = update_findings_persons_by_id2
        # cur.execute(query, (new_parent_id, birth_fpid))
        # conn.commit()

    def update_partner(self, final, conn, cur, widg):
    
        def update_partners_child(birth_fpid, order, parent_type, new_partner_id):
            query1 = '''
                UPDATE findings_persons
                SET (person_id2, age2) = (?, "")
                WHERE findings_persons_id = ?
             '''

            query2 = '''
                UPDATE findings_persons
                SET (person_id1, age1) = (?, "")
                WHERE findings_persons_id = ?
             '''
            
            if parent_type == "Mother":
                if order == "1-2":                    
                    cur.execute(query2, (new_partner_id, birth_fpid))
                elif order == "2-1":                    
                    cur.execute(query1, (new_partner_id, birth_fpid))  
            elif parent_type == "Father":
                if order == "1-2":                    
                    cur.execute(query1, (new_partner_id, birth_fpid))
                elif order == "2-1":                    
                    cur.execute(query2, (new_partner_id, birth_fpid))
            conn.commit()

        def get_new_partner_id(final, widg):
            new_partner_id = 0
            if "#" in final:
                new_partner_id = final.split("#")[1]    
            elif len(final) == 0:
                # user unlinks partner by deleting existing name in entry
                pass
            else:
                new_partner_id = open_new_person_dialog(
                    self, widg, self.root, self.treebard, self.formats)
            return new_partner_id     

        orig = self.original
        new_partner_id = get_new_partner_id(final, widg)
        print("line", looky(seeline()).lineno, "new_partner_id:", new_partner_id)
        # if dialog canceled change nothing in db
        if new_partner_id is None:
            widg.delete(0, 'end')
            widg.insert(0, orig)
            return
        elif new_partner_id == 0:
            new_partner_id = None
        
        for k,v in self.progeny_dicts.items():
            if widg != v["widget"]:
                continue
            for child in v["children"]:
                update_partners_child(
                    child["findings_persons_id"], 
                    child["order"], 
                    v["parent_type"], 
                    new_partner_id)

    def update_child_name(self, widg, conn, cur):

        def update_child(widg, parent_id, child, cur, conn):
            orig_child_id = child["id"]
            child_id = None 
            birth_id = None
            gender = "unknown"
            fpid = child["findings_persons_id"]
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
                #   since the nukes tables does allow changes to partners
                #   and children of the current person.
                cur.execute(select_finding_id_birth, (orig_child_id,))
                birth_id = cur.fetchone()[0]
                cur.execute(delete_findings_persons, (birth_id,))
                conn.commit()
                # HAVE TO BLANK OUT GENDER, BIRTH, DEATH TOO
            else:
                child_id = open_new_person_dialog(
                    self, widg, self.root, self.treebard, self.formats)
                print("line", looky(seeline()).lineno, "child_id:", child_id)
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

        for k,v in self.progeny_dicts.items():
            for child in v["children"]:
                if widg != child["name_widg"]:
                    continue
                else:
                    parent_id = k
                    update_child(widg, parent_id, child, cur, conn)

    def update_child_gender(self):
        print("line", looky(seeline()).lineno, "self.progeny_dicts:", self.progeny_dicts)

    def update_child_birth(self):
        print("line", looky(seeline()).lineno, "self.progeny_dicts:", self.progeny_dicts)

    def update_child_death(self):
        print("line", looky(seeline()).lineno, "self.progeny_dicts:", self.progeny_dicts)

    def get_final(self, evt):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        widg = evt.widget
        self.final = widg.get()
        if self.final == self.original: return
        col = widg.grid_info()["column"]
        widg_name = widg.winfo_name()
        if widg_name == "ma":
            self.update_mother(self.final, conn, cur, widg)
        elif widg_name == "pa":
            self.update_father(self.final, conn, cur, widg)
        elif widg_name.startswith("pard"):
            if col == 2:
                self.update_partner(self.final, conn, cur, widg)                
            else:
                print(
                    "line", 
                    looky(seeline()).lineno, 
                    "case not handled for col", col)
        else:
            if col == 1:
                self.update_child_name(widg, conn, cur)
            elif col == 2:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
                self.update_child_gender()
            elif col == 3:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
                self.update_child_birth()
            elif col == 5:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
                self.update_child_death()
            else:
                print("line", looky(seeline()).lineno, "case not handled:")    

        cur.close()
        conn.close()
        self.treebard.main.findings_table.redraw()

    def make_nuke_inputs(self, current_person=None):
        '''
            This is run in main.py and events table redraw().
        '''
        self.nuke_inputs = []
        if current_person:
            self.current_person = current_person
        else:
            self.current_person = get_current_person()
        self.make_nuke_frames()
        self.make_nuke_dicts()
        self.populate_nuke_tables()
        self.bind_inputs()
        self.make_new_kin_inputs()
        self.update_idletasks()
        wd = self.nuke_window.winfo_reqwidth()
        ht = self.right_panel.winfo_reqheight()
        self.nuke_canvas.config(width=wd, height=ht)        
        self.nuke_canvas.config(scrollregion=self.nuke_canvas.bbox('all'))

        if len(self.progeny_dicts) != 0:
            self.newkinvar.set(100)
        else:
            # set to non-existent value so no Radiobutton will be selected
            self.newkinvar.set(999)
        self.fix_buttons()

    def populate_nuke_tables(self):   
        # formats = make_formats_dict()
        lst = [
            self.current_person_parents[1]["name"], 
            self.current_person_parents[2]["name"]]
        for name in lst:
            if name == "name unknown":
                idx = lst.index(name)
                lst[idx] = ""
        a = 0
        for name in lst:
            if name and a == 0:
                self.ma_input.insert(0, name)
            elif name and a == 1:
                self.pa_input.insert(0, name)
            a += 1

        top_child_rows = []
        self.pardrads = []
        n = 0
        for i, (k,v) in enumerate(self.progeny_dicts.items(), start=1):
            n = (i * 2) - 1
            name = v["partner_name"]
            pard_kin_type = "{}:".format(v["partner_kin_type"].title())
            pard_id = k
            pard = "pard_{}_{}".format(pard_id, n)
            pardframe = Frame(self.nuke_window)
            pardframe.grid(column=0, row=n, sticky="ew")
            pardrad = Radiobutton(
                pardframe, variable=self.newkinvar, 
                value=n, anchor="w", command=self.fix_buttons)
            self.pardrads.append(pardrad)
            pardrad.grid(column=0, row=n)
            if len(v["children"]) != 0:
                ma_pa = "Children's {}:".format(v["parent_type"])
                pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            else:
                pardlab = LabelH3(
                    pardframe, text=pard_kin_type, anchor="w")
            self.pardlabs.append(pardlab)
            pardlab.grid(column=1, row=n)
            pardent = EntryAuto(
                pardframe, width=48, autofill=True, 
                values=self.person_autofill_values, name=pard)
            pardent.insert(0, name)
            pardent.grid(column=2, row=n)
            EntryAuto.all_person_autofills.append(pardent)
            pardent.bind("<KeyRelease-Delete>", self.open_input_message)
            pardent.bind("<KeyRelease-BackSpace>", self.open_input_message)

            v["widget"] = pardent
            self.nuke_inputs.append(pardent)
            progeny_frame = Frame(self.nuke_window)
            progeny_frame.grid(column=0, row=n+1)
            top_child_rows.append(progeny_frame)

            r = 0
            for dkt in v["children"]:
                c = 0
                for i in range(6):
                    if c == 0:
                        spacer = Frame(progeny_frame, width=48)
                        spacer.grid(column=c, row=r)
                    elif c == 1:
                        text = dkt["name"]
                        ent = EntryAuto(
                            progeny_frame, width=0, autofill=True, 
                            values=self.person_autofill_values)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["name_widg"] = ent
                        EntryAuto.all_person_autofills.append(ent)
                        ent.bind("<KeyRelease-Delete>", self.open_input_message)
                        ent.bind("<KeyRelease-BackSpace>", self.open_input_message)
                    elif c == 2:
                        text = dkt["gender"]
                        ent = EntryAuto(progeny_frame, width=0)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["gender_widg"] = ent
                    elif c == 3:
                        text = dkt["birth"]
                        ent = EntryAuto(progeny_frame, width=0)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["birth_widg"] = ent
                    elif c == 4:
                        text = "to"
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        lab = LabelEntry(progeny_frame, text=text, anchor="w")
                        lab.grid(column=c, row=r, sticky="w")
                    elif c == 5:
                        text = dkt["death"]
                        ent = EntryAuto(progeny_frame, width=0)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["death_widg"] = ent 
                    c += 1
                r += 1
           
        self.last_row = n + 2

        for frm in top_child_rows:            
            top_row = frm.grid_slaves(row=0)            
            top_row.reverse()  
            z = 1
            for widg in top_row[1:]:
                widg.config(width=self.findings_table.kin_widths[z] + 2)
                z += 1

        # don't know why config_generic isn't enough here
        for widg in self.pardlabs:
            widg.config(font=self.formats["heading3"])

    def make_parents_dict(self, ma_id=None, pa_id=None):
        '''
            Treebard assumes that if someone exists, then they were born 
            exactly once, had one mother and one father, and we can base 
            application design decisions on these assumptions. I am finding it 
            unsymmetrical and odd to have some persons in the tree not have a 
            birth event while others do. I'm going to try auto-creating a birth 
            event for every person as the user creates the person. It will make
            updates to the parents section at the top of the nukes table easy
            and symmetrical since there will be no special case to deal with--
            the person who exists but hasn't been born yet. (The birth event
            will not slip into the attributes table because it has already been
            forbidden to appear anywhere but the events table.) This will also 
            save the user time; they won't have to create a birth event for 
            anyone.
        '''

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute(select_finding_id_birth, (self.current_person,))
        birth_id = cur.fetchone()
        if birth_id:
            birth_id = birth_id[0]
            cur.execute(
                '''
                    SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 FROM findings_persons WHERE finding_id = ?
                ''',
                (birth_id,))
            birth_record = cur.fetchall()
            if len(birth_record) != 0:
                self.birth_record = birth_record[0]
            else:
                self.birth_record = None
        else:
            print("line", looky(seeline()).lineno, "no birth id:")

        ma_name = ""
        pa_name = ""
        parent1 = None
        parent2 = None
        if self.birth_record:
            parent1 = self.birth_record[2:4]
            parent2 = self.birth_record[4:]
            if parent1[1] == 1:
                ma_id = parent1[0]
                pa_id = parent2[0]
            elif parent1[1] == 2:
                ma_id = parent2[0]
                pa_id = parent1[0]
            self.current_person_parents[0] = self.birth_record[0:2]
        else:
            cur.execute(
                '''
                    INSERT INTO findings_persons
                    VALUES (null, ?, ?, '', 1, ?, '', 2)
                ''',
                (birth_id, ma_id, pa_id))
            conn.commit()

            cur.execute(
                '''
                SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'findings_persons'
                ''')
            fpid = cur.fetchone()[0]
            self.birth_record = (fpid, birth_id, ma_id, 1, pa_id, 2)               

            self.current_person_parents[0] = self.birth_record[0:2]

        if ma_id:
            ma_name = get_any_name_with_id(ma_id)
        if pa_id:
            pa_name = get_any_name_with_id(pa_id)

        self.current_person_parents[1]["id"] = ma_id
        self.current_person_parents[2]["id"] = pa_id
        self.current_person_parents[1]["name"] = ma_name
        self.current_person_parents[2]["name"] = pa_name
        self.current_person_parents[1]["widget"] = self.ma_input
        self.current_person_parents[2]["widget"] = self.pa_input  
        cur.close()
        conn.close()

    def make_nuke_dicts(self):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.make_parents_dict()

        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 FROM findings_persons WHERE person_id1 = ? AND kin_type_id1 IN (1,2)
            ''',
            (self.current_person,))
        result1 = cur.fetchall()
        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1,  person_id2, kin_type_id2 FROM findings_persons WHERE person_id2 = ? AND kin_type_id2 IN (1,2)
            ''',
            (self.current_person,))
        result2 = cur.fetchall()
        births = []
        self.progeny_dicts = {}
        births = [tup for q in (result1, result2) for tup in q]

        marital_event_types = get_all_marital_event_types()
        qlen = len(marital_event_types)
        sql = '''
                SELECT person_id1, person_id2
                FROM findings_persons
                JOIN finding
                    ON finding.finding_id = findings_persons.finding_id
                WHERE event_type_id in ({})                    
            '''.format(",".join("?" * qlen))
        cur.execute(sql, marital_event_types)
        partners1 = cur.fetchall()

        progenies = {}
        all_partners = []        
        partners = []
        partners = [tup for tup in partners1 if self.current_person in tup]
        event_pards = []
        offspring_pards = []
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
                "partner_kin_type": "", "widget": None, "children": [],
                "marital_events": []}
            self.progeny_dicts[pard_id] = progeny

        self.collect_couple_events(cur)

        for k,v in progenies.items():
            pardner = k
            if v["offspring"] is True:
                for tup in births:
                    order = "{}-{}".format(str(tup[3]), str(tup[5]))                
                    if tup[4] == pardner:
                        parent_type = tup[5]
                        pard_id = tup[4]
                        self.make_pard_dict(pard_id, parent_type)
                        if pard_id == pardner:
                            self.progeny_dicts[pardner]["children"].append(
                                {"findings_persons_id": tup[0], 
                                    "birth_id": tup[1], "order": order})
                    elif tup[2] == pardner:
                        parent_type = tup[3]
                        pard_id = tup[2]
                        self.make_pard_dict(pard_id, parent_type) 
                        if pard_id == pardner:
                            self.progeny_dicts[pardner]["children"].append(
                                {"findings_persons_id": tup[0], 
                                    "birth_id": tup[1], "order": order})      

            if v["events"] is True and v["offspring"] is False:
                self.make_pard_dict(pardner, "")
        for pard_id in progenies:
            for k,v in self.progeny_dicts.items():
                if k == pard_id:
                    for dkt in v["children"]:
                        self.finish_progeny_dict(dkt, cur)
        
        main_sorter = [0, 0, 0]
        for k,v in self.progeny_dicts.items():
            kids = v["children"]
            kids = sorted(kids, key=lambda i: i["sorter"])
            v["children"] = kids
            if len(v["children"]) != 0:
                main_sorter = v["children"][0]["sorter"]
            if len(v.get("sorter")) == 0:
                v["sorter"] = main_sorter
        self.progeny_dicts = dict(
            sorted(
                self.progeny_dicts.items(), key=lambda i: i[1]["sorter"]))
        cur.close()
        conn.close()

    def make_pard_dict(self, pard_id, parent_type):
        if parent_type == 1:
            parent_type = "Mother"
        elif parent_type == 2:
            parent_type = "Father"
        partner_name = get_any_name_with_id(pard_id)
        self.progeny_dicts[pard_id]["parent_type"] = parent_type
        self.progeny_dicts[pard_id]["partner_name"] = partner_name   

    def collect_couple_events(self, cur):
        marital_events = self.get_marital_event_types() 
        for lst in marital_events:
            if lst[1] == self.current_person:
                del lst[1:3]
            elif lst[3] == self.current_person:
                del lst[3:5]            

        self.sorters = []
        for lst in marital_events:
            self.save_marital_events(lst, cur)

        self.sorters = sorted(self.sorters, key=lambda i: i[1])
        for k,v in self.progeny_dicts.items():
            for sorter in self.sorters:
                if sorter[0] == k:
                    v["sorter"] = sorter[1]

    def save_marital_events(self, lst, cur):
        partner_id = lst[1]
        for k,v in self.progeny_dicts.items():
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
                    {"findings_persons_id": lst[0], "finding": lst[3]})

    def finish_progeny_dict(self, dkt, cur):   
        cur.execute(
            '''
                SELECT person_id, date
                FROM finding
                WHERE finding_id = ?
                    AND event_type_id = 1
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
        name = get_any_name_with_id(born_id)

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

    def open_input_message(self, evt):
        '''
            A dialog opens on press of Delete or BackSpace in one of the person 
            inputs. It looks like getting focus to return to the place where it
            started is not going to be easy, probably because the original
            widget is destroyed and replaced. I tried getting the original's
            row & column but it didn't work--when the dialog closes, focus keeps
            returning to the same place, root I guess, anyway the first Tab press
            just goes back to the first widget on the page.
        '''
        widg = evt.widget        
        if len(self.original) == 0 or len(widg.get()) != 0: return
        widg_name = widg.winfo_name()
        if widg_name in ("ma", "pa"):
            reltype = "parent"
            radtext = (
                "Unlink the deleted parent from the current person.", 
                "Completely remove all traces of the deleted parent from the "
                "entire tree. (Delete the person.)")
        elif widg_name.startswith("pard"):
            reltype = "partner"
            radtext = (
                "SEE DO LIST--Unlink the deleted partner from the current person. All marital events will be removed from the deleted partner but retained by the current person with no known partner. If they have children together, the offspring event will be unlinked from the partner but retained by the current person, and the child in question will have an unknown co-parent. If they have children AND marital events together, removing the parent as co-parent will not delete the marital events.", 
                "Unlink the deleted partner from the current person. All marital events will be removed from both partners and permanently removed from the tree.", 
                "Completely remove all traces of the deleted partner from the "
                "entire tree. (Delete the person.)")
        else:
            reltype = "child"
            radtext = (
                "Unlink the deleted child from the partner of the current person only. The offspring event will be retained by the current person with no known co-parent.", 
                "Unlink the deleted child from the current person only. The offspring event will be retained by the current person's partner with no known co-parent.",
                "Unlink the deleted child from both the current person and his/her partner. The child's parents are unknown.", 
                "Completely remove all traces of the deleted child from the "
                "entire tree. (Delete the person.)")
        unlinker = InputMessage(
            self.root, root=self.root, title="Delete or Unlink?", ok_txt="OK", 
            radtext=radtext, radio=True, cancel_txt="CANCEL", grab=True, 
            head1="Clarify whether to unlink or delete the person:", 
            wraplength=650)
        self.show = unlinker.show()
        self.delete_or_unlink(reltype)

    def delete_or_unlink(self, reltype):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        birth_fpid = self.current_person_parents[0][0]
        if reltype == "parent":
            if self.show == 0:
                cur.execute(self.query, (None, birth_fpid))
                conn.commit()
            elif self.show == 1:
                pass

        elif reltype == "partner":
            if self.show == 0:
                pass

            elif self.show == 1:
                pass

            elif shelf.show == 2:
                pass

        elif reltype == "child":
            if self.show == 0:
                pass

            elif self.show == 1:
                pass

            elif shelf.show == 2:
                pass

        cur.close()
        conn.close()
        self.treebard.main.findings_table.redraw()

# line 681 self.current_person_parents: [(11, 128), {'id': 5564, 'name': 'Phoebe Tellhouse', 'widget': <autofill.EntryAuto object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.ma>}, {'id': None, 'name': '', 'widget': <autofill.EntryAuto object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.pa>}]




'''
    Two means of determining partnership are used. 1) a couple has 
    children together, or 2) a couple are linked by a common couple
    event such as marriage or divorce regardless of whether they
    have children together.

    Problem is, if user unlinks a partner from current person's
    marriage event, should Treebard auto-unlink the partner from the
    divorce event too? Since partnerships are detected only on the
    basis of existing marital events if there are no children, the
    answer is yes. Not unlinking the marital events from a deleted
    partner. or not editing a changed name on marital events if the
    partner's name is changed... would be a disaster. And the deleted
    partner would show up on the nukes table if the links were left
    intact. The only way around this would be to find another way
    to detect childless couples that doesn't involve detecting
    marital events. (What about kin types such as spouse, wife, etc.)

    Couple events are determined by a boolean in the event_type 
    database table. But not all couple events are evidence for 
    a partnership that you'd want on the nukes (nuclear family) table.
    But all couple events are treated the same in other ways, for 
    example, if two people get engaged, the user only has to create 
    the event for one of them, and Treebard auto-creates the event
    for the other person; all couple events should work this way.

    So a second boolean is used to distinguish non-binding couple
    events such as "first kiss" or "engagement" or "marriage banns".
    For inclusion in the nukes table, partnership will be marked
    by the boolean column called "marital". This category includes
    anything that should mark a partnership even if there are no children,
    such as marriage, wedding, divorce, cohabitation, separation, etc.

    (The event or dated attribute "marital status" isn't even a couple
    event, since it makes no reference to who the partner is and would
    be asked of one person at a time. Even if both partners in a couple 
    answered this question at the same time, the user would have to 
    enter each answer separately for the two people.)

    Kin types are used to state for example that a partner is a spouse,
    wife, husband, etc. They aren't used to detect anything, because
    they are too loose, the user just decides what to call a partner,
    such as "boyfriend", "mistress", etc. The event should have all the
    power, not kin type, when it comes to determining partnership if 
    there are no children to determine it. The user should be the one
    to decide whether to include a mistress on the nukes table, by
    inputting a cohabitation event, for example, for a man with a 
    second family hidden away somewhere. Unlike some genieware, Treebard
    differentiates between "spouse" and "mother of children", so it's
    not necessary to create a hypothetical spouse in order to identify the
    parents in a nuclear family.
''' 