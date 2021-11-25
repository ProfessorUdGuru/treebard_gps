# 2022_refactor_notes_dialog_2

# version _2: refactoring the autoscroll feature using the old custom_listbox_widget.py code since that code worked well, so will have to rewrite some of these procedures ie some restructuring


import tkinter as tk
import sqlite3
from scrolling import Scrollbar, ScrolledText
from window_border import Dialogue
from widgets import (
    Label, Frame, Button, Entry, Canvas, LabelFrame, LabelH3, FrameHilited6,
    LabelMovable, Toplevel, LabelHeader)
from toykinter_widgets import run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from styles import config_generic, make_formats_dict
from names import get_name_with_id
from messages import (
    open_yes_no_message, notes_msg, open_message, InputMessage)
from message_strings import note_dlg_msg
from utes import center_window, create_tooltip
from files import get_current_file
from query_strings import (
    update_note, select_count_subtopic, insert_note, insert_findings_notes,
    select_notes_refresh, update_note_private, update_note_subtopic,
    select_private_note, delete_findings_notes, select_count_findings_notes_note_id,
    delete_note, select_count_findings_notes_finding_id, select_note_id,
    update_findings_notes,     
    
)
import dev_tools as dt
from dev_tools import looky, seeline




multi_page_list = [
    'nunc', 'incididunt', 'congue', 'tortor', 'tempo', 'fusc', 'ante', 'dictum', 'Tristique', 'sed', 'urna', 'aliquet', 'Consectetur', 'Tortor', 'posuere', 'Vitae', 

    'veli', 'purus', 'tellu', 'laoreet', 'ame', 'rhoncus', 'Magna', 'lorem', 'neque', 'quis', 'Quam', 'dolore', 'vitae', 'bibendum', 'Gravida', 'sempe', 'faucibus', 'magni',  

    'Scelerisque', 'Suspendisse', 'lacus', 'odi', 'in', 'labore', 'amet', 'proin', 'arcu', 'ultrices', 'u', 'duis', 'non', 'eu', 'donec', 'eli', 'sodale', 'ac', 'egestas', 'rhoncu', 'ut', 'malesuada', 'urn', 'ipsum', 'consectetur', 'tincidunt', 'sodales', 'fames', 'facilisis', 'nisi', 'et', 'vita', 'gravida', 'sociis', 'In', 'sagittis', 'do', 'justo', 'penatibus', 'vel', 'Semper', 'scelerisque', 'libero', 'nisl', 'accumsan', 'tempor', 'vivamus', 'at', 'nam', 'Netus', 'metus', 'Lorem', 'Accumsan', 'id', 'rutrum', 'fusce', 'mattis', 'suspendisse', 'sit', 'consectetur adipiscing', 'nis', 'auctor', 'adipiscing', 'consequat', 'Dui', 'cum', 'tellus', 'Luctus', 'est', 'viverra', 'Id', 'Proin', 'aliqu', 'natoque', 'semper', 'felis', 'feugiat', 'quisque', 'eiusmod', 'adipiscin', 'dolor', 'volutpat', 'magna', 'eget', 'a', 'risus' 
]

one_page_list = [
    "balloon", "frog", "unicorn", "geezerware", "rain jacket for everybody",
    "umbrella", "horsefeathers", "automaton", "the matrix", "genealogy",
    "hyperinflation", "semi-serious"]

short_note = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
'''

long_note = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
'''

class NotesDialog(Toplevel):
    ''' `toc` means Table of Contents. '''

    def __init__(self, master, topicslist, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.master = master
        self.topicslist = topicslist

        self.formats = make_formats_dict()

        self.autoscroll_on_arrow = False

        self.make_containers()
        self.make_toc_scrollable() 
        self.make_inputs()
        # 20 characters * font size but shouldn't hard-code font-size 12 
        #   (had to change to 11 anyway)   
        self.toc_width = 20 * 11     
        self.make_table_of_contents() 
        self.size_toc()
        self.bind_class('Label', '<Tab>', self.stop_tab_traversal1)
        self.bind_class('Label', '<Shift-Tab>', self.stop_tab_traversal2)
           
        self.bind_all("<Key-Up>", self.focus_topicslist)
        self.bind_all("<Key-Down>", self.focus_topicslist)
        
        self.focus_set()

    def make_containers(self):
        spacer = Frame(self)
        spacer.grid(column=0, row=0, sticky="news")
        self.left_panel = FrameHilited6(self)
        self.left_panel.grid(column=0, row=1, sticky="news", padx=(12,0))
        self.right_panel = Frame(self)
        self.right_panel.grid(column=1, row=0, sticky="news", rowspan=2)
        self.bottom_panel = Frame(self)
        self.bottom_panel.grid(column=0, row=2, columnspan=2, sticky="news")

    def focus_topicslist(self, evt):
        widg = evt.widget
        if widg.winfo_class() == "Label" or widg.winfo_class() == "Text":
            return
        last = self.topics[self.length - 1]
        first = self.topics[0]
        sym = evt.keysym
        if sym == "Up":
            print("line", looky(seeline()).lineno, "running:")
            last.focus_set()
            self.toc_canvas.yview_moveto(1.0)
        elif sym == "Down":
            first.focus_set()
            self.toc_canvas.yview_moveto(0.0)

    def make_inputs(self):
        self.toc_head = LabelH3(self.left_panel, text="TABLE OF CONTENTS")
        self.toc_head.grid(column=0, row=0, sticky="news", pady=6)
        self.note_header = Entry(self.right_panel, width=36)
        self.note_header.grid(column=0, row=0, sticky="w", padx=(12,0), pady=6)
        self.note = ScrolledText(self.right_panel)
        self.note.grid(column=0, row=1, padx=12)

        self.done = Button(self.bottom_panel, text="DONE")
        self.done.grid()  

        self.note.text.insert(1.0, short_note)

    def size_toc(self):
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
            width=self.toc_width,
            height=self.canv_ht,
            scrollregion=(0, 0, self.toc_width, self.win_ht))  
        self.widg_ht = int(self.win_ht / self.length)
        lines_fit = int(self.canv_ht / self.widg_ht)
        if self.length > lines_fit:
            self.autoscroll_on_arrow = True

    def make_toc_scrollable(self):
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(1, weight=1)
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
        if widg not in self.topics:
            return
        self.note_header.focus_set()
        return('break')

    def stop_tab_traversal2(self, evt):
        widg = evt.widget
        if widg not in self.topics:
            return
        self.done.focus_set()
        return('break')

    def select_item(self, evt, next_item=None, prev_item=None):

        for widg in self.topics:
            widg.config(bg=self.formats['bg'])

        sym = evt.keysym
        evt_type = evt.type

        if evt_type == '4':
            selected = evt.widget
        elif evt_type == '2' and sym == 'Down':
            selected = next_item
        elif evt_type == '2' and sym == 'Up':
            selected = prev_item

        selected.config(bg=self.formats['highlight_bg'])

        win_from_screentop = self.winfo_rooty()
        winbottom = win_from_screentop + self.canv_ht

        ratio_canv_win = self.canv_ht / self.win_ht

        widg_winpos = selected.winfo_y()
        ratio_widgpos_winsize = widg_winpos / self.win_ht

        widget_ratio = 1 / self.length 
        up_ratio = ratio_widgpos_winsize - ratio_canv_win + widget_ratio

        widg_from_screentop = selected.winfo_rooty()
        # autoscroll during arrow traversal if selected widget out of view
        if widg_from_screentop > winbottom - self.widg_ht + self.budge:
            print("line", looky(seeline()).lineno, "running:")
            self.toc_canvas.yview_moveto(float(ratio_widgpos_winsize))
        elif widg_from_screentop < win_from_screentop + self.budge:
            if self.autoscroll_on_arrow is True:
                self.toc_canvas.yview_moveto(float(up_ratio))
        selected.focus_set()

    def traverse_on_arrow(self, evt):
        widg = evt.widget
        sym = evt.keysym
        self.update_idletasks()
        next_item = widg.tk_focusNext()
        prev_item = widg.tk_focusPrev()
        if sym == 'Down':
            if next_item in self.topics:
                self.select_item(evt, next_item=next_item)
            else:
                next_item = self.topics[0]
                next_item.focus_set()
                next_item.config(bg=self.formats['highlight_bg'])
                self.toc_canvas.yview_moveto(0.0)
        elif sym == 'Up':
            if prev_item in self.topics:
                self.select_item(evt, prev_item=prev_item)
            else:
                prev_item = self.topics[self.length-1]
                prev_item.focus_set()
                prev_item.config(bg=self.formats['highlight_bg'])
                if self.autoscroll_on_arrow is True:
                    self.toc_canvas.yview_moveto(1.0)

    def make_table_of_contents(self):
        for child in self.toc.winfo_children():
            child.destroy()
        self.topics = []
        r = 0
        for stg in self.topicslist:
            text = self.topicslist[r]
            lab = Label(
                self.toc, takefocus=1, anchor="w", 
                text=text, width=self.toc_width)
            self.topics.append(lab)
            lab.grid(column=0, row=r+1, sticky="ew")
            lab.bind("<Button-1>", self.select_item)
            lab.bind("<FocusIn>", self.highlight)
            lab.bind("<FocusOut>", self.unhighlight)
            lab.bind("<Key-Up>", self.traverse_on_arrow, add="+") 
            lab.bind("<Key-Down>", self.traverse_on_arrow, add="+")
            if len(text) > 20:
                create_tooltip(lab, text)
            r += 1
        self.length = len(self.topics)

    def make_new_note(self, final):

        self.topicslist.insert(0, final)
        self.make_table_of_contents()
        self.topics[0].focus_set()

        self.size_toc()        

    def highlight(self, evt):
        evt.widget.config(bg=self.formats["highlight_bg"])

    def unhighlight(self, evt):
        evt.widget.config(bg=self.formats["bg"])

if __name__ == "__main__":

    root = tk.Tk()

    def open_note():
        note_dlg = NotesDialog(root, multi_page_list)
        note_dlg.geometry("+800+300")

        config_generic(note_dlg)   

    b = Button(root, text=" ... ", command=open_note)
    b.grid()
    b.focus_set()

    config_generic(root)
    root.mainloop()

# display selected note
# create new note
# see if canvas moveto etc still work after adding a new note
# change order in toc
# rcm command change note title
# delete note
# private/public
# save to db new or edited note
# add combo & autofill to link note to any element

# rcm help dialog: Navigating the Table of Contents. The Table of Contents is entered and navigated by clicking an item in the list or by pressing the up or down arrow key from anywhere in the notes dialog except from within the note input itself. For example, if the topic title input is in focus, pressing the up arrow will start traversing the list from the bottom, or pressing the down arrow will start traversing from the top. As you traverse the list of topics, it will scroll automatically if there are too many topics to fit in the window, or you can use the vertical scrollbar which will appear if it's needed. There's no horizontal scrollbar for long titles, but if you can't read a title due to its length, pointing at it with the mouse will show a tooltip with the full title. Inside the note input, the arrow keys are just arrow keys. To move in and out of the note input, the table of contents, or other widgets, use the Tab key to go forward or Shift+Tab key to go backward. The note title input above the note input displays the topic of the current note. To change which note is displayed, traverse the table of contents as described above, or change the topic manually by typing in the note title input. The note input will display no text if the input doesn't show an existing topic, so in order to create a new note, just type a new topic and a new note, in either order, and click SUBMIT CHANGES when done. You can enter any number of notes without pressing DONE to close the dialog. To delete a note, press the delete key when its topic is selected in the table of contents. To change an existing note's topic, right-click any topic in the table of contents and a dialog will open to accept the new topic. All note topics within a single tree must be unique, for example, there can't be two topics entitled "Spring Wedding", but there can be a "Robert & Marian's Spring Wedding" as well as a "Fido and Barfy's Spring Wedding". Or a "Spring Wedding 1" and Spring Wedding 2" if you like numbers. Any text will be accepted as a note topic as long as it's unique within the entire tree. The purpose of this is to make it easy to link any note to any number of persons, place, events, or citation. So you won't be copy-pasting notes that need to be seen in more than one place, and the database won't be storing the same text twice. To edit or replace a stored note without renaming it, just change the text and the changes will be saved on pressing SUBMIT CHANGES. If the note is too trivial and short to deserve a topic, then you can use the Particulars column in the events table. Due to the vast limitations of GEDCOM and the whole idea of sharing data from person to person when everyone uses different software, the bar has been raised by Treebard so that this all-important Note functionality can work the way it should. No genieware should suffer from the lack of any of the features described above, at the very least.





