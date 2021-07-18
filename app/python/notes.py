# notes.py (import as notes)

import tkinter as tk
import sqlite3
from widgets import (
    LabelButtonText, Toplevel, LabelH3, Button, Frame, LabelFrame, 
    Radiobutton, Entry, Label, StatusbarTooltips,
    run_statusbar_tooltips, LabelMovable)
from scrolling import ScrolledText
from messages import ErrorMessage
from styles import make_formats_dict, ThemeStyles
from names import get_name_with_id
from right_click_menu import make_rc_menus, RightClickMenu
from message_strings import note_dlg_msg
from utes import center_window, create_tooltip
from custom_listbox_widget import Listbox
from files import get_current_file, current_file
from query_strings import (
    update_note, select_count_subtopic, insert_note, insert_findings_notes,
    select_notes_refresh, update_note_private, update_note_subtopic,
    select_private_note, delete_findings_notes, select_count_findings_notes_note_id,
    delete_note, select_count_findings_notes_finding_id, select_note_id,
    update_findings_notes,     
    
)
import dev_tools as dt



formats = make_formats_dict()
# current_file = get_current_file()[0]
ST = ThemeStyles()

class NotesDialog(Toplevel):
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

        self.birth_name = get_name_with_id(current_person)
        self.title('{} ({})'.format('Notes for an Event', self.birth_name))

        self.current_person = current_person
        self.root = master
        self.finding_id = finding_id
        self.header = header
        self.pressed = pressed

        # self.self.new_index = None
        self.current_note_text = ''
        self.current_subtopic = ''
        self.current_note_id = None
        self.new_subtopic_label_text = 'New Note'
        self.current_subtopic_index = None
        self.new_subtopic_name = ''

        self.current_file = get_current_file()[0]

        self.bind('<Escape>', self.close_roles_dialog)
        self.subtopics = []

        self.privacy = tk.IntVar()
        
        self.refresh_notes_per_finding()
        self.rc_menu = RightClickMenu(self.root)
        self.make_widgets()
        self.protocol('WM_DELETE_WINDOW', self.close_roles_dialog)

    def make_widgets(self):

        self.title('{}{} ({})'.format(
            'Notes for Conclusion #', 
            self.finding_id,
            self.birth_name))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        header = Frame(self)
        header.grid_columnconfigure(1, weight=1)
        header.grid_rowconfigure(0, weight=1)

        self.notes_dialog_header = Frame(header)

        content = Frame(self)

        left_panel = Frame(content)

        topiclab = Label(left_panel, text='Note Subtopics')

        self.toc = Listbox(
            left_panel,
            self.sorted_subtopics,
            view_height=424, 
            view_width=180,
            scrollbar=False)

        self.new_index = len(self.subtopics)
        self.toc.insert(self.new_index, self.new_subtopic_label_text)
        self.toc.focus_set()
        self.toc.selection_set(0)
        
        self.toc.store_new_subtopic_name = self.store_new_subtopic_name
        self.toc.pass_ctrl_click = self.open_links_dialog
        self.toc.pass_delete_key = self.delete_note

        self.selected_subtopic = Label(content, text='New Note')        

        self.note_input = ScrolledText(content)

        note_submit = Button(
            content, 
            text='Submit Changes',
            command=self.save_changes)

        order = Button(
            content, 
            text='Change Order of Subtopics', 
            command=self.reorder_notes)

        radframe = LabelFrame(content, text='Make selected note...')

        self.public = Radiobutton(
            radframe, 
            text='...public', 
            anchor='w',
            variable=self.privacy,
            value=0,
            command=self.save_privacy_setting)

        self.private = Radiobutton(
            radframe, 
            text='...private', 
            anchor='w',
            variable=self.privacy,
            value=1,
            command=self.save_privacy_setting)

        close = Button(content, text='DONE', command=self.close_roles_dialog)

        # notes_statusbar = StatusbarTooltips(self)

        # visited = (
            # (above, 
                # 'this is a notes_statusbar message', 
                # 'this is a tooltip'), 
            # (below, 
                # 'this is also a notes_statusbar message', 
                # 'this is another tooltip'))

        # run_statusbar_tooltips(
            # visited, 
            # notes_statusbar.status_label, 
            # notes_statusbar.tooltip_label)

        # grid in self
        header.grid(column=0, row=0, columnspan=2, pady=12, sticky='we')
        content.grid(column=0, row=1, sticky='news', padx=(0,6))
        # notes_statusbar.grid(column=0, row=2, sticky='ew')

        # grid in header
        self.notes_dialog_header.grid(column=1, row=0, sticky='ew')
        self.notes_dialog_header.grid_columnconfigure(0, weight=1)

        # grid in content
        left_panel.grid(
            column=0, row=1, sticky='news', 
            rowspan=2, pady=24)
        self.selected_subtopic.grid(column=1, row=1, sticky='w')
        self.note_input.grid(
            column=1, row=2, columnspan=3, sticky='nsew', padx=(0,24), pady=12)
        note_submit.grid(column=3, row=3, sticky='se')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        order.grid(column=1, row=4)
        radframe.grid(column=2, row=5, sticky='n', pady=24)
        close.grid(column=3, row=6, sticky='se', padx=24, pady=(0,24))

        # grid in left_panel
        topiclab.grid(column=0, row=0)
        self.toc.grid(column=0, row=1)
        for child in self.toc.listbox_content.winfo_children():        
            child.bind('<<ListboxSelected>>', self.switch_note)

        self.subtopic_widgets = self.toc.listbox_content.winfo_children()

        # grid in radframe
        self.public.grid(column=0, row=0, sticky='news', padx=24)
        self.private.grid(column=0, row=1, sticky='news', padx=24)

        # rcm_widgets = (self.subtopic_input, self.note_input.text)
        # make_rc_menus(
            # rcm_widgets, 
            # self.rc_menu, 
            # note_dlg_msg,
            # header_parent=self.notes_dialog_header, 
            # header=self.header, 
            # which_dlg='notes')

        ST.config_generic(self) 
        center_window(self)

    def open_links_dialog(self):
        links = Toplevel(self.root)
        links.title('Link Notes to Multiple Entities')
        instrux = LabelH3(
            links, 
            text='The current note can be linked to any number of Entities\n'
                'such as Persons, Places, Assertions, Conclusions, or Sources.')
        instrux.grid(padx=24, pady=24)

    def save_changes(self):

        self.save_new_subtopic()

        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        new_note_text = self.note_input.text.get(1.0, 'end-1c')
        subtopic = self.current_subtopic
        cur.execute(update_note, (new_note_text, subtopic))
        conn.commit()
        cur.close()
        conn.close()

        self.master.current_note_text = new_note_text
        self.refresh()

    def save_new_subtopic(self):
        if self.selected_subtopic.cget('text') != self.new_subtopic_label_text:
            return
        self.subtopic_dialog = Toplevel(self.root)
        self.subtopic_dialog.title('New Note: Subtopic Input Dialog')
        headlab = LabelH3(self.subtopic_dialog, text='Unique subtopic name for new note:')
        self.subtopic_input = Entry(self.subtopic_dialog, width=64)
        self.subtopic_input.focus_set()
        buttonbox = Frame(self.subtopic_dialog)
        self.subtopic_dialog.grid_columnconfigure(0, weight=1)
        new_note_ok = Button(
            buttonbox, 
            text='Submit Note and Subtitle', 
            command=self.submit_new_note)
        new_note_cancel = Button(
            buttonbox, text='Cancel', command=self.close_subtopic_dialog)

        headlab.grid(column=0, row=0, pady=(24,0), columnspan=2)
        self.subtopic_input.grid(column=0, row=1, padx=24, pady=24, columnspan=2)
        buttonbox.grid(column=1, row=2, sticky='we', padx=24, pady=24)
        new_note_ok.grid(column=0, row=0, sticky='e', padx=12)
        new_note_cancel.grid(column=1, row=0, sticky='e', padx=12)

        self.subtopic_dialog.bind('<Escape>', self.close_subtopic_dialog)
        self.subtopic_dialog.protocol('WM_DELETE_WINDOW', self.close_subtopic_dialog)

    def submit_new_note(self):
        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        new_note_text = self.note_input.text.get(1.0, 'end-1c')
        new_subtopic = self.subtopic_input.get()
        cur.execute(select_count_subtopic, (new_subtopic,))
        count = cur.fetchone()[0]
        if count > 0:
            non_unique_subtopic = ErrorMessage(
                self, 
                message="Each subtopic can be\nused once in a tree.")
            non_unique_subtopic.title('Non-unique Note Title Error')
            self.subtopic_input.focus_set()            
            return

        if len(new_subtopic) == 0:
            blank_subtopic = ErrorMessage(
                self, 
                message="Blank notes are OK\n"
                    "but not blank note titles.")
            blank_subtopic.title('Blank Note Title Error')
            self.subtopic_input.focus_set()
            return
        cur.execute(insert_note, (new_note_text, new_subtopic))
        conn.commit()
        cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'note'")
        new_note_id = cur.fetchone()[0]
    
        cur.execute(
            insert_findings_notes, 
            (self.finding_id, new_note_id, self.new_index))
        conn.commit()
        cur.close()
        conn.close()

        self.master.current_note_text = new_note_text
        self.refresh_notes_per_finding()
        self.toc.insert(self.new_index, new_subtopic)
        items = self.toc.listbox_content.winfo_children()
        for child in items: 
            child.bind('<<ListboxSelected>>', self.switch_note)
        self.toc.resize_scrollbar()
        self.toc.selection_set(self.new_index)
        self.switch_note()
        self.pressed.config(text=' ... ')
        self.new_index = len(self.subtopics)
        self.close_subtopic_dialog()
        self.refresh()

    def refresh_notes_per_finding(self):
        conn = sqlite3.connect(self.current_file)
        cur = conn.cursor()
        cur.execute(select_notes_refresh, (self.finding_id,))
        notes = cur.fetchall()
        all_subtopics = []
        if len(notes) != 0:
            for tup in notes:
                all_subtopics.append([tup[1], tup[3]])
        all_subtopics.sort(key=lambda i: i[1])
        self.sorted_subtopics = []
        for lst in all_subtopics:
            self.sorted_subtopics.append(lst[0])

        self.subtopics = self.sorted_subtopics
        self.notesdict = {}
        for tup in notes:
            self.notesdict[tup[0]] = [tup[1], tup[2]]
        cur.close()
        conn.close()

    def close_roles_dialog(self, evt=None):
        self.destroy()
        self.master.focus_set()

    def close_subtopic_dialog(self, evt=None):
        self.subtopic_dialog.destroy()

    def save_privacy_setting(self):
        privacy_setting = self.privacy.get()
        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_note_private, (privacy_setting, self.current_note_id))
        conn.commit()
        cur.close()
        conn.close()

    def get_selected_subtopic(self):
        # "is not None" has to be explicit here
        if self.toc.curselection() is not None:
            self.current_subtopic_index = self.toc.curselection()            
        else:
            return
        self.current_subtopic = self.toc.get(self.current_subtopic_index)
        if len(self.notesdict) != 0:
            for k,v in self.notesdict.items():            
                if v[0] == self.current_subtopic:
                    break
            self.current_note_id = k
            self.current_note_text = v[1]

    def store_new_subtopic_name(self):
        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(
            update_note_subtopic, 
            (self.toc.new_subtopic_name, self.current_note_id))
        conn.commit()
        cur.close()
        conn.close()

        self.subtopic_widgets = self.toc.listbox_content.winfo_children()
        for child in self.subtopic_widgets:
            child.bind('<<ListboxSelected>>', self.switch_note)
            if child.winfo_reqwidth() > self.toc.view_width:
                create_tooltip(child, self.toc.new_subtopic_name)

    def switch_note(self, evt=None):
        
        self.get_selected_subtopic()
        if len(self.current_subtopic) == 0:
            return
        self.selected_subtopic.config(text=self.current_subtopic)
        if self.current_subtopic == self.new_subtopic_label_text:
            self.note_input.text.delete(1.0, 'end')
            return
        self.note_input.text.delete(1.0, 'end')
        self.note_input.text.insert(1.0, self.current_note_text) 

        conn = sqlite3.connect(self.current_file)
        cur = conn.cursor()
        cur.execute(
            select_private_note, 
            (self.current_subtopic, self.finding_id))
        privacy_setting = cur.fetchone()

        if privacy_setting:
            privacy_setting = privacy_setting[0]

        cur.close()
        conn.close()

        if privacy_setting is None:
            return
        elif privacy_setting == 0:
            self.public.select()
        elif privacy_setting == 1:
            self.private.select()

    def delete_note(self):
        '''
            Since any given note can be re-used more than once by linking it 
            to any number of findings, delete note from note table only if 
            the note_id no longer exists at all in the findings_notes table; 
            not every time a note_id is deleted from the findings_notes table. 
        '''

        def ok_delete():
            run_delete()
            cancel_delete()

        def cancel_delete():
            self.focus_set()
            deleter.destroy()

        def run_delete():

            note_count_per_finding = 0

            self.toc.delete(selected)
            self.note_input.text.delete(1.0, 'end')
            self.selected_subtopic.config(text='')
            cur.execute(delete_findings_notes, (deletable, self.finding_id))
            conn.commit()

            if delete_var.get() == 1:
                cur.execute(select_count_findings_notes_note_id, (deletable,))
                linked_notes = cur.fetchone()[0]

                if linked_notes == 0:
                    cur.execute(delete_note, (deletable,))
                    conn.commit()
                cur.execute(
                    select_count_findings_notes_finding_id, 
                    (self.finding_id,))
                note_count_per_finding = cur.fetchone()[0]

            cur.close()
            conn.close()

            self.toc.selection_clear()

            if note_count_per_finding == 0:
                self.pressed.config(text='     ')        

            self.refresh()

        selected = self.toc.curselection()
        subtopic = self.toc.get(selected)
        if subtopic is None:
            return

        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_note_id, (subtopic,))
        deletable = cur.fetchone()
        if deletable is None:
            return
        elif deletable is not None:
            deletable = deletable[0]

        delete_var = tk.IntVar()

        deleter = Toplevel(self)
        deleter.title('Delete Note Dialog')
        
        instrux = LabelH3(
            deleter, 
            text='Any note can be linked to any number of entities.')

        radio1 = Radiobutton(
            deleter,
            text='Delete this instance of this note.',
            value=0,
            variable=delete_var)

        radio2 = Radiobutton(
            deleter,
            text='Delete all instances of this note.',
            value=1,
            variable=delete_var)

        instrux.grid(column=0, row=0, columnspan=2, padx=24, pady=24)
        radio1.grid(column=0, row=1)
        radio2.grid(column=1, row=1)

        buttonbox = Frame(deleter)
        buttonbox.grid(column=1, row=2, sticky='e')
        b1 = Button(buttonbox, text='OK', command=ok_delete)
        b2 = Button(buttonbox, text='Cancel', command=cancel_delete)
        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0)

    def refresh(self):

        self.refresh_notes_per_finding()
        self.toc.make_listbox_content()
        self.subtopic_widgets = self.toc.listbox_content.winfo_children()
        for child in self.subtopic_widgets:
            child.bind('<<ListboxSelected>>', self.switch_note)

    def reorder_notes(self):
        '''
        '''
        if self.toc.size() < 2:
            return

        self.order_dlg = Toplevel(self)
        self.order_dlg.grab_set()
        self.order_dlg.protocol('WM_DELETE_WINDOW', self.ignore_changes)
        self.order_dlg.bind('<Return>', self.save_close_reorder_dlg)
        self.order_dlg.bind('<Escape>', self.ignore_changes)
        self.order_dlg.grid_columnconfigure(0, weight=1)
        self.order_dlg.title('Reorder Subtopics')

        instrux = (
            'Tab or Ctrl+Tab selects movable subtopic.\n'
            'Arrow keys change subtopic order up or down.')
         
        top = LabelH3(self.order_dlg, text=instrux, anchor='center')

        self.labels = Frame(self.order_dlg)

        e = 0
        for subtopic in self.subtopics:           
            lab = LabelMovable(self.labels, text=subtopic, anchor='w')
            if e == 0:
                first = lab
            e += 1
            lab.grid(column=0, row=e, padx=3, sticky='ew')
        first.focus_set()

        close2 = Button(
            self.order_dlg, 
            text='OK', 
            command=self.save_close_reorder_dlg)

        top.grid(column=0, row=0, pady=(24,0), padx=24, columnspan=2)
        self.labels.grid(column=0, row=1, columnspan=2, padx=24, pady=24)
        self.labels.grid_columnconfigure(0, weight=1)
        close2.grid(column=1, row=2, sticky='se', padx=12, pady=(0,12))

        center_window(self.order_dlg)

    def ignore_changes(self, evt=None):
        self.order_dlg.grab_release()
        self.order_dlg.destroy()
        self.focus_set()

    def save_close_reorder_dlg(self, evt=None):
        '''
            Replace the values list.
        '''

        q = 0
        new_order = []
        save_order = []
        for child in self.labels.winfo_children():
            text = child.cget('text')
            new_order.append(text)
            save_order.append([text, q])
            q += 1

        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        for lst in save_order:
            cur.execute(select_note_id, (lst[0],))
            note_id = cur.fetchone()[0]
            cur.execute(
                update_findings_notes, 
                (lst[1], self.finding_id, note_id))
            conn.commit()
        cur.close()
        conn.close() 
        self.subtopics = self.toc.items = new_order
        self.refresh()
        self.order_dlg.grab_release()
        self.order_dlg.destroy()
        self.focus_set()





