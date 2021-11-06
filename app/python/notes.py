# notes.py

import tkinter as tk
import sqlite3
from window_border import Border 
from widgets import (
    Toplevel, LabelH3, Button, Frame, LabelFrame, 
    Radiobutton, Entry, Label, LabelMovable, LabelDots, LabelHeader)
from toykinter_widgets import  StatusbarTooltips, run_statusbar_tooltips
from scrolling import ScrolledText, Scrollbar, resize_scrolled_content
from messagesx import ErrorMessage
from messages import open_yes_no_message, notes_msg
from right_click_menu import RightClickMenu, make_rc_menus
from styles import make_formats_dict, config_generic
from names import get_name_with_id
from message_strings import note_dlg_msg
from utes import center_window, create_tooltip
from custom_listbox_widget import Listbox
from files import current_file
from query_strings import (
    update_note, select_count_subtopic, insert_note, insert_findings_notes,
    select_notes_refresh, update_note_private, update_note_subtopic,
    select_private_note, delete_findings_notes, select_count_findings_notes_note_id,
    delete_note, select_count_findings_notes_finding_id, select_note_id,
    update_findings_notes,     
    
)
import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

class NotesDialog(Toplevel):
    def __init__(
            self, master, finding_id, header, current_person, 
            pressed=None, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.current_person = current_person
        self.root = master
        self.finding_id = finding_id
        self.header = header
        self.pressed = pressed

        self.current_note_text = ''
        self.current_subtopic = ''
        self.current_note_id = None
        self.new_subtopic_label_text = 'New Note'
        self.current_subtopic_index = None
        self.new_subtopic_name = ''

        self.current_name = get_name_with_id(self.current_person)

        self.bind('<Escape>', self.close_notes_dialog)
        self.subtopics = []

        self.privacy = tk.IntVar()
        
        self.refresh_notes_per_finding()
        self.rc_menu = RightClickMenu(self.root)
        self.make_widgets()
        self.geometry("+100+20")

    def make_widgets(self):

        def show_message():
            self.header = "\n".join(self.header)
            header_text = "Notes for Conclusion #{}: {}".format(
                self.finding_id, self.header)
            self.header_msg = LabelHeader(
                self.window,
                text=header_text)
            self.header_msg.grid(
                column=0, row=0, sticky='news', columnspan=4, 
                ipadx=12, ipady=12, padx=(24,0), pady=18)

        self.canvas = Border(self)

        self.canvas.title_1.config(text="Notes Dialog")
        self.canvas.title_2.config(text="Current Person: {}, id #{}".format(
            self.current_name, self.current_person))

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
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
        show_message()

        self.make_inputs()

        config_generic(self) 

        resize_scrolled_content(self, self.canvas, self.window)

    def make_inputs(self):

        left_panel = Frame(self.window)

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

        self.selected_subtopic = Label(self.window, text='New Note')        

        self.note_input = ScrolledText(self.window)

        note_submit = Button(
            self.window, 
            text='SUBMIT CHANGES',
            command=self.save_changes)

        order = Button(
            self.window, 
            text='CHANGE ORDER OF SUBTOPICS', 
            command=self.reorder_notes)

        radframe = LabelFrame(self.window, text='Make selected note...')

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

        close = Button(self.window, text='DONE', command=self.close_notes_dialog)

        visited = (
            (self.toc, 
                'this is a notes_statusbar message', 
                'this is a tooltip'), 
            (note_submit, 
                'this is also a notes_statusbar message', 
                'this is another tooltip'))

        run_statusbar_tooltips(
            visited, 
            self.canvas.statusbar.status_label, 
            self.canvas.statusbar.tooltip_label)

        # rcm_widgets = (self.subtopic_input, self.note_input.text)
        # make_rc_menus(
            # rcm_widgets, 
            # self.rc_menu, 
            # note_dlg_msg)

        # grid in self.window
        left_panel.grid(
            column=0, row=1, sticky='s', 
            rowspan=2, padx=(24,6))
        self.selected_subtopic.grid(column=1, row=1, sticky='w', columnspan=3)
        self.note_input.grid(
            column=1, row=2, columnspan=3, sticky='nsew', padx=(0,24))
        note_submit.grid(column=3, row=4, sticky='e', padx=(0,24))
        order.grid(column=0, row=4, columnspan=2, sticky='w', padx=(24,0))
        radframe.grid(column=2, row=4, pady=(24,0))
        close.grid(column=3, row=5, sticky='e', padx=24)

        # grid in left_panel
        topiclab.grid(column=0, row=0)
        self.toc.grid(column=0, row=1)
        for child in self.toc.listbox_content.winfo_children():        
            child.bind('<<ListboxSelected>>', self.switch_note)

        self.subtopic_widgets = self.toc.listbox_content.winfo_children()

        # grid in radframe
        self.public.grid(column=0, row=0, sticky='news', padx=24)
        self.private.grid(column=0, row=1, sticky='news', padx=24)

        config_generic(self) 
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

        conn = sqlite3.connect(current_file)
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
        headlab = LabelH3(
            self.subtopic_dialog, text='Unique subtopic name for new note:')
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
        self.subtopic_dialog.protocol(
            'WM_DELETE_WINDOW', self.close_subtopic_dialog)

    def submit_new_note(self):
        conn = sqlite3.connect(current_file)
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
        conn = sqlite3.connect(current_file)
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

    def close_notes_dialog(self, evt=None):
        self.destroy()
        self.master.focus_set()

    def close_subtopic_dialog(self, evt=None):
        self.subtopic_dialog.destroy()

    def save_privacy_setting(self):
        privacy_setting = self.privacy.get()
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_note_private, (privacy_setting, self.current_note_id))
        conn.commit()
        cur.close()
        conn.close()

    def get_selected_subtopic(self):
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
        conn = sqlite3.connect(current_file)
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

        conn = sqlite3.connect(current_file)
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
            msg[0].destroy()

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

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_note_id, (subtopic,))
        deletable = cur.fetchone()
        if deletable is None:
            return
        elif deletable is not None:
            deletable = deletable[0]

        delete_var = tk.IntVar()

        msg = open_yes_no_message(
            self, 
            notes_msg[0], 
            "Delete Note Dialog", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(command=ok_delete)
        msg[3].config(command=cancel_delete)

        radio1 = Radiobutton(
            msg[0],
            text='Delete this instance of this note.',
            value=0,
            variable=delete_var)

        radio2 = Radiobutton(
            msg[0],
            text='Delete all instances of this note.',
            value=1,
            variable=delete_var)

        radio1.grid(column=0, row=1)
        radio2.grid(column=1, row=1)

        msg[4].grid(column=1, row=2, sticky='e', padx=(0,12), pady=12)

    def refresh(self):

        self.refresh_notes_per_finding()
        self.toc.make_listbox_content()
        self.subtopic_widgets = self.toc.listbox_content.winfo_children()
        for child in self.subtopic_widgets:
            child.bind('<<ListboxSelected>>', self.switch_note)

    def reorder_notes(self):

        if self.toc.size() <= 2:
            return

        self.order_dlg = Toplevel(self)
        self.order_dlg.grab_set()
        self.order_dlg.protocol('WM_DELETE_WINDOW', self.ignore_changes)
        self.order_dlg.bind('<Return>', self.save_close_reorder_dlg)
        self.order_dlg.bind('<Escape>', self.ignore_changes)
        self.order_dlg.grid_columnconfigure(0, weight=1)
        self.order_dlg.title('Reorder Subtopics')

        instrux = (
            'Tab or Shift + Tab selects movable subtopic.\n'
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

        conn = sqlite3.connect(current_file)
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
