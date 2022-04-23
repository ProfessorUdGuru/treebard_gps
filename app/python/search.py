# search.py

import tkinter as tk
import sqlite3
from files import app_path, get_current_file
from widgets import (
    Toplevel, Frame, Button, Entry, LabelH2, Label, LabelH3,
    LabelNegative, configall, Border, Scrollbar, make_formats_dict)
from right_click_menu import RightClickMenu, make_rc_menus
from scrolling import MousewheelScrolling, resize_scrolled_content
from toykinter_widgets import run_statusbar_tooltips
from persons import open_new_person_dialog, update_person_autofill_values
from redraw import redraw_person_tab
from dates import OK_PREFIXES, format_stored_date
from messages_context_help import search_person_help_msg
from query_strings import (
    select_person_distinct_like, select_name_details,
    select_finding_sorter, select_name_sort_order, select_person_death_date,
    select_person_birth_date,  
    select_finding_mother, select_finding_father
)
import dev_tools as dt
from dev_tools import looky, seeline





current_file, current_dir = get_current_file()
COL_HEADS = ('ID', 'Name', 'Birth', 'Death', 'Mother', 'Father')

NONPRINT_KEYS = (
    'Return', 'Tab', 'Shift_L', 'Shift_R', 'Escape', 
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
    'F9', 'F10', 'F11', 'F12', 'Caps_Lock', 'Control_L', 
    'Control_R', 'Win_L', 'Win_R', 'Alt_R', 'Alt_L', 
    'App', 'space', 'Up', 'Down', 'Left', 'Right', 
    'Num_Lock', 'Home', 'Prior', 'End', 'Next', 'Insert', 
    'Pause')

def get_matches(search_input):
 
    got = search_input.get()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(
        select_person_distinct_like, (
            '%{}%'.format(got), 
            '%{}%'.format(got)))
    all_matches = cur.fetchall()
    all_matches = [list(i) for i in all_matches]

    for lst in all_matches:
        person_id = lst[0]
        cur.execute(select_name_details, (person_id,))
        other_names = cur.fetchall()
        other_names = [list(tup) for tup in other_names]
        if other_names:
            lst.append(other_names)
        elif not other_names:
            lst.append('')

    cur.close()
    conn.close()
    return all_matches

class PersonSearch(Toplevel):
    def __init__(
            self, master, root, treebard, entry, findings_table, 
            show_top_pic, person_autofill_values, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.master = master # Main
        self.root = root
        self.treebard = treebard
        self.entry = entry
        self.findings_table = findings_table
        self.show_top_pic = show_top_pic
        self.person_autofill_values = person_autofill_values

        self.formats = make_formats_dict()

        self.result_rows = []
        self.hilit_row = None
        self.unhilit_row = None

        self.sent_text = '' 
 
        self.all_matches = [] 
        self.tkvars = {}
        self.sort_by = None 

        self.widget = None
        self.nametip = None
        self.nametip_text = None
        self.pointed_to = None

        self.person_id = None

        self.ma_id = None
        self.pa_id = None
        self.offspring_event = None

        self.rc_menu = RightClickMenu(self.root, treebard=self.treebard)

        self.make_widgets()

    def make_widgets(self):

        self.title('Person Search')
        self.geometry('+100+20')

        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, self.root, self.formats)
        self.canvas.title_1.config(text="Person Search Dialog")
        self.canvas.title_2.config(text="")

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
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

        buttonbox = Frame(self.window)
        self.b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=self.cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1)
        buttonbox.grid(column=0, row=3, sticky='e', pady=6)

        self.b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.make_inputs()
        configall(self, self.formats)
        self.maxsize(
            int(self.winfo_screenwidth() * 0.90),
            int(self.winfo_screenheight() * 0.90))

    def make_inputs(self):

        self.columnconfigure(1, weight=1)

        header = Frame(self.window)
        header.grid(column=0, row=0, sticky='ew')

        self.search_dlg_heading = LabelH2(
            header, 
            text='Person Search')
        self.search_dlg_heading.grid(column=0, row=0, pady=(24,0))

        instrux = Label(
            header, text='Search for person by name(s) or id number:')
        instrux.grid(column=0, row=1, sticky='e', padx=24, pady=12)

        self.sent_text = self.entry.get()

        self.search_input = Entry(header)
        self.search_input.grid(column=1, row=1, sticky='w', padx=12, pady=12)
        self.search_input.insert(0, self.sent_text)
        self.search_input.focus_set()
        self.search_input.bind('<KeyRelease>', self.handle_key_press)

        self.person_adder = Button(
            header, 
            text='ADD NEW PERSON',
            command=lambda master=self,
                inwidg=self.entry,
                root=self.root,
                inwidg2=self.search_input: self.make_new_person(
                    master, inwidg, root, self.treebard, self.formats, 
                    inwidg2, person_autofill_values=self.person_autofill_values)) 

        self.person_adder.grid(column=2, row=1, padx=12, pady=12)

        self.search_table = Frame(self.window)
        self.search_table.grid(
            column=0, row=1, sticky='news', padx=48, pady=48)

        visited = (
            (self.search_input, 
                "Person Search Input", 
                "Type any part of any name or ID number; table will fill "
                    "with matches."),
            (self.search_table, 
                "Person Search Table", 
                "Select highlighted row with Enter or Space key to change "
                    "current person, or click any row."))   
     
        run_statusbar_tooltips(
            visited, 
            self.canvas.statusbar.status_label, 
            self.canvas.statusbar.tooltip_label)

        rcm_widgets = (
            self.search_input, self.search_dlg_heading, self.search_table)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu, 
            search_person_help_msg) 

        self.make_header_row()
        resize_scrolled_content(self, self.canvas, self.window)

    def make_new_person(self, master, inwidg, root, treebard, formats, 
        inwidg2, person_autofill_values=None):
        open_new_person_dialog(
            master, inwidg, root, self.treebard,  
            inwidg2, person_autofill_values=self.person_autofill_values)
        self.person_autofill_values = update_person_autofill_values()
        inwidg.delete(0, 'end')

    def cancel(self):
        self.grab_release()
        self.entry.focus_set()
        self.root.lift()
        self.destroy()

    def handle_key_press(self, evt): 
        ''' 
            Recreate a results table when a character is typed into or removed
            from the input entry at top of search dialog.
        '''

        if evt.keysym in NONPRINT_KEYS:
            return
        elif evt.keysym.isalnum() is False:
            return

        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] not in (0, 1):
                child.destroy()

        self.all_matches = get_matches(self.search_input)
        self.make_search_dialog_cells()

    def make_header_row(self):

        for col in range(0, 6):
            var = tk.StringVar()
            self.tkvars[col] = var
            lab = LabelH3(
                self.search_table, 
                text=COL_HEADS[col], 
                cursor='hand2',
                anchor='w')
            lab.grid(column=col, row=0, sticky='ew', ipadx=12)
            lab.bind('<Button-1>', self.track_column_state) 

    def make_search_dialog_cells(self):
        self.result_rows = []
        c = 0
        for person_row in self.all_matches:
            self.make_row_list_for_search_results_table(person_row)
            row_list = self.row_list
            self.result_rows.append(row_list)
            c += 1

        for i in range(0, 6):
            if i == 0:
                init_sort = i
                self.tkvars[init_sort].set('clicked_once')
            else:
                no_sort = i
                self.tkvars[no_sort].set('not_clicked')
        self.result_rows = sorted(
            self.result_rows, 
            key=lambda q: q[init_sort])   

        row = 2
        for lst in self.result_rows:
            col = 0
            for val in lst:
                if col in (0,1,4,5):
                    text = lst[col]
                    lst[col] = val
                elif col in (2,3):
                    text = val[1]
                    
                else:
                    break

                lab = LabelSearch(
                    self.search_table, self.formats, cursor='hand2')
                lab.grid(column=col, row=row, sticky='ew', ipadx=12)
                lab.config(text=text)

                if lab.grid_info()['row'] != 0:
                    if lab.grid_info()['column'] in (0, 1):
                        self.widget = lab
                        self.make_nametip()                       
            
                col += 1
            row += 1

        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] not in (0, 1):
                child.bind('<Button-1>', self.select)
                child.bind('<Return>', self.select)
                child.bind('<Key-space>', self.select)
                child.bind('<FocusIn>', self.highlight_on_focus)                
                child.bind('<FocusOut>', self.unhighlight_on_unfocus)
                child.bind('<Key-Up>', self.go_up)
                child.bind('<Key-Down>', self.go_down)
                if child.grid_info()['column'] == 0:
                    child.config(takefocus=1)
        resize_scrolled_content(self, self.canvas, self.window)
        self.maxsize(
            int(self.winfo_screenwidth() * 0.90),
            int(self.winfo_screenheight() * 0.90))

        self.search_input.focus_set()

    def select(self, evt):
        current_name = None
        current_person = None

        if evt.widget.grid_info()['row'] == 0:
            return

        self.hilit_row = evt.widget.grid_info()['row']
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] in (0, 1):
                pass            
            elif (child.grid_info()['row'] == self.hilit_row and 
                    child.grid_info()['column'] == 1):
                print("line", looky(seeline()).lineno, "child['text']:", child['text'])
                print("line", looky(seeline()).lineno, "child.cget('text'):", child.cget('text'))
                current_name = child['text'] # should be child.cget('text') ?
        # click name or id in table to change current person
        if evt.type == '4':
            if (evt.widget.grid_info()['column'] == 0 and 
                    evt.widget.grid_info()['row'] == self.hilit_row):
                current_person = int(evt.widget['text'])
            elif (evt.widget.grid_info()['column'] in (1,2,3,4,5) and 
                    evt.widget.grid_info()['row'] == self.hilit_row):
                for child in self.search_table.winfo_children():
                    if (child.grid_info()['row'] == self.hilit_row and
                            child.grid_info()['column'] == 0):
                        current_person = int(child['text'])
            
        if evt.type != '4':
            current_person = int(evt.widget['text'])

        current_name = self.person_autofill_values[current_person][0]["name"]
            
        self.close_search_dialog()
        # if type(current_name) is tuple: # is this the old name type routine?
            # use_name = list(current_name)
            # current_name = "({}) {}".format(use_name[1], use_name[0])
        redraw_person_tab(
            main_window=self.master,
            current_person=current_person,
            current_name=current_name)
        # self.show_top_pic(current_file, current_dir, current_person)

        # self.master.current_person_label.config(
            # text="Current Person (ID): {} ({})".format(
                # current_name, current_person))

    def close_search_dialog(self):
        self.destroy()

    def go_up(self, evt):
        next = evt.widget.tk_focusPrev()
        next.focus_set()

    def go_down(self, evt):
        prior = evt.widget.tk_focusNext()
        prior.focus_set()

    def highlight_on_focus(self, evt):
        self.hilit_row = evt.widget.grid_info()['row']
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] in (0, 1):
                pass
            elif child.grid_info()['row'] == self.hilit_row:
                child.config(bg=self.formats['highlight_bg'])

    def unhighlight_on_unfocus(self, evt):
        self.unhilit_row = evt.widget.grid_info()['row']
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] in (0, 1):
                pass            
            elif child.grid_info()['row'] == self.unhilit_row:
                child.config(bg=self.formats['bg']) 

    def track_column_state(self, evt):
        ''' 
            Bound to column head labels.
            Each column uses its own Tkinter variable to track one of two
            possible states: 1st click or no click. If on being clicked 
            the column was the last one clicked, its state is 'clicked_once'
            so it sorts descending. Otherwise, the column's state is
            'not_clicked' so it sorts ascending. On changing columns 
            the newly clicked column always sorts ascending. ID column 
            autosorts ascending on load.
        '''

        sortcol = evt.widget.grid_info()['column']

        keycols = (0, 6, 10, 11, 7, 8)

        a = 0
        for value in keycols:
            if a == sortcol:
                self.sortkey = value                
            a += 1

        self.sort_by = evt.widget.grid_info()['column']
        ascending = sorted(self.result_rows, key=lambda f: f[self.sortkey])
        descending = sorted(
            self.result_rows, key=lambda f: f[self.sortkey], reverse=True)

        if self.tkvars[self.sort_by].get() == 'not_clicked':
            for k,v in self.tkvars.items():
                if v.get() == 'clicked_once':
                    v.set('not_clicked')
            self.tkvars[self.sort_by].set('clicked_once')
            self.row_list = ascending

        elif self.tkvars[self.sort_by].get() == 'clicked_once':
            self.tkvars[self.sort_by].set('not_clicked')
            self.row_list = descending
        
        self.reorder_column()   

    def reorder_column(self):
        ''' Reconfigure labels in table. '''

        cells = []
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] > 1:
                cells.append([child])

        new_text = []
        for row in self.row_list:     
            new_text.extend(
                (row[0], row[1], row[2][1], row[3][1], row[4], row[5]))

        a = 0
        for lst in cells:
            lst.append(new_text[a])
            a += 1

        for lst in cells:
            lst[0].config(text=lst[1])

    def make_row_list_for_search_results_table(self, unique_match):
        ''' 
            Gets a tuple (person_id, other_names) for one person at a time
            from the Search class which has collected matches from a search  
            input. The unique person data is used to create a row list which 
            will be used to create a sortable search results table with one
            person per row. The other_names value is a list of names by 
            results-table row which will be displayed in a nametip.  
        '''

        self.row_list = []
        self.found_person = unique_match[0]
        self.row_list.append(self.found_person)
        self.other_names = unique_match[1]

        self.display_name = self.person_autofill_values[self.found_person][0]["name"]
        # self.display_name = self.person_autofill_values[self.found_person]["birth name"]
        # if self.display_name is None or len (self.display_name) == 0:
            # self.display_name = self.person_autofill_values[self.found_person]["alt name"]            

        self.row_list.append(self.display_name)
        ext = [[], [], '', '', '', '', '', [], [], []]
        self.row_list.extend(ext[0:])

        # this has to run last
        self.get_values()

    def get_values(self):
        self.get_death()
        self.get_birth()
        if self.other_names:
            self.get_other_names()
        else:
            self.row_list[9] = ''
        self.make_sorters()

    def make_sorters(self):
        ''' 
            self.ma_id & self.pa_id don't exist yet at this point and 
            if there is no birth/offspring event they won't. 
        '''
        self.row_list[6] = self.get_sort_names(self.row_list[0])
        if self.offspring_event:
            self.row_list[10] = self.make_sorter_for_formatted_dates(
                self.row_list)        
            self.row_list[11] = self.make_sorter_for_formatted_dates(
                self.row_list)  

    def make_sorter_for_formatted_dates(self, row):
        ''' 
            Add a sortable date to the search results row lists, for birth 
            column or death column, whichever was clicked. Prefix is 
            stripped out. The storable date string is converted to a list of 
            integers [y,m,d] which extends the existing date key's value for 
            use to sort the table by the date column; BC year integers are made
            negative.
        '''
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_finding_sorter, (self.offspring_event,))
        sorter = cur.fetchone()
        if sorter:
            sorter = sorter[0].split(",")
            sorter = [int(i) for i in sorter]
        else:
            sorter = [0,0,0]

        cur.close()
        conn.close()
        return sorter

    def get_sort_names(self, subject):

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute(select_name_sort_order, (subject,))
     
        sort_name = cur.fetchone()
        cur.close()
        conn.close()
        if sort_name:
            sort_name = sort_name[0].lower()
        elif not sort_name:
            sort_name = ''
        return sort_name

    def get_death(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_person_death_date, (self.found_person,))
        death_date = cur.fetchone()
        cur.close()
        conn.close()

        self.death_date = ['-0000-00-00-------', '']

        if death_date is None:
            self.row_list[3] = self.death_date
            return
        storable_date = death_date[0]
        self.death_date = [storable_date, format_stored_date(storable_date)]

        self.row_list[3] = self.death_date

    def get_birth(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_person_birth_date, (self.found_person,))
        birth_date = cur.fetchone()
        cur.close()
        conn.close()

        self.birth_date = ['-0000-00-00-------', '']

        if birth_date is None:
            self.row_list[2] = self.birth_date
            return

        storable_date = birth_date[1]
        self.birth_date = [storable_date, format_stored_date(storable_date)]
        self.row_list[2] = self.birth_date
        self.offspring_event = birth_date[0]
        self.get_ma()
        self.get_pa()

        self.row_list[7] = self.get_sort_names(self.ma_id)
        self.row_list[8] = self.get_sort_names(self.pa_id)

    def get_ma(self):
        name = None
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        # cur.execute(select_persons_persons_ma_id1, (self.offspring_event,))
        # mom = cur.fetchone()
        # if mom:
            # self.ma_id = mom[0]
        # else:
        cur.execute(select_finding_mother, (self.offspring_event,))
        mom = cur.fetchone()
        if mom:
            self.ma_id = mom[0]
        else:
            self.ma_id = None

        if self.ma_id is not None:
            name = self.person_autofill_values[self.ma_id][0]["name"]
            # name = self.person_autofill_values[self.ma_id]["birth name"]
            # if name is None or len(name) == 0:
                # name = self.person_autofill_values[self.ma_id]["alt name"]        
        
        self.row_list[4] = name

        cur.close()
        conn.close()

    def get_pa(self):
        name = None
        
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute(select_finding_father, (self.offspring_event,))
        pop = cur.fetchone()
        if pop:
            self.pa_id = pop[0]
        else:
            # cur.execute(select_persons_persons_pa_id2, (self.offspring_event,))
            # pop = cur.fetchone()
            # if pop:
                # self.pa_id = pop[0]
            # else:
            self.pa_id = None
        if self.pa_id is not None:
            name = self.person_autofill_values[self.pa_id][0]["name"]
            # name = self.person_autofill_values[self.pa_id]["birth name"]
            # if name is None or len(name) == 0:
                # name = self.person_autofill_values[self.pa_id]["alt name"]
        
        self.row_list[5] = name

        cur.close()
        conn.close()

    def get_other_names(self):
        ''' 
            For nametips. 
        '''

        tip_names = []
        for lst in self.other_names:
            name = lst[0]
            name_type = lst[1]
            tip_names.append([name_type, name])

        name_tips = []
        for lst in tip_names:
            sub = ': '.join(lst)
            name_tips.append(sub)
        name_tips = '\n'.join(name_tips)

        for lst in self.other_names:
            name = lst[0]
            name_type = lst[1]
            name_kv = '{}: {}'.format(name_type, name)
            if lst[2]:
                used_by = lst[2]
            else:
                used_by = 'unknown'
            usedby_kv = 'name used by: {}'.format(used_by)

        self.row_list[9] = name_tips

    def show_nametip(self):
        ''' 
            The nametips will point out that there may be no birth name 
            stored for the person. Or the user might type "Daisy" and 
            get "Alice". The nametip will show that Alice's nickname is 
            Daisy.

            See kintips in events_table.py for a similar hover tip that looks
            the same and has slightly simpler code. A class could be made by
            comparing them and parameterizing the differences.
        '''     
        maxvert = self.winfo_screenheight()

        if self.nametip or not self.nametip_text:
            return
        x, y, cx, cy = self.widget.bbox('insert')        

        self.nametip = d_tip = tk.Toplevel(self.widget)

        label = LabelNegative(
            d_tip, 
            text=self.nametip_text, 
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
        d_tip = self.nametip
        self.nametip = None
        if d_tip:
            d_tip.destroy()

    def make_nametip(self):
        ''' Runs once on widget construction. '''

        self.widget.bind('<Enter>', self.handle_enter)
        self.widget.bind('<Leave>', self.on_leave)

    def handle_enter(self, evt):
        """ Get person id from text in column 0 of pointed row. Find that
            person id as row[id] in search results dicts. In that dict get
            row[other names].
        """

        self.pointed_to = evt.widget
        pointed_row = self.pointed_to.grid_info()['row']
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] in (0, 1):
                pass
            elif (child.grid_info()['column'] == 0 and 
                    child.grid_info()['row'] == pointed_row):
                self.person_id = child['text']
        for row in self.result_rows:
            if row[0] == self.person_id:
                pointed_dict = row
                self.nametip_text = pointed_dict[9]

        if self.nametip_text:
            self.show_nametip()

    def on_leave(self, evt):
        self.other_names = []
        self.off()

class LabelSearch(Label): 
    """ Label for search results column cells. Since this widget responds to 
        several different events, and then still has to respond to the 
        colorizer, somewhere along the way it made the code simpler to treat
        this class separately from other labels. 
    """

    def __init__(self, master, formats, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)

        self.formats = formats
        self.config(anchor='w')






