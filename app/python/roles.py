# roles

import tkinter as tk
import sqlite3
from files import current_file
from widgets import(
    Toplevel, Canvas, Frame, LabelH3, ClickAnywhereCombo, 
    EntryAutofillHilited, Button, Label, ButtonQuiet)
from toykinter_widgets import StatusbarTooltips, run_statusbar_tooltips
from scrolling import Scrollbar
from styles import make_formats_dict, config_generic
from names import get_all_persons, get_name_with_id, PersonAdd
from right_click_menu import RightClickMenu, make_rc_menus
from message_strings import role_dlg_msg, gen_edit_role_rows
from query_strings import (
    select_roles, select_role_type_id, insert_findings_roles, 
    update_findings_roles_person, insert_role_type, 
    update_findings_roles_role_type, update_findings_roles_null_person,
    delete_findings_role, select_count_findings_roles, select_role_types,
    select_findings_roles_generic, select_couple_event_ids, 
    select_couple_event_roles)
import dev_tools as dt




formats = make_formats_dict()

class RolesDialog(Toplevel):
    def __init__(
            self,
            master,
            current_person,
            finding_id=None,
            header=None,
            pressed=None,
            *args,
            **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        birth_name = get_name_with_id(current_person)
        self.title('{} ({})'.format('Roles for an Event', birth_name))

        self.current_person = current_person
        self.root = master
        self.finding_id = finding_id
        self.header = header
        self.pressed = pressed

        self.original_role_type = ''
        self.original_role_person = ''

        self.user_input_person = ''

        self.role_types = []
        self.findings_roles_id = 0
        self.edited_role_id = 0

        self.got_row = 0

        self.role_types = []
        self.persons = get_all_persons()

        self.roles_per_finding = []

        self.rc_menu = RightClickMenu(self.root)
        self.make_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_roles_dialog)
       
    def make_widgets(self):
        '''
            The attribute self.header passes values used in a convoluted
            process kept in message_strings.py and right_click_menu.py.
        '''

        # auto-scrollbar

        self.role_canvas = Canvas(
            self,
            # bd=0,
            # highlightthickness=0
)
        self.role_canvas.grid(column=0, row=0, sticky='news')

        self.role_content = Frame(self.role_canvas)

        self.role_content.grid_columnconfigure(0, weight=1)
        self.role_content.grid_columnconfigure(1, weight=0)
        self.role_content.grid_columnconfigure(2, weight=1)
        self.role_content.grid_rowconfigure(1, weight=1)

        vscroll = Scrollbar(
            self, width=16, hideable=True, 
            command=self.role_canvas.yview)
        vscroll.grid(column=1, row=0, sticky='ns')
        hscroll = Scrollbar(
            self, orient='horizontal', width=16, hideable=True, 
            command=self.role_canvas.xview)
        hscroll.grid(column=0, row=2, sticky='ew') 

        self.role_canvas.config(
            yscrollcommand=vscroll.set,
            xscrollcommand=hscroll.set)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # widgets

        roles_table = Frame(self.role_content)
        new_roles_area = Frame(self.role_content)

        roles_dialog_header = Frame(self.role_content)

        self.rolfrm = Frame(self.role_content)

        self.make_roles_table()

        new_roles_header = LabelH3(new_roles_area, text='Create New Role')

        self.role_type_input = ClickAnywhereCombo(
            new_roles_area, values=self.role_types)

        self.person_input = EntryAutofillHilited(new_roles_area)
        self.person_input.values = self.persons
        self.person_input.autofill = True
        self.person_input.config(textvariable=self.person_input.var)
        # self.person_input.fix_max_width()

        self.add_butt = Button(
            new_roles_area, 
            text='Add',
            command=self.get_add_state)
        self.done_butt = Button(
            new_roles_area,
            text='Done',
            command=self.add_and_close)
        self.close_butt = Button(
            new_roles_area,
            text='Close',
            command=self.close_roles_dialog)

        roles_statusbar = StatusbarTooltips(self)
        roles_statusbar.grid(column=0, row=3, sticky='ew')

        roles_table.grid(column=0, row=0)
        new_roles_area.grid(column=0, row=2)

        roles_dialog_header.grid(column=0, row=0, ipadx=12, padx=24, pady=(36,12))
        self.rolfrm.grid(column=0, row=1, columnspan=2)       
        self.rolfrm.grid_columnconfigure(4, weight=1)

        new_roles_header.grid(column=0, row=0, padx=6, pady=6)

        self.role_type_input.grid(column=0, row=1, padx=(24,6), pady=6)
        self.person_input.grid(column=1, row=1, padx=6, pady=6)
        self.add_butt.grid(column=2, row=1, padx=6, pady=6)
        self.done_butt.grid(column=3, row=1, padx=6, pady=6)
        self.close_butt.grid(column=4, row=2, padx=(6,24), pady=(6,24))

        self.make_edit_row()
        self.get_role_types()

        visited = (
            (roles_dialog_header, 
                '', 
                'Type, date, place & particulars of this event if known.'),
            (self.edit_role_type, 
                'Edit Role Type Input', 
                'Existing roletype can be changed to a different type.'), 
            (self.edit_role_person, 
                'Edit Role Person Input', 
                'Existing role person can be changed or new person made.'),
            (self.ok_butt, 
                'Edit Role OK Button', 
                'Submit changes to this role.'),
            (self.cancel_butt, 
                'Edit Role Cancel Button', 
                'Close role edit row, make no changes.'),
            (self.delete_butt, 
                'Edit Role Delete Button', 
                'Delete this role but not the role type or role person.'),
            (self.role_type_input, 
                'New Role: Type Input', 
                'Select role type or create a new one.'), 
            (self.person_input, 
                'New Role: Person Input', 
                'Select role person, add new one, or leave blank.'),
            (self.add_butt, 
                'Add New Role Button', 
                'Make a new role and leave dialog open.'), 
            (self.done_butt, 
                'Add New Role & Close Dialog Button', 
                'Make a new role and close dialog.'),
            (self.close_butt, 
                'Close Dialog Button', 
                'Close dialog without making another role.'))

        run_statusbar_tooltips(
            visited, 
            roles_statusbar.status_label, 
            roles_statusbar.tooltip_label)

        rcm_widgets = (
            self.role_type_input, self.person_input, self.add_butt, 
            self.done_butt, self.close_butt)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            role_dlg_msg, 
            header_parent=roles_dialog_header, 
            header=self.header, 
            which_dlg='roles')

        self.role_canvas.create_window(
            0, 0, anchor=tk.NW, window=self.role_content)
        config_generic(self) 
        self.resize_window()
        self.resize_scrollbar() 

    def make_roles_list(self):

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_roles, (self.finding_id,))
        roles_per_finding = cur.fetchall()
        if roles_per_finding:
            self.roles_per_finding = [list(i) for i in roles_per_finding]

        for lst in self.roles_per_finding:
            name = get_name_with_id(lst[2])
            lst.append(lst[2])
            lst[2] = name

        cur.close()
        conn.close()

    def make_roles_table(self):

        def get_clicked_row(evt):
            self.got_row = evt.widget.grid_info()['row'] 

        def on_hover(evt):
            evt.widget.config(text='Edit') 

        def on_unhover(evt):
            evt.widget.config(text='')

        self.make_roles_list()

        first_butt = None
        n = 0
        for lst in self.roles_per_finding:
            labelr = Label(self.rolfrm, text=lst[1], anchor='e')
            sep = Label(self.rolfrm, text='|', anchor='w')
            labelp = Label(self.rolfrm, text=lst[2], anchor='w')
            editx = ButtonQuiet(
                self.rolfrm, 
                width=2,
                command=self.grid_edit_row)
            labelr.grid(column=0, row=n, padx=6, pady=3, sticky='ew')
            sep.grid(column=1, row=n)
            labelp.grid(column=2, row=n, padx=6, pady=3, sticky='ew')
            editx.grid(column=3, row=n, padx=6, pady=3)
            if n == 0:
                first_butt = editx
            editx.bind('<Enter>', on_hover)
            editx.bind('<Leave>', on_unhover)
            editx.bind('<Button-1>', get_clicked_row)
            editx.bind('<space>', get_clicked_row)
            self.rc_menu.loop_made[editx] = gen_edit_role_rows
            n += 1
        if first_butt:
            first_butt.focus_set()

    def grid_edit_row(self):
        self.edited_role_id = self.roles_per_finding[self.got_row][0]
        for child in self.rolfrm.winfo_children():
            if child.winfo_class() != 'Label':
               pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 0:
                    self.original_role_type = self.roles_per_finding[self.got_row][1]
                elif child.grid_info()['column'] == 2:
                    self.original_role_person = self.roles_per_finding[self.got_row][2]
        self.edit_row.grid(row=self.got_row)

        self.edit_role_type.delete(0, 'end')
        self.edit_role_person.delete(0, 'end')
        self.edit_role_type.insert(0, self.roles_per_finding[self.got_row][1])
        self.edit_role_type.focus_set()

        chosen_person_id = self.roles_per_finding[self.got_row][4]
        if chosen_person_id is None:
            self.edit_role_person.insert(0, '')

        else:
            self.edit_role_person.insert(
                0, '{}  #{}'.format(
                    self.roles_per_finding[self.got_row][2], 
                    str(chosen_person_id)))

        self.edit_row.lift()
        self.resize_scrollbar()
        self.resize_window()

    def make_edit_row(self):

        def cancel_edit_row():
            self.edit_row.grid_remove()
            self.resize_scrollbar()
            self.resize_window()

        self.edit_row = Frame(self.rolfrm)

        self.edit_role_type = ClickAnywhereCombo(
            self.edit_row, values=self.role_types)

        self.edit_role_person = EntryAutofillHilited(self.edit_row)
        self.edit_role_person.values = self.persons
        self.edit_role_person.autofill = True
        self.edit_role_person.config(textvariable=self.edit_role_person.var)

        self.ok_butt = Button( 
            self.edit_row, 
            text='OK',
            command=self.get_edit_state)
        self.cancel_butt = Button(
            self.edit_row,
            text='Cancel',
            command=cancel_edit_row)
        self.delete_butt = Button(
            self.edit_row,
            text='Delete',
            command=self.delete_role)
        self.edit_row.grid(column=0, row=0, columnspan=5, sticky='ew')

        self.edit_role_type.grid(column=0, row=0, padx=6, pady=6)
        self.edit_role_person.grid(column=1, row=0, padx=6, pady=6)
        self.ok_butt.grid(column=2, row=0, padx=6, pady=6)
        self.cancel_butt.grid(column=3, row=0, padx=6, pady=6)
        self.delete_butt.grid(column=4, row=0, padx=6, pady=6)
        self.edit_row.grid_remove()

    def get_edit_state(self):
        '''
            Detect and respond to changes in existing roles on OK button.
        '''
        edited_role_type = self.edit_role_type.get()
        edited_role_person = self.edit_role_person.get()
        if edited_role_type in self.role_types:
            if edited_role_type != self.original_role_type:
                self.update_role_type(edited_role_type)
        else:
            self.make_new_role_type(edited_role_type)
            self.update_role_type(edited_role_type)
        if edited_role_person in self.persons:
            if edited_role_person != self.original_role_person:
                self.change_role_person(edited_role_person)
        elif len(edited_role_person) == 0:
            findings_roles_id = self.roles_per_finding[self.got_row][0]
            self.set_role_person_unknown(findings_roles_id)
        else:
            self.make_new_person(from_edit=True, edited_role_person=edited_role_person)
            edited_person_id = self.person_add.new_person_id
            self.update_role_person(edited_person_id)
        self.original_role_type = edited_role_type
        self.original_role_person = self.edit_role_person.get()
        self.edit_row.grid_remove()

    def get_add_state(self):

        if len(self.role_type_input.get()) == 0:
            self.role_type_input.focus_set()
            return
        chosen_role_type = self.role_type_input.get()
        self.user_input_person = self.person_input.get()            
        if chosen_role_type not in self.role_types:
            self.make_new_role_type(chosen_role_type)
        self.make_new_role(chosen_role_type)

    def make_new_role(self, role_type):
        if len(self.user_input_person) == 0:            
            role_person_id = None
        elif self.user_input_person not in self.persons:
            self.make_new_person()
            role_person_id = self.person_add.new_person_id
        else:
            role_person_id = self.person_input.get().split('  #')[1]

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_role_type_id, (role_type,))
        role_type_id = cur.fetchone()[0]
        cur.execute(
            insert_findings_roles, 
            (self.finding_id, role_type_id, role_person_id))
        conn.commit()
        cur.close()
        conn.close()
        dont_destroy = []
        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                edit_row_frame = child
                dont_destroy.append(edit_row_frame)
                break
        for child in self.rolfrm.winfo_children():
            if child.master == edit_row_frame:
                dont_destroy.append(child)
        for child in self.rolfrm.winfo_children():
            if child not in dont_destroy:
                child.destroy()
        self.make_roles_table()
        
        self.pressed.config(text=' ... ')
        self.role_type_input.delete(0, 'end')
        self.person_input.delete(0, 'end')
        self.resize_scrollbar()
        self.resize_window() 
        self.make_roles_list()

    def make_new_person(self, from_edit=False, edited_role_person=None):
        '''
            Do not make the person-add dialog modal, because it prevents
            the right-click menu from working right. This means the user
            can go back and forth from roles dialog to person-add dialog
            and make manual changes. It works fine. The only problem is if
            ADD is clicked twice, there will be two person-add dialogs and
            the first one can't be closed without reloading the app. So
            instead of making the person-add dialog modal, the buttons
            on the roles dialog are disabled while the person-add dialog is open.
        '''

        def close_dialog():
            self.add_butt.config(state='normal')
            self.done_butt.config(state='normal')
            self.close_butt.config(state='normal')
            self.new_role_person_dialog.destroy() 

        self.new_role_person_dialog = Toplevel(self)
        self.new_role_person_dialog.resizable(False, False)
        self.add_butt.config(state='disabled')
        self.done_butt.config(state='disabled')
        self.close_butt.config(state='disabled')
        self.person_add = PersonAdd(
            self.new_role_person_dialog, 
            self.person_input, 
            self.root)   
        self.person_add.grid(column=0, row=0)
        self.person_add.name_input.delete(0, 'end')
        if from_edit is False:
            self.person_add.name_input.insert(0, self.user_input_person)
        else:
            self.person_add.name_input.insert(0, edited_role_person)
        self.person_add.add_butt.config(command=self.person_add.add_person)

        closer = Button(
            self.person_add.buttonbox, 
            text='Close',
            width=8,
            command=close_dialog)
        closer.grid(column=1, row=0, padx=6, pady=6)

        self.person_add.new_person_statusbar.grid(column=0, row=2, sticky='ew')

        self.new_role_person_dialog.protocol("WM_DELETE_WINDOW", close_dialog)
        self.person_add.gender_input.focus_set()
        config_generic(self.new_role_person_dialog)
        self.new_role_person_dialog.wait_window()
        self.persons = get_all_persons() 

    def change_role_person(self, edited_role_person):
        '''
            Change role person to a person that already exists.
        '''

        new_person_data = edited_role_person.split('  #')
        new_person_id = new_person_data[1]
        new_person_name = new_person_data[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_findings_roles_person, (new_person_id, self.edited_role_id))
        conn.commit()
        cur.close()
        conn.close()

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 2:
                    child.config(text=new_person_name)
        self.resize_scrollbar()
        self.resize_window()
        self.make_roles_list()

    def make_new_role_type(self, edited_role_type):
        '''
            Get user pref w/ dialog. Connect to db, insert new role_type.
        '''

        if len(edited_role_type) == 0:
            return
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(insert_role_type, (edited_role_type,))
        conn.commit()
        cur.close()
        conn.close()

        self.get_role_types()

    def update_role_type(self, edited_role_type):

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_role_type_id, (edited_role_type,))
        chosen_role_type_id = cur.fetchone()
        if chosen_role_type_id:
            chosen_role_type_id = chosen_role_type_id[0]

        cur.execute(
            update_findings_roles_role_type, 
            (chosen_role_type_id, self.edited_role_id))
        conn.commit()

        cur.close()
        conn.close()

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 0:
                    child.config(text=edited_role_type)

        self.resize_scrollbar()
        self.resize_window()

        self.get_role_types()
        self.make_roles_list()

    def update_role_person(self, edited_person_id):
        '''
            Change person in existing role to newly created person.
        '''

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(
            update_findings_roles_person, 
            (edited_person_id, self.edited_role_id))
        conn.commit()
        cur.close()
        conn.close()

        edited_role_person_name = get_name_with_id(edited_person_id)

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 2:
                    child.config(text=edited_role_person_name)
        self.resize_scrollbar()
        self.resize_window()  
        self.make_roles_list() 

    def set_role_person_unknown(self, findings_roles_id):

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(
            update_findings_roles_null_person, 
            (findings_roles_id,))
        conn.commit()
        cur.close()
        conn.close() 

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 2:
                    child.config(text='')

        self.resize_scrollbar()
        self.resize_window()  
        self.make_roles_list()       

    def delete_role(self):

        def delete_role_from_db():
            '''
                Un-nest this function to use self.xxxxx instead of nonlocal.
            '''

            nonlocal role_count_per_finding
            
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(delete_findings_role, (self.edited_role_id,))
            conn.commit()
            cur.execute(select_count_findings_roles, (self.finding_id,))
            role_count_per_finding = cur.fetchone()[0]

            cur.close()
            conn.close()
            self.make_roles_list()

        role_count_per_finding = 0
        delete_role_from_db()
        if role_count_per_finding == 0:
            self.pressed.config(text='     ')
        self.edit_row.grid_remove()
        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                child.destroy()
            elif child.grid_info()['row'] > self.got_row:
                row = child.grid_info()['row']
                child.grid(row=row-1)
        self.resize_scrollbar()
        self.resize_window()

    def add_and_close(self):
        self.get_add_state()
        self.close_roles_dialog()

    def close_roles_dialog(self, evt=None):
        self.destroy()

    def get_role_types(self):

        self.role_types = []

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_role_types)
        role_types = cur.fetchall()
        cur.close()
        conn.close()
        role_types = [i[0] for i in role_types]

        role_types.sort()

        self.role_types = role_types

        for widg in (self.edit_role_type, self.role_type_input):
            widg.config(values=self.role_types)

    def resize_scrollbar(self):
        self.update_idletasks()                     
        self.role_canvas.config(scrollregion=self.role_canvas.bbox("all")) 

    def resize_window(self):
        self.update_idletasks()
        page_x = self.role_content.winfo_reqwidth() + 24
        page_y = self.role_content.winfo_reqheight() + 48
        self.geometry('{}x{}'.format(page_x, page_y))

    def get_roles(self, evt):

        def use_values():
            ''' 
                Gets all roles for current person's finding rows. When 
                dots are clicked in findings table roles column, the dialog
                opens showing the right roles for that person and that role. 
            '''

            generic_event_roles = get_generic_event_roles()
            couple_event_roles = get_couple_event_roles()
            all_roles = generic_event_roles + couple_event_roles
            unique_ids = []
            for lst in all_roles:
                if lst[0] not in unique_ids:
                    unique_ids.append(lst[0])
            all_roles_by_finding = []
            for lst in all_roles:
                for id in unique_ids:
                    roles_per_finding = []
                    if lst[0] == id:
                        roles_per_finding.append(lst)
                    for item in roles_per_finding:
                        if len(item) > 0:
                            all_roles_by_finding.append(item)
            final = []
            for i in range(len(unique_ids)):  
                final.append([])
            t = 0
            for id in unique_ids:
                for lst in all_roles_by_finding:
                    if lst[0] == id:
                        final[t].append(lst)
                t += 1

        def get_generic_event_roles():
            '''
                Example: employer in an Occupation event is generic role.
                Flower girl in a Wedding event is couple-event role because
                it will be linked to both spouses.
            '''
            cur.execute(select_findings_roles_generic, (self.current_person,))
            generic_event_roles = cur.fetchall()
            generic_event_roles = [list(i) for i in generic_event_roles]

            return generic_event_roles

        def get_couple_event_ids():
            ''' 
                For use in getting couple event roles and
                couple event notes.
            ''' 
            cur.execute(select_couple_event_ids, (self.current_person,))
            couple_event_ids = cur.fetchall()
            couple_event_ids = [i[0] for i in couple_event_ids]
            qmarks = len(couple_event_ids)

            return couple_event_ids, qmarks  

        def get_couple_event_roles():

            couple_event_ids = get_couple_event_ids()

            select_couple_event_roles = select_couple_event_roles.format(','.join('?' * couple_event_ids[1]))

            cur.execute(select_couple_event_roles, couple_event_ids[0])

            couple_event_roles = cur.fetchall()
            couple_event_roles = [list(i) for i in couple_event_roles]

            return couple_event_roles

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        self.use_values()
        cur.close()
        conn.close()



