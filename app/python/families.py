# families.py


import tkinter as tk
import sqlite3
from widgets import (
    Frame, LabelH3, Label, Button, Canvas, LabelEntry, Radiobutton, LabelFrame,
    FrameHilited)
from custom_combobox_widget import Combobox
from files import get_current_file
from autofill import EntryAutoHilited, EntryAuto    
from scrolling import Scrollbar
from names import (open_new_person_dialog, make_all_names_list_for_person_select,
    get_any_name_with_id, delete_person_from_tree, update_person_autofill_values)
from messages import InputMessage
from dates import format_stored_date, get_date_formats, OK_MONTHS
from events_table import get_current_person
from query_strings import (
    select_finding_id_birth, delete_findings_persons, select_persons_persons,
    select_person_id_gender, select_finding_date, select_finding_id_birth,
    select_finding_id_death, select_finding_date_and_sorter,
    update_findings_persons_finding, insert_persons_persons_one_person,
    insert_findings_persons_new_parent, select_findings_persons_birth,
    update_persons_persons_1, update_persons_persons_2, select_kin_type_string,
    update_persons_persons1_by_finding, update_persons_persons2_by_finding,
    select_kin_type_alt_parent, update_findings_persons_kintype1,
    update_findings_persons_kintype2
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

    cur.close()
    conn.close()

    return marital_event_types

class NuclearFamiliesTable(Frame):
    def __init__(
            self, master, root, treebard, current_person, findings_table, 
            right_panel, formats, person_autofill_values=[], 
            *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
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

        self.nuke_containers = []
        self.current_person_alt_parents = []

        self.delete_or_unlink_ok = False

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

    def make_nuke_widgets_perm(self):
        
        self.pardlabs = []
        self.parentslab = LabelFrame(self.nuke_window) 
        labelwidget = LabelH3(self.parentslab, text="Parents of the Current Person")
        self.pardlabs.append(labelwidget)
        self.parentslab.config(labelwidget=labelwidget)
        palab = Label(self.parentslab, text="Father", anchor="e")
        self.pa_input = EntryAuto(
            self.parentslab, width=30, autofill=True, cursor="hand2", 
            values=self.person_autofill_values, name="pa")
        malab = Label(self.parentslab, text="Mother", anchor="e")
        self.ma_input = EntryAuto(
            self.parentslab, width=30, autofill=True, cursor="hand2",
            values=self.person_autofill_values, name="ma")

        # children of self.nuke_window
        self.parentslab.grid(column=0, row=0, sticky="w")

        # children of self.parentslab
        palab.grid(column=0, row=0, sticky="ew", padx=(12,12), pady=(6,12))
        self.pa_input.grid(column=1, row=0, pady=(6,12), padx=(0,0))
        malab.grid(column=2, row=0, sticky="ew", padx=(12,12), pady=(6,12))
        self.ma_input.grid(column=3, row=0, pady=(6,12), padx=(0,0))

        EntryAuto.all_person_autofills.extend([self.ma_input, self.pa_input])
        for ent in (self.pa_input, self.ma_input):
            ent.bind("<KeyRelease-Delete>", self.open_delete_or_unlink_dialog)
            ent.bind("<KeyRelease-BackSpace>", self.open_delete_or_unlink_dialog)
            ent.bind("<FocusIn>", self.get_original, add="+")
            ent.bind("<FocusOut>", self.get_final, add="+")
            ent.bind("<Double-Button-1>", self.change_current_person)
        

    def fix_button_state(self):
        
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
        """ Get self.new_kin_frame into the correct row by ungridding it in 
            self.findings_table.forget_cells() and regridding it in self.make_nuke_inputs()
        """
        self.new_kin_frame = Frame(self.nuke_window)
        self.kinradnew = Radiobutton(
            self.new_kin_frame, variable=self.newkinvar,
            value=100, anchor="w", 
            command=self.fix_button_state)
        self.new_kin_input = EntryAutoHilited(
            self.new_kin_frame, self.formats, width=48, 
            autofill=True, 
            values=self.person_autofill_values)
        self.pardmaker = Button(
            self.new_kin_frame, 
            text="ADD PARTNER", width=12, 
            command=self.add_partner)
        self.childmaker = Button(
            self.new_kin_frame, 
            text="ADD CHILD", width=12, 
            command=self.add_child)

        # children of self.new_kin_frame
        self.kinradnew.grid(column=0, row=0)
        self.new_kin_input.grid(column=1, row=0)
        self.pardmaker.grid(column=2, row=0, padx=(6,0), pady=(12,0))
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
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
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

    def get_original(self, evt):
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
            for k,v in self.progeny_dicts.items():
                if v["widget"] == widg:
                    print("line", looky(seeline()).lineno, "v['children']:", v['children'])
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

    def make_parent(self, widg, conn, cur):
        """ Add a parent from a blank input on the nukes table. """
        print("line", looky(seeline()).lineno, "self.final:", self.final)
        if "#" in self.final:
            new_parent_id = self.final.split("  #")[1]
        else:
            new_parent_id = open_new_person_dialog(
                self, widg, self.root, self.treebard, self.formats)
        if widg.winfo_name() == "pa":
            parent_type = 2
        elif widg.winfo_name() == "ma":
            parent_type = 1
        birth_id = self.current_person_parents[0][1]
        cur.execute(select_findings_persons_birth, (birth_id,))
        fpid = cur.fetchone()
        if fpid:
            # We know one parent is blank and one is not, so find out what to update.
            fpid, ppid = fpid
            cur.execute(select_persons_persons, (ppid,))
            persons_persons = cur.fetchone()
            print("line", looky(seeline()).lineno, "persons_persons:", persons_persons)
            if persons_persons[0] is None:
                cur.execute(update_persons_persons_1, (new_parent_id, ppid))
            elif persons_persons[1] is None:
                cur.execute(update_persons_persons_2, (new_parent_id, ppid))
            conn.commit()
        else:
            # if there's no row yet for persons_persons, make one
            cur.execute(insert_persons_persons_one_person, (new_parent_id,))
            conn.commit()
            cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "persons_persons"')
            ppid = cur.fetchone()[0]
            cur.execute(insert_findings_persons_new_parent, (birth_id, parent_type, ppid))
            conn.commit()

    def update_partner(self, final, conn, cur, widg):
    
        def update_partners_child(birth_fpid, order, parent_type, new_partner_id):
            select_findings_persons_ppid = '''
                SELECT persons_persons_id
                FROM findings_persons
                WHERE findings_persons_id = ?
            '''
            update_findings_persons_age2_blank = '''
                UPDATE findings_persons
                SET age2 = ""
                WHERE findings_persons_id = ?
            '''
            update_persons_persons_2 = '''
                UPDATE persons_persons
                SET person_id2 = ?
                WHERE persons_persons_id = ?
            '''
            update_findings_persons_age1_blank = '''
                UPDATE findings_persons
                SET age1 = ""
                WHERE findings_persons_id = ?
            '''
            update_persons_persons_1 = '''
                UPDATE persons_persons
                SET person_id1 = ?
                WHERE persons_persons_id = ?
            '''
            cur.execute(select_findings_persons_ppid, (birth_fpid,))
            ppid = cur.fetchone()[0]
            
            if parent_type == "Father":
                if order == "1-2":   
                    cur.execute(update_findings_persons_age2_blank, (birth_fpid,))
                    conn.commit()
                    cur.execute(update_persons_persons_2, (new_partner_id, ppid))
                    conn.commit()
                elif order == "2-1":      
                    cur.execute(update_findings_persons_age2_blank, (birth_fpid,))
                    conn.commit()
                    cur.execute(update_persons_persons_2, (new_partner_id, ppid))
                    conn.commit()
                    
            elif parent_type == "Mother":
                if order == "1-2":      
                    cur.execute(update_findings_persons_age2_blank, (birth_fpid,))
                    conn.commit()
                    cur.execute(update_persons_persons_2, (new_partner_id, ppid))
                    conn.commit()
                elif order == "2-1":   
                    cur.execute(update_findings_persons_age2_blank, (birth_fpid,))
                    conn.commit()
                    cur.execute(update_persons_persons_2, (new_partner_id, ppid))
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
        # if dialog canceled change nothing in db
        if new_partner_id is None:
            widg.delete(0, 'end')
            widg.insert(0, orig)
            return
        elif new_partner_id == 0:
            new_partner_id = None
        else:
            for k,v in self.progeny_dicts.items():
                if widg != v["widget"]:
                    continue
                elif widg == v["widget"]:
                    if k != new_partner_id:
                        print("line", looky(seeline()).lineno, "v:", v)
                else: 
                    print("line", looky(seeline()).lineno, "case not handled:")
        
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

    def update_parent(self, final, conn, cur, widg, kin_type=None):
        """ If the field is not blank, emulate a disabled field for any input that tries to
            change the contents to a different person (to change a parent, partner, or child,
            make that person the current person first.)
        """
        print("line", looky(seeline()).lineno, "running:")
        for dkt in self.current_person_parents[1:]:
            print("line", looky(seeline()).lineno, "dkt:", dkt)
            if widg == dkt["widget"]:
                iD = dkt["id"]
                name = dkt["name"]
                break
        bare_name = None
        if "(" in name:
            bare_name = name.split(" (")[-2]
            name_id = "{}  #{}".format(bare_name, iD)
        else:
            name_id = "{}  #{}".format(name, iD)
        ok_content = (name, name_id, bare_name, "") 
        print("line", looky(seeline()).lineno, "ok_content:", ok_content)
        print("line", looky(seeline()).lineno, "self.current_person_parents:", self.current_person_parents)
        if len(self.original) != 0 and self.final not in ok_content:
            widg.delete(0, "end")
            widg.insert(0, self.original)
            return
        elif len(self.final) == 0:
            print("line", looky(seeline()).lineno, "unlink is true:")
            print("line", looky(seeline()).lineno, "iD:", iD)
            # if unlink from partner, also unlink from all kids of these 2 parents but kids stay linked to current person
            print("line", looky(seeline()).lineno, "self.progeny_dicts[iD]:", self.progeny_dicts[iD])
            print("line", looky(seeline()).lineno, "self.current_person:", self.current_person)
        elif len(self.original) == 0:
            self.make_parent(widg, conn, cur)
            # people = make_all_names_list_for_person_select()
            # all_birth_names = EntryAuto.create_lists(people)
            # for ent in EntryAuto.all_person_autofills:
                # ent.values = all_birth_names
            update_person_autofill_values()

    def update_altparent(self, final, conn, cur, widg, column, row, kin_type=None):
        """ Maybe this can be combined with update_parent by parameterizing the 
            2 separate methods. 
        """
        print("line", looky(seeline()).lineno, "final:", final)
        print("line", looky(seeline()).lineno, "widg:", widg)
        print("line", looky(seeline()).lineno, "kin_type:", kin_type) 
        print("line", looky(seeline()).lineno, "column:", column)
        print("line", looky(seeline()).lineno, "row:", row)
        print("line", looky(seeline()).lineno, "self.current_person_alt_parents:", self.current_person_alt_parents)
# line 493 final: Louis Decicco
# line 494 widg: .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.altparent_l0
# line 495 kin_type: 95
# line 496 column: 1
# line 497 row: 1
# line 498 self.current_person_alt_parents: [[[137, 1090, ['foster parent', 'foster parent']], {'id': None, 'name': None, 'widget': <autofill.EntryAuto object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.altparent_l0>, 'label': <widgets.Label object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.!label3>}, {'id': 5810, 'name': 'Marta Morrow', 'widget': <autofill.EntryAuto object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.altparent_r0>, 'label': <widgets.Label object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.!label4>}]]

        y = 1
        for lst in self.current_person_alt_parents:
            for dkt in lst[1:]:
                if widg == dkt["widget"]:
                    fpid, finding_id = lst[0][0:2]
                    break
            y += 1                

        if "#" in final:
            alt_parent_id = final.split("  #")[1]
            print("line", looky(seeline()).lineno, "fpid, finding_id:", fpid, finding_id)
            # if column == 1:
                # cur.execute(update_persons_persons1_by_finding, (alt_parent_id, finding_id))
            # elif column == 3:
                # cur.execute(update_persons_persons2_by_finding, (alt_parent_id, finding_id))
            # conn.commit()
            
        else:
            alt_parent_id = open_new_person_dialog(
                self, widg, self.root, self.treebard, self.formats)

        if column == 1:
            cur.execute(update_persons_persons1_by_finding, (alt_parent_id, finding_id))
        elif column == 3:
            cur.execute(update_persons_persons2_by_finding, (alt_parent_id, finding_id))
        conn.commit()

        update_person_autofill_values()
        


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
            self.update_altparent(self.final, conn, cur, widg, column, row, kin_type=kin_type)
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

    def make_nuke_inputs(self, current_person=None, on_load=False):
        '''
            Run in main.py on_load=True and in events_table.py redraw() 
            on_load=False.
        '''
        self.nuke_inputs = []
        if current_person:
            self.current_person = current_person
        else:
            self.current_person = get_current_person()
        if on_load:
            self.make_nuke_widgets_perm()
        self.make_nuke_dicts()
        self.populate_nuke_tables()
        for widg in self.nuke_inputs:
            widg.bind("<FocusIn>", self.get_original, add="+")
            widg.bind("<FocusOut>", self.get_final, add="+")
        if on_load:
            self.make_new_kin_inputs()
        self.new_kin_frame.grid(column=0, row=self.last_row, sticky="ew")
        for row in range(self.nuke_window.grid_size()[1]):
            self.nuke_window.rowconfigure(row, weight=1)
            
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
        self.fix_button_state()

    def populate_nuke_tables(self):
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
            self.nuke_containers.append(pardframe)
            pardrad = Radiobutton(
                pardframe, variable=self.newkinvar, 
                value=n, anchor="w", command=self.fix_button_state)
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
                pardframe, width=48, autofill=True, cursor="hand2", 
                values=self.person_autofill_values, name=pard)
            pardent.insert(0, name)
            pardent.grid(column=2, row=n)
            EntryAuto.all_person_autofills.append(pardent)
            pardent.bind("<KeyRelease-Delete>", self.open_delete_or_unlink_dialog)
            pardent.bind("<KeyRelease-BackSpace>", self.open_delete_or_unlink_dialog)
            pardent.bind("<Double-Button-1>", self.change_current_person)

            v["widget"] = pardent
            self.nuke_inputs.append(pardent)
            progeny_frame = Frame(self.nuke_window)
            progeny_frame.grid(column=0, row=n+1)
            self.nuke_containers.append(progeny_frame)
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
                            progeny_frame, width=0, autofill=True, cursor="hand2", 
                            values=self.person_autofill_values)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["name_widg"] = ent
                        EntryAuto.all_person_autofills.append(ent)
                        ent.bind("<KeyRelease-Delete>", self.open_delete_or_unlink_dialog)
                        ent.bind("<KeyRelease-BackSpace>", self.open_delete_or_unlink_dialog)
                        ent.bind("<Double-Button-1>", self.change_current_person)
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
            the person who exists but hasn't been born yet. This will also 
            save the user time; they won't have to create a birth event for 
            anyone. Then when the user inputs an alternate parent event 
            (guardianship, fosterage, adoption), the same process will create
            inputs for the alternate parents. All symmetrical procedures except
            that the person's birth is assumed so exactly two inputs are always
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

        ma_name = ""
        pa_name = ""
        parent1 = None
        parent2 = None
        if self.parent_record:
            parent1 = self.parent_record[2:4]
            parent2 = self.parent_record[4:]
            if parent1[1] == 1:
                ma_id = parent1[0]
                pa_id = parent2[0]
            elif parent1[1] == 2:
                ma_id = parent2[0]
                pa_id = parent1[0]
            self.current_person_parents[0] = self.parent_record[0:2]
        else:
            # This only runs when there are no parents recorded.
            print("812 if this is still needed there will have to be inserts to persons_persons and to findings_persons, at least")
            self.current_person_parents[0][1] = birth_id
            # cur.execute(
                # '''
                    # INSERT INTO findings_persons
                    # VALUES (null, ?, ?, '', 1, ?, '', 2)
                # ''',
                # (birth_id, ma_id, pa_id))
            # conn.commit()

            # self.current_person_parents[0] = self.parent_record[0:2]

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
        
        alt_parent_details = []

        r = 0
        for event in alt_parent_events:
            event = list(event)
            event[1] = [int(i) for i in event[1].split(",")]
            alt_parent_events[r] = event
            r += 1
        alt_parent_events = sorted(alt_parent_events, key=lambda i: i[1])
        
        for event in alt_parent_events:
            parent_couple = [
                [None, None], 
                {"id": None, "name": None, "widget": None, "label": None}, 
                {"id": None, "name": None, "widget": None, "label": None}]
            cur.execute(
            '''
                SELECT persons_persons_id, kin_type_id1, kin_type_id2, findings_persons_id
                FROM findings_persons
                WHERE finding_id = ?
            ''',
            (event[0],))
            couple_details = list(cur.fetchone())
            alt_parent_type = []
            for kintype in couple_details[1:3]:
                cur.execute(select_kin_type_string, (kintype,))
                alt_parent_type.append(cur.fetchone()[0])
            parent_couple[0] = [couple_details.pop(), event[0], alt_parent_type]
            alt_parent_details.append(couple_details)
            self.current_person_alt_parents.append(parent_couple)
        print("line", looky(seeline()).lineno, "self.current_person_alt_parents:", self.current_person_alt_parents)

        for lst in alt_parent_details:
            cur.execute(
            '''
                SELECT person_id1, person_id2
                FROM persons_persons
                WHERE persons_persons_id = ?
            ''',
            (lst[0],))
            couple_ids = cur.fetchone()
            lst.insert(2, couple_ids[1])
            lst.insert(1, couple_ids[0])

        # u = 0
        # for lst in alt_parent_details:
            # cur.execute(
            # '''
                # SELECT gender
                # FROM person
                # WHERE person_id = ?
            # ''',
            # (lst[1],))
            # gender = cur.fetchone()
            # if gender and gender == "female":
                # continue
            # else:
                # copy = []
                # # This re-ordering is supposed to get females to display to the 
                # #   left of males but if gender is unknown obviously it doesn't
                # #   work so if user wants females on left he has to label them
                # #   females. If I change this to the traditional order whith the
                # #   males on the left, the same problem will exist with males
                # #   recorded as gender unknown. Try to leave it alone and see
                # #   what happens. If it proves to be glitchy then just don't 
                # #   order by gender at all, and see if that works better.
                # for i in (0, 3, 4, 1, 2):
                    # copy.append(lst[i])
                # alt_parent_details[u] = copy
            # u += 1

        w = 0
        for lst in alt_parent_details:
            print("line", looky(seeline()).lineno, "lst:", lst)
            name1 = None
            name2 = None
            id1 = lst[1]
            id2 = lst[3]
            if id1:
                name1 = get_any_name_with_id(id1)
                self.current_person_alt_parents[w][1]["id"] = id1
            if id2:
                name2 = get_any_name_with_id(id2)
                self.current_person_alt_parents[w][2]["id"] = id2
            if name1:
                self.current_person_alt_parents[w][1]["name"] = name1
                lst[1] = name1
                cur.execute(
                '''
                    SELECT kin_types 
                    FROM kin_type
                    WHERE kin_type_id = ?
                ''',
                (lst[2],))
                result = cur.fetchone()[0]
                lst[2] = result
            else:
                alt_parent_type = self.current_person_alt_parents[w][0][2]
                lst[2] = alt_parent_type[0]
            if name2:
                print("line", looky(seeline()).lineno, "self.current_person_alt_parents:", self.current_person_alt_parents)
                self.current_person_alt_parents[w][2]["name"] = name2
                lst[3] = name2
                cur.execute(
                '''
                    SELECT kin_types 
                    FROM kin_type
                    WHERE kin_type_id = ?
                ''',
                (lst[4],))
                result = cur.fetchone()[0]
                lst[4] = result
            else:
                alt_parent_type = self.current_person_alt_parents[w][0][2]
                lst[4] = alt_parent_type[1]
            w += 1
       
        j = 0
        for lst in alt_parent_details:
            lab_l = Label(self.parentslab, anchor="e")
            ent_l = EntryAuto(
                self.parentslab, width=30, autofill=True, cursor="hand2", 
                values=self.person_autofill_values,
                name="altparent_l{}".format(str(j)))
            if lst[1]:
                ent_l.insert(0, lst[1])
            self.current_person_alt_parents[j][1]["widget"] = ent_l
            self.current_person_alt_parents[j][1]["label"] = lab_l
            if lst[2]:
                lab_l.config(text=lst[2].title())

            lab_r = Label(self.parentslab, anchor="e")
            ent_r = EntryAuto(
                self.parentslab, width=30, autofill=True, cursor="hand2", 
                values=self.person_autofill_values,
                name="altparent_r{}".format(str(j)))
            if lst[3]:
                ent_r.insert(0, lst[3]) 
            self.current_person_alt_parents[j][2]["widget"] = ent_r
            self.current_person_alt_parents[j][2]["label"] = lab_r
            if lst[4]:
                lab_r.config(text=lst[4].title())

            EntryAuto.all_person_autofills.extend([ent_l, ent_r])
            for ent in (ent_l, ent_r):
                ent.bind("<KeyRelease-Delete>", self.open_delete_or_unlink_dialog)
                ent.bind("<KeyRelease-BackSpace>", self.open_delete_or_unlink_dialog)
                ent.bind("<FocusIn>", self.get_original, add="+")
                ent.bind("<FocusOut>", self.get_final, add="+")
                ent.bind("<Double-Button-1>", self.change_current_person) 
                self.nuke_containers.append(ent)
            for lab in (lab_l, lab_r):
                lab.bind("<Double-Button-1>", self.change_kin_type)

            self.nuke_containers.extend([lab_l, lab_r])           
            j += 1

    def grid_alt_parents(self):
        """ Grid widgets as children of self.parentslab. """
        x = 1
        for lst in self.current_person_alt_parents:
            z = 0
            for person in lst[1:]:
                label = person["label"]
                widget = person["widget"]
                label.grid(column=z, row=x, sticky="ew", padx=12, pady=(6,12))
                widget.grid(column=z+1, row=x, pady=(6,12))
                z += 2 
            x += 1

    def make_nuke_dicts(self):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.make_parents_dict()

# DO NOT DELETE THIS PROBABLY WILL BE NEEDED? ********************************************************
 # 111, 'adoptive mother'
# 112, 'adoptive father'
# 122, 'foster father'
# 121, 'foster mother'
# 131, 'legal guardian'
# 130, 'guardian'
# 110, 'adoptive parent'
# 120, 'foster parent'
        # all_parent_types = (1, 2, 111, 112, 122, 121, 131, 130, 110, 120)

        # cur.execute(
            # '''
                # SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 
                # FROM findings_persons 
                # JOIN persons_persons
                    # ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                # WHERE person_id1 = ? AND kin_type_id1 IN (1, 2, 111, 112, 122, 121, 131, 130, 110, 120)
            # ''',
            # (self.current_person,))
        # result1 = cur.fetchall()
        # cur.execute(
            # '''
                # SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 
                # FROM findings_persons 
                # JOIN persons_persons
                    # ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                # WHERE person_id2 = ? AND kin_type_id2 IN (1, 2, 111, 112, 122, 121, 131, 130, 110, 120)
            # ''',
            # (self.current_person,))

        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id1 = ? AND kin_type_id1 IN (1, 2)
            ''',
            (self.current_person,))
        result1 = cur.fetchall()
        cur.execute(
            '''
                SELECT findings_persons_id, finding_id, person_id1, kin_type_id1, person_id2, kin_type_id2 
                FROM findings_persons 
                JOIN persons_persons
                    ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
                WHERE person_id2 = ? AND kin_type_id2 IN (1, 2)
            ''',
            (self.current_person,))
        result2 = cur.fetchall()
        births = []
        self.progeny_dicts = {}
        births = [tup for q in (result1, result2) for tup in q]
        print("line", looky(seeline()).lineno, "births:", births)
        # ********************************************************************************************


        marital_event_types = get_all_marital_event_types()
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
                        print("line", looky(seeline()).lineno, "parent_type:", parent_type)
                        pard_id = tup[4]
                        self.make_pard_dict(pard_id, parent_type, cur)
                        if pard_id == pardner:
                            self.progeny_dicts[pardner]["children"].append(
                                {"findings_persons_id": tup[0], 
                                    "birth_id": tup[1], "order": order})
                    elif tup[2] == pardner:
                        parent_type = tup[3]
                        print("line", looky(seeline()).lineno, "parent_type:", parent_type)
                        pard_id = tup[2]
                        self.make_pard_dict(pard_id, parent_type, cur) 
                        if pard_id == pardner:
                            self.progeny_dicts[pardner]["children"].append(
                                {"findings_persons_id": tup[0], 
                                    "birth_id": tup[1], "order": order})      

            if v["events"] is True and v["offspring"] is False:
                self.make_pard_dict(pardner, "", cur)
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
        print("line", looky(seeline()).lineno, "self.progeny_dicts:", self.progeny_dicts)

    def make_pard_dict(self, pard_id, parent_type, cur):
        if parent_type == 1:
            parent_type = "Mother"
        elif parent_type == 2:
            parent_type = "Father"
        elif parent_type is None:
            print("line", looky(seeline()).lineno, "parent_type:", parent_type)
            # cur.execute(select_
            print("line", looky(seeline()).lineno, "self.progeny_dicts:", self.progeny_dicts)
            print("line", looky(seeline()).lineno, "pard_id:", pard_id)
            # self.progeny_dicts[pard_id]["parent_type"] = "rotorooter"
            
            
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

    def open_delete_or_unlink_dialog(self, evt):
        '''
            Open a dialog on press of Delete or BackSpace in one of the person 
            inputs. 

            It looks like getting focus to return to the place where it
            started is not going to be easy, probably because the original
            widget is destroyed and replaced. I tried getting the original's
            row & column but it didn't work--when the dialog closes, focus keeps
            returning to the same place, root I guess, anyway the first Tab press
            just goes back to the first widget on the page. Fix later.
        '''

        widg = evt.widget        
        if len(self.original) == 0 or len(widg.get()) != 0: 
            return
        widgname = widg.winfo_name()
        parent_type = ""
        message = "Clicking OK will unlink this person from the current person "
        "and relevant events (listed below). If your real goal is to delete "
        "the person from the tree, change the person's name, etc., first "
        "double-click the person to make them the current person."
        self.changing_values = {}
        if widgname in ("ma", "pa"):
            col = widg.grid_info()["column"]
            relative_type = "parent"
            if col == 1:
                parent_type = "ma"
            elif col == 3:
                parent_type = "pa"
        elif widgname.startswith("pard"):
            relative_type = "partner"
        else:
            relative_type = "child"
        self.unlinker = InputMessage(
            self.root, root=self.root, title="Confirm Unlink", ok_txt="OK", 
            cancel_txt="CANCEL", grab=True, head1=message, wraplength=650,
            head2=self.changing_values.items())
        if self.unlinker.ok_was_pressed: 
            self.show = self.unlinker.show()
            self.ok_unlink(relative_type, parent_type)

    def ok_unlink(self, relative_type, parent_type):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        birth_fpid = self.current_person_parents[0][0]
        if relative_type == "parent":
            print("line", looky(seeline()).lineno, "self.show:", self.show)
            print("line", looky(seeline()).lineno, "parent_type:", parent_type)
            print("line", looky(seeline()).lineno, "birth_fpid:", birth_fpid)
            print("line", looky(seeline()).lineno, "self.changing_values:", self.changing_values)
            # if self.show == 0:
                # cur.execute(self.query, (None, birth_fpid))
                # conn.commit()
            # elif self.show == 1:
                # if parent_type == "ma":
                    # parent_id = self.current_person_parents[1]["id"]
                # elif parent_type == "pa":
                    # parent_id = self.current_person_parents[2]["id"]
                # delete_person_from_tree(parent_id)

        elif relative_type == "partner":
            if self.show == 0:
                pass

            elif self.show == 1:
                pass

            elif self.show == 2:
                pass

        elif relative_type == "child":
            if self.show == 0:
                pass

            elif self.show == 1:
                pass

            elif shelf.show == 2:
                pass

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
# HOW TO GET THE RIGHT FPID???
            # print("line", looky(seeline()).lineno, "self.current_person_alt_parents:", self.current_person_alt_parents)
# line 1422 self.current_person_alt_parents: [[[139, 1097, ['guardian', 'guardian']], {'id': 5843, 'name': 'Raphael Fish', 'widget': <autofill.EntryAuto object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.altparent_l0>, 'label': <widgets.Label object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.!label3>}, {'id': None, 'name': None, 'widget': <autofill.EntryAuto object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.altparent_r0>, 'label': <widgets.Label object .!border.!main.!tabbook.!framehilited2.!frame.!frame.!frame.!nuclearfamiliestable.!canvas.!frame.!labelframe.!label4>}]]

            print("line", looky(seeline()).lineno, "self.current_person_alt_parents[row - 1][0][0]:", self.current_person_alt_parents[row - 1][0][0])
            fpid = self.current_person_alt_parents[row - 1][0][0]

            print("line", looky(seeline()).lineno, "col:", col)
            print("line", looky(seeline()).lineno, "new_id, fpid:", new_id, fpid)
# line 1455 names_ids: [('adoptive parent', 110), ('adoptive mother', 111), ('adoptive father', 112), ('foster parent', 120), ('foster mother', 121), ('foster father', 122), ('guardian', 130), ('legal guardian', 131)]
# line 1432 self.current_person_alt_parents[row - 1][0][0]: 139
# line 1435 col: 0
# line 1436 new_id, fpid: 112 139
            if col == 0:
                cur.execute(update_findings_persons_kintype1, (new_id, fpid))
            elif col == 2:
                cur.execute(update_findings_persons_kintype2, (new_id, fpid))                
            conn.commit()
            cancel_change()
            cur.close()
            conn.close()

        def cancel_change():
            frm.destroy()

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        # conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_kin_type_alt_parent)
        names_ids = cur.fetchall()
        print("line", looky(seeline()).lineno, "names_ids:", names_ids)
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
        


'''
    Two means of determining partnership are used. 1) a couple has 
    children together, or 2) a couple are linked by a common couple
    event such as marriage or divorce regardless of whether they
    have children together.

    Trying to provide the user with options for unlinking (from one
    or both persons involved, etc.) proved to be an ever-expanding bag of
    worms. Seems better to do a simple unlink and let the user do
    the work instead of giving the user unlink options that are wordy and 
    hard to understand, including
    the option to delete a person altogether, and
    then write hundreds of lines of tangled, unmaintainable code to make it possible for the
    program to do what the user should be carefully doing himself one
    piece at a time so he'll know how the change was made and when. The rest of this was written in an attempt to figure out what to do, and the answer turned out to be,
    "as little as possible"...

    (old:)
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

# dev docs: parents & alternate parents
'''
    The database for person_id 1's biological parents looks like this:
    select * from findings_persons where finding_id = 1;
    findings_persons_id|finding_id|age1|kin_type_id1|age2|kin_type_id2|persons_persons_id
    3|1|33|2|42|1|3
    select * from finding where finding_id = 1;
    finding_id|date|particulars|age|person_id|event_type_id|date_sorter
    1|-1884-ap-7-------||0|1|1|1884,4,7
    select * from persons_persons where persons_persons_id = 3;
    persons_persons_id|person_id1|person_id2
    3|2|3

    Treebard auto-creates an offspring event for each biological parent 
    based on the finding_id where event_type_id is 1 (birth event). Such
    auto-created events use the same finding_id as the child's birth event.

    Unlike birth, the terms "adoption" and "fosterage" refer to either parents (the fosterers) or 
    child (the one fostered), so a distinguishing word pair corresponding
    to birth/offspring (for child/parents) isn't necessary in English but would be desirable. It could be
    correct to say that these are events with up to three participants:
    a child and two parents. The event could be displayed as fosterage, adoption,
    or guardianship for all the parties involved. But this would be
    ambiguous because you'd have to guess based on age which is the child.
    So the right way is to use more contrived but less ambiguous terms in
    both the GUI and the code so everyone's role in the event can be 
    instantly understood.

    To keep the code symmetrical, the events adoption, guardianship, and 
    fosterage will be treated like birth, as the event experienced by
    the child. The more contrived terms will be used for the parents:
    "adopted a child, granted guardianship, fostered a child".

    Since it's possible for a person to be adopted or fostered by more
    than one guardian or couple, the functionality of the
    kintips will have to be expanded to show guardians when the user
    points at an adoption, fosterage, or guardianship. The kintips will
    name the child when the user points as the contrived events listed
    above. The kintips are in addition to the inclusion of the pertinent
    names in the immediate family table.

    In the case of a guardianship, there's no semantic distinction between the 
    male and female partner if the guardianship is granted to a couple, as there is with
    terminology like adoptive mother or foster father.
    If two guardians of the same child are
    partners, they'll be in the same record in the persons_persons db table, so they would be displayed together as parents in the nukes table.
    Otherwise, they'd be displayed on separate lines in both tables.

    The user will have the option of displaying adoptive parents, foster
    parents, and guardians with the roles feature. For example the user
    might choose to show adoptive parents who raised a child for many
    years as parents in the immediate family table, but show temporary
    foster parents in the roles dialog. The user has to be free to do it
    either way in any case, because an unofficial foster parent or a 
    legal guardian could raise a child from birth to majority, or for
    some substantial portion of his childhood, in which case the guardians
    should be displayed as parents. It has to be up to the user, but to
    show a pair of persons as parents, the parent system will have to be
    used, rather than the role system.
'''