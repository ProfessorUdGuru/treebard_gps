# search.py

import tkinter as tk
import sqlite3
from files import project_path, current_file
from window_border import Border
from scrolling import MousewheelScrolling, Scrollbar, resize_scrolled_content
from styles import config_generic, make_formats_dict
from widgets import (
    Toplevel, Frame, Button, MessageHilited, Entry, LabelH2, Label, LabelH3,
    LabelNegative)
from names import get_name_with_id, open_new_person_dialog
from dates import OK_PREFIXES, format_stored_date
from query_strings import (
    select_person_distinct_like, select_name_details,
    select_finding_sorter, select_name_sort_order, select_person_death_date,
    select_person_birth_date, select_findings_persons_ma_id1, 
    select_findings_persons_ma_id2, select_findings_persons_pa_id1,
    select_findings_persons_pa_id2,
)
import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()
COL_HEADS = ('ID', 'Birth Name', 'Birth', 'Death', 'Mother', 'Father')

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
            names_tab, pic, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.master = master # this is an instance of Main (a Frame)
        self.root = root
        self.treebard = treebard
        self.entry = entry
        self.findings_table = findings_table
        self.names_tab = names_tab
        self.pic = pic

        self.result_rows = []
        self.hilit_row = None
        self.unhilit_row = None

        self.sent_text = '' 
 
        self.new_current_id = None
        self.new_current_person = None

        self.all_matches = [] 
        self.tkvars = {}
        self.sort_by = None 

        self.widget = None
        self.nametip = None
        self.x = self.y = 0

        self.nametip_text = None
        self.name_list = []

        self.pointed_to = None
        self.person_id = None

        self.ma_id = None
        self.pa_id = None
        self.offspring_event = None

        self.make_widgets()

    def make_widgets(self):

        self.title('Person Search')
        self.geometry('+100+20')
        # self.grab_set()

        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, size=3) # don't hard-code size
        self.canvas.title_1.config(text="Person Search Dialog")
        self.canvas.title_2.config(text="")

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
            text='Add New Person',
            command=lambda master=self,
                inwidg=self.entry,
                root=self.root,
                inwidg2=self.search_input: open_new_person_dialog(
                    master, inwidg, root, inwidg2))
            # command=lambda inwidg=self.search_input, 
                # treebard=self.treebard, 
                # host_dlg=self,
                # inwidg2=self.search_input: open_new_person_dialog(
                    # host_dlg, inwidg, self.root))

# people = make_values_list_for_person_select()        
# all_birth_names = EntryAuto.create_lists(people)
# self.person_entry.values = all_birth_names


        self.person_adder.grid(column=2, row=1, padx=12, pady=12)

        self.search_table = Frame(self.window)
        self.search_table.grid(
            column=0, row=1, sticky='news', padx=48, pady=48)

        # # STATUSTIPS
        # visited = [
            # (self.search_input, 
            # "Person Search Input", 
            # "Type any part of any name or ID number; table will fill "
                # "with matches."),
            # (self.search_table.mainframe, 
            # "Person Search Table", 
            # "Select highlighted row with Enter or Space key to change "
                # "current person, or double-click any row.")]

        # tips = stt.StatusBarTooltips(self) 

        # tips.status.grid(column=0, row=3, sticky='w', ipadx=3, ipady=3)
        # tips.tooltip.grid(column=0, row=3, sticky='e', ipadx=3, ipady=3)

        # tips.run_statusbar_tooltips(visited, tips.status, tips.tooltip)

        # # RIGHT-CLICK CONTEXT HELP
        # self.master.master.rc_menu.help_per_context = {
            # self.search_input : (
                # 'This person search tool is especially helpful if you know only '
                # 'part of the name you\'re looking for. Also, if there\'s more than '
                # 'one person with an identical name, the other way to select a '
                # 'person--the autofill person select field--won\'t work for '
                # 'duplicate names unless you know the ID. This search dialog '
                # 'will help you '
                # 'differentiate among several people with similar names by '
                # 'showing birth and death dates and parent names for each '
                # 'person. Just type any part of any name, ID number, nickname, '
                # 'a.k.a., etc. and the search table will fill with matching '
                # 'names. Tab out of the input field to the table and navigate '
                # 'up and down using the Tab or Ctrl+Tab keys or the Up/Down arrow ' 
                # 'keys. You can select a new current person but you don\'t have '
                # 'to. The search tool is also an easy way to look up a name '
                # 'or ID number you need.', 
                # 'Person Search Input Context Help'),
            # self.search_dlg_heading : (
                # 'After tabbing into the search results table, you can '
                # 'navigate up and down the table with Tab or Ctrl+Tab keys, or '
                # 'Up/Down arrow keys. To choose a new current person, press '
                # 'Enter or Spacebar when the person you want is highlighted, '
                # 'or double-click any row whether it\'s highlighted or not. '
                # 'The table can be sorted '
                # 'ascendingly or descendingly by single clicks of the column '
                # 'heads. If you typed "lou" and '
                # '"Fred Jenkins" pops up, what\'s going on? Point at the name '
                # 'and a nametip will pop up giving the needed information: '
                # '"Nickname: Louie", along with any other names, ID numbers, '
                # 'nicknames, pseudonyms, married names, mis-spellings, and any '
                # 'other name information you\'ve entered for Fred Jenkins. '
                # 'And because this search tool is so '
                # 'powerful, you have to close it before you\'ll be able to '
                # 'close this help dialog. Just kidding. No I\'m not. Remind '
                # 'me to fix that.', 
                # 'Person Search Table Context Help')}

        # when adding a widg & msg to rc_help.help_per_context above, 
        #    remember to add widg to tuple below

        # for widg in (self.search_input, self.search_dlg_heading):
            # widg.bind(
                # "<Button-3>", 
                # self.master.master.rc_menu.attach_rt_clk_menu)

        self.make_header_row()

        config_generic(self)

        resize_scrolled_content(self, self.canvas, self.window)

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
                    self.search_table, cursor='hand2')
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
                # child.bind('<Double-Button-1>', self.select)
                child.bind('<Return>', self.select)
                child.bind('<Key-space>', self.select)
                child.bind('<FocusIn>', self.highlight_on_focus)                
                child.bind('<FocusOut>', self.unhighlight_on_unfocus)
                child.bind('<Key-Up>', self.go_up)
                child.bind('<Key-Down>', self.go_down)
                if child.grid_info()['column'] == 0:
                    child.config(takefocus=1)
        config_generic(self)
        resize_scrolled_content(self, self.canvas, self.window)
        self.maxsize(
            int(self.winfo_screenwidth() * 0.90),
            int(self.winfo_screenheight() * 0.90))

        self.search_input.focus_set()

    def select(self, evt):

        if evt.widget.grid_info()['row'] == 0:
            return

        self.hilit_row = evt.widget.grid_info()['row']
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] in (0, 1):
                pass            
            elif (child.grid_info()['row'] == self.hilit_row and 
                    child.grid_info()['column'] == 1):
                self.new_current_person = child['text']
        # handle the double-click event
        if evt.type == '4':
            if (evt.widget.grid_info()['column'] == 0 and 
                    evt.widget.grid_info()['row'] == self.hilit_row):
                self.new_current_id = evt.widget['text']
            elif (evt.widget.grid_info()['column'] in (1,2,3,4,5) and 
                    evt.widget.grid_info()['row'] == self.hilit_row):
                for child in self.search_table.winfo_children():
                    if (child.grid_info()['row'] == self.hilit_row and
                            child.grid_info()['column'] == 0):
                        self.new_current_id = child['text']
            
        if evt.type != '4':
            self.new_current_id = evt.widget['text']

        self.new_current_person = get_name_with_id(self.new_current_id)
        self.close_search_dialog()

        self.findings_table.redraw(evt, current_person=self.new_current_id)

        self.master.current_person_label.config(
            text="Current Person (ID): {} ({})".format(
                self.new_current_person, self.new_current_id))

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
                child.config(bg=formats['highlight_bg'])

    def unhighlight_on_unfocus(self, evt):
        self.unhilit_row = evt.widget.grid_info()['row']
        for child in self.search_table.winfo_children():
            if child.grid_info()['row'] in (0, 1):
                pass            
            elif child.grid_info()['row'] == self.unhilit_row:
                child.config(bg=formats['bg']) 

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
            person per row. The other_names value is a list of names by results
            table row which will be displayed in a nametip.  
        '''

        self.row_list = []
        self.found_person = unique_match[0]
        self.row_list.append(self.found_person)
        self.other_names = unique_match[1]

        self.display_name = get_name_with_id(self.found_person)

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
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_findings_persons_ma_id1, (self.offspring_event,))
        mom = cur.fetchone()
        if mom:
            self.ma_id = mom[0]
        else:
            cur.execute(select_findings_persons_ma_id2, (self.offspring_event,))
            mom = cur.fetchone()
            if mom:
                self.ma_id = mom[0]
            else:
                self.ma_id = None

        self.row_list[4] = get_name_with_id(self.ma_id)

        cur.close()
        conn.close()

    def get_pa(self):
        
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute(select_findings_persons_pa_id1, (self.offspring_event,))
        pop = cur.fetchone()
        if pop:
            self.pa_id = pop[0]
        else:
            cur.execute(select_findings_persons_pa_id2, (self.offspring_event,))
            pop = cur.fetchone()
            if pop:
                self.pa_id = pop[0]
            else:
                self.pa_id = None

        self.row_list[5] = get_name_with_id(self.pa_id)
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
        ''' Some rows in the search results table have no name
            because the displayed findings only show birth names. The
            nametips will point out that there may be no birth name 
            stored for the person. Or the user might type "Daisy" and 
            get "Alice". The nametip will show that Alice's nickname is 
            Daisy. 
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
            bg=formats['highlight_bg'])
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
        ''' 
            Get person id from text in column 0 of pointed row. Find that
            person id as row[id] in search results dicts. In that dict get
            row[other names].
        '''

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
    ''' 
        Label for search results column cells. Since this widget responds to 
        several different events, and then still has to respond to the 
        colorizer, somewhere along the way it made the code simpler to treat
        this class separately from other labels. 
    '''

    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()
        self.config(anchor='w')






