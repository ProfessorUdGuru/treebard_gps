# families.py
import tkinter as tk
import sqlite3
from widgets import (
    Frame, LabelH3, Label, Button, Canvas, LabelEntry, Radiobutton, LabelFrame)
from files import get_current_file
from styles import make_formats_dict
from autofill import EntryAutoHilited, EntryAuto    
from scrolling import Scrollbar
from names import get_any_name_with_id, open_new_person_dialog
from dates import format_stored_date, get_date_formats, OK_MONTHS
from query_strings import (
    select_finding_id_birth, 
    update_findings_persons_by_id1, update_findings_persons_by_id2,
    update_findings_persons_by_id1_unlink, update_findings_persons_by_id2_unlink,
)
import dev_tools as dt
from dev_tools import looky, seeline



class NuclearFamiliesTable(Frame):
    def __init__(
            self, master, current_person, findings_table, right_panel, 
            person_autofill_values=[], *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.current_person = current_person
        self.person_autofill_values = person_autofill_values
        self.date_prefs = get_date_formats(tree_is_open=1)
        self.findings_table = findings_table
        self.right_panel = right_panel

        self.current_person_parents = [{},{}]
        self.newkinvar = tk.IntVar()

        self.make_widgets()

    def make_widgets(self):

        # nuke_table = Frame(persons_tab)
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
        new_kin_input = EntryAutoHilited(
            new_kin_frame, width=48, 
            autofill=True, 
            values=self.person_autofill_values)
        new_kin_input.grid(column=1, row=0)
        self.pardmaker = Button(
            new_kin_frame, 
            text="ADD PARTNER", width=12, 
            command=self.edit_partner)
        self.pardmaker.grid(column=2, row=0, padx=(6,0), pady=(12,0))
        self.childmaker = Button(
            new_kin_frame, 
            text="ADD CHILD", width=12, 
            command=self.edit_child)
        self.childmaker.grid(column=3, row=0, padx=(6,0), pady=(12,0))
        
    def edit_partner(self):
        print("howdy pardner")

    def edit_child(self):
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
            new_parent_id = final.split("#")[1]
        elif len(final) == 0:
            new_parent_id = None
            unlink = True
        else:
            new_parent_id = open_new_person_dialog(
                self, widg, self.root, self.treebard)
        return new_parent_id, unlink 

    def update_mother(self, final, conn, cur, widg):
        new_parent_id, unlink = self.edit_parent(final, widg)
        birth_id = self.current_person_parents[0][1]
        old_ma_id = self.current_person_parents[1]["id"]
        birth_fpid = self.current_person_parents[0][0]
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
        old_pa_id = self.current_person_parents[2]["id"]
        birth_fpid = self.current_person_parents[0][0]
        if self.birth_record[3] == 2:
            which = 1
        elif self.birth_record[5] == 2:
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
                    self, widg, self.root, self.treebard)
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
        s = 0
        for brood in self.brood_dicts:
            for k,v in brood.items():
                if widg != v[0]["widget"]:
                    continue
                for child in v[1]:
                    update_partners_child(
                        child["birth_fpid"], 
                        child["order"], 
                        v[0]["parent_type"], 
                        new_partner_id)
                break
            s += 1        

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
                print("line", looky(seeline()).lineno, "self.final:", self.final)
            elif col == 2:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
            elif col == 3:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
            elif col == 5:
                print("line", looky(seeline()).lineno, "self.final:", self.final)
            else:
                print("line", looky(seeline()).lineno, "case not handled:")    

        cur.close()
        conn.close()

    def make_nuke_inputs(self, current_person=None):
        self.nuke_inputs = []
        if current_person:
            self.current_person = current_person
        self.make_nuke_frames()
        self.make_nuke_dicts()
        self.populate_nuke_tables()
        self.bind_inputs()
        self.make_new_kin_inputs()
        self.update_idletasks()
        wd = self.nuke_window.winfo_reqwidth() + 12
        ht = self.right_panel.winfo_reqheight()
        # The +72 is a hack only needed when a broodless current person
        #   precedes a brooded one. Don't know what causes the new brooded
        #   person to get prior reqheight but this fixed it for now.
        self.nuke_canvas.config(width=wd, height=ht+72)        
        self.nuke_canvas.config(scrollregion=(0, 0, wd, ht+72))
        if len(self.brood_dicts) != 0:
            self.newkinvar.set(100)
        else:
            # set to non-existent value so no Radiobutton will be selected
            self.newkinvar.set(999)
        self.fix_buttons()

    def populate_nuke_tables(self):
        formats = make_formats_dict()
        lst = [
            self.current_person_parents[1]["name"], 
            self.current_person_parents[2]["name"]]
        for name in lst:
            if name == "name unknown":
                idx = lst.index(name)
                lst[idx] = ""
        self.ma_input.insert(0, lst[0])
        self.pa_input.insert(0, lst[1])
        self.pardrads = []
        n = 1

        for brood in self.brood_dicts:
            for k,v in brood.items():
                name, ma_pa, pard_id = (v[0]["partner_name"], v[0]["parent_type"], k)
            ma_pa = "Children's {}:".format(ma_pa)
            pard = "pard_{}_{}".format(pard_id, n)
            pardframe = Frame(self.nuke_window)
            pardframe.grid(column=0, row=n, sticky="ew")
            pardrad = Radiobutton(
                pardframe, variable=self.newkinvar, 
                value=n, anchor="w", command=self.fix_buttons)
            self.pardrads.append(pardrad)
            pardrad.grid(column=0, row=n)
            pardlab = LabelH3(pardframe, text=ma_pa, anchor="w")
            self.pardlabs.append(pardlab)
            pardlab.grid(column=1, row=n)
            pardent = EntryAuto(
                pardframe, width=48, autofill=True, 
                values=self.person_autofill_values, name=pard)
            pardent.insert(0, name)
            pardent.grid(column=2, row=n)
            v[0]["widget"] = pardent
            self.nuke_inputs.append(pardent)
            brood_frame = Frame(self.nuke_window)
            brood_frame.grid(column=0, row=n+1) 
            r = 0
            for dkt in v[1]:
                c = 0
                for i in range(6):
                    if c == 0:
                        spacer = Frame(brood_frame, width=48)
                        spacer.grid(column=c, row=r)
                    elif c == 1:
                        text = dkt["name"]
                        ent = EntryAuto(
                            brood_frame, width=0, autofill=True, 
                            values=self.person_autofill_values)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["name_widg"] = ent
                    elif c == 2:
                        text = dkt["gender"]
                        ent = EntryAuto(brood_frame, width=0)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["gender_widg"] = ent
                    elif c == 3:
                        text = dkt["birth"]
                        ent = EntryAuto(brood_frame, width=0)
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
                        lab = LabelEntry(brood_frame, text=text, anchor="w")
                        lab.grid(column=c, row=r, sticky="w")
                    elif c == 5:
                        text = dkt["death"]
                        ent = EntryAuto(brood_frame, width=0)
                        if len(text) > self.findings_table.kin_widths[c]:
                            self.findings_table.kin_widths[c] = len(text)
                        ent.insert(0, text)
                        ent.grid(column=c, row=r, sticky="w")
                        self.nuke_inputs.append(ent)
                        dkt["death_widg"] = ent 
                    c += 1
                r += 1
            top_row = brood_frame.grid_slaves(row=0)
            top_row.reverse()
            top_row_values = []
            for widg in top_row[1:]:
                if widg.winfo_class() == 'Entry':
                    top_row_values.append(widg.get())
                else:
                    top_row_values.append(widg.cget("text"))
            z = 1
            for widg in top_row[1:]:
                widg.config(width=self.findings_table.kin_widths[z] + 2)
                z += 1
            n += 2
        self.last_row = n

        # don't know why config_generic isn't enough here
        for widg in self.pardlabs:
            widg.config(font=formats["heading3"])

    def make_parents_dict(self):
        birth_fpid, birth_id = self.birth_record[0:2]
        parent1 = self.birth_record[2:4]
        parent2 = self.birth_record[4:]
        if parent1[1] == 1:
            ma_id = parent1[0]
            pa_id = parent2[0]
        elif parent1[1] == 2:
            ma_id = parent2[0]
            pa_id = parent1[0]
        self.current_person_parents.insert(0, (self.birth_record[0:2]))
        ma_name = get_any_name_with_id(ma_id)
        pa_name = get_any_name_with_id(pa_id)

        self.current_person_parents[1]["id"] = ma_id
        self.current_person_parents[2]["id"] = pa_id
        self.current_person_parents[1]["name"] = ma_name
        self.current_person_parents[2]["name"] = pa_name
        self.current_person_parents[1]["widget"] = self.ma_input
        self.current_person_parents[2]["widget"] = self.pa_input

    def make_nuke_dicts(self):
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
            self.birth_record = cur.fetchall()[0]
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
        self.brood_dicts = []
        births = [tup for q in (result1, result2) for tup in q]

        broods = []
        for tup in births:
            if tup[2] != self.current_person:
                if tup[2] not in broods:
                    broods.append(tup[2])
            elif tup[4] != self.current_person:
                if tup[4] not in broods:
                    broods.append(tup[4])

        for pard_id in broods:
            brood = {pard_id: [{}, []]}
            self.brood_dicts.append(brood)

        m = 0
        for pardner in broods:
            for tup in births:
                order = "{}-{}".format(str(tup[3]), str(tup[5]))                
                if tup[4] == pardner:
                    parent_type = tup[5]
                    pard_id = tup[4]
                    self.make_pard_dict(pard_id, parent_type, m)
                    if pard_id == pardner:
                        self.brood_dicts[m][pardner][1].append(
                            {"birth_fpid": tup[0], 
                                "birth_id": tup[1], "order": order})
                elif tup[2] == pardner:
                    parent_type = tup[3]
                    pard_id = tup[2]
                    self.make_pard_dict(pard_id, parent_type, m) 
                    if pard_id == pardner:
                        self.brood_dicts[m][pardner][1].append(
                            {"birth_fpid": tup[0], 
                                "birth_id": tup[1], "order": order})
            m += 1

        for pard_id in broods:
            for brood in self.brood_dicts:
                for k,v in brood.items():
                    if k == pard_id:
                        for dkt in v[1]:
                            self.finish_brood_dict(dkt, cur) 

        for brood in self.brood_dicts:
            brood_values = list(brood.values())
            brood_values[0][1] = sorted(brood_values[0][1], key=lambda i: i["sorter"])

        compare = []
        for brood in self.brood_dicts:
            for k,v in brood.items():
                compare.append((k, v[1][0]["sorter"]))
            compare = sorted(compare, key=lambda j: j[1])

        copy = []
        for tup in compare:
            key = tup[0]
            for brood in self.brood_dicts:
                if brood.get(key) is None:
                    continue
                else:
                    copy.append(brood) 
        self.brood_dicts = copy

        # instead of trying to sort this above, maybe better to insert this into the sorted list of dicts when it's done NO THE RIGHT WAY IS TO add spouses to the dict as keys as a first step so they're treated like everything else, since it will be necessary to detect marital events for brooded/non-brooded partners equally

        spouses = self.collect_couple_events(cur)

        cur.close()
        conn.close()

    def collect_couple_events(self, cur):
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

            Couple events are determined by a boolean in the events_type 
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
            not necessary to create a bogus spouse in order to identify the
            parents in a nuclear family.
        ''' 
        cur.execute(
            '''
                SELECT event_type_id 
                FROM event_type
                WHERE marital = 1
            ''')

        marital_event_types = [i[0] for i in cur.fetchall()]
        qlen = len(marital_event_types)
        marital_event_types.insert(0, self.current_person)
        marital_event_types.insert(0, self.current_person)
        
        sql = '''
                SELECT findings_persons_id, person_id1, kin_type_id1, person_id2, kin_type_id2, date
                FROM findings_persons
                JOIN finding
                    ON finding.finding_id = findings_persons.finding_id
                WHERE (person_id1 = ? OR person_id2 = ?) 
                    AND event_type_id in ({})
            '''.format(",".join(["?"] * qlen))
        cur.execute(sql, marital_event_types)
        copy = [list(i) for i in cur.fetchall()]

        spouses = copy
        print("line", looky(seeline()).lineno, "spouses:", spouses)
# line 1086 copy: [[69, 632, 12, 8, 5599, 7, 'abt-1910-au-15-ad------'], [72, 646, 6, 7, 12, 8, '-1905---------'], [73, 649, 6, 7, 12, 8, '-1905---------']]

        o = 0
        for lst in spouses:
            if lst[1] == self.current_person:
                del lst[1:3]
            elif lst[3] == self.current_person:
                del lst[3:5]
            o += 1
        print("line", looky(seeline()).lineno, "spouses:", spouses)
        for lst in spouses:
            self.save_marital_events(lst, cur)

        # remove partners who have children
        g = 0
        for brood in self.brood_dicts:
            x = list(brood.keys())
            key = x[0]
            for lst in spouses:
                if key in lst:
                    del copy[g]
            g += 1
        # remove duplicates due to multiple marital events w/ same partner
        #    what's left is a list of unique partners to add (childless)
        childless_partners = []
        for lst in copy:
            if lst[1] not in childless_partners:
                childless_partners.append(lst[1])        
        print("line", looky(seeline()).lineno, "childless_partners:", childless_partners)
# line 1082 copy: [[69, 632, 12, 8, 5599, 7, 'abt-1910-au-15-ad------'], [72, 646, 6, 7, 12, 8, '-1905---------'], [73, 649, 6, 7, 12, 8, '-1905---------']]
# line 1113 childless_partners: [6]
# line 1117 copy: [[72, 646, 6, 7, '-1905---------'], [73, 649, 6, 7, '-1905---------']] 
# add to parents dict: marital_pfid, marital_finding_id,, marital_event_type, marital_finding_date, partner_kin_type SO THAT when a partner is edited/deleted, the change can be propagated to all marital events for that couple

                       
        # print("line", looky(seeline()).lineno, "self.brood_dicts:", self.brood_dicts)                        
        return spouses
 


# line 991 self.brood_dicts: [{5635: [{'parent_type': 'Mother', 'partner_name': 'Harmony Maryland Hobgood (stage name)'}, [{'birth_fpid': 93, 'birth_id': 668, 'order': '2-1', 'gender': 'male', 'birth': '1920', 'sorter': [1920, 0, 0], 'death': '', 'name': 'Ross Aldo Marquis (stage name)', 'id': 5783}]]}, {5599: [{'parent_type': 'Mother', 'partner_name': 'Selina Savoy'}, [{'birth_fpid': 95, 'birth_id': 670, 'order': '1-2', 'gender': 'unknown', 'birth': 'Aug 1, 1915', 'sorter': [1915, 8, 1], 'death': '', 'name': 'Albertha Siu Sobel', 'id': 5711}, {'birth_fpid': 97, 'birth_id': 672, 'order': '2-1', 'gender': 'male', 'birth': 'Apr 14, 1921', 'sorter': [1921, 4, 14], 'death': 'June 29, 1961', 'name': 'Clarence Bracken', 'id': 5677}, {'birth_fpid': 94, 'birth_id': 669, 'order': '2-1', 'gender': 'female', 'birth': 'Jan 18, 1922', 'sorter': [1922, 1, 18], 'death': '', 'name': 'Moira Harding', 'id': 5740}, {'birth_fpid': 98, 'birth_id': 673, 'order': '2-1', 'gender': 'male', 'birth': 'Aug 6, 1927', 'sorter': [1927, 8, 6], 'death': '', 'name': 'Noe Whitton', 'id': 5685}, {'birth_fpid': 96, 'birth_id': 671, 'order': '2-1', 'gender': 'male', 'birth': 'Sep 30, 1929', 'sorter': [1929, 9, 30], 'death': '', 'name': "Joe-John O'Keefe", 'id': 5732}]]}]

    def save_marital_events(self, lst, cur):
        print("line", looky(seeline()).lineno, "lst:", lst)
# line 1129 lst: [69, 5599, 7, 'abt-1910-au-15-ad------']
# line 1129 lst: [72, 6, 7, '-1905---------']
# line 1129 lst: [73, 6, 7, '-1905---------']
        partner_id = lst[1]
        print("line", looky(seeline()).lineno, "partner_id:", partner_id)
        # FIRST ADD MISSING (CHILDLESS) PARTNERS TO MAIN DICT HERE
        for brood in self.brood_dicts:
            for k,v in brood.items():
                print("line", looky(seeline()).lineno, "k:", k)
                if partner_id == k:

                    cur.execute(
                        '''
                            SELECT kin_types
                            FROM kin_type
                            WHERE kin_type_id = ?
                        ''',
                        (lst[2],))
                    kin_type = cur.fetchone()[0]


                    v[0]["partner_kin_type"] = kin_type
                    print("line", looky(seeline()).lineno, "kin_type:", kin_type)

        print("line", looky(seeline()).lineno, "self.brood_dicts:", self.brood_dicts          )
        # NEXT ADD MARITAL EVENT DICTS WITH marital_event_pfid & marital_event_date

    def make_pard_dict(self, pard_id, parent_type, m):
        if parent_type == 1:
            parent_type = "Mother"
        elif parent_type == 2:
            parent_type = "Father"
        partner_name = get_any_name_with_id(pard_id)
        self.brood_dicts[m][pard_id][0]["parent_type"] = parent_type
        self.brood_dicts[m][pard_id][0]["partner_name"] = partner_name   

    def finish_brood_dict(self, dkt, cur):   
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

        sorter = [0,0,0]
        if birth_date != "-0000-00-00-------":
            sorter = birth_date.split("-")[1:4] 
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