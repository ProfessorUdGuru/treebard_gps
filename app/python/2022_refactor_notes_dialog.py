# 2022_refactor_notes_dialog _x

# version _2: refactoring the autoscroll feature using the old custom_listbox_widget.py code since that code worked well, so will have to rewrite some of these procedures ie some restructuring

# replace listbox with new TableOfContents class, add combo & autofill to link note to any element, add scrollbar to Text, remove scrollbar from toc and add paging, remove reorder dialog and make it part of the arrow functionality with a mode selection view/reorder, change subtopic to topic, remove subtopic dialog and make the label that displays the current topic editable, put New... at top of toc instead of bottom, no scrollbar in toplevel, tab to enter and leave toc, traversal w/in is by arrow only

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

print(set(multi_page_list))

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

        self.make_containers()
        self.make_toc_scrollable() 
        self.make_inputs()   
        self.toc_width = 20 * 11     
        self.make_table_of_contents() 
        self.size_toc()
        self.bind_class('Label', '<Tab>', self.stop_tab_traversal1)
        self.bind_class('Label', '<Shift-Tab>', self.stop_tab_traversal2)
           
        self.bind_all("<Key-Up>", self.focus_topicslist)
        self.bind_all("<Key-Down>", self.focus_topicslist)


        self.current_page = 1
        
        self.focus_set()

    def print_focused_widget(self, evt):
        print(self.focus_get())

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
            last.focus_set()
        elif sym == "Down":
            first.focus_set()

    def make_inputs(self):
        self.titlepad = 6
        self.toc_head = LabelH3(self.left_panel, text="TABLE OF CONTENTS")
        self.toc_head.grid(column=0, row=0, sticky="news", pady=self.titlepad)
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
        panel_height = self.right_panel.winfo_reqheight()
        note_header_height = self.note_header.winfo_reqheight()
        self.toc_height = note_height = self.note.winfo_reqheight()
        title_height = self.toc_head.winfo_reqheight()
        self.canvas_height = note_height + note_header_height - title_height - (
            self.left_panel.bd * 4) - (self.titlepad * 2)
        self.toc_canvas.config(
            width=self.toc_width,
            height=self.canvas_height,
            scrollregion=(0, 0, self.toc_width, self.win_ht))
        temp = Label(self, text="x")
        line_height = temp.winfo_reqheight()
        temp.destroy()
        self.pages = (self.toc_height / self.canvas_height) + 1
        self.lines = int(self.canvas_height / line_height)
        # self.pages = int(self.toc_height / note_height) + 1
        # self.lines = int(note_height / line_height)

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

    def traverse_on_arrow(self, evt):
        widg = evt.widget
        sym = evt.keysym
        self.length = len(self.topics)
        nexxt = widg.tk_focusNext()
        prev = widg.tk_focusPrev()
        first = self.topics[0]
        last = self.topics[self.length - 1]
        if sym == "Up":
            if prev.winfo_class() == "Label":
                prev.focus_set()
            else:
                last.focus_set()
                self.toc_canvas.yview_moveto(1.0)
        elif sym == "Down":
            if nexxt.winfo_class() == "Label":
                nexxt.focus_set()
            else:
                first.focus_set()
                self.toc_canvas.yview_moveto(0.0)
        else:
            print("line", looky(seeline()).lineno, "case not handled:")

        idx = self.topicslist.index(widg.cget('text'))
        self.autoscroll(widg, idx, sym)

    # def traverse_on_arrow(self, evt):
        # if evt.keysym not in ('Up', 'Down'):
            # return
        # len_items = len(self.items)
        # widg_ht = int(
            # self.listbox_content.winfo_reqheight()/len_items)
        # self.update_idletasks()
        # items = self.listbox_content.winfo_children()
        # next_item = evt.widget.tk_focusNext()
        # prev_item = evt.widget.tk_focusPrev()
        # if evt.keysym == 'Down':
            # if next_item in items:
                # self.select_item(evt, next_item=next_item)
            # else:
                # next_item = items[0]
                # next_item.focus_set()
                # next_item.config(bg=formats['bg'])
                # self.listbox_canvas.yview_moveto(0.0)

        # elif evt.keysym == 'Up':
            # if prev_item in items:
                # self.select_item(evt, prev_item=prev_item)
            # else:
                # prev_item = items[len_items-1]
                # prev_item.focus_set()
                # prev_item.config(bg=formats['bg'])
                # self.listbox_canvas.yview_moveto(1.0)



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
            lab.bind("<Button-1>", self.switch_note_on_click) 
            lab.bind("<FocusIn>", self.highlight)
            lab.bind("<FocusOut>", self.unhighlight)
            lab.bind("<Enter>", self.highlight)
            lab.bind("<Leave>", self.unhighlight)
            lab.bind("<Key-Up>", self.traverse_on_arrow, add="+") 
            lab.bind("<Key-Down>", self.traverse_on_arrow, add="+")
            if len(text) > 20:
                create_tooltip(lab, text)
            r += 1

    def make_new_note(self, final):

        self.topicslist.insert(0, final)
        self.make_table_of_contents()
        self.topics[0].focus_set()

        self.size_toc()        

    def switch_note_on_click(self, evt):
        widg = evt.widget

        widg.focus_set()
        widg.config(bg=self.formats["highlight_bg"])

    def highlight(self, evt):
        evt.widget.config(bg=self.formats["highlight_bg"])

    def unhighlight(self, evt):
        evt.widget.config(bg=self.formats["bg"])

    def autoscroll(self, widg, idx, sym):
        # print("line", looky(seeline()).lineno, "self.current_page:", self.current_page)
        if self.pages <= 1: return
        if (idx + 1) % self.lines != 0: return

        widg_ht = self.win_ht / self.length
        widg_ratio = 1 / self.length
        widg_pos = widg.winfo_y()
        print("line", looky(seeline()).lineno, "widg_pos:", widg_pos)
        ratio = float(widg_pos / self.win_ht)
        print("line", looky(seeline()).lineno, "ratio:", ratio)
        self.toc_canvas.yview_moveto(ratio)





        # widget_ht = int(self.list_height / len(self.items))
        # widget_pos_in_screen = selected_item.winfo_rooty()
        # widget_pos_in_list = selected_item.winfo_y()
        # window_top = self.winfo_rooty()
        # window_bottom = window_top + self.view_height
        # window_ratio = self.view_height / self.list_height
        # list_ratio = widget_pos_in_list / self.list_height
        # widget_ratio = widget_ht / self.list_height
        # up_ratio = list_ratio - window_ratio + widget_ratio 

        # if widget_pos_in_screen > window_bottom - 0.75 * widget_ht:
            # self.listbox_canvas.yview_moveto(float(list_ratio))
        # elif widget_pos_in_screen < window_top:
            # self.listbox_canvas.yview_moveto(float(up_ratio))









        # # print("line", looky(seeline()).lineno, "self.pages:", self.pages)
        # # print("line", looky(seeline()).lineno, "self.lines:", self.lines)
        # # print("line", looky(seeline()).lineno, "self.win_ht:", self.win_ht)
        # # print("line", looky(seeline()).lineno, "idx, sym:", idx, sym)
        # per_page_ratio = self.lines / self.length
        # if sym == "Down":
            # if (idx + 1) % self.lines == 0:
                # ratio = self.current_page * per_page_ratio
                # print("line", looky(seeline()).lineno, "ratio going down:", ratio)
                # self.current_page += 1
                # self.toc_canvas.yview_moveto(ratio)
        # elif sym == "Up":
            # if (idx + 1) % self.lines == 0:
                # ratio = self.current_page * per_page_ratio
                # print("line", looky(seeline()).lineno, "ratio going up:", ratio)
                # self.current_page -= 1
                # self.toc_canvas.yview_moveto(ratio)
        # print("line", looky(seeline()).lineno, "self.current_page:", self.current_page)
           
       

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

# DO LIST

# clean dupes out of big list
# Use pages not position or visibility to make the canvas autoscroll when the highlighted label is not visible, just move one page at a time.
# when click lab to hilite it goes into focus ok but shd also stay hilited



