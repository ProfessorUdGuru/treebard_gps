# roles.py

import tkinter as tk
import sqlite3
from files import get_current_file
from widgets import (
    Frame, Toplevel, Label, ButtonQuiet, Border,
    LabelH3, Button, LabelHeader, LabelNegative, Combobox,
    EntryAutoPerson, EntryAutoPersonHilited, Scrollbar, open_message,
    configall, make_formats_dict)
from right_click_menu import RightClickMenu, make_rc_menus
from scrolling import resize_scrolled_content
from toykinter_widgets import run_statusbar_tooltips  
from messages import roles_msg
from messages_context_help import roles_dlg_help_msg, role_edit_help_msg
from persons import ( 
    make_all_names_dict_for_person_select, check_name, get_original,
    update_person_autofill_values, open_new_person_dialog)
from query_strings import (
    select_roles, select_role_types, select_role_type_id,
    update_findings_roles_role_type, update_findings_roles_person,
    insert_findings_roles, delete_findings_role,
    select_count_findings_roles, insert_role_type)

import dev_tools as dt
from dev_tools import looky, seeline





class RolesDialog(Toplevel):
    def __init__(
            self, master, finding_id, header, current_person, treebard,
            pressed=None, person_autofill_values=None, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.root = master
        self.finding_id = finding_id
        self.header = header
        self.current_person = current_person
        self.treebard = treebard
        self.pressed = pressed
        self.person_autofill_values = person_autofill_values

        self.formats = make_formats_dict()

        self.role_types = []
        
        self.roles_per_finding = []

        self.widget = None
        self.idtip = None
        self.idtip_text = None
        self.idtip_bindings = {"on_enter": [], "on_leave": []}
        self.person_inputs = []

        self.current_name = self.person_autofill_values[self.current_person][0]["name"]

        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)
        self.make_widgets()

    def make_widgets(self):

        def show_message():
            self.header = "\n".join(self.header)
            header_text = "Roles for Conclusion #{}: {}".format(
                self.finding_id, self.header)
            self.window.columnconfigure(0, weight=1)
            self.window.rowconfigure(0, weight=1)
            self.header_msg = LabelHeader(self.window, text=header_text)
            self.header_msg.grid(
                column=0, row=0, sticky='news', 
                ipadx=12, ipady=12, padx=(24,0), pady=18)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        self.canvas = Border(self, self.root)

        self.canvas.title_1.config(text="Roles Dialog")
        self.canvas.title_2.config(text="Current Person: {}, id #{}".format(
            self.current_name, self.current_person))

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
      
        self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

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
        show_message()
        self.make_inputs()
        EntryAutoPerson.person_autofills.extend(
            [self.person_input, self.edit_role_person_input])

        visited = (
            (self.header_msg, 
                '', 
                'Event-type, date, place & particulars of this conclusion if known.'),
            (self.edit_role_type, 
                'Edit Role Type Input', 
                'Existing role type can be changed to a different type.'), 
            (self.edit_role_person_input, 
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
                'Select role person or add new person.'),
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
            self.role_type_input.entry, self.person_input, self.add_butt, 
            self.done_butt, self.close_butt)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            roles_dlg_help_msg)

        configall(self, self.formats)

        resize_scrolled_content(self, self.canvas, self.window)

    def make_inputs(self):

        self.rolfrm = Frame(self.window)
        new_roles_area = Frame(self.window)
        self.make_roles_table()

        new_roles_header = LabelH3(new_roles_area, text='Create New Role')

        self.role_type_input = Combobox(
            new_roles_area, self.root, values=self.role_types)

        self.person_input = EntryAutoPersonHilited(
            new_roles_area, width=32, 
            autofill=True, values=self.person_autofill_values) 
        self.person_input.bind("<FocusIn>", get_original, add="+")
        
        self.add_butt = Button(
            new_roles_area, 
            text='ADD',
            command=self.get_add_state)
        self.done_butt = Button(
            new_roles_area,
            text='DONE',
            command=self.add_and_close)
        self.close_butt = Button(
            new_roles_area,
            text='CANCEL',
            command=self.close_roles_dialog)
        self.bind('<Escape>', self.close_roles_dialog)

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

        self.make_idtips()

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
            if type(lst[2]) is tuple:
                lst[2] = "({}) {}".format(lst[2][1], lst[2][0])
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
            self.rc_menu.loop_made[editx] = role_edit_help_msg
            n += 1
        if first_butt:
            first_butt.focus_set()

    def make_roles_list(self):

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_roles, (self.finding_id,))
        roles_per_finding = cur.fetchall()
        if roles_per_finding:
            self.roles_per_finding = [list(i) for i in roles_per_finding]

        for lst in self.roles_per_finding:
            iD = lst[2]
            name = self.person_autofill_values[iD][0]["name"]
            lst.append(iD)
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
                    print("line", looky(seeline()).lineno, "self.original_role_person:", self.original_role_person)
        self.edit_row.grid(row=self.got_row)

        self.edit_role_type.delete(0, 'end')
        self.edit_role_person_input.delete(0, 'end')
        self.edit_role_type.insert(0, self.roles_per_finding[self.got_row][1])
        self.edit_role_type.focus_set()

        chosen_person_id = self.roles_per_finding[self.got_row][4]
        if chosen_person_id is None:
            self.edit_role_person_input.insert(0, '')

        else:
            self.edit_role_person_input.insert(0, self.roles_per_finding[self.got_row][2])

        self.edit_row.lift()
        resize_scrolled_content(self, self.canvas, self.window)

    def get_role_types(self):
        current_file = get_current_file()[0]
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
        for widg in (self.role_type_input.entry, self.person_input):
            if len(widg.get()) == 0:
                widg.focus_set()
                return
        chosen_role_type = self.role_type_input.get()
        self.user_input_person = self.person_input.get() 
        if chosen_role_type not in self.role_types:
            chosen_role_type = self.make_new_role_type(chosen_role_type)
        self.make_new_role(chosen_role_type)

    def make_new_role_type(self, new_role_type):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(insert_role_type, (new_role_type,))
        conn.commit()
        cur.close()
        conn.close()
        return new_role_type

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

        self.edit_role_person_input = EntryAutoPersonHilited(
            self.edit_row, width=32, 
            autofill=True, values=self.person_autofill_values)  
        self.edit_role_person_input.bind("<FocusIn>", get_original, add="+")

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
        self.edit_role_person_input.grid(column=1, row=0, padx=6, pady=6)
        self.ok_butt.grid(column=2, row=0, padx=6, pady=6)
        self.cancel_butt.grid(column=3, row=0, padx=6, pady=6)
        self.delete_butt.grid(column=4, row=0, padx=6, pady=6)
        self.edit_row.grid_remove()

    def make_new_role(self, role_type):

        def err_done2(entry, msg2):
            entry.delete(0, 'end')
            msg2[0].grab_release()
            msg2[0].destroy()
            entry.focus_set()

        if len(self.user_input_person) == 0: 
            self.person_input.focus_set()
            return

        name_data = check_name(ent=self.person_input)

        if name_data is None:
            msg2 = open_message(
                self, 
                roles_msg[0], 
                "Person Name Unknown", 
                "OK")
            msg2[0].grab_set()
            msg2[2].config(
                command=lambda entry=self.edit_role_person_input, msg=msg2: err_done2(
                    entry, msg))
            return
        elif name_data == "add_new_person":
            role_person_id = open_new_person_dialog(
                self, self.person_input, self.root, self.treebard, 
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
        else:
            role_person_id = name_data[1]

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_role_type_id, (role_type,))
        role_type_id = cur.fetchone()[0]
        cur.execute(
            insert_findings_roles, 
            (self.finding_id, role_type_id, role_person_id))
        conn.commit()
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
        cur.close()
        conn.close()

    def get_edit_state(self):
        """ Detect and respond to changes in existing roles on OK button.
        """
        def err_done1(entry, msg):
            entry.delete(0, 'end')
            msg[0].grab_release()
            msg[0].destroy()
            entry.focus_set()

        edited_role_type = self.edit_role_type.get()
        if edited_role_type in self.role_types:
            if edited_role_type != self.original_role_type:
                self.update_role_type(edited_role_type)
        else:
            self.make_new_role_type(edited_role_type)
            self.update_role_type(edited_role_type)

        edited_role_person = self.edit_role_person_input.get()

        name_data = check_name(ent=self.edit_role_person_input)
        if name_data == "add_new_person":
            role_person_id = open_new_person_dialog(
                self, self.edit_role_person_input, self.root, self.treebard,  
                person_autofill_values=self.person_autofill_values)
            self.person_autofill_values = update_person_autofill_values()
            self.change_role_person(edited_role_person, role_person_id)
        elif name_data is None:
            msg1 = open_message(
                self, 
                roles_msg[0], 
                "Person Name Unknown", 
                "OK")
            msg1[0].grab_set()
            msg1[2].config(
                command=lambda entry=self.edit_role_person_input, msg=msg1: err_done1(
                    entry, msg))
            return
        else:
            role_person_id = name_data[1]
            new_name = self.person_autofill_values[role_person_id][0]["name"]                    
            self.change_role_person(new_name, role_person_id)

        self.original_role_type = edited_role_type
        self.original_role_person = edited_role_person
        self.edit_row.grid_remove()

    def delete_role(self):

        def delete_role_from_db():
            nonlocal role_count_per_finding  
            current_file = get_current_file()[0]
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(delete_findings_role, (self.edited_role_id,))
            conn.commit()
            cur.execute(select_count_findings_roles, (self.finding_id,))
            role_count_per_finding = cur.fetchone()[0]

            self.make_roles_list()
            cur.close()
            conn.close()

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
        current_file = get_current_file()[0]
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

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 0:
                    child.config(text=edited_role_type)

        resize_scrolled_content(self, self.canvas, self.window)

        self.get_role_types()
        self.make_roles_list()
        cur.close()
        conn.close()

    def change_role_person(self, new_person_name, new_person_id):
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(
            update_findings_roles_person, (new_person_id, self.edited_role_id))
        conn.commit()

        for child in self.rolfrm.winfo_children():
            if child.winfo_class() == 'Frame':
                pass
            elif child.grid_info()['row'] == self.got_row:
                if child.grid_info()['column'] == 2:
                    print("line", looky(seeline()).lineno, "new_person_name:", new_person_name)
                    child.config(text=new_person_name.strip("+"))
        resize_scrolled_content(self, self.canvas, self.window)
        self.make_roles_list()
        cur.close()
        conn.close()

    def show_idtip(self, iD, name_type):
        """Based on show_idtip() in families.py."""
        maxvert = self.winfo_screenheight()

        if self.idtip or not self.idtip_text:
            return
        x, y, cx, cy = self.widget.bbox('insert')        

        self.idtip = d_tip = Toplevel(self.widget)
        label = LabelNegative(
            d_tip, 
            text=self.idtip_text, 
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
        d_tip = self.idtip
        self.idtip = None
        if d_tip:
            d_tip.destroy()

    def handle_enter(self, evt):
        row = evt.widget.master.grid_info()['row']
        iD, name_type = self.person_inputs[row][1:]
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

        row = 0
        for lst in self.roles_per_finding:
            iD = lst[4]
            name_type = self.person_autofill_values[iD][0]["name type"]
            widg = self.edit_role_person_input
            self.person_inputs.append((widg, iD, name_type))
            row += 1

        widg = self.edit_role_person_input
        name_in = widg.bind("<Enter>", self.handle_enter)
        name_out = widg.bind("<Leave>", self.on_leave)
        self.widget = widg
        self.idtip_bindings["on_enter"].append([widg, name_in])
        self.idtip_bindings["on_leave"].append([widg, name_out])


