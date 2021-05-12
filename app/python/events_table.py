# events_table [import as evts]

import tkinter as tk
import sqlite3
from files import get_current_file
from window_border import Border 
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, 
    KinTip, EntryAutofill, Separator, LabelH3, Button)
from styles import make_formats_dict, ThemeStyles
from names import get_name_with_id
from roles import RolesDialog
from notes import NotesDialog
from places import (
    place_strings, get_autofill_places, ValidatePlace, 
    make_autofill_strings)
# from scrolling import (
    # Combobox, Scrollbar, resize_scrolled_content, MousewheelScrolling)
from query_strings import (
    select_nested_place_string, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_types_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple_age, select_findings_details_couple_generic,
    select_finding_id_birth, select_person_id_kin_types_birth,
    select_finding_ids_age_parents, select_person_id_birth,
    select_findings_details_offspring, select_all_findings_roles_ids, 
    select_finding_ids_offspring, select_all_findings_notes_ids,
    select_count_finding_id_sources, 
    # update_finding_nested_places,
    select_nestings_and_ids, select_place, update_finding_particulars,
    update_finding_age, update_current_person,
    # insert_place_new, insert_nested_places,
    # select_all_nested_pairs, insert_nested_pair,
    # select_all_nested_pairs, insert_nested_pair, select_place_place_id,
    # select_place_id1, select_place_id2,
    # select_nested_places_same, select_place_id1, select_place_id2,
)
import dev_tools as dt



formats = make_formats_dict()
ST = ThemeStyles()
current_file = get_current_file()[0]
# findings_export = []

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

# def do_place_update(right_nest, finding):
    # print('55 right_nest, finding is', right_nest, finding)
    # conn = sqlite3.connect(current_file)
    # cur = conn.cursor()
    # cur.execute(
        # update_finding_nested_places, 
        # (right_nest, finding))
    # conn.commit()
    # cur.close()
    # conn.close()

def get_findings():

    current_person = get_current_person()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    # get couple event types and couple kin types
    cur.execute(select_all_event_types_couple)
    couple_event_types = cur.fetchall()
    couple_event_types = [i[0] for i in couple_event_types]

    cur.execute(select_all_kin_types_couple)
    couple_kin_type_ids = cur.fetchall()
    couple_kin_type_ids = [i[0] for i in couple_kin_type_ids]

    # get generic events
    generic_findings = []
    cur.execute(select_all_findings_current_person, (current_person,))
    generic_finding_ids = cur.fetchall()
    generic_finding_ids = [i[0] for i in generic_finding_ids]

    for finding_id in generic_finding_ids: 
        cur.execute(select_findings_details_generic, (finding_id,))

        generic_finding_details = cur.fetchone()
        generic_finding_details = list(generic_finding_details) 

        place_to_show = generic_finding_details[3]
        cur.execute(select_nested_place_string, (place_to_show,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        generic_finding_details[3] = place_string
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
                SELECT finding_id, kin_type_id 
                FROM findings_persons 
                WHERE person_id = (SELECT person_id FROM current WHERE current_id = 1)
                    AND kin_type_id in ({}) 
            '''.format(
                ','.join('?' * len(couple_kin_type_ids)))

    cur.execute(sql, couple_kin_type_ids)

    finding_ids_kin_type_ids = cur.fetchall()

    for event in finding_ids_kin_type_ids:
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

        place_to_show = couple_generic_details[0][4]
        cur.execute(select_nested_place_string, (place_to_show,))
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

        place_to_show =  offspring_details[2]
        cur.execute(select_nested_place_string, (place_to_show,))
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

    couple_finding_ids = [i[0] for i in finding_ids_kin_type_ids]
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
    def __init__(self, master, view, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.view = view
        self.treebard = treebard
        self.headers = []
        self.widths = [[], [], [], [], []]
        self.nested_place_id = None

        self.screen_height = self.winfo_screenheight()

        self.make_header()
        self.make_table_cells()

    def size_column_to_header(self):
        '''
            Get length of each cell in the column and size the header to 
            fit the longest content in the column. If the background is
            the same as the general background, the entries will all fit
            the column and sticky='ew' takes care of the rest. The +2 is
            because the Age column header could be longer than its contents
            and it acts like padx in the other columns. If edited content
            is not all visible, a tooltip will show what the entry holds
            till the table is redrawn.
        '''

        self.header_widths = []
        for lst in self.widths:
            self.header_widths.append(max(lst))
        x = 0
        for widg in self.headers:
            widg.config(width=self.header_widths[x]+2)
            x += 1

    def get_initial(self, evt):
        self.initial = evt.widget.get()

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
            self.final = ValidatePlace(
                self.view, 
                self.treebard, 
                self.finding, 
                self.final,
                self.findings,
                widg)
            self.final.sift_place_input()

        def update_particulars():
            cur.execute(update_finding_particulars, (self.final, self.finding))
            conn.commit()

        def update_age():
            cur.execute(update_finding_age, (self.final, self.finding))
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
            update_particulars()
        elif col_num == 4:
            update_age()

        cur.close()
        conn.close()

    def make_table_cells(self, qty=1998):
        '''
            EntryAutofill was used for all the text columns to keep the code 
            symmetrical for all the text columns, with autofill set to False
            except for the places column.
        '''

        self.table_cells = []
        for i in range(int(qty/9)):
            row = []
            for j in range(9):
                if j < 5:
                    cell = EntryAutofill(self)
                    cell.initial = ''
                    cell.final = ''
                    cell.finding = None
                    cell.bind('<FocusIn>', self.get_initial)
                    cell.bind('<FocusOut>', self.get_final)

                    if j == 4:
                        cell.config(width=7)
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
        self.table_size = len(finding_ids)
        i = 0
        for row in self.table_cells[0:self.table_size]:
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

        for row in self.findings:
            widg = row[2][0]
            widg.autofill = True
            widg.config(textvariable=widg.var)
            widg.values = place_strings

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

        def open_kin_tip(evt, kin):

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
            instrux = KinTip(self.kin_tip, text=kin[0])
            instrux.grid()

        # So newly created place autofill strings
        #   can be used immediately without first reloading the app.
        # findings_export = self.findings

        r = 2
        for row in self.findings:
            event_type = row[0][1]
            c = 0
            for col in row[0:9]:
                widg = col[0]
                if c == 1:
                    text = col[1][0]
                elif c in (0, 2, 3, 4):
                    text = col[1]

                elif c == 5: # kin
                    # parents
                    if event_type == 'birth':
                        self.kin_buttons = []
                        f = 0
                        for kin in col[1]:
                            kinlab = LabelButtonText(
                                row[c][0],
                                text=kin[2],
                                anchor='w',
                                font=formats['heading3'])
                            kinlab.grid(column=f, row=0)
                            kinlab.bind(
                                '<Enter>', 
                                lambda evt, kin=kin: open_kin_tip(evt, kin))
                            kinlab.bind('<Leave>', self.destroy_kintip)
                            kinlab.bind(
                                '<Button-1>', 
                                lambda evt, kin=kin: self.go_to(evt, kin))
                            self.kin_buttons.append(kinlab)
                            f += 1
                    # spouse or child
                    else:
                        if len(col[1]) != 0:
                            kin = col[1]
                            if kin:
                                text = kin[2]
                            kinlab = LabelButtonText(
                                row[c][0],
                                text=text,
                                anchor='w',
                                font=formats['heading3'])
                            kinlab.grid(column=0, row=0)
                            kinlab.bind(
                                '<Enter>', 
                                lambda evt, kin=kin: open_kin_tip(evt, kin))
                            kinlab.bind('<Leave>', self.destroy_kintip)
                            kinlab.bind(
                                '<Button-1>', 
                                lambda evt, kin=kin: self.go_to(evt, kin))
                            self.kin_buttons.append(kinlab)
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
        
        self.size_column_to_header()

    def go_to(self, evt, parent):
        new_current_person = parent[1]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(update_current_person, (new_current_person,))
        conn.commit()
        cur.close()
        conn.close()
        self.forget_cells()
        self.set_cell_content()

    def destroy_kintip(self, evt=None):
        self.kin_tip.destroy()

    def forget_cells(self):
        self.update_idletasks()
        for lst in self.cell_pool:
            for widg in lst[1]:
                if widg.winfo_subclass() == 'EntryAutofill':
                    widg.delete(0, 'end')
                elif widg.winfo_subclass() == 'Frame':
                    self.destroy_kintip()
                    for button in self.kin_buttons:
                        button.destroy()
                elif widg.winfo_subclass() == 'LabelButtonText':
                    widg.config(text='')
                widg.grid_forget()

    def make_header(self):
        '''
            To make columns line up with headers without excessive 
            tweakings, use the same kind of widgets in the header 
            as used in the table. Also use left-justified columns
            instead of trying to center under the header. Get a solid
            baseline of perfectly lined-up columns before adding any 
            padding between columns. Anytime there is more than a few
            pixels of padding needed, use a spacer column or row, not
            padding, but before trying a spacer make sure sticky and
            columnconfigure etc. are being used right. Add all padding
            on one side and use the same side everywhere.
        '''

        y = 0
        for heading in FINDING_TABLE_HEADS:
            head = EntryAutofill(self)
            head.insert(0, heading)
            head.config(width=len(head.get()), state='disabled')
            head.grid(column=y, row=0, sticky='w')
            if y == 4:
                head.config(width=7)
            if y in (6, 7, 8):
                head.grid(column=y, row=0, sticky='w', padx=(2,0))
            else:
                head.grid(column=y, row=0, sticky='w')
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

'''
    Previously I used an autofill code which restarted the search for matches each time
    the user typed a comma. This worked well for simple nested places, but simple nested
    places are no longer being used. When you type "Par" and "Paris" fills in, there's no
    way for the user to know whether it's Paris, France that's filled in or Paris, Texas.
    So the fill-in values have to be stored as complete strings in a separate table. When a change is made to
    the place or places_places table, more code has to run to update the nested_places 
    table also, in order to redefine the possible strings that can autofill when characters
    are typed. The program will know what the string is made of when it's selected in the
    autofill entry, because the string's elements are stored in the nested_places table.
    Possibly the nested places table stretches the normalization of the database a bit, 
    but maybe not, because each cell has only one value and there is nothing to keep you
    from selecting them in any order you want instead of nest0, nest1, nest2, nest3, etc.
    But the purpose of the table is to concatenate strings in the order of the columns.
    The nested_places table doesn't store every possible string, just the ones the user
    selects and uses. Possibly if a string is deselected, a check might run to see if it's
    still being used somewhere else? If not, its string could be deleted. Example: user
    selects "Denver, Black Twp, Denver Co, Colorado, USA". If all possible strings were
    going to be stored, then "Denver, Denver Co, Colorado, USA" and all the other possible
    strings would have to be stored. But there's no reason to store a string the user has
    never selected. The key to understanding this system is that the finding table where
    events are stored has a place_id column for a foreign key. This column references the
    nested_places_id, not the place_id where single place names are stored. But since nested
    places is a junction table, those simple places are in turn stored in nested places as 
    foreign keys. So by selecting what looks like a string, the user is actually selecting
    a previously defined chain of specific single places. If he wants Paris, Texas, he 
    doesn't get Paris, France.
'''

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

    from widgets import EntryAutofill

    root = tk.Tk()
    root.geometry('+800+300')

    auto = EntryAutofill(root, width=50)
    auto.config(textvariable=auto.var)
    strings = make_autofill_strings()
    # auto.values = short_values
    auto.values = strings
    auto.autofill = True
    auto.focus_set()   

    move = tk.Entry(root)

    auto.grid()
    move.grid()

    root.mainloop()


# DO LIST

# refactor duplicate place dialog to use sets, do it in a git branch

# Have to make one permanent edit row and ungrid it on close, this is because I learned last time since there is only ever one of them it's better to grid_remove instead of destroy it.

# When dlg opens, the entry is a label showing the hint. Add an edit button after the hint like the one on the roles dialog. The edit button turns the hint field into an entry and adds Merge, Delete, and Cancel buttons. On Merge, Delete or cancel the buttons are destroyed and turn back into a label and an Edit button. The place edit thing might be a class so it can also be used in the places tab.

# One problem with detecting known places for filtering down possible matches, when there are unmatched places the nest count is wrong for existing places (singles). EG if there's a 4-nest place and a township is inserted, the current code looks for a 5-nest place to get matches from and there's no results. So maybe have to get a count of new places, subtract that from the total, and look for nests that length. Or just use a count of the singles and look for that length of nesting? TRIED THAT and it shows potential but now I have hard-coded dict keys that started life as list indexes and it's getting complicated so before proceeding I have to change the dict of dicts to a list of dicts instead of using indexes as dict keys.

# Might have to create a new column somwhere called highest_place so it's not in the nesting and it can also be undisplayed

#   Do cases for new places, see doc strings for cases.
#   Dupe, A Co, Colorado, USA -- have to open new place dialog bec too many choices but keep it super simple, no editing, just one field for each id and make them look it up themselves so need a lookup field for place IDs but they'll have to decide for themselves and fill it in and click OK.

# Refactor new place dialog into a flat table or rows at least with each row showing a string of values for a whole nested place string. A radiobutton appears at the left of each row and instead of prefilling each element I will only have to prefill one radio button. Each value is shown as an ID/name pair, or new/name, no lookup of IDs is required. No typing into any but the bottom row labeled "other" and its radio preselects if you type into that row. Change nesting to 9 rows instead of 12. npd opens after ever single focus out of a place input unless the contents were not changed, so it's predictable. OK button is in focus when it opens so one click is all that's needed to accept prefilled choice. No input tricks, just type either the id or the place. No splitting, use separate inputs for every id and name. Put a tester autofill so user can be assured the place is available for autofill before he closes the dialog, and it can also be used as a search field unless an ID is needed in which case maybe a search field will also be necessary.

# Open an R U SURE message when creating duplicate places by typing a place string that already exists: "A place by the name _____ already exists. Click OK to create a new place with with same name, or press Cancel. Hint: in use existing places, you can input place ID numbers in these fields. IDs can be searched from the search field in the new place dialog. To keep this dialog from opening, type "new place" in front of the place name." Make it work whether they type quotes around new place or not, single or double.
# already tested changing number of nests in the new place dialog where there aren't enough, i.e. the USA had to be left off the end, and it didn't work right, it added a new place and did that right but it shouldn't have added a new place. The solution is to detect when that is being done and re-draw the new place dialog with an added combo prefilled with "USA" in red and then it will be input right. Also give the user an "Add another nest to this place" button so the user can anticipate and add the USA the first time.
# If new place dialog is opened and the cancel button is pushed, should the autofill have re-inserted into it whatever was in it before the user typed anything?
# do something with editing existing place strings that are changed, eg if a place is deleted then some strings have to be deleted from nested_strings and some nestings have to be deleted from places_places as well. Delete bad places and superfluous nest strings using the gui. Probably do this on the places tab and maybe have a message on the new place dialog like, "You can't edit existing places here (eg change a spelling) so do it in the places tab instead."
# Make an R U Sure or something when creating a place by the same name. The need to merge places is to be avoided at all cost and this won't happen very often.
# add aliases for places and main pic for current place
# find out why there's so much space between cols esp after place
# add error dialogs
# fix titles on root and new place dialog
# REFACTOR place input to db from scratch. 
#   0) everything is done in one place in new place input module. Not in events table. The code in events table for updating place in db shd be exactly the same as the code there for updating a plain string. All the work has to be done in one place and only the final results sent back to events table. Model that first, it is step 0. 
#   1) make sure the combo display is PERFECT before proceeding. Forget about the "or" for places with more than one nesting string and get rid of any 2nd nesting strings anyway. Correct any ambiguity at this time. The user has to know what's going on.
#   2) define all possible combinations of choices before writing any code. Do it in an orderly way with a fixed framework such as a dict which names each thing so indexes don't have to be fiddled with. The possible states of each comma-delimited element have to be defined by the same series of tests and set booleans or whatever so the right thing will be done with each element.
#   3) put it in the db and immediately rerun the code that makes the place autofill values available so no reloading is needed to use the new place and/or new string.
#   4) things to avoid: globality. pass all values as soon as they exist to the place where they will be needed.
#   5) places where values have to be updated: 3 db tables, autofill values, entry display
#   6) use existing queries but the python for sorting the input is really bad. 
# findings_export has to be changed at the right time so the lst will be all new nestings immediately after nesting is made, see model . 
# MODEL THIS: when changing old place in events table to different old place in evts table, everything works right.
# If changing all of an existing place in the events table, everything works, but when changing part of an existing place to a new place, the new place dialog doesn't open and nothing goes into the db.
# when changing an old place to a new place that doesn't all exist yet ?, the new place dialog opens but the new place doesn't become available for fill-in immed (?at all?) and it ?doesn't get stored in db for next time app loads either.
# when making a totally new or partly new place in events table where there was a blank, the new place goes into the db but not into the finding table.
# valid input to place field should go into finding table, test thoroughly
# Change something (eg a place) in events table. Change current person by clicking kin button then changing back to original current person. Unedited values are shown in original current person events table. Don't know if they're messed up in db too but it rolls back the display somehow to previous values.
# # MAKE THIS DO SOMETHING bottom of window_border, check others
# clicking any widget on a dialog shd change the title bar color of that dialog to main color and all other title bars incl. root to neutral color. Commented this, need to get back to it. It was in a different module and have to make it work in the right place. It used instance variable to colorize all the title bar widgets in the clicked dialog after decolorizing title bar widgets in all dialogs incl root.
# add menubar, ribbon menu, footer
# add picture and attrib table
# IDEA for copy/pasting citations. This is still tedious and uncertain bec you never know what's in a clipboard, really. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, maybe a C for Copy, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys.
# refactor dates validation to use regular expressions

# dev docs, new place dialog:

# when inputting a place w/out all its ancestors eg "Dallas, Texas" w/out the "USA", it creates a separate autofill string and the result is that if the whole thing is also put in (with the USA), the autofill will not do anything till you type the U so is completely useless if you have strings with one or more final elements omitted. To solve this, 1) don't let the user make incomplete strings; detect when the last element of a string being input is missing something and add another combo for it and prefill it. 2) Don't allow blank combos. (I think that's already taken care of.) 3) create a feature where the user can designate top ancestors as not for display. I don't like this and maybe the user should just get used to using country names, that's why long ones have abbrevs like USA, US, UK, USSR etc. It's bad genealogy to leave off the country name so maybe for now at least it can be disallowed. But what if there's no country name? That's the problem withdisallowing things. If I write smart software that detects things and tells the user what to do, that's bad because I can't detect all possibilities. For example, before there was a Texas, USA, there was a Republic of Texas. So detecting that the user has not done something write and forcing some policy is bad news because it will keep people from doing what they want, for example if someone doesn't know "Republic of Texas" and tries to call it just Texas without the country name, because they do know it wasn't in the Union yet... bad. So maybe the best thing for now is to live with the fact that a few place names will have to be typed most of the way through and let the user make alternate strings as he sees fit. The feature mentioned doesn't even need to be built as long as the user knows he can leave off country names and that's how the autofill will work, it will only autofill what has previously been entered.

#   Let's say a place autofill doesn't fill in because user has entered a previously unused string of nested places, e.g. "Paris, Lamar Co, TX". "Paris" and "Texas" are already in the db but the user wants to insert a county. Why not just accept the new place without an annoying dialog? Because there may be another place called Paris, and it's not our business to guess which Paris the user is talking about. We can guess which one he's probably talking about, and pre-select it in the combobox so that most of the time, the user can just accept pre-selected combobox values and click OK. This avoids annoying the user more than necessary with superfluous choices. There are at least two problems that the new place dialog forestalls. 1) mis-spelling an existing place will open the dialog. User can click Cancel and fix his spelling (or there should be a way of assigning spelling variants and aliases to a place if that's what the user intended); 2) in other genieware, it's a frequent problem with place autofill widgets that the wrong "Paris" would fill in the first time a new string containing "Paris" is typed, and the user would use the wrong nested place string dozens of times before finding out that his Texan ancestors came from France. Each of these mistakes would have to be hunted down and corrected. So Treebard has a policy of having the user confirm new nested place names, and Treebard doesn't autofill place strings that have never been used. It would be easy to do this by restarting the search for autofill matches every time the user typed a comma, but this is exactly when the wrong Paris gets plunked down in the middle of Texas. In Treebard, the user is given the opportunity to look at all the places in a new nested place string to make sure they are each the place he intended. The hard part for us is to make this as easy as possible by determining that there's already a place called "Paris" in a place called "Texas", so instead of making the user select "Texas" in the dialog, we pre-select it and it's probably right. But namings are not predictable by us and the needs of the user could be more complex than we might imagine, so the user has to be given the freedom to make place strings any way he wants, so that a few edge cases don't ruin his experience of using Treebard. The only thing Treebard won't do is to make two different places called "Paris, Texas". This sounds bad but it's not, because chances are, if there are two cities named "Paris" in Texas, they won't both be in Lamar County. But if there were, then chances are they'd be in different precincts or townships. So the worst case scenario is the extremely rare occasion wherein two cities a few inches apart from each other have the same name. But even in a case like this, research will show that the residents of these places have a way of distinguishing the two places. For example, "Glenwood" vs. "West Glenwood". The need to differentiate two similarly named places that happen to be close together doesn't originate with data entry. Research should always turn up a unique name or nickname for each place and if even that doesn't work, the extreme edge case will have the user creating a nickname himself. I doubt this will ever happen though. The other thing that Treebard places won't do for the user is to guess on capitalization. The user has to input new places as he wants them to appear. Treebard will never change the capitalization of a place name from the way the user first enters it unless the user changes the capitalization himself. However, when using the autofill for places that already exist, capitalization is not the user's problem.

# CASES not handled:
# Case: input Paris, Tennessee, USA. new place dialog opens but without "new place "Paris" prefilled in combo entry. This is OK. There are already three places named Paris. User can select one of them or just type Paris in the entry and that will tell Treebard to make a new place called Paris. Or he can type an ID and Treebard will use that place.

# user docs, places autofill:
# All places except for The Whole Universe are nested in a larger place, and someone has probably figured out a container for the whole universe but we'll skip right to the practical, everyday nitty gritty. A practical example of a nested place is Paris, Lamar County, Texas, USA. When you add this place to your database, Treebard will automatically make sure that the following autofill place strings are stored for you, so you never have to type them all the way out again:
#    Paris, Lamar County, Texas, USA
#    Lamar County, Texas, USA
#    Texas, USA
#    USA
# But what if you want to use a place called "Lamar County, Texas" and not add the country? No problem, you just enter it that way and accept the string that way when Treebard shows you the new place dialog. In this way you can create autofill strings for places that already exist, and the new place dialog is easy to use so you won't accidentally create copies of places that already exist; just the autofill strings you need. Then if you never use the whole autofill string (with USA at the end), you'll never see it again because the values you're offered first are the ones you've used most recently. But if you did want to use the full string (the one with USA at the end), just start typing "u..." after the first part autofills, and the "USA" will fill in anyway. This is especially helpful if you intend to add "United States of America" after every USA place name, as suggested by some purists. Treebard has no opinion about that; it's up to you. We have two main options for improving the user options here: 1) add a "default place" option so you can tell Treebard never to display "United States of America" unless you actually type it in; or 2) give the user the option to give each place both a long name and short name. But then we'd have to ask you when you want to use the long and when to use the short... I can sense the code bloat... anyway, please register your vote. Which way would you like it best? The third option is to leave it the way it is, and you just enter what you want each time. Since it's autofill, it's already easy... why make it complicated?







# ADDED NOTE: there are so many cities that are located in more than one county that Wikipedia has a list of them: https://en.wikipedia.org/wiki/List_of_U.S._municipalities_in_multiple_counties.

# ADDED NOTE: not using jurisdiction categories allows a flexibility matching the reality of how we humans do things. So we don't have to stand on our heads to input places like this: Baltimore, Maryland is not in any county and the capital city of the United States is not in any of the 50 states. In Treebard there is nothing to do to accomodate these exceptions to the norm. Just enter them as "Baltimore, Maryland, USA" and "Washington, District of Columbis, USA". Treebard has no opinion about this.

# ADDED NOTE: Treebard doesn't add or take away from what you enter as a place. Treebard doesn't add or remove jurisdictional titles such as "County". Just enter it the way you want it to be seen. This flexibility matches the facts of the situation. For example, in England, a county is called by its name only: just "Leicester". But not far from there in Ireland, the word "County" comes first, as in "County Down". In the US as far as I know, everyone says "County" after the county name, but since I said "everyone" there will be plenty of exceptions. For example, in Louisiana there are no counties at all, just parishes. Where I live now in the Philippines there are provinces instead of states, like in Canada. But there are no counties or parishes. There are baranggays, which are much smaller than American counties, and puroks, which are even smaller than that, each with its own governmental jurisdiction. The point is that it would be kinda silly for Treebard to build a jurisdictional naming structure into itself when literally every country would be an exception to anything we could possibly come up with. The same goes for people's names. Where I come from, there are first, middle and last names. But you don't have to be Chinese to feel that this convention is completely foreign. Iceland for example has a very different system. So building a system around American ways of doing things is something we try to avoid. Even if every single Treebard user forever and ever was an American (or a "United Statesian" as some feel we should be called), many of our very own ancestors never lived in America, never set foot on the place, or never even heard of it. The suffix "-centric" comes to mind. Here at Treebard University we want to be people-centric, instead of orbiting around any particular set of traditions including dead ones and ones that haven't been born yet. It's impossible to do anything perfectly but sometimes the best software is not trying so hard to be all things to all people. We like to let the user make the decisions, and one way to do that is to sometimes do less. In a less containerized structure, the user gets to design his own approach without feeling like he is cheating the program.

# it just occurred to me that I don't know how to store a nested place once user chooses it. Another table will be needed called findings_places. The columns will reference finding_id and places_places_id. But places_places_id refers to only one part of the place. Would it be possible to add finding_id col to places_places? Doesn't seem to fit. I think what I need is a nested place table. A unique id will identify each unique combination of places chosen and delete them if unchosen(?). The row will also have up to 12 columns which each reference one place_id and the unused columns are null. The findings_places table will then have cols for finding_id and nested_place_id. But wait. Each finding has only one place. A m-m table isn't needed for this part. The place_id col on the finding table could be used but instead of ref'ing place_id it will ref nested_place_id. Then on loading the events table, the stored placename string could be displayed directly and not by storing a list of strings or a concatenated string but by querying the nested_places table and getting each value individually. The concern is to not store more than one Unit in a single table cell. Then when user edits the value in the place row, the nested place row will be created for a new combination of places if it doesn't already exist. There will have to be a Python procedure for editing the nested_places table. The good news is that loading values for autofill place values will come directly from this table, joined to place table so strings will display for stored ids. Typing a new place name will involve storing data in three tables. The place table will get a new row. The nested place table will get a new row. Then the id from the new nested place table row will be stored as FK in place_id col of finding table. But I don't know how to take strings from the user and convert them to IDs. When an existing string is chosen, it won't matter, but when a new string is created, a way of telling what is what will have to be created. First thing to do is to use my new autofillentry to get nested place values out of the nested_places table but first I have to create the nested place table. It seems I will need a procedure for deciding what to store in the table and storing it. Getting it back out is easy, just make the strings using the ids and join them with commas. For now I'll create the table and give it all ten of denver's possible nestings and make it work with an autofillentry. Possibly this many-many-recursive-query class will not be used to display strings at all, but rather to create storable chains of ids. I'll start by cheating some data into a new table and see what happens. But instead of creating a table with 12 cols--which ties me into a 12-value string--and has twelve identical tables that are supposed to be in order and that is not right for relational db, there is not supposed to be a fixed order of the tables--why can't the table just have an id, a place_id fk, and a sort order column? Then if a change is made you might only change the sort order. Sort order could be read off of the results of the m-m-recursive-query. But this won't work for populating a values list for an autofill. The m-m query would have to be redone. So what this 12-col-table really is, is a types table, except that the types are generated by code. I don't think there's any way to do it without putting all twelve cols in order... so the right thing to do is not to have twelve cols but to store a csv and just display it. But then the parts of the string have no meaning so it's back to twelve fk cols, so that for each string its corresponding place id follows it around the code. Too bad the cols have to be read in order but I don't know any way around it. When a new place is made or an old place changed, use self.tree_id to generate the list of ids to be stored.

# user docs:
# can't use in place names: 
#   '  #' (two spaces before a number sign aka hashtag character; one space is OK)
#   the phrase "new place"
#   double quotation mark ". Single quotation mark ' aka apostrophe is OK.






