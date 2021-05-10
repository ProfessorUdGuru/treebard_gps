# places.py

import tkinter as tk
import sqlite3
from files import get_current_file
from window_border import Border
from styles import ThemeStyles, make_formats_dict
from widgets import (
    Toplevel, Frame, Button, LabelH3, Label, RadiobuttonBig, MessageHilited, 
    LabelH3, Entry, ButtonQuiet, Separator)
from scrolling import (
    Combobox, Scrollbar, resize_scrolled_content, MousewheelScrolling)
from query_strings import (
    select_all_nested_places, select_place, select_place_id,
    select_nested_places_same, select_place_id1, select_place_id2,
    select_related_places, insert_place_new, insert_nested_places,
    select_all_nested_pairs, insert_nested_pair, update_finding_nested_places,
    select_nested_places_id, select_count_places, select_place_nickname)

import dev_tools as dt



formats = make_formats_dict()
ST = ThemeStyles
current_file = get_current_file()[0]

class ValidatePlace:
    def __init__(self, master, treebard, finding, place_input, findings, widg):

        self.view = master
        self.treebard = treebard
        self.finding = finding
        self.place_input = place_input
        self.findings = findings
        self.widg = widg

        self.place_dicts = []
        self.singles = []
        self.places_entered = []
        self.labels = []

    def sift_place_input(self):

        # NEED TO REFACTOR THIS METHOD TO USE PAIRS FROM places_places. It's
        #    wrong to use nested places for this as it's not what nested_places
        #    was designed to do and it's too flaky, hard to understand, and 
        #    taking on too much with too little to go on, and too complicated.
        print('57 self.place_input is', self.place_input)

        def find_right_place_id(dkt, multiples, idx):
            '''
                If there's more than one place by the same name, get the id
                for the right one and put it in the dict.
            '''

            print('57 dkt, multiples, idx is', dkt, multiples, idx)

            # new_places = 0
            # for d in self.place_dicts:
                # if d['id'][0] is None:
                    # new_places += 1
            # length = len(self.place_dicts) - new_places
            # eligibles = []
            # for nest in nested_place_ids:
                # if len(nest) == length:
                    # eligibles.append(nest)
            # # print('68 eligibles is', eligibles)
            # deletables = []
            # print('70 self.singles is', self.singles)
# # HAVE TO REDEFINE self.singles BY ADDING NEW SINGLES TO IT AS THEY ARE FOUND AND THEN RERUNNING THE CODE TO FILTER OUT ELIGIBLES AGAIN, MAYBE RUN IT IN A LOOP FOR EACH DICT WHRE THERE ARE MULTIPLES, TRY JUST HARD-CODEDLY RUNNING THE FILTER ONE MORE TIME EG WHEN THERE'S ONLY ONE ITEM IN self.singles THE FIRST TIME THRU EG USA/8. IOW WHATEVER WAS DONE TO FILTER DOWN TO OHIO/125, DO IT AGAIN FOR WASHINGTON COUNTY/None. ONE PROBLEM IS THAT WASHINGTON COUNTY WAS DONE FIRST. IT'S NOT ADJACENT TO ANYTHING IN self.singles SO ELIGIBLES WASN'T WEEDED OUT RELEVANT TO WASHINTON CO THE FIRST TIME THRU. IT MIGHT HELP IF THE NEST NEAREST THE ITEM IN SELF.SINGLES IS RUN FIRST AND THE SINGULAR RESULT FROM THAT RUN THEN ADDED TO SELF.SINGLES, THEN ON THE NEXT RUN IT SHD CATCH THE NEXT MULTIPLES AND GET NONE FOR THIS EXAMPLE. THAT SHD WORK BUT MAYBE BETTER TO MOTHBALL THIS VERSION AND TRY INSTEAD TO REFACTOR THIS SEARCH PROCESS USING PAIRS FROM places_places INSTEAD OF STRINGS FROM nested_places AND IF THAT PROVES WORSE THEN COME BACK TO THIS VERSION AND DO AS SUGGESTED ABOVE BUT i THINK I'M TRYING TO DO IT THE HARD WAY HERE, SHD BE COMPARING PAIRS ONLY. THE PAIRS ARE THE SOURCE OF THE NESTINGS ANYWAY.
            # for num in self.singles:
                # for nest in eligibles:
                    # if num not in nest:
                        # if nest not in deletables:
                            # deletables.append(nest)
            # for nest in deletables:
                # eligibles.remove(nest)
            # print('77 eligibles is', eligibles)
            # filtered_multiples = []
            # for nest in eligibles:
                # for num in multiples:
                    # if num in nest and num not in filtered_multiples:
                        # filtered_multiples.append(num)
            # if len(filtered_multiples) == 1:
                # dkt['id'] = filtered_multiples
            # else:
                # print('81 self.place_dicts is', self.place_dicts)
                # sort_parent_child_same_name(filtered_multiples, eligibles, idx)

        # def sort_parent_child_same_name(filtered_multiples, eligibles, idx):
            # '''
                # When a nest is in a parent by the same name as itself, this
                # determines which is child, which is parent. If the filtered 
                # multiples aren't all in the same nesting, the nesting doesn't 
                # fall in this category.
            # '''

            # filtered = []
            # for nest in eligibles:
                # keep = True
                # for num in filtered_multiples:
                    # if num not in nest:
                        # keep = False
                # if keep is True:
                    # filtered.append(nest)
            # if len(filtered) == 0: # i.e. multiples aren't in the same nesting
                # return
            # dkt['id'] = [filtered[0][idx]]

        def make_place_dicts(j, name):
            cur.execute(select_place_id, (name,))
            match = cur.fetchall()
            match = [i[0] for i in match]
           
            if len(match) == 0:
                self.place_dicts[j]['id'] = [None]
            else:
                self.place_dicts[j]['id'] = match 
 
            self.place_dicts[j]['input'] = name            

        def insert_new_place_db(new_place):
            print('339 new_place is', new_place)
            print('340 self.place_dicts is', self.place_dicts)

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        j = 0
        for name in self.place_input.split(', '):
            self.place_dicts.append({})
            make_place_dicts(j, name)
            j += 1
        # print('124 self.place_dicts is', self.place_dicts)

        for dkt in self.place_dicts:
            if dkt['id'] == [None]:
                continue
            length = len(dkt['id'])
            if length == 1:
                self.singles.append(dkt['id'][0])
        # print('132 self.place_dicts is', self.place_dicts)

        idx = 0
        for dkt in self.place_dicts:
            length = len(dkt['id'])
            multiples = []
            if length > 1:
                multiples.extend(dkt['id'])
                find_right_place_id(dkt, multiples, idx) 
                idx =+ 1
        # print('142 self.place_dicts is', self.place_dicts)

        for dkt in self.place_dicts:
            if dkt['id'][0] is None:
                insert_new_place_db(dkt['input'])
        print('147 self.place_dicts is', self.place_dicts)

        reverse_place_dicts = list(reversed(self.place_dicts))
        e = 0
        for dkt in reverse_place_dicts:

            for num in dkt['id']:
                if num is not None:
                    cur.execute(
                        '''
                            SELECT place_id1
                            FROM places_places
                            WHERE place_id2 = ?
                        ''',
                        (num,))
                    childs = cur.fetchall()
                    childs = [i[0] for i in childs]
                    print('175 childs is', childs)

                    for num2 in childs:
                        print("179 reverse_place_dicts[e + 1]['id'] is", reverse_place_dicts[e + 1]['id'])
                        if num2 in reverse_place_dicts[e + 1]['id']:
                            print('180 num2 is', num2)
                            cur.execute(
                                '''
                                    SELECT place_id1
                                    FROM places_places
                                    WHERE place_id2 = ?
                                ''',
                                (num2,))
                            childs = cur.fetchall()
                            print('186 childs is', childs)
                            break

                else:
                    print('177 num is', num)
                    # check for inserting new level and updating nestings
            e += 1

        for dkt in self.place_dicts:
            '''
                Before putting any more time into this dialog, try to come up 
                with a practical use for it. Does it do anything besides 
                detecting identical place strings? There are easier ways to do 
                that. EDIT: came up with a good use right away. During development
                this is badly needed to alert me if I'm not catching something.
            '''
# Wrongly opens when inputting "Washington County, Ohio, USA".
        
            if len(dkt['id']) > 1:
                print('154 dkt is', dkt)
                print('155 self.place_dicts is', self.place_dicts)
                selection_message = DuplicatePlaceDialog(
                    self.view,
                    self.place_input,
                    'Duplicate place names have been stored. Use which one?', 
                    'Duplicate Place Names Selection',
                    ('OK', 'Cancel'),
                    self.treebard,
                    do_on_ok=self.input_places_to_db,
                    selection=dkt['id'])
        cur.close()
        conn.close()

    def input_places_to_db(self):
        return # REMOVE WHEN READY TO RUN THIS CODE
        print('165 self.place_dicts is', self.place_dicts)
        def input_new_place(place):
            cur.execute(insert_place_new, (place,))
            conn.commit()

            cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'place'")
            new_place_id = cur.fetchone()[0]
            input_this.append(new_place_id)            

        def input_old_place(place):
            input_this.append(place)

        def input_nest_to_db(nest):
            len_nest = len(nest)
            new_place_string = tuple(nest + [None] * (9 - len_nest))
            if new_place_string[0]:
                cur.execute(insert_nested_places, new_place_string)
            conn.commit()

            cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'nested_places'")
            new_place_string_id = cur.fetchone()[0]
            return new_place_string_id

        input_this = []
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        for place in self.places_entered:
            place_type = type(place)
            if place_type is str:
                if len(place) == 0:
                    continue
                input_new_place(place)
            elif place_type is int:
                input_old_place(place)
        if len(input_this) == 1:
            input_this.append(None)

        for i in range(len(input_this) - 1):
            pair = (input_this[i], input_this[i+1])
            cur.execute(select_all_nested_pairs)
            all_pairs = cur.fetchall()
            if pair not in all_pairs:
                cur.execute(insert_nested_pair, (pair))
                conn.commit()

        nestings = []
        old_nestings = []
        for f in range(len(input_this)):
            nestings.append(input_this[f:])
        if len(nestings) > 0:
            old_nestings = get_autofill_places()
        else:
            pass
        if len(old_nestings) > 0:
            r = 0
            for nest in nestings:
                if nest not in old_nestings:
                    new_place_string_id = input_nest_to_db(nest)
                    if r == 0:
                        right_nest = new_place_string_id 
                    r += 1
                else:
                    if r == 0:
                        lacking_nulls = 9 - len(nest)        
                        nest = tuple(nest + [None] * lacking_nulls)
                        cur.execute(select_nested_places_id, nest)
                        right_nest = cur.fetchone()[0]
                    r += 1
            self.do_place_update(right_nest)

        place_strings = make_autofill_strings()
        for row in self.findings:
            widg = row[2][0]
            widg.values = place_strings

        place_string = []
        for num in nestings[0]:
            if num:
                cur.execute(select_place, (num,))
                stg = cur.fetchone()[0]
                place_string.append(stg)
            else:
                break
        place_string = ', '.join(place_string)
        self.widg.delete(0, 'end')
        self.widg.insert(0, place_string)
        cur.close()
        conn.close()

    def do_place_update(self, right_nest):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(
            update_finding_nested_places, 
            (right_nest, self.finding))
        conn.commit()
        cur.close()
        conn.close()

class DuplicatePlaceDialog():
    def __init__(
            self,
            parent, 
            place_input,
            message, 
            title,
            button_labels,
            treebard,
            do_on_ok=None,
            selection=None
):

        self.parent = parent
        self.place_input = place_input
        self.message = message
        self.title = title
        self.button_labels = button_labels
        self.treebard = treebard
        self.do_on_ok = do_on_ok
        self.selection = selection

        self.got_row = 0

        self.make_widgets()
            # self.parent, 
            # self.title,
            # message,
            # self.button_labels, 
            # self.treebard,
            # do_on_ok=self.do_on_ok)

    def make_widgets(self):
        # self,
        # parent, 
        # title, 
        # message, 
        # button_labels, 
        # treebard, 
        # do_on_ok=None):

        def show_message():

            window.columnconfigure(1, weight=1)
            window.rowconfigure(1, weight=1)
            lab = MessageHilited(window, text=self.message, justify='left', aspect=1200)
            lab.grid(column=1, row=1, sticky='news', padx=3, pady=3)

        def ok():
            if self.do_on_ok:
                self.do_on_ok()
            cancel()

        def cancel():
            selection_dialog.destroy()

        selection_dialog = Toplevel(self.parent)
        selection_dialog.columnconfigure(1, weight=1)
        selection_dialog.rowconfigure(4, weight=1)
        canvas = Border(selection_dialog, size=3) # size shd not be hard-coded            
        canvas.title_1.config(text=self.title)
        canvas.title_2.config(text='')

        window = Frame(canvas)
        canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

        self.treebard.scroll_mouse.append_to_list([canvas, window])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        window.vsb = Scrollbar(
            selection_dialog, 
            hideable=True, 
            command=canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            selection_dialog, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        buttonbox = Frame(window)
        b1 = Button(buttonbox, text=self.button_labels[0], width=7, command=ok)
        b2 = Button(buttonbox, text=self.button_labels[1], width=7, command=cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        window.columnconfigure(2, weight=1)
        window.rowconfigure(1, minsize=60)
        minsize = len(self.selection) * 96
        window.rowconfigure(2, weight=1, minsize=minsize)
        window.rowconfigure(3, minsize=48)
        buttonbox.grid(column=1, row=3, sticky='se')

        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.frm = Frame(window)
        self.frm.grid(column=1, row=2, sticky='news')

        show_message()
        self.show_choices()
        self.make_edit_row()

        resize_scrolled_content(selection_dialog, canvas, window)

        selection_dialog.focus_set()

    def make_edit_row(self):
        self.edit_row = Frame(self.frm)

        self.ent = Entry(self.edit_row, width=60)

        merge_butt = Button( 
            self.edit_row, 
            text='Merge',
            # command=get_edit_state
)
        cancel_butt = Button(
            self.edit_row,
            text='Cancel',
            command=self.remove_edit_row
)
        delete_butt = Button(
            self.edit_row,
            text='Delete',
            # command=delete_role
)
        self.edit_row.grid(column=0, row=self.got_row, columnspan=4, sticky='ew')
        self.ent.grid(column=0, row=0, padx=3, pady=3)
        merge_butt.grid(column=2, row=0, padx=6, pady=6)
        cancel_butt.grid(column=3, row=0, padx=6, pady=6)
        delete_butt.grid(column=4, row=0, padx=6, pady=6)
        self.edit_row.grid_remove()

    def remove_edit_row(self):
        self.edit_row.grid_forget()
        # resize_scrollbar()
        # resize_window()

    def grid_edit_row(self):
        self.edit_row.grid(column=0, row=self.got_row, columnspan=4, sticky='ew')
        for child in self.frm.winfo_children():
            if child.grid_info()['column'] == 1 and child.grid_info()['row'] == self.got_row:
                nickname = child.cget('text')
        self.ent.delete(0, 'end')
        self.ent.insert(0, nickname)
        self.ent.focus_set()

    def get_clicked_row(self, evt):
        self.got_row = evt.widget.grid_info()['row'] 

    def on_hover(self, evt):
        evt.widget.config(text='Edit') 

    def on_unhover(self, evt):
        evt.widget.config(text='')

    def show_choices(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        var = tk.IntVar()
        d = 0
        for place_id in self.selection:

            cur.execute(select_place_nickname, (place_id,))
            nickname = cur.fetchone()[0]

            place_string = 'Place ID #{}: {}'.format(place_id, self.place_input)

            rad = RadiobuttonBig(self.frm, variable=var, text=place_string)
            rad.grid(column=0, row=d, columnspan=2)
            if d == 0:
                rad.focus_set()

            lab = Label(self.frm, text='Duplicate place name hint:')
            lab.grid(column=0, row=d+1, sticky='w')

            hint = Label(self.frm, text=nickname)
            hint.grid(column=1, row=d+1, sticky='w', padx=(0,3))

            sep = Separator(self.frm, 3)
            sep.grid(column=0, row=d+2, sticky='ew', columnspan=3, pady=(3,0))

            editx = ButtonQuiet(self.frm, width=2, command=self.grid_edit_row)
            editx.grid(column=2, row=d+1)
            editx.bind('<Enter>', self.on_hover)
            editx.bind('<Leave>', self.on_unhover)
            editx.bind('<Button-1>', self.get_clicked_row)
            editx.bind('<space>', self.get_clicked_row)
            editx.bind('<FocusIn>', self.on_hover)
            editx.bind('<FocusOut>', self.on_unhover)

            d += 3

        cur.close()
        conn.close()

def get_autofill_places():

    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_nested_places)
    nested_place_ids = cur.fetchall()
    cur.close()
    conn.close()
    nested_place_ids = [[i for i in lst if i] for lst in [list(j) for j in nested_place_ids]]
    return nested_place_ids

def make_autofill_strings():
    nested_place_ids = get_autofill_places()
    strings = [', '.join([get_string_with_id(num) for num in lsst]) for lsst in nested_place_ids]
    return strings

def get_string_with_id(num):
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_place, (num,))
    stg = cur.fetchone()[0]  
    cur.close()
    conn.close()
    return stg

place_strings = make_autofill_strings()
nested_place_ids = get_autofill_places()



'''

240 self.place_dict is {0: {'input': 'Portland', 'id': [146, 788, 791]}, 1: {'input': 'New Twp', 'id': [None]}, 2: {'input': 'Meigs County', 'id': [787]}, 3: {'input': 'Ohio', 'id': [125, 782, 785]}, 4: {'input': 'USA', 'id': [8]}}

input where only the highest place eg USA is known: there's no way to slim down the multiples bec most of them are in the US so most of them don't get removed during the sifting process. Probably going to have to open a new place dialog any time there's only one known place? Test.

269 self.place_dict is {0: {'input': 'Portland', 'id': [146, 788, 791]}, 1: {'input': 'New County', 'id': [None]}, 2: {'input': 'Maine', 'id': [682, 683]}, 3: {'input': 'USA', 'id': [8]}}

199 self.place_dict is {0: {'input': 'Dupe', 'id': [206, 207]}, 1: {'input': 'A Co', 'id': [208, 208]}, 2: {'input': 'Colorado', 'id': [7]}, 3: {'input': 'USA', 'id': [8]}}

            Terminology:
            nested place, nested place string, nesting: 'Florida, United States'
            nest, place: 'Florida' or 'United States'
            parent: larger containing nest
            child: smaller contained nest
            match: a nest matching user-input is in the database so has an ID

            Most need for a new place dialog was illusional. TEST THIS BY INPUTTING REAL DATA ABOUT REAL PLACES THAT CHANGED PARENTS, NAMES, BORDERS ETC. INCLUDE THE SPAN OF TIME FIELD.

            Handle these cases: SEE DO LIST @ bottom of events_table.py for more cases
            if no matches for at least one nest in a nested place:
                if at least one match for one nest in that nesting:
                    get known ids, don't open new place dialog
                elif no matches for any nest in that nesting:
                    create new ids, don't open new place dialog;
            elif exactly one match in every nest: 
                all the place nests already exist unambiguously, so 
                    don't open new place dialog;
            elif more than one match in at least one nest: 
                if two or more places by the same name have the same parent: 
                    open new place dialog; SEE BELOW*
                else:
                    don't open new place dialog

            Opening a dialog all the time (or ever?) for user confirmation is wrong. Multiple matches can almost always be weeded down to exactly one. This is because a nested place is almost always unique. There may be dozens of places named "Paris", but how many of these places are nested in a larger place called "Ile-de-France", which is in turn nested in an even larger place called "France"? Exactly one. The same strategy works for Paris, Texas. In very few cases it won't work to identify a place by its nesting, and in those cases a new place dialog can open for user confirmation. I'm no longer sure there is such a case. If so, it would probably have to do with historical border changes, name changes and jurisdiction changes.

            *In the extremely rare case of two different
            places by the same name having different parents by the same name,
            an error message will direct the user to input unique names for one
            of the pairs. The sample database contains two different places 
            named 'Dupe, A Co, Colorado, USA' for testing this case, so code can
            be written eventually to deal with it properly. The user should never
            have to nickname a place, though by doing research he'd probably find
            a suitable distinguishing historical nickname anyway. It's possible
            that no such edge case actually exists where there is not a unique
            nickname for each place, since nearby places were named uniquely
            for practical purposes before computer genealogy came along. The
            real problem is when the places aren't close to each other, in which
            case historically they didn't need to be distinguished from each other.
            The primary key does this for the simple purposes of the database, but
            in our case there are nested strings to deal with and the user enters
            these strings, not place IDs; then the code has to figure out what
            place is intended. So if the places aren't close to each other, there's still not a problem because one will be nested in Africa and the other in Greece. In any case this one is not an emergency and I doubt it will ever be needed.

            The new goal is to handle all data in a single nested 
            dictionary, with one dict for each place entered into the events 
            table place column autofill. The keys can't be the entered
            data because that's a string and you can have place names
            repeated in a nesting, e.g. "Sassari, Sassari, Sardegna, Italy" but dict keys
            can't be repeated without extra code. You'd think that the ID should be the dict key. But if the id
            is not known then in the case where there are already two or more
            places by the same name in the database, the dict key could be a 
            list of possible ids. But in the case where there is not yet any place
            by the name entered, a quick insert to the database to get an ID
            is wrong because the user might change his mind about entering the
            place, so the right thing to use as the index is the
            index of the dict as if it were within the list of dicts. This seems to make the
            idea of using a dict instead of a list of dicts beside the point but it's still easier to use
            a dict for this than a bunch of complex indexing in a list of lists. If it doesn't help I might go back to a list of dicts but for now I'll try a single nested dict for each user input on tabbing out of the place field.
            Here is the intended list of dicts for 
                Paris, Linn County, Iowa, USA
            There are multiple Parises and multiple Linn Counties in the database 
            so it will test the code well:
            
            self.place_dict = {
                0 : {'input' : 'Paris', 'id' : [30, 32, 34, 684, 685, etc.]} ,
                1 : {'input' : 'Linn County', 'id' : [743, 758]},
                2 : {'input' : 'Iowa', 'id' : [116]}
                3 : {'input' : 'USA', 'id' : [8]}
            }

            TRIED THAT and it shows potential but now I have hard-coded dict keys that started life as list indexes and it's getting complicated because so before proceeding I have to change the dict of dicts to a list of dicts instead of using indexes as dict keys. The goal is now to save each nest as a dict in a list where the outer list index is the nesting order. Using place_id as primary key starts out looking like this...

            self.place_dicts = [
                (30, 32, 34, 684, 685, etc.) : {
                    'input' : 'Paris', 
                    'widget' : '', 
                    'final' : ''},
                (743, 758) : {
                    'input' : 'Linn County', 
                    'widget' : '', 
                    'final' : ''},
                (116) : {
                    'input' : 'Iowa', 
                    'widget' : '', 
                    'final' : ''},
                (8) : {
                    'input' : 'USA', 
                    'widget' : '', 
                    'final' : ''},
            ]
    
            ...and gets filtered down to this:

            self.place_dicts = [
                (684) : {
                    'input' : 'Paris', 
                    'widget' : '', 
                    'final' : ''},
                (743) : {
                    'input' : 'Linn County', 
                    'widget' : '', 
                    'final' : ''},
                (116) : {
                    'input' : 'Iowa', 
                    'widget' : '', 
                    'final' : ''},
                (8) : {
                    'input' : 'USA', 
                    'widget' : '', 
                    'final' : ''},
            ]

            But this won't work either, because for new places the key will start out as [None], and [None] == [None], so the keys aren't unique and I can't have more than one new place in a nesting that way. 

            What if all new places were instantly given an ID and put into the dict that way instead of having Nones hanging out causing trouble? Is there any question when new input exists that a new place needs to be made? No. The reason I hadn't wanted to make a new place immediately is that I'd hoped to avoid miscellaneous hits on the db and do input all at once after everything is validated, but really if there is no doubt that a place is a new place, then it can just be created immed. But I was thinking, what if the user hits Cancel? Well there's no cancel button. When he tabs out the places are going to be created anyway, and if he changes his mind he'll just have to delete or edit the place in the places tab. Actually when there's a new place dialog there will be a cancel button in which case the new places would have to be deleted. Also the multiple hits on the db problem was about needing to update 3 db tables when creating one place. So it's still better not to make new places till all is validated or it will get messy. One alternative is to fool around with assigning temp names when id is None, to be used for dict keys. Another is to use itermediatry collections until the validation is complete but in that case there's no reason to use a dict at all.

            So if inserting two new places the temporary keys will be strings made from the list indexes. The collection will look like this and by the time the temp keys need to be replaced with real db table IDs, the dict will be ready to discard anyway:

            self.place_dicts = [
                ['0'] : {
                    'input' : 'Union Station Depot', 
                    'widget' : '', 
                    'final' : ''},
                [684] : {
                    'input' : 'Paris', 
                    'widget' : '', 
                    'final' : ''},
                ['2'] : {
                    'input' : 'Sandbag Township', 
                    'widget' : '', 
                    'final' : ''},
                [743] : {
                    'input' : 'Linn County', 
                    'widget' : '', 
                    'final' : ''},
                [116] : {
                    'input' : 'Iowa', 
                    'widget' : '', 
                    'final' : ''},
                [8] : {
                    'input' : 'USA', 
                    'widget' : '', 
                    'final' : ''},
            ]

        But this is hard to loop over or else it's just hard for me personally to understand it and the reason is that it's more complex than necessary. There's no reason for it to be a NESTED dict. I already have a reference to the dicts, which are the outer list indices. What's needed is just a simple dict for each place nest at a position within the list. Go back to having a key called ['id']. This is the final form, including two new places which will now automatically have a reference to their position since it's a LIST of dicts instead of a DICT of dicts:

            self.place_dicts = [
                {
                    'id' : [None],
                    'input' : 'Union Station Cafe', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [30, 32, 34, 684, 685, etc.],
                    'input' : 'Paris', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [None],
                    'input' : 'Southwell Township', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [743, 758],
                    'input' : 'Linn County', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [116],
                    'input' : 'Iowa', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [8],
                    'input' : 'USA', 
                    'widget' : '', 
                    'final' : ''},
            ]
    
            ...and gets filtered down to this:

            self.place_dicts = [
                {
                    'id' : [None],
                    'input' : 'Union Station Cafe', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [684],
                    'input' : 'Paris', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [None],
                    'input' : 'Southwell Township', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [743],
                    'input' : 'Linn County', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [116],
                    'input' : 'Iowa', 
                    'widget' : '', 
                    'final' : ''},
                {
                    'id' : [8],
                    'input' : 'USA', 
                    'widget' : '', 
                    'final' : ''},
            ]

        This is now ready to submit to the database, with IDs autogenerated for the new places and instantly used for all three database tables where they're needed. I don't think the 'widget' and 'final' keys will be used but I'm not done yet so who knows.

'''