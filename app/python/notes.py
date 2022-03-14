# notes.py

import tkinter as tk
import sqlite3
from scrolling import Scrollbar, ScrolledText, resize_scrolled_content
from window_border import Border, Dialogue
from widgets import (
    Label, Button, Entry, Canvas, LabelFrame, LabelH3, FrameHilited6,
    LabelMovable, Toplevel, LabelHeader, Radiobutton, Frame)
from custom_combobox_widget import Combobox
from autofill import EntryAutoHilited, EntryAutoPersonHilited
from toykinter_widgets import run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from messages_context_help import notes_dlg_help_msg, links_dlg_help_msg
from styles import config_generic
from places import make_all_nestings    
from messages import (
    open_yes_no_message, notes_msg, open_message, InputMessage)
from utes import center_dialog, create_tooltip, OK_PRINT_KEYS
from files import get_current_file
from links import ELEMENTS
from query_strings import (
    insert_note, update_note_privacy, select_note_privacy, select_note_id,
    update_note_edit, update_findings_notes, insert_findings_notes_new,
    update_findings_notes_order, select_findings_notes_order, 
    select_notes_per_finding, select_notes_linked, select_all_place_ids,
    delete_findings_notes_linked, update_note_topic,
)
import dev_tools as dt
from dev_tools import looky, seeline





class NotesDialog(Toplevel):
    ''' `toc` means Table of Contents. '''

    def __init__(
            self, master, finding, header, current_person, treebard, 
            formats, pressed=None, person_autofill_values=None, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.root = master
        self.finding = finding
        self.header = header
        self.current_person = current_person
        self.treebard = treebard
        self.formats = formats
        self.pressed = pressed
        self.person_autofill_values = person_autofill_values

        self.current_file = get_current_file()[0]
        self.selected = None
        self.topics = []
        self.notes = []

        # self.current_name = get_name_with_id(self.current_person)
        self.current_name = self.person_autofill_values[self.current_person]["birth name"]
        if self.current_name is None or len(self.current_name) == 0:
            self.current_name = self.person_autofill_values[self.current_person]["alt name"]

            

        self.privacy = tk.IntVar()
        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        # self.formats = make_formats_dict()

        self.autoscroll_on_arrow = False

        self.make_widgets()
        self.make_containers()
        self.make_toc_scrollable()
 
        self.make_inputs()

        # 20 characters * font size but shouldn't hard-code font-size 12 
        #   (had to change to 11 anyway)   
        self.toc_width = 20 * 11     
        self.make_table_of_contents() 
        self.size_toc() 


        config_generic(self)
        resize_scrolled_content(self, self.canvas, self.window)
        center_dialog(self, frame=self.window)


        self.bind_class('Label', '<Tab>', self.stop_tab_traversal1)
        self.bind_class('Label', '<Shift-Tab>', self.stop_tab_traversal2)

        for widg in (self.note_header, self.order, self.linker, self.public, 
                self.private, self.close):
            widg.bind("<Key-Up>", self.focus_topicslist)
            widg.bind("<Key-Down>", self.focus_topicslist)

        self.bind('<Escape>', self.close_notes_dialog)

    def make_widgets(self):

        self.canvas = Border(self, self.root, self.formats)

        self.canvas.title_1.config(text="Notes Dialog")
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

    def make_containers(self):
        self.header = "\n".join(self.header)
        header_text = "Notes for Conclusion #{}: {}".format(
            self.finding, self.header)
        self.header_msg = LabelHeader(self.window, text=header_text)
        self.left_panel = FrameHilited6(self.window)
        self.right_panel = Frame(self.window)
        self.bottom_panel = Frame(self.window)

        self.header_msg.grid(
            column=1, row=1, sticky='news', columnspan=2, 
            ipadx=12, ipady=12)
        self.left_panel.grid(column=1, row=2)
        self.right_panel.grid(column=2, row=2)
        self.bottom_panel.grid(column=1, row=3, sticky='news', columnspan=2)

    def make_inputs(self):
        self.toc_head = LabelH3(self.left_panel, text="TABLE OF CONTENTS")
        self.note_header = Entry(self.right_panel, width=36)
        self.note = ScrolledText(self.right_panel)

        self.order = Button(
            self.bottom_panel, 
            text='CHANGE ORDER OF TOPICS', 
            command=self.reorder_notes)
        radframe = LabelFrame(self.bottom_panel, text='Make selected note...')
        self.linker = Button(
            self.bottom_panel, 
            text='LINK TO...',
            command=self.add_links)
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
        self.close = Button(
            self.bottom_panel, text='DONE', command=self.close_notes_dialog)

        # grid in left_panel
        self.toc_head.grid(column=0, row=0, sticky="news", pady=6)
        # grid in right_panel
        self.note_header.grid(column=0, row=0, sticky="w", padx=(12,0), pady=6)
        self.note.grid(column=0, row=1, padx=(12,0))
        # grid in bottom_panel
        self.bottom_panel.columnconfigure(2, weight=1)
        self.order.grid(column=0, row=0, columnspan=2, sticky='w')
        radframe.grid(column=2, row=0, pady=(12,0))
        self.linker.grid(column=3, row=0, sticky='e')
        self.close.grid(column=3, row=1, sticky='e')
        # grid in radframe
        self.public.grid(column=0, row=0, sticky='news', padx=12)
        self.private.grid(column=0, row=1, sticky='news', padx=12) 

        visited = (
            (self.left_panel, 
                'Table of Contents', 
                'Arrow or click topic to view, rename, or unlink note.'), 
            (self.linker, 
                'Link Button', 
                'Opens dialog to link this note to other elements.'),
            (self.public, 
                'Public Note Option', 
                'Public notes will be shared when sharing tree.'),
            (self.private, 
                'Private Note Option', 
                "Private notes stay on the tree creator's copy of Treebard."),
            (self.order, 
                'Reorder Topics Button', 
                'Press to reorder topics in table of contents.'),
            (self.note.text, 
                'Note Input & Readout', 
                'Create and edit notes of any length.'),
            (self.note_header, 
                'Note Topic Input', 
                'Select, create, or edit a note topic.'),
)

        run_statusbar_tooltips(
            visited, 
            self.canvas.statusbar.status_label, 
            self.canvas.statusbar.tooltip_label)

        rcm_widgets = (
            self.note_header, self.note.text, self.toc_head, self.linker, 
            radframe, self.order)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            notes_dlg_help_msg)

        self.note_header.focus_set()
        self.note_header.bind("<FocusIn>", self.display_note)
        self.note_header.bind("<KeyRelease>", self.display_note)
        self.note.text.bind("<FocusOut>", self.make_new_note)
        self.note_header.bind("<FocusOut>", self.make_new_note)

    def focus_topicslist(self, evt):
        last = self.topiclabs[self.length - 1]
        first = self.topiclabs[0]
        sym = evt.keysym
        if sym == "Up":
            last.focus_set()
            self.selected = last
            self.toc_canvas.yview_moveto(1.0)
        elif sym == "Down":
            first.focus_set()
            self.selected = first
            self.toc_canvas.yview_moveto(0.0)
        self.display_note()

    def add_links(self):
        '''
            This dialog is modal so all the possible value lists for the 
            Combobox don't have to be refreshed before the autofill entry
            can be used. This way, the lists can be populated once when
            this dialog opens.
        '''

        # people = make_all_names_list_for_person_select()        
        # self.all_names = EntryAutoPersonHilited.create_lists(people)

        places = make_all_nestings(select_all_place_ids)
        self.place_autofill_values = EntryAutoHilited.create_lists(places)

        def close_linker():
            self.link_dlg.grab_release()
            self.link_dlg.destroy()

        self.link_dlg = Dialogue(self)
        self.link_dlg.grab_set()
        self.link_dlg.canvas.title_1.config(text="Note-to-Elements Links")
        self.link_dlg.canvas.title_2.config(text="")
        lab = LabelHeader(
            self.link_dlg.window, 
            text=notes_msg[1], 
            justify='left', wraplength=450)
        lab.grid(
            column=0, row=0, sticky='news', padx=12, pady=12, 
            columnspan=2, ipadx=6, ipady=3)    

        self.combo = Combobox(
            self.link_dlg.window, self.root, values=sorted(ELEMENTS))
        self.combo.grid(column=0, row=1, sticky="w", padx=12)

        self.link_input = EntryAutoHilited(
            self.link_dlg.window, width=36, autofill=True)
        self.link_input.grid(column=0, row=2, pady=6, sticky="ew", padx=12)
        self.link_input.bind("<FocusIn>", self.get_link_type, add="+")

        buttonbox = Frame(self.link_dlg.window)
        buttonbox.grid(
            column=0, row=3, sticky='e', padx=(0,12), pady=12, columnspan=2)
        ok_butt = Button(
            buttonbox, text="OK", 
            command=self.save_link, 
            width=6)
        ok_butt.grid(column=0, row=0, sticky='e')
        cancel_butt = Button(
            buttonbox, text="DONE", command=close_linker, width=6)
        cancel_butt.grid(column=1, row=0, padx=(6,0), sticky='e')
        self.combo.entry.focus_set()
       
        self.link_dlg.resize_window()

    def get_link_type(self, evt):

        self.link_type = self.combo.entry.get()
        self.link_input.delete(0, 'end')
        
        if self.link_type not in ELEMENTS:
            return
        elif self.link_type == "persons":
            # self.link_input.values = self.all_names
            self.link_input.values = self.person_autofill_values
        elif self.link_type == "places":
            self.link_input.values = self.place_autofill_values
        else:
            print("line", looky(seeline()).lineno, "self.link_type:", self.link_type)
        
    def save_link(self):
        got = self.link_input.get()
        if self.link_type == "persons":
            element_id = got.split("  #")[1]

    def ignore_changes(self, evt=None):
        self.order_dlg.grab_release()
        self.order_dlg.destroy()
        self.focus_set()

    def reorder_notes(self):

        if self.length <= 2:
            return

        self.order_dlg = Toplevel(self)
        self.order_dlg.columnconfigure(1, weight=1)
        self.order_dlg_canvas = Border(self.order_dlg, self.root, self.formats)
        self.order_dlg_window = Frame(self.order_dlg_canvas)
        self.order_dlg_canvas.create_window(
            0, 0, anchor='nw', window=self.order_dlg_window)

        self.order_dlg.grab_set()
        self.order_dlg.bind('<Return>', self.save_close_reorder_dlg)
        self.order_dlg.bind('<Escape>', self.ignore_changes)
        self.order_dlg_canvas.title_1.config(text="Re-order Topics")
        self.order_dlg_canvas.title_2.config(text="")
        self.make_widgets_reorder_dlg()
        self.make_inputs_reorder_dlg()
        config_generic(self.order_dlg)
        resize_scrolled_content(
            self.order_dlg, self.order_dlg_canvas, self.order_dlg_window) 
        self.order_dlg.maxsize(
            int(self.order_dlg_window.winfo_reqwidth() + 24), 
            int(self.winfo_screenheight() * 0.80))

    def make_widgets_reorder_dlg(self):
        scridth = 16
        scridth_n = Frame(self.order_dlg_window, height=scridth)
        scridth_w = Frame(self.order_dlg_window, width=scridth)
       
        self.treebard.scroll_mouse.append_to_list(
            [self.order_dlg_canvas, self.order_dlg_window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.order_dlg_window.vsb = Scrollbar(
            self.order_dlg, 
            hideable=True, 
            command=self.order_dlg_canvas.yview,
            width=scridth)
        self.order_dlg_window.hsb = Scrollbar(
            self.order_dlg, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.order_dlg_canvas.xview)
        self.order_dlg_canvas.config(
            xscrollcommand=self.order_dlg_window.hsb.set, 
            yscrollcommand=self.order_dlg_window.vsb.set)
        self.order_dlg_window.vsb.grid(column=2, row=4, sticky='ns')
        self.order_dlg_window.hsb.grid(column=1, row=5, sticky='ew')

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

    def make_inputs_reorder_dlg(self):

        reorder_msg = (
            'Tab or Shift + Tab selects movable topic. '
            'Arrow keys change topic order up or down.')
         
        reorder_lab = LabelHeader(
            self.order_dlg_window, text=reorder_msg, wraplength=450)

        self.reorder_labs = Frame(self.order_dlg_window)

        e = 0
        for topic in self.topics:           
            lab = LabelMovable(self.reorder_labs, text=topic, anchor='w')
            if e == 0:
                first = lab
            e += 1
            lab.grid(column=0, row=e, padx=3, sticky='ew')
        first.focus_set()

        close2 = Button(
            self.order_dlg_window, 
            text='OK', 
            command=self.save_close_reorder_dlg)

        reorder_lab.grid(
            column=0, row=0, pady=(12,0), padx=12, 
            columnspan=2, ipadx=6, ipady=3)
        self.reorder_labs.grid(column=0, row=1, columnspan=2, padx=12, pady=12)
        self.reorder_labs.grid_columnconfigure(0, weight=1)
        close2.grid(column=1, row=2, sticky='se', padx=12, pady=(0,12))

        center_dialog(self.order_dlg, frame=self.order_dlg_window)

    def save_close_reorder_dlg(self, evt=None):
        q = 0
        new_order = []
        save_order = []
        for child in self.reorder_labs.winfo_children():
            text = child.cget('text')
            new_order.append(text)
            save_order.append([text, q])
            q += 1

        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        for lst in save_order:
            cur.execute(select_note_id, (lst[0],))
            result = cur.fetchone()
            if result:
                note_id = result[0]
            else:
                continue
            cur.execute(
                update_findings_notes, 
                (lst[1], self.finding, note_id))
            conn.commit()
        cur.close()
        conn.close()
        self.make_table_of_contents()
        self.order_dlg.grab_release()
        self.order_dlg.destroy()
        self.focus_set()

    def save_privacy_setting(self):
        selected_topic = self.selected.cget("text")
        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_note_privacy, (
            self.privacy.get(), selected_topic))
        conn.commit()
        cur.close()
        conn.close()

    def close_notes_dialog(self, evt=None):
        self.destroy()
        self.root.focus_set()

    def size_toc(self):
        # if self.length == 0: # added 20220220 to avoid division by zero error but there are consequences
            # return
        self.update_idletasks()
        self.win_ht = self.toc.winfo_reqheight()
        panel_ht = self.right_panel.winfo_reqheight()
        note_header_height = self.note_header.winfo_reqheight()
        self.toc_height = note_height = self.note.winfo_reqheight()
        title_ht = self.toc_head.winfo_reqheight()
        bd_ht = 3 * 2
        plug = title_ht + bd_ht
        self.budge = title_ht + plug
        self.canv_ht = note_height + note_header_height - plug
        self.toc_canvas.config(
            width=self.toc_width, # this is the problem
            height=self.canv_ht,
            scrollregion=(0, 0, self.toc_width, self.win_ht)) 
        self.widg_ht = int(self.win_ht / self.length)
        lines_fit = int(self.canv_ht / self.widg_ht)
        if self.length > lines_fit:
            self.autoscroll_on_arrow = True

    def make_toc_scrollable(self):
        self.toc_canvas = Canvas(self.left_panel)
        self.toc_canvas.grid(column=0, row=1, sticky="news")
        self.toc = Frame(self.toc_canvas)
        self.toc_canvas.create_window(0, 0, anchor='nw', window=self.toc)
        sbv = Scrollbar(
            self.left_panel, 
            command=self.toc_canvas.yview,
            hideable=True)
        sbv.grid(column=1, row=1, sticky="ns")
        self.toc_canvas.config(yscrollcommand=sbv.set)

    def stop_tab_traversal1(self, evt):
        '''
            Two similar callbacks are needed for binding to both `Tab` and
            `Shift-Tab` because Tkinter's `evt.keysym` detects `Tab` for both.
        '''
        widg = evt.widget
        if widg not in self.topiclabs:
            return
        self.note_header.focus_set()
        return('break')

    def stop_tab_traversal2(self, evt):
        widg = evt.widget
        if widg not in self.topiclabs:
            return
        self.done.focus_set()
        return('break')

    def select_item(self, evt, next_item=None, prev_item=None):

        for widg in self.topiclabs:
            widg.config(bg=self.formats['bg'])

        sym = evt.keysym
        evt_type = evt.type

        if evt_type == '4':
            self.selected = evt.widget
            self.display_note()
        elif evt_type == '2' and sym == 'Down':
            self.selected = next_item
        elif evt_type == '2' and sym == 'Up':
            self.selected = prev_item

        self.selected.config(bg=self.formats['highlight_bg'])
        self.update_idletasks()

        current_scrollratio = 0.0
        top_of_selected = self.selected.winfo_rooty()
        top_of_port = self.toc_canvas.winfo_rooty()
        height_of_selected = self.selected.winfo_reqheight()
        bottom_of_selected = top_of_selected + height_of_selected
        bottom_of_port = top_of_port + self.canv_ht
        page_ratio = self.canv_ht / self.win_ht

        # autoscroll in 1-page increments during arrow traversal 
        #   if selected widget goes out of view
        if bottom_of_selected > bottom_of_port:
            current_scrollratio += page_ratio
            self.toc_canvas.yview_moveto(float(current_scrollratio))
        elif top_of_selected < top_of_port:
            if self.autoscroll_on_arrow is True:
                current_scrollratio -= page_ratio
                self.toc_canvas.yview_moveto(float(current_scrollratio))

        self.selected.focus_set()

    def traverse_on_arrow(self, evt):
        widg = evt.widget
        sym = evt.keysym
        self.update_idletasks()
        next_item = widg.tk_focusNext()
        prev_item = widg.tk_focusPrev()
        if sym == 'Down':
            if next_item in self.topiclabs:
                self.select_item(evt, next_item=next_item)
            else:
                next_item = self.topiclabs[0]
                next_item.focus_set()
                next_item.config(bg=self.formats['highlight_bg'])
                self.selected = next_item
                self.toc_canvas.yview_moveto(0.0)
        elif sym == 'Up':
            if prev_item in self.topiclabs:
                self.select_item(evt, prev_item=prev_item)
            else:
                prev_item = self.topiclabs[self.length-1]
                prev_item.focus_set()
                prev_item.config(bg=self.formats['highlight_bg'])
                self.selected = prev_item
                if self.autoscroll_on_arrow is True:
                    self.toc_canvas.yview_moveto(1.0)
        self.display_note()

    def make_table_of_contents(self):
        for child in self.toc.winfo_children():
            child.destroy()

        conn = sqlite3.connect(self.current_file)
        cur = conn.cursor()
        cur.execute(select_notes_per_finding, (self.finding,))
        self.values = cur.fetchall()
        cur.close()
        conn.close()

        self.topics = [i[0] for i in self.values]
        self.notes = [i[1] for i in self.values]
        self.topiclabs = []
        r = 0
        for tup in self.values:
            text = self.values[r][0]
            lab = Label(
                self.toc, takefocus=1, anchor="w", 
                text=text, width=self.toc_width)
            self.topiclabs.append(lab)
            lab.grid(column=0, row=r+1, sticky="ew")
            lab.bind("<Button-1>", self.select_item)
            lab.bind("<FocusIn>", self.highlight)
            lab.bind("<FocusOut>", self.unhighlight)
            lab.bind("<Key-Up>", self.traverse_on_arrow, add="+") 
            lab.bind("<Key-Down>", self.traverse_on_arrow, add="+")
            lab.bind("<Delete>", self.delete_selected_note)
            lab.bind("<BackSpace>", self.rename_selected_note)
            if len(text) > 20:
                create_tooltip(lab, text)
            r += 1
        self.length = len(self.topiclabs)

    def rename_selected_note(self, evt):

        widg = evt.widget
        old_txt = widg.cget("text")

        msg = InputMessage(
            self, root=self.root, return_focus_to=widg, title="Rename Note", 
            ok_txt="OK", cancel_txt="CANCEL", entry=True, grab=True, 
            head1="Rename {} to:".format(old_txt), head2="(any unique title)")

        if msg.ok_was_pressed:
            new_txt = msg.show()

            conn = sqlite3.connect(self.current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(update_note_topic, (new_txt, old_txt))
            conn.commit()
            cur.close()
            conn.close()
            self.make_table_of_contents()

    def delete_selected_note(self, evt):

        def ok_delete_note():
            msg[0].grab_release()
            msg[0].destroy()
            self.note_header.focus_set()
            proceed()

        def cancel_delete_note():
            msg[0].grab_release()
            msg[0].destroy()
            widg.focus_set()

        def proceed():
            conn = sqlite3.connect(self.current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(select_notes_linked, (topic, self.finding))
            to_delete = cur.fetchone()
            for num in to_delete:
                cur.execute(delete_findings_notes_linked, (num,))
                conn.commit()
            cur.close()
            conn.close()
            # recalculate scrollregion height            
            win_ht_new = self.win_ht - widg_ht
            self.toc_canvas.config(
                width=self.toc_width,
                height=self.canv_ht,
                scrollregion=(0, 0, self.toc_width, win_ht_new))
            self.make_table_of_contents()

        widg = evt.widget
        topic = widg.cget('text')
        widg_ht = widg.winfo_reqheight()
        msg = open_yes_no_message(
            self, 
            notes_msg[5], 
            "Unlink Note Confirmation", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[2].config(command=ok_delete_note)
        msg[3].config(command=cancel_delete_note)

    def make_new_note(self, evt):
        '''
            Tkinter automatically adds a newline character at the end of the 
            data in the Text, widget, so to detect an empty Text widget, use 
            get(1.0, 'end-1c') instead of get(1.0, 'end'). This gets the text 
            up to 1 character from the end.
        '''

        topic = self.note_header.get()
        note = self.note.text.get(1.0, 'end-1c')        

        if (len(self.note.text.get(1.0, 'end-1c')) == 0 or 
                len(topic) == 0):
            return
        if topic in self.topics:
            idx = self.topics.index(topic)
            self.edit_note(idx, topic, note)
            return

        new_topic = self.note_header.get()
        new_note = note 
        self.topiclabs[0].focus_set()
        self.save_new_note(new_topic, new_note)
        self.make_table_of_contents()
        self.size_toc()
        resize_scrolled_content(self, self.canvas, self.window) 

    def edit_note(self, idx, topic, note):

        def save_edited_text():
            conn = sqlite3.connect(self.current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(update_note_edit, (final, topic))
            conn.commit()
            cur.close()
            conn.close()
            self.make_table_of_contents()

        orig = self.notes[idx]
        final = note
        if orig == final:
            pass
        else:
            save_edited_text()        

    def save_new_note(self, new_topic, new_note):

        def reorder_notes():
            cur.execute(select_findings_notes_order, (self.finding,))
            order = [list(i) for i in cur.fetchall()]
            for lst in order:
                lst[0] += 1
            for lst in order:
                cur.execute(update_findings_notes_order, tuple(lst))
                conn.commit()

        conn = sqlite3.connect(self.current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(insert_note, (new_note, new_topic))
        conn.commit()
        cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'note'")
        new_note_id = cur.fetchone()[0]
        reorder_notes()
        cur.execute(insert_findings_notes_new, (self.finding, new_note_id))
        conn.commit()
        cur.close()
        conn.close()

    def highlight(self, evt):
        evt.widget.config(bg=self.formats["highlight_bg"])

    def unhighlight(self, evt):
        evt.widget.config(bg=self.formats["bg"])

    def display_note(self, evt=None):

        def do_it(selected_topic):
            if selected_topic is None:
                self.note.text.delete(1.0, 'end')
                return
            idx = self.topics.index(selected_topic)
            note_to_display = self.notes[idx]
            self.note_header.delete(0, 'end')
            self.note_header.insert(0, selected_topic)
            self.note.text.delete(1.0, 'end')
            self.note.text.insert(1.0, note_to_display)
            self.selected = self.topiclabs[idx]
            self.selected.focus_set()
            conn = sqlite3.connect(self.current_file)
            cur = conn.cursor()
            cur.execute(select_note_privacy, (selected_topic,))
            privacy_setting = cur.fetchone()[0]
            cur.close()
            conn.close()
            if privacy_setting == 0:
                self.public.select()
            elif privacy_setting == 1:
                self.private.select()

        selected_topic = None
        if evt is None:
            selected_topic = self.selected.cget("text")
            do_it(selected_topic)
            return
        etype = evt.type
        widg = evt.widget
        sym = evt.keysym
        if etype == "4": # Button-1
            selected_topic = widg.cget('text')
        elif etype == "9": # FocusIn
            if len(widg.get()) == 0:
                pass
            else:
                selected_topic = widg.get().strip()
        elif etype == "3": # KeyRelease
            if widg is self.note_header:
                if (len(sym) == 1 or 
                        sym in OK_PRINT_KEYS or 
                        sym in ("BackSpace", "Delete")):
                    selected_topic = self.note_header.get()
                    if selected_topic in self.topics:
                        do_it(selected_topic)
                    else:
                        self.note.text.delete(1.0, 'end')

if __name__ == "__main__":

    finding = 1
    header = ["birth", "14 Jan 1845", "Colorado, USA", "born at home"]
    current_person = 3
    treebard = None

    def open_note():
        note_dlg = NotesDialog(
            root, finding, header, current_person, treebard)

    root = tk.Tk()

    b = Button(root, text=" ... ", command=open_note)
    b.grid()
    b.focus_set()
    config_generic(root)
    root.mainloop()





