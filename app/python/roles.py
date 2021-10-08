# roles.py

import tkinter as tk
import sqlite3
from files import current_file
from window_border import Border 
from widgets import (
    Frame, Toplevel, Label, LabelButtonText, ButtonQuiet,
    LabelH3, Button, EntryHilited1, LabelHeader)
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from right_click_menu import RightClickMenu, make_rc_menus
from message_strings import role_dlg_msg, gen_edit_role_rows
from styles import make_formats_dict, config_generic
from names import (
    get_name_with_id, make_values_list_for_person_select, PersonAdd,
    get_all_persons)
from scrolling import Scrollbar, resize_scrolled_content
from toykinter_widgets import run_statusbar_tooltips
from query_strings import (
    select_roles, select_role_types, select_role_type_id,
    update_findings_roles_role_type, update_findings_roles_person,
    insert_findings_roles, delete_findings_role,
    select_count_findings_roles,

)

import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

class LabelDotsRoles(LabelButtonText):
    ''' 
        Display clickable dots if more info, no dots 
        if no more info. 
    '''
    def __init__(
            self, 
            master,
            *args, **kwargs):
        LabelButtonText.__init__(self, master, *args, **kwargs)

        self.master = master
        self.current_person = None
        
        self.root = master.master

        self.finding_id = None
        self.header = []
        self.config(width=5, font=formats['heading3'])
        self.bind('<Button-1>', self.open_dialog)

    def open_dialog(self, evt):
        dlg = RolesDialog(
            self.master, 
            self.finding_id, 
            self.header, 
            self.current_person,
            pressed=evt.widget)

class RolesDialog(Toplevel):
    def __init__(
            self, master, finding_id, header, current_person, 
            pressed=None, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.root = master
        self.finding_id = finding_id
        self.header = header
        self.current_person = current_person
        self.pressed = pressed

        self.role_types = []
        self.persons = get_all_persons()
        self.roles_per_finding = []

        self.current_name = get_name_with_id(self.current_person)
        people = make_values_list_for_person_select()        
        self.all_birth_names = EntryAuto.create_lists(people)

        self.rc_menu = RightClickMenu(self.root)
        self.make_widgets()

    def make_widgets(self):

        def show_message():
            self.header = "\n".join(self.header)
            header_text = "Roles for Conclusion #{}: {}".format(
                self.finding_id, self.header)
            self.window.columnconfigure(0, weight=1)
            self.window.rowconfigure(0, weight=1)
            self.header_msg = LabelHeader(
                self.window,
                text=header_text)
            self.header_msg.grid(
                column=0, row=0, sticky='news', 
                ipadx=12, ipady=12, padx=(24,0), pady=18)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        self.canvas = Border(self, size=3) # don't hard-code size   

        self.canvas.title_1.config(text="Roles Dialog")
        self.canvas.title_2.config(text="Current Person: {}, id #{}".format(
            self.current_name, self.current_person))

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        # DO NOT DELETE THESE LINES, UNCOMMENT IN REAL APP
        # self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
        # self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.window.vsb = Scrollbar(
            self, 
            hideable=True, 
            command=self.canvas.yview,
            width=scridth)
        self.window.hsb = Scrollbar(
            self, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=self.window.hsb.set, 
            yscrollcommand=self.window.vsb.set)
        self.window.vsb.grid(column=2, row=4, sticky='ns')
        self.window.hsb.grid(column=1, row=5, sticky='ew')

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, minsize=60)
        self.frm = Frame(self.window)
        self.frm.grid(column=1, row=2, sticky='news', pady=12)
        self.frm.columnconfigure(0, weight=1)
        show_message()
        self.make_inputs()

        visited = (
            (self.header_msg, 
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
            self.canvas.statusbar.status_label, 
            self.canvas.statusbar.tooltip_label)

        rcm_widgets = (
            self.role_type_input, self.person_input, self.add_butt, 
            self.done_butt, self.close_butt)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            role_dlg_msg)

        config_generic(self) 

        resize_scrolled_content(self, self.canvas, self.window)

    def make_inputs(self):

        self.rolfrm = Frame(self.window)
        new_roles_area = Frame(self.window)

        self.make_roles_table()

        new_roles_header = LabelH3(new_roles_area, text='Create New Role')

        self.role_type_input = Combobox(
            new_roles_area, self.root, values=self.role_types)

        self.person_input = EntryAutoHilited(
            new_roles_area, width=32, 
            autofill=True, values=self.all_birth_names)
        
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

        self.rolfrm.grid(column=0, row=1, columnspan=2)       
        self.rolfrm.columnconfigure(4, weight=1)
        new_roles_area.grid(column=0, row=2)

        new_roles_header.grid(column=0, row=0, padx=6, pady=(18,6))

        self.role_type_input.grid(column=0, row=1, padx=(24,6), pady=6)
        self.person_input.grid(column=1, row=1, padx=6, pady=6)
        self.add_butt.grid(column=2, row=1, padx=6, pady=6)
        self.done_butt.grid(column=3, row=1, padx=6, pady=6)
        self.close_butt.grid(column=4, row=2, padx=(6,24), pady=(6,24))

        self.make_edit_row()
        self.get_role_types()

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
        resize_scrolled_content(self, self.canvas, self.window)

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
            widg.config_values(self.role_types)

    def get_add_state(self):

        if len(self.role_type_input.get()) == 0:
            self.role_type_input.focus_set()
            return
        chosen_role_type = self.role_type_input.get()
        self.user_input_person = self.person_input.get()            
        if chosen_role_type not in self.role_types:
            self.make_new_role_type(chosen_role_type)
        self.make_new_role(chosen_role_type)

    def add_and_close(self):
        self.get_add_state()
        self.close_roles_dialog()

    def close_roles_dialog(self, evt=None):
        self.destroy()

    def make_edit_row(self):

        def cancel_edit_row():
            self.edit_row.grid_remove()
            resize_scrolled_content(self, self.canvas, self.window)

        self.edit_row = Frame(self.rolfrm)

        self.edit_role_type = Combobox(
            self.edit_row, self.root, values=self.role_types)

        self.edit_role_person = EntryAutoHilited(self.edit_row, width=32, 
            autofill=True, values=self.all_birth_names)

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

    def delete_role(self):

        def delete_role_from_db():

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
        resize_scrolled_content(self, self.canvas, self.window)

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

        resize_scrolled_content(self, self.canvas, self.window)
        # self.resize_scrollbar()
        # self.resize_window()

        self.get_role_types()
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
        resize_scrolled_content(self, self.canvas, self.window)
        self.make_roles_list()

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
        cur.execute(
            update_findings_roles_person, (new_person_id, self.edited_role_id))
        conn.commit()
        cur.close()
        conn.close()

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 2:
                    child.config(text=new_person_name)
        # self.resize_scrollbar()
        # self.resize_window()
        resize_scrolled_content(self, self.canvas, self.window)
        self.make_roles_list()

# DO LIST
# TEST:
# make new role
# edit existing role person and/or role type
# make new role type
# make new role person
# delete a role
