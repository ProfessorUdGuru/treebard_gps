# events_table

import tkinter as tk
import sqlite3
from files import current_file
from window_border import Border 
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, Radiobutton,
    KinTip, LabelH3, Button, Entry, MessageHilited, EntryHilited1)
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from nested_place_strings import make_all_nestings
from toykinter_widgets import Separator
from styles import make_formats_dict, config_generic
from names import get_name_with_id, make_values_list_for_person_select
from roles import RolesDialog
from notes import NotesDialog
from places import place_strings, ValidatePlace, places_places
from scrolling import Scrollbar, resize_scrolled_content
from error_messages import open_error_message, event_table_err
from query_strings import (
    select_finding_places_nesting, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_type_ids_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple_age, select_findings_details_couple_generic,
    select_finding_id_birth, select_person_id_kin_types_birth,
    select_finding_ids_age_parents, select_person_id_birth,
    select_findings_details_offspring, select_all_findings_roles_ids, 
    select_finding_ids_offspring, select_all_findings_notes_ids,
    select_count_finding_id_sources, select_nesting_fk_finding,
    select_nestings_and_ids, select_place, update_finding_particulars,
    update_finding_age, update_current_person, select_all_place_ids,
    select_all_event_types, select_event_type_id, insert_finding_new,
    insert_finding_new_couple, insert_findings_persons_new_couple,
    select_all_kin_types_couple, select_all_names_ids, insert_finding_places_new,
    select_max_persons_persons_id, insert_persons_persons_new,
    select_kin_type_string, update_findings_persons_couple_age,
    select_event_type_couple, insert_kin_type_new,
    update_kin_type_kin_code, select_max_finding_id, insert_place_new,
    insert_places_places_new, insert_finding_places_new_event,
    insert_event_type_new, select_max_event_type_id)

import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

FINDING_TABLE_HEADS = (
    'Event', 'Date', 'Place', 'Particulars', 'Age', 
    'Kin', 'Roles', 'Notes', 'Sources')

def get_current_person():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person_id)
    current_person = cur.fetchone()[0]
    cur.close()
    conn.close()
    return current_person

def update_particulars(input_string, finding):
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
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_event_types)
    event_types = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return event_types

def get_findings():
    current_person = get_current_person()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    # get couple event types and couple kin types
    cur.execute(select_all_event_types_couple)
    couple_event_types = cur.fetchall()
    couple_event_types = [i[0] for i in couple_event_types]

    cur.execute(select_all_kin_type_ids_couple)
    couple_kin_type_ids = [i[0] for i in cur.fetchall()]

    # get generic events
    generic_findings = []
    cur.execute(select_all_findings_current_person, (current_person,))
    generic_finding_ids = cur.fetchall()
    generic_finding_ids = [i[0] for i in generic_finding_ids]

    for finding_id in generic_finding_ids: 
        cur.execute(select_findings_details_generic, (finding_id,))

        generic_finding_details = cur.fetchone()
        generic_finding_details = list(generic_finding_details) 

        cur.execute(select_finding_places_nesting, (finding_id,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        generic_finding_details.insert(3, place_string)
        generic_finding_details[1] = generic_finding_details[1:3]

        del generic_finding_details[2]
        generic_finding_details.insert(0, finding_id)
        generic_findings.extend([generic_finding_details])

    for lst in generic_findings:
        if lst[3] == 'unknown':
            lst[3] = ''

    couple_age_spouse = []
    generic_couple_findings = []

    sql =   '''
                SELECT finding_id, persons_persons_id 
                FROM findings_persons 
                WHERE person_id = (SELECT person_id FROM current WHERE current_id = 1)
                    AND kin_type_id in ({}) 
            '''.format(
                ','.join('?' * len(couple_kin_type_ids)))
    cur.execute(sql, couple_kin_type_ids)

    finding_ids_persons_persons_ids = cur.fetchall()
   
    for event in finding_ids_persons_persons_ids:
        cur.execute(select_findings_details_couple_age, event)
        got = cur.fetchall()
        finding_id = event[0]
        for tup in got:
            if len(got) == 2:
                couple_finding_details = [finding_id, got[0], got[1]]
            elif len(got) == 1:
                couple_finding_details = [finding_id, got[0], (None, '')]
        couple_age_spouse.append(couple_finding_details)       
        cur.execute(select_findings_details_couple_generic, (finding_id,))
        couple_generic_details = cur.fetchall()
        couple_generic_details = [list(i) for i in couple_generic_details]
        couple_generic_details[0].insert(0, finding_id)
        cur.execute(select_finding_places_nesting, (finding_id,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        couple_generic_details[0][4] = place_string
        generic_couple_findings.extend(couple_generic_details)

    for item in generic_couple_findings:
        if item[4] == 'unknown':
            item[4] = ''

    # get birth events
    cur.execute(select_finding_id_birth, (current_person,))
    birth_id = cur.fetchone()
    parents = (None, None)
    if birth_id:
        birth_id = birth_id[0]
        cur.execute(select_person_id_kin_types_birth, (birth_id,))
        parents = cur.fetchall()
        parents.insert(0, birth_id)

    cur.execute(select_finding_ids_age_parents, (current_person,))
    children = cur.fetchall()
    children = [list(i) for i in children]
    for lst in children:
        finding_id = lst[0]

        cur.execute(select_person_id_birth, (finding_id,))
        offspring = cur.fetchone()
        if offspring:
            lst.insert(2, offspring[0])

    kids = []
    for lst in children:
        child_id = lst[2]
        
        cur.execute(select_findings_details_offspring, (child_id,))
        offspring_details = list(cur.fetchall()[0])

        cur.execute(select_finding_places_nesting, (finding_id,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        offspring_details[2] = place_string
        if offspring_details[2] == 'unknown':
            offspring_details[2] = ''

        name = get_name_with_id(child_id)
        new_list = [lst[0], lst[1], [name, child_id, 'child']] 
        new_list.insert(1, 'offspring')
        new_list.insert(2, [offspring_details[0], offspring_details[1]])
        new_list.insert(3, offspring_details[2])
        new_list.insert(4, offspring_details[3])
        kids.append(new_list) 

    finding_ids = []

    for lst in generic_findings:
        if lst[0] not in finding_ids:
            finding_ids.append(lst[0])
    for lst in generic_couple_findings:
        if lst[0] not in finding_ids:
            finding_ids.append(lst[0])
    for lst in children:
        if lst[0] not in finding_ids:
            finding_ids.append(lst[0])

    couple_findings = []
    for finding in generic_couple_findings:
        for spouse_age in couple_age_spouse:
            if finding[0] == spouse_age[0]:
                for spouse in spouse_age[1:]:
                    if spouse[0] == current_person:
                        finding.append(spouse[1])
                for spouse in spouse_age[1:]:
                    if spouse[0] != current_person:
                        spouse_id = spouse[0]
                        name = get_name_with_id(spouse_id)
                        kin_type = spouse[2]
                        finding.append([name, spouse_id, kin_type])
        finding[2] = finding[2:4]
        del finding[3]
        couple_findings.append(finding)

    couple_finding_ids = [i[0] for i in finding_ids_persons_persons_ids]
    all_finding_ids = generic_finding_ids + couple_finding_ids

    cur.execute(select_all_findings_roles_ids)

    non_empty_roles = cur.fetchall()
    non_empty_roles = [i[0] for i in non_empty_roles]

    current_roles = []
    for role_id in all_finding_ids:
        if role_id in non_empty_roles:
            current_roles.append(role_id)
    cur.execute(select_finding_ids_offspring, (current_person,))
    offspring_events = cur.fetchone()

    if offspring_events:
        offspring_roles = []
        for finding_id in offspring_events:
            if finding_id in non_empty_roles:
                offspring_roles.append(finding_id)
        current_roles.extend(offspring_roles)
    non_empty_roles = current_roles

    cur.execute(select_all_findings_notes_ids)

    non_empty_notes = cur.fetchall()
    non_empty_notes = [i[0] for i in non_empty_notes]

    current_notes = []
    for note_id in all_finding_ids:
        if note_id in non_empty_notes:
            current_notes.append(note_id)
    cur.execute(select_finding_ids_offspring, (current_person,))
    offspring_events = cur.fetchone()

    if offspring_events:
        offspring_notes = []
        for finding_id in offspring_events:
            if finding_id in non_empty_notes:
                offspring_notes.append(finding_id)
        current_notes.extend(offspring_notes)
    non_empty_notes = current_notes

    source_count = []
    for finding_id in finding_ids:
        cur.execute(select_count_finding_id_sources, (finding_id,))
        src_count = cur.fetchone()
        source_count.append((finding_id, src_count[0]))

    cur.close()
    conn.close()    

    return (
        generic_findings,
        couple_findings, 
        parents, 
        kids,
        finding_ids,
        non_empty_roles,
        non_empty_notes,
        source_count)

class EventsTable(Frame):
    def __init__(self, master, root, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.treebard = treebard

        self.current_person = get_current_person()

        self.inwidg = None
        self.headers = []
        self.widths = [[], [], [], [], []]
        self.kintips = []
        self.kin_buttons = []

        self.screen_height = self.winfo_screenheight()
        self.column_width_indecrement = 0
        self.new_row = 0

        event_types = get_all_event_types()
        self.event_types = EntryAuto.create_lists(event_types)

        self.root.bind(
            "<Control-S>", 
            lambda evt, curr_per=self.current_person: self.go_to(
                evt, current_person=curr_per))
        self.root.bind(
            "<Control-s>", 
            lambda evt, curr_per=self.current_person: self.go_to(
                evt, current_person=curr_per))

        self.make_header()
        self.make_table_cells()

    def size_columns_to_content(self):
        '''
            Get length of each cell in the column and size the top row cells to 
            fit the longest content in the column. The whole column will follow
            this size. The method make_table_cells() has some influence in this
            sizing process because column 0 (Event) sets itself to Tkinter's default
            width=20 if you don't tell it not to and column 4 (Age) should be 
            smaller than the others. Any of this could be improved, especially
            if Tkinter would let us detect and set Labels and Entries to their
            required width but they use different default characters so even
            setting them to the same width doesn't work. One workaround might
            be to have a button in the Preferences > Fonts tab or someplace which
            increases or decreases the column width and redraws the table. Not
            desirable, but I'm trying to avoid manually resizable columns since
            I believe with religious fervor that they are inexcusable and I'm
            waiting to be proven wrong. Thus for future reference: 
            self.column_width_indecrement. If this works out, the button might
            want to be on the Fonts tab since the setting would most often have to
            be changed when redrawing the table in different fonts. Another thing to
            consider is making the input and output fonts the same font family to
            see if that helps.
        '''

        self.header_widths = []
        for lst in self.widths:
            self.header_widths.append(max(lst))
        for row in self.cell_pool:
            c = 0
            for ent in row[1][0:5]:
                if ent.winfo_class() == 'Entry':
                    if ent.winfo_subclass() == 'EntryAuto':
                        if len(ent.grid_info()) != 0:
                            if ent.grid_info()['row'] == 2:
                                ent.config(
                                    width=self.header_widths[c] + self.column_width_indecrement)
                                c += 1      

    def get_initial(self, evt):
        self.initial = evt.widget.get()
        self.inwidg = evt.widget

    def get_final(self, evt):
        widg = evt.widget
        final = widg.get()
        if final != self.initial:
            self.final = final
            for row in self.findings:
                c = 0
                for col in row[0:-1]:
                    if col[0] == widg:
                        self.finding = row[9]
                        col_num = c
                    c += 1
        
            self.update_db(widg, col_num)

    def update_db(self, widg, col_num):

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

        def update_age():
            if couple is False:
                cur.execute(update_finding_age, (self.final, self.finding))
                conn.commit() 
            else:
                cur.execute(
                update_findings_persons_couple_age, 
                (self.final, self.finding, self.current_person))
                conn.commit()

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        if col_num == 0:
            pass
        elif col_num == 1:
            pass
        elif col_num == 2:
            update_place()
        elif col_num == 3:
            update_particulars(self.final, self.finding)
        elif col_num == 4:
            couple = False
            for row in self.findings:
                if row[9] == self.finding: 
                    event_string = row[0][1]
                    cur.execute(select_event_type_couple, (event_string,))
                    couple_or_not = cur.fetchone()[0]
                    if couple_or_not == 1:
                        couple = True
                    else: couple = False
                    break
            update_age()            

        cur.close()
        conn.close()

    def make_table_cells(self, qty=1998):
        '''
            EntryAuto was used for all the text columns to keep the code 
            symmetrical for all the text columns, with autofill defaulting to 
            False except for the places column.
        '''
        self.place_autofill_values = EntryAuto.create_lists(place_strings)
        self.table_cells = []
        for i in range(int(qty/9)): # 222
            row = []
            for j in range(9):
                if j < 5:
                    if j == 2:
                        cell = EntryAuto(
                            self, 
                            autofill=True, 
                            values=self.place_autofill_values)
                    else:                        
                        cell = EntryAuto(self)
                    cell.initial = ''
                    cell.final = ''
                    cell.finding = None
                    cell.bind('<FocusIn>', self.get_initial, add="+")
                    cell.bind('<FocusOut>', self.get_final, add="+")
                    if j == 0:
                        cell.config(width=1)
                    elif j == 4:
                        cell.config(width=5)
                elif j == 5:
                    cell = Frame(self, bd=0, highlightthickness=0)
                elif j == 6:
                    cell = LabelDots(self, current_file, RolesDialog)
                elif j == 7:
                    cell = LabelDots(self, current_file, NotesDialog)
                elif j == 8:
                    cell = LabelButtonText(
                        self,
                        width=6,
                        anchor='w',
                        font=formats['heading3'])
                row.append(cell)
            self.table_cells.append(row)
        
        self.event_input = EntryAutoHilited(
            self, autofill=True, values=self.event_types)
        self.add_event_button = Button(
            self, text="NEW EVENT", command=self.make_new_event)
        self.set_cell_content()

    def set_cell_content(self):

        findings_data = get_findings()

        generic_findings = findings_data[0]
        couple_findings = findings_data[1]
        parents = findings_data[2]
        children = findings_data[3]
        finding_ids = findings_data[4]
        non_empty_roles = findings_data[5]
        non_empty_notes = findings_data[6]
        source_count = findings_data[7]

        self.cell_pool = []

        i = 0
        for row in self.table_cells[0:len(finding_ids)]:
            self.cell_pool.append([finding_ids[i], row])
            i += 1
        self.findings = []
        for finding_id in finding_ids:
            c = 0
            for row in self.cell_pool:
                if row[0] == finding_id:
                    right_cells = row[1]
                    c += 1
                    for final_list in (couple_findings, generic_findings, children):
                        for lst in final_list:
                            if finding_id == lst[0]:
                                right_row = lst[1:]
                                couple_or_no = len(right_row)
                                if couple_or_no == 5:
                                    right_row.extend([[], '     ', '     ', []])
                                elif couple_or_no == 6:
                                    right_row.extend(['     ', '     ', []])
                                row_list = [list(i) for i in zip(right_cells, right_row)]
                                row_list.append(finding_id)
                                self.findings.append(row_list)

        ma = None
        pa = None
        for row in self.findings:
            if row[0][1] == 'birth':
                finding_id = row[9]
                break
        for row in self.findings:
            if row[9] == finding_id:            
                for item in parents:
                    if item == finding_id:
                        for parent in parents[1:]:
                            if parent[1] == 'mother':
                                ma = parent
                            elif parent[1] == 'father':
                                pa = parent
                    continue
                if ma:
                    ma = [get_name_with_id(ma[0]), ma[0], ma[1]]
                    row[5][1].append(ma)
                if pa:
                    pa = [get_name_with_id(pa[0]), pa[0], pa[1]]
                    row[5][1].append(pa)

        for row in self.findings:
            widg = row[6][0]
            finding_id = row[9]
            widg.finding_id = finding_id
            if row[9] in non_empty_roles:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]
                row[6][1] = ' ... '
            else:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]

        for row in self.findings:
            widg = row[7][0]
            finding_id = row[9]
            widg.finding_id = finding_id
            if row[9] in non_empty_notes:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]
                row[7][1] = ' ... '
            else:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]

        for row in self.findings:
            for src in source_count:
                if row[9] == src[0]:
                    row[8][1] = src

        # sort by date
        for row in self.findings:
            event_type = row[0][1]
            if event_type == 'birth':
                row[1][1][1] = '-10000,0,0'
            elif event_type == 'death':
                row[1][1][1] = '10000,0,0'
            elif event_type == 'burial':
                row[1][1][1] = '10001,0,0'

        for row in self.findings:
            sorter = row[1][1][1]
            sorter = sorter.split(',')
            sorter = [int(i) for i in sorter]
            row[1][1][1] = sorter
           
        self.findings = sorted(self.findings, key=lambda i: i[1][1][1])

        self.show_table_cells()

    def show_table_cells(self):
        r = 2
        for row in self.findings:
            event_type = row[0][1]
            c = 0
            for col in row[0:9]:
                cellval = col[1]
                widg = col[0]
                if c == 1:
                    text = cellval[0]
                elif c in (0, 2, 3, 4):
                    text = cellval
                elif c == 5: # kin
                    kinframe = row[c][0]
                    self.make_kin_button(event_type, cellval, kinframe)
                elif c == 6: # roles
                    widg.config(text=col[1])
                elif c == 7: # notes
                    widg.config(text=col[1])
                elif c == 8: # sources
                    widg.config(text=row[8][1][1], width=8)
                if c in (6, 7, 8):
                    widg.grid(column=c, row=r, sticky='w', pady=(3,0), padx=(2,0))
                else:
                    widg.grid(column=c, row=r, sticky='ew', pady=(3,0))
                if c < 5:
                    widg.insert(0, text)
                    self.widths[c].append(len(text))
                c += 1
            r += 1

        self.fix_tab_traversal()
        for row_num in range(self.grid_size()[1]):
            self.grid_rowconfigure(row_num, weight=0)
        self.new_row = row_num + 1
        
        self.size_columns_to_content()

        self.event_input.grid(column=0, row=self.new_row, pady=6)
        self.add_event_button.grid(column=1, row=self.new_row, pady=6)

    def make_kin_button(self, event_type, cellval, kinframe):
        ma_pa = False
        if event_type == 'birth':
            ma_pa = True                    
        if len(cellval) == 0:
            text = ""
        else:
            kin = cellval
            if kin:
                if ma_pa is False:
                    text = kin[2]
                else:
                    text = 'parents'
            kinlab = LabelButtonText(
                kinframe,
                text=text,
                anchor='w',
                font=formats['heading3'])
            kinlab.grid(column=0, row=0)
            kinlab.bind(
                '<Button-1>', 
                lambda evt, kin=kin: self.open_kin_tip(evt, kin))
            self.kin_buttons.append(kinlab)
            kinframe.grid()

    def open_kin_tip(self, evt, kin):

        def make_kin_tip(lst):
            self.instrux = KinTip(
                self.kin_tip, 
                text="{} (id #{})".format(lst[0], lst[1]))
            self.instrux.grid(sticky="news")
            self.instrux.instrux2.bind('<Button-1>', self.go_to)

        def highlight(event):
            event.widget.config(bg=formats["head_bg"])

        def unhighlight(event):
            event.widget.config(bg=formats["bg"])

        if evt.widget.winfo_rooty() < 96:
            y_offset = 32
        else:
            y_offset = -84

        self.kin_tip = Toplevel(self)
        x, y, cx, cy = evt.widget.bbox("insert")
        x = x + evt.widget.winfo_rootx() + y_offset
        y = y + cy + evt.widget.winfo_rooty() + y_offset
        self.kin_tip.wm_geometry('+{}+{}'.format(x, y))
        self.kin_tip.wm_overrideredirect(1)
        self.kintips.append(self.kin_tip)

        # spouse or child
        if len(kin) == 3:
            make_kin_tip(kin)
        # parents
        else:
            for lst in kin:
                make_kin_tip(lst)

        ex = LabelButtonText(
            self.instrux, 
            text="x", 
            width=2,
            font=("arial black", 3))
        ex.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
        ex.bind('<Button-1>', self.destroy_kintip)
        ex.bind('<Control-Button-1>', self.destroy_all_kintips)
        ex.bind('<Enter>', highlight)
        ex.bind('<Leave>', unhighlight)

    def destroy_kintip(self, evt=None):
        if evt:
            tip = evt.widget.master.master
            idx = self.kintips.index(tip)
            del self.kintips[idx]
            tip.destroy()
        for widg in self.kintips:
            widg.lift()

    def destroy_all_kintips(self, evt=None):
        for widg in self.kintips:
            widg.destroy()
        self.kintips = []

    def go_to(self, evt=None, current_person=None):
        if evt and evt.type == "4":
            text = evt.widget.cget("text")
            person_id = text.split("#")[1]
            self.instrux.person_id = int(person_id.rstrip(")"))
            self.current_person = self.instrux.person_id
        else:
            self.current_person = current_person

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_person, (self.current_person,))
        conn.commit()
        cur.close()
        conn.close()
        self.forget_cells()
        self.new_row = 0 
        self.set_cell_content()

    def forget_cells(self):
        self.update_idletasks()
        for lst in self.cell_pool:
            for widg in lst[1]:
                if widg.winfo_subclass() == 'EntryAuto':
                    widg.delete(0, 'end')
                elif widg.winfo_subclass() == 'Frame':
                    self.destroy_all_kintips()
                    for button in self.kin_buttons:
                        button.destroy()
                elif widg.winfo_subclass() == 'LabelButtonText':
                    widg.config(text='')
                widg.grid_forget()
        self.event_input.grid_forget()
        self.add_event_button.grid_forget()

    def make_header(self):
        
        y = 0
        for heading in FINDING_TABLE_HEADS:
            head = LabelH3(self, text=heading, anchor='w')
            head.grid(column=y, row=0, sticky='ew')
            if y in (6, 7, 8):
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

    def make_new_event(self):
        new_event = self.event_input.get().strip()
        self.new_event_dialog = NewEventDialog(
            self.root, 
            self.treebard,
            self,
            new_event,
            self.current_person,
            self.place_autofill_values,   
            self.go_to)
        self.event_input.delete(0, 'end')

class NewEventDialog(Toplevel):
    def __init__(
            self, master, treebard, events_table,
            new_event, 
            current_person, place_autofill_values, 
            go_to, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.root = master
        self.treebard = treebard
        self.events_table = events_table
        self.new_event = new_event
        self.current_person = current_person
        self.place_autofill_values = place_autofill_values
        self.go_to = go_to

        self.new_event_type = False

        self.new_kin_type_codes = [None, None]

        self.current_name = get_name_with_id(self.current_person)
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        people = make_values_list_for_person_select()        
        self.all_birth_names = EntryAuto.create_lists(people)

        cur.execute(select_all_kin_types_couple)
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

    def input_new_event_type(self):

        def ok_new_evt_type():
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            couple_event = couplevar.get()
            cur.execute(insert_event_type_new, (
                self.event_type_id, self.new_event, couple_event))
            conn.commit()

            event_types = get_all_event_types()
            more_event_types = EntryAuto.create_lists(event_types)
            self.events_table.event_input.values = more_event_types

            self.couple_event = couple_event
            cancel_new_evt_type()
            cur.close()
            conn.close()

        def cancel_new_evt_type():
            id_couple_event.grab_release()
            id_couple_event.destroy()
            self.deiconify()
            self.focus_set()    
            self.lift()
            self.grab_set()

        text = ( 
            "Generic event type: one primary participant or a parent, e.g. "
                "'Birth', 'Career', 'Adopted a child'.",
            "Couple event type: two equal participants, e.g. 'Husband', "
                "'Wife', 'Spouse'.")
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
            command=ok_new_evt_type)
        butt2 = Button(
            buttonframe, text="CANCEL", width=6, 
            command=cancel_new_evt_type)

        lab.grid(column=0, row=0, pady=12)
        buttonframe.grid(column=0, row=3, sticky='e', pady=(0,12))
        butt1.grid(column=0, row=0, sticky='e', padx=12, pady=6)
        butt2.grid(column=1, row=0, sticky='e', padx=12, pady=6)
        butt1.focus_set()
        
        self.wait_window(id_couple_event)
        self.make_widgets()

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
        canvas = Border(self, size=3) # don't hard-code size            
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
        # DO NOT DELETE THESE LINES, UNCOMMENT IN REAL APP
        # self.treebard.scroll_mouse.append_to_list([canvas, window])
        # self.treebard.scroll_mouse.configure_mousewheel_scrolling()

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
        date_input = EntryHilited1(self.generic_data_inputs)
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
        date_input.grid(column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        lab2.grid(column=0, row=2, sticky="e", pady=(0,1))
        self.place_input.grid(
            column=1, row=2, sticky="w", padx=(3,0), pady=(0,1))
        lab3.grid(column=0, row=3, sticky="e")
        self.particulars_input.grid(column=1, row=3, sticky="w", padx=(3,0))
        if self.couple_event == 0:
            self.b1.config(command=self.add_event)
            self.show_one_person()
        elif self.couple_event == 1:
            self.b1.config(command=self.validate_kin_types)
            self.show_other_person()

        date_input.focus_set()

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
        self.new_evt_msg.config(text="Information about the new event "
            "relating to the current person and the other person in the event.")
        sep1 = Separator(self.frm, width=3)
        sep2 = Separator(self.frm, width=3)
        sep1.grid(column=0, row=1, columnspan=2, sticky="ew", pady=(12,0))
        sep2.grid(column=0, row=3, columnspan=2, sticky="ew", pady=(12,0))

        name1 = Label(self.couple_data_inputs, text=self.current_name)
        age1 = Label(self.couple_data_inputs, text="Age")
        self.age1_input = EntryHilited1(self.couple_data_inputs, width=6)
        kintype1 = Label(self.couple_data_inputs, text="Kin Type")
        self.kin_type_input1 = Combobox(
            self.couple_data_inputs, self.root, values=self.kin_types)

        spacer = Frame(self.couple_data_inputs)

        name2 = Label(self.couple_data_inputs, text="Partner")
        self.other_person_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, autofill=True, values=self.all_birth_names)
        self.other_person_input.bind("<FocusOut>", self.catch_dupe_partner)
        age2 = Label(self.couple_data_inputs, text="Age")
        self.age2_input = EntryHilited1(self.couple_data_inputs, width=6)
        kintype2 = Label(self.couple_data_inputs, text="Kin Type")
        self.kin_type_input2 = Combobox(
            self.couple_data_inputs, self.root, values=self.kin_types)

        name1.grid(column=0, row=0, sticky="w", columnspan=2, pady=(9,1))
        age1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.age1_input.grid(column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        kintype1.grid(column=0, row=2, sticky="e")
        self.kin_type_input1.grid(column=1, row=2, sticky="w", padx=(2,0))

        self.couple_data_inputs.columnconfigure(2, weight=1)
        spacer.grid(column=2, row=0, sticky="news", rowspan=3)

        name2.grid(column=3, row=0, sticky="e", pady=(9,1))
        self.other_person_input.grid(column=4, row=0, sticky="w", padx=(3,0), pady=(9,1))
        age2.grid(column=3, row=1, sticky="e", pady=(0,1))
        self.age2_input.grid(column=4, row=1, sticky="w", padx=(3,0), pady=(0,1))
        kintype2.grid(column=3, row=2, sticky="e", padx=(9,0))
        self.kin_type_input2.grid(column=4, row=2, sticky="w", padx=(2,0))  

    def cancel(self):
        self.root.focus_set()
        self.root.lift()
        self.destroy()

    def add_event(self):          

        def couple_ok():                
            if len(other_person) != 0:
                other_person_all = other_person.split(" #")
                other_person_id = other_person_all[1]
                cur.execute(select_max_persons_persons_id)
                persons_persons_id = cur.fetchone()[0] + 1
                cur.execute(
                    insert_persons_persons_new, 
                    (persons_persons_id, self.current_person, other_person_id))
                conn.commit()
                self.kin_type_list = list(
                    zip(self.kin_type_list, self.new_kin_type_codes))
                self.kin_type_list = [list(i) for i in self.kin_type_list]

                g = 0
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
                    g += 1

                cur.execute(
                    insert_findings_persons_new_couple,
                    (self.new_finding, self.current_person, age_1, 
                        self.kin_type_list[0][0], persons_persons_id))
                conn.commit()
                cur.execute(
                    insert_findings_persons_new_couple, 
                    (self.new_finding, other_person_id, age_2, 
                        self.kin_type_list[1][0], persons_persons_id))
                conn.commit()

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        age_1 = self.age1_input.get()
        if self.couple_event == 1:
            age_2 = self.age2_input.get()
            other_person = self.other_person_input.get()

        if self.couple_event == 0:
            cur.execute(
                insert_finding_new, 
                (self.new_finding, age_1, self.event_type_id, self.current_person))
            conn.commit()            
        else:
            cur.execute(
                insert_finding_new_couple, 
                (self.new_finding, self.event_type_id,))
            conn.commit()

            couple_ok()  
        
        if len(self.place_string) == 0:
            cur.execute(insert_finding_places_new, (self.new_finding,))
            conn.commit()
        else:
            self.update_db_place()

        update_particulars(self.particulars_input.get().strip(), self.new_finding)

        cur.close()
        conn.close()
        self.cancel()
        self.go_to(current_person=self.current_person)

    def update_db_place(self):
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        ids = []
        for dkt in self.place_dicts:            
            ids.append(dkt["id"])
        qty = len(self.place_dicts)
        nulls = 9 - qty
        ids = ids + [None] * nulls
        ids.append(self.new_finding)
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
                print("line", looky(seeline()).lineno, "child, parent:", child, parent)
                cur.execute(insert_places_places_new, (child, parent))
                conn.commit()
            else:
                if (child, parent) not in places_places:
                    places_places.append((child, parent))
                    cur.execute(insert_places_places_new, (child, parent))
                    conn.commit()
            q += 1
        print("line", looky(seeline()).lineno, "ids:", ids)
        cur.execute(insert_finding_places_new_event, tuple(ids))
        conn.commit() 
        place_strings.insert(0, self.place_string)

        self.place_autofill_values = EntryAuto.create_lists(place_strings)
            
        cur.close()
        conn.close()

    def validate_kin_types(self):

        def err_done2(widg):
            msg[0].destroy() 
            self.grab_set()
            widg.focus_set()

        if len(self.other_person_input.get()) == 0:
            self.catch_empty_partner()
            return

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
                    event_table_err[1], 
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

    def catch_empty_partner(self):

        def err_done3():
            msg[0].destroy()
            self.grab_set()
            self.other_person_input.focus_set()            

        msg = open_error_message(
            self, 
            event_table_err[2], 
            "Missing Person in Couple", 
            "OK")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(command=err_done3)

    def catch_dupe_partner(self, evt):

        def err_done (): 
            self.other_person_input.focus_set()
            self.other_person_input.delete(0, 'end')
            self.grab_set()
            msg[0].destroy()

        if self.couple_event == 0: return
        person_and_id = self.other_person_input.get().split("#")
        print("line", looky(seeline()).lineno, "person_and_id:", person_and_id)
        if len(person_and_id[0]) == 0: return
        if self.current_person == int(person_and_id[1]):
            msg = open_error_message(
                self, 
                event_table_err[0], 
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

def highlight_current_title_bar(): # DON'T DELETE
    # MOVED HERE FROM window_border.py... I think currently the title bars
    #    are the right color except for the root when another dialog is in focus,
    #    anyway check it and make it right
    # for k,v in perm_dialogs.items():
        # border = v['canvas']
        # for widg in (
                # border.title_bar, border.title_frame, border.logo, 
                # border.title_1, border.title_1b, border.title_2, 
                # border.txt_frm, border.buttonbox, border.border_top, 
                # border.border_left, border.border_right, 
                # border.border_bottom):
            # widg.config(bg=NEUTRAL_COLOR)
    pass

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

# BRANCH: events_table
# what if user inputs a new name?  (couple & generic events)
# make it possible to edit event_type in an existing row including making new event type see also `if self.new_event not in self.event_types:` (couple & generic events)
# make it impossible to create more than one birth or death event
# add tooltips/status bar messages
# open kintips with spacebar when kin button is in focus, not just mouse click
# bind all ok buttons to Return and cancel buttons to Escape
# on small dlgs which don't use the Treebard border, make all the border X buttons use the existing cancel() method whatever it is for that dlg
# detect if kintips text is too long and if so change font-size to boilerplate
# add probate and ? to list of autosorted events ie: Birth, other, Death, Burial, there has to be an exception for probate bec it takes place anytime after death, maybe even before burial, esp if someone's grave is moved, then generally the 2nd burial will take place after probate. THE SOLUTION IS to have a separately sorted-by-date list of things that can take place after death such as probate, burial, reburial and sort these things according to a definite order first, resort acc to date, then append to main event date which is sorted by date except for birth and death which are always first and last. Will also need another question on the new event type dlg as to whether or not this event type can take place after death optionally or always, in which case an after-death event dialog will have to open up so the user can insert after death event type into the existing order of after death events. Note on the dlg that to trump the defined order of after-death dates, insert a date (even if abt or est) to put the event where it belongs in an individuals history. NOTE the burial event which till now has been last on the events table will be replaced by the whole sublist of after-death events. 

# BRANCH: dates
# finish refactoring dates validation

# BRANCH: front_page
# replace ttk.Notebooks
# add menubar, ribbon menu, footer
# add picture and attrib table
# add buttons to place tab for alias and edit/delete place but don't make them do anything

# BRANCH: fonts
# make fonts tab on prefs tabbook
# replace all comboboxes and all other ttk widgets

# BRANCH: sources
# IDEA for copy/pasting citations. This is still tedious and uncertain bec you never know what's in a clipboard, really. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, maybe a C for Copy, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys. If this idea isn't practical, it still leads to the notion of a tabular display of citations which would make copy & paste very easy instead of showing citations a click apart from each other, and seeing them all together might be useful for the sake of comparison?

# add to do list for combobox: when scrolling if the mouse strays off the scrollbar the dropdown undrops, I've seen a way to fix that but what was it?
# add to main do list re: all dialogs: run the same code when clicking X on title bar
# add to do list for new_event dialog: add person search button 









