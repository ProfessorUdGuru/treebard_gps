# sets_for_nested_places

import tkinter as tk
from widgets import (
    Toplevel, Frame, Button, Label, RadiobuttonBig, MessageHilited, 
    Entry, ButtonQuiet)
from place_autofill import EntryAuto
from toykinter_widgets import Separator
from query_strings import (
    select_all_nested_places, select_place, select_place_id, 
    select_place_hint, select_all_places, select_all_places_places, 
    select_first_nested_place, update_place_hint, select_place_id2, 
    select_max_place_id, select_place_id1, update_finding_nested_places,
    insert_place_new_with_id, insert_nested_pair, insert_nested_places,
    select_nested_places_id, select_places_places_id)
from files import current_file
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
import dev_tools as dt
from dev_tools import looky, seeline
import sqlite3







def get_autofill_places():

    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_nested_places)
    nested_place_ids = cur.fetchall()
    cur.close()
    conn.close()
    nested_place_ids = [[i for i in lst if i] 
        for lst in [list(j) for j in nested_place_ids]]
    return nested_place_ids

def make_autofill_strings():
    nested_place_ids = get_autofill_places()
    strings = [', '.join([get_string_with_id(num) 
        for num in lsst]) for lsst in nested_place_ids]
    return strings

def get_string_with_id(num):
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_place, (num,))
    stg = cur.fetchone()[0]  
    cur.close()
    conn.close()
    return stg

def get_all_places_places():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_places_places)
    places_places = cur.fetchall()
    cur.close()
    conn.close()
    return places_places

def make_global_place_lists():
    place_strings = make_autofill_strings()
    nested_place_ids = get_autofill_places()
    places_places = get_all_places_places()
    return place_strings, nested_place_ids, places_places

place_strings, nested_place_ids, places_places = make_global_place_lists()

conn = sqlite3.connect(current_file)
cur = conn.cursor()
cur.execute(select_all_places)
all_place_names = [i[0] for i in cur.fetchall()]
cur.close()
conn.close()

unique_place_names = set(all_place_names)

            # self.final = ValidatePlace(
                # self.root, 
                # self.treebard, 
                # self.finding, 
                # self.final,
                # self.findings,
                # widg)

class ValidatePlace():

    # def __init__(self, root, treebard, place_input, finding):
    def __init__(self, root, treebard, place_input, finding, nested_place):

        self.root = root
        self.treebard = treebard
        self.place_input = place_input
        self.finding = finding
        self.nested_place = nested_place

        self.place_dicts = []

        self.new_places = False
        self.inner_duplicates = False
        self.outer_duplicates = False
        self.open_dialog = True
        self.all_new = False
        self.all_known = False

        self.make_place_dicts()
        self.id_orphans()
        self.see_whats_needed()
        self.open_new_places_dialog()

    def make_place_dicts(self):
        '''
        User must separate nests with a comma and any number of spaces including 
        no spaces. Nestings will be stored correctly with a comma and one space
        separating nests, and autofill relies on places being typed this way,
        but the validation process doesn't care about spaces, just the comma.

        This method systematically stores the traits of each nest before anything 
        else is done, instead of haphazardly swatting at a moving target with a bunch of
        conditional tests. For example, it might seem lame to store the index when the
        index could be detected at any time, but if it's stored up front then the
        detection procedure won't interrupt the procedure for doing something
        with the nestings based on the detected traits. This lets us change the
        position of the nest within the nesting later (e.g. if a new nest is inserted),
        without changing the list of dicts, by changing the value of dkt['index'].

        The traits of a nesting are: 
            "id" : list of place IDs whose nest string matches nest input,
            "input" : nest string input,
            "same_out" : how many nests are stored with the same spelling,
            "same_in" : how many nests in this nesting are spelled the same as input 
        '''

        def get_matching_ids(nest):
            cur.execute(select_place_id, (nest,))
            ids = cur.fetchall()
            ids = [i[0] for i in ids]
            return ids
    
        def flag_inner_dupes():
            n = 0
            for dkt in self.place_dicts:
                if len(dkt["id"]) > 1:
                    name = dkt["input"]
                    if self.place_list.count(name) > 1:
                        dkt["inner_dupe"] = True
                    else:
                        dkt["inner_dupe"] = False
                n += 1

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.place_list = self.place_input.split(",")
        self.place_list = [self.place_list[i].strip() for i in range(len(self.place_list))]
        self.length = len(self.place_list)

        self.place_dicts = [
            (
                { 
                    "id" : get_matching_ids(x),
                    "input" : x}) 
            for x in self.place_list]
        flag_inner_dupes()
        cur.close()
        conn.close()

    def id_orphans(self):
        '''
            If a nest by an input spelling exists (single or duplicate), 
            and is not the largest nest in the nesting, and the next nest in the nesting is not its parent, create a temp_id
            for it in case the user intends to create a new place instead
            of using an existing place by that name. For orphans there will
            be both an id and a temp_id in the dict. All temp_ids have to be assigned at the same time so they are unique, therefore a temp_id of 0 is created here. Later on any temp_id of 0 will be given its real value.
        '''
        def seek_parent_ids(ids, parent_ids):
            orphan = False
            pairs_in_db = []
            pairs_in_input = []
            pairs = None
            for num in ids:
                cur.execute(select_place_id2, (num,))
                parent_id_in_db = [i[0] for i in cur.fetchall()]
                for iD in parent_id_in_db:
                    pairs_in_db.append((num, iD))
                for iD in parent_ids:
                    pairs_in_input.append((num, iD))
                pairs = tuple(pairs_in_db)
            if pairs:
                st = set(pairs).intersection(pairs_in_input)
                if len(st) == 0:
                    orphan = True
            return orphan

        orphans = []

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        x = 0
        for dkt in self.place_dicts[0:-1]:
            ids = dkt["id"]
            parent_ids = self.place_dicts[x + 1]["id"]
            parent_len = len(parent_ids)
            if parent_len == 0:
                orphan = True
            else:
                orphan = seek_parent_ids(ids, parent_ids)            
            orphans.append(orphan)
            x += 1

        cur.close()
        conn.close()
        
        s = 0
        for dkt in self.place_dicts[0:-1]:
            if orphans[s] is True:
                dkt["temp_id"] = 0
            s += 1            

    def see_whats_needed(self):
        for dkt in self.place_dicts:
            if len(dkt["id"]) == 0:
                self.new_places = True
            elif len(dkt["id"]) > 0:
                if dkt.get("temp_id") is not None:
                    self.new_places = True
                elif len(dkt["id"]) > 1 and dkt["inner_dupe"] is False:
                    self.outer_duplicates = True
                elif len(dkt["id"]) > 1 and dkt["inner_dupe"] is True:
                    self.inner_duplicates = True
                elif len(dkt["id"]) == 1:
                    pass
                else:
                    print("line", looky(seeline()).lineno, "case not handled", dkt['id'])
            else:
                print("line", looky(seeline()).lineno, "case not handled")
        if self.new_places is True:
            self.make_new_places()
        if self.inner_duplicates is True:
            self.handle_inner_duplicates()
        if self.outer_duplicates is True:
            self.handle_outer_duplicates()

    def make_new_places(self):
        '''
            The place IDs have to be assigned at the same time so that each
            number is unique, then entry to the database has to be done all
            at the same time while this information is still correct. After
            the max ID is obtained from the database, no db tranactions can
            occur which insert to any of the place tables till these temp IDs
            are either used or discarded.
        '''
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_max_place_id)
        temp_id = cur.fetchone()[0] + 1
        for dkt in self.place_dicts:
            if (
                (dkt.get("id") is not None and dkt.get("temp_id") is not None) 
                    or len(dkt["id"]) == 0):
                dkt["temp_id"] = temp_id
                temp_id += 1
        cur.close()
        conn.close()

    def handle_inner_duplicates(self):
        '''
            This will handle one pair of inner duplicates. Otherwise, tell the
            user to find unique historically correct names for some places.
        '''

        def handle_non_contiguous_dupes():
            # apparently this won't be needed
            pass

        inner_dupes_idx = []
        i = 0
        for nest in self.place_list:
            if self.place_list.count(nest) > 1:
                same = nest
                inner_dupes_idx.append(i)
            i += 1
        if len(inner_dupes_idx) == 0:
            return
        if abs(inner_dupes_idx[0] - inner_dupes_idx[1]) != 1:
            handle_non_contiguous_dupes()

        inner_dupes = []
        for dkt in self.place_dicts:
            if dkt["input"] == same:
                inner_dupes.extend(dkt["id"])
                break
        pairs = [(i, j) for i in inner_dupes for j in inner_dupes if i != j]
        right_pair = set(pairs).intersection(places_places)

        for tup in right_pair: # there's only one
            right_pair = tup
        selected_ids = tuple(zip(inner_dupes_idx, right_pair))
        b = 0
        for dkt in self.place_dicts:
            for tup in selected_ids:
                if tup[0] == b:
                    dkt["id"] = [tup[1]]
            b += 1

    def handle_outer_duplicates(self):

        def pinpoint_child(parent, children):
            conn = sqlite3.connect(current_file)
            cur = conn.cursor()
            cur.execute(select_place_id1, (parent,))
            possible_children = [i[0] for i in cur.fetchall()]
            
            cur.close()
            conn.close()

            st = set(possible_children).intersection(children)
            child = list(st)

            return child

        def seek_child():
            u = 0
            known = None
            child = None
            for dkt in self.place_dicts:
                if len(dkt["id"]) == 1:
                    known = dkt["id"][0]
                else:
                    u += 1
                    continue
                # u - 1 will refer to the last item if u == 0, don't allow that:
                if u != 0:
                    if known is not None and len(self.place_dicts[u - 1]["id"]) != 1:
                        children = tuple(self.place_dicts[u - 1]["id"])
                        child = pinpoint_child(known, children)
                        self.place_dicts[u - 1]["id"] = child
                        return
                    else:
                        u += 1
                        continue
        
        for dkt in self.place_dicts:
            seek_child()

    def open_new_places_dialog(self):
        '''
            Open dialog by default. If one case is found which needs the dialog 
            open, break the loop or return to stop looking through the cases. 
        '''                   

        def test_for_all_new():
            z = 0
            for dkt in self.place_dicts:
                if dkt.get("temp_id") is not None and len(dkt["id"]) == 0:
                    if z != len(self.place_dicts) - 1:
                        z += 1
                        continue
                    else:
                        self.open_dialog = False
                        self.all_new = True
                        return

        def test_for_all_known():
            known = 0
            z = 0
            for dkt in self.place_dicts:
                if len(dkt["id"]) != 1 or dkt.get("temp_id") is not None:
                    pass
                elif len(dkt["id"]) == 1 and dkt.get("temp_id") is None:
                    known += 1
                z += 1
            if z == known: 
                self.open_dialog = False
                self.all_known = True

        def test_for_new_plus_known():
            new = 0
            known = 0
            z = 0
            for dkt in self.place_dicts:
                if len(dkt["id"]) > 1:
                    return
                elif len(dkt["id"]) == 1 and dkt.get("temp_id") is None:
                    known += 1
                elif len(dkt["id"]) == 1 and dkt.get("temp_id") is not None:
                    known += 1
                    new += 1
                elif len(dkt["id"]) == 0 and dkt.get("temp_id") is None:
                    print("line", looky(seeline()).lineno, "case not handled")
                elif len(dkt["id"]) == 0 and dkt.get("temp_id") is not None:
                    new += 1
                else:
                    print("line", looky(seeline()).lineno, "case not handled")                    
                z += 1
            if new == 0 and known == 0:
                self.open_dialog = False

        test_for_all_new()
        test_for_all_known()
        test_for_new_plus_known()
 
        if self.open_dialog is True:
            self.new_place_dialog = NewPlaceDialog(
                self.root,
                self.place_dicts,
                "Clarify place selections where there is not exactly one ID "
                "number.\n\nPress the EDIT button to add or edit hints for "
                "duplicate place names (or any place name) so you won't have "
                "to look up place IDs.\n\nIf you're entering a new place name "
                "that has no duplicates, an ID number has been assigned which "
                "you can just OK.\n\nIf, for even one of the levels in your "
                "nested place, there is no correct option, press CANCEL and use "
                "the Places Tab inputs to custom-create the desired nested "
                "place before trying to use it.", 
                "New and Duplicate Places Dialog",
                ("OK", "CANCEL"),
                self.treebard,
                do_on_ok=self.collect_place_ids)
        else:
            print("line", looky(seeline()).lineno, "self.place_dicts:", self.place_dicts)
            print("line", looky(seeline()).lineno, "self.all_new:", self.all_new)
            print("line", looky(seeline()).lineno, "self.all_known:", self.all_known)
            if self.all_new is True:
                self.update_new_places()
            elif self.all_known is True:
                self.update_known_places()
            else:
                print("line", looky(seeline()).lineno, "normally should run from collect_place_ids(), not here?")
                self.update_mixed_places()

    def update_new_places(self):
        conn = sqlite3.connect(current_file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        places = []
        places_places = []
        nested_places = []
        # insert new places
        for dkt in self.place_dicts: 
            new_id = dkt["temp_id"]
            (place_id, place_name) = (new_id, dkt["input"])           
            cur.execute(insert_place_new_with_id, (place_id, place_name))
            conn.commit()
            places.append(new_id)
        # insert new places into existing places_places
        for i in range(len(places) - 1):
            places_places.append((places[i], places[i + 1]))
            a = i + 1
        places_places.append((places[a], None))
        for tup in places_places:
            cur.execute(insert_nested_pair, tup)
            conn.commit()
        # insert new nested_places
        k = 0
        r = len(places)
        for j in range(r):
            nested_places.append(places[k:r])
            k += 1
            if k == r:
                break
        nested_place_tuples = []
        for lst in nested_places:
            qty = 9 - len(lst)
            nulls = [None] * qty
            tup = tuple(lst + nulls)
            nested_place_tuples.append(tup) 
        t = 0
        for tup in nested_place_tuples:
            cur.execute(insert_nested_places, tup)
            conn.commit()
            if t == 0:
                cur.execute(
                    "SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'nested_places'")
                nested_places_id = cur.fetchone()[0]
            t += 1
            
        # update nested_place_id in right row of self.findings
        cur.execute(update_finding_nested_places, (nested_places_id, self.finding))
        conn.commit()

        # update global place lists so they will be current immediately
        EntryAuto.recent_items.insert(0, self.place_input)
        self.update_global_place_lists()        

        cur.close()
        conn.close()

    def update_global_place_lists(self):
        place_strings, nested_place_ids, places_places = make_global_place_lists()
        EntryAuto.create_lists(place_strings) 

    def update_known_places(self):
        # update nested_place_id in right row of self.findings
        input_ids = []
        for dkt in self.place_dicts:
            input_ids.append(dkt["id"][0])
        qty = len(input_ids)
        nulls = [None] * (9 - qty)
        nesting = tuple(input_ids + nulls)
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_nested_places_id, nesting)
        nested_places_id = cur.fetchone()[0]
        cur.execute(update_finding_nested_places, (nested_places_id, self.finding))
        conn.commit()
        EntryAuto.recent_items.insert(0, self.place_input)
        cur.close()
        conn.close()

    def update_mixed_places(self, ids=None):

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        print("line", looky(seeline()).lineno, "self.place_dicts:", self.place_dicts)
        # make ordered list of knowns in input
        print("line", looky(seeline()).lineno, "self.place_input:", self.place_input)
        print("line", looky(seeline()).lineno, "ids:", ids)
        # create a list of all relevant ordered pairs from knowns list
        knowns = ids["known"]
        knowns.append(None)
        pairs = []
        frog = len(knowns) - 1
        f = frog
        for i in range(frog):
            a = knowns.pop(0)
            for j in range(f):
                pairs.append((a, knowns[j]))
            f -= 1
        print("line", looky(seeline()).lineno, "pairs:", pairs)

        # find pairs in places_places that contain any of these pairs
        related_pairs = []
        for pair in pairs:
            if pair in places_places:
                related_pairs.append(pair)
        print("line", looky(seeline()).lineno, "related_pairs:", related_pairs) 

# line 516 self.place_dicts: [{'id': [833], 'input': 'Raton'}, {'id': [834], 'input': 'Colfax County'}, {'id': [835], 'input': 'New Mexico', 'temp_id': 845}, {'id': [8], 'input': 'USA'}]
# line 518 self.place_input: Raton, Colfax County, New Mexico, USA
# line 519 ids: {'all': [833, 834, 835, 8], 'known': [833, 834, 835, 8]}
# line 531 pairs: [(833, 834), (833, 835), (833, 8), (833, None), (834, 835), (834, 8), (834, None), (835, 8), (835, None), (8, None)]
# line 541 related_pairs: [(833, 834), (834, 835), (835, None), (8, None)]
# line 552 pair: (833, 834)
# line 552 pair: (834, 835)
# line 552 pair: (835, None)
# line 552 pair: (8, None)
# line 556 correctable_pairs: [467, 468, 469, 8]

# sqlite> select * from nested_places where nest0 in (833, 834, 835) or nest1 in (833, 834, 835) or nest2 in (833, 834, 835) or nest3 in (833, 834, 835) or nest5 in (833, 834, 835) or nest6 in (833, 834, 835);
# nested_places_id|nest0|nest1|nest2|nest3|nest4|nest5|nest6|nest7|nest8
# 578|833|834|835||||||
# 579|834|835|||||||
# 580|835||||||||

        # detect affected pairs
        correctable_pairs = []
        for pair in related_pairs:
            print("line", looky(seeline()).lineno, "pair:", pair)
            cur.execute(select_places_places_id, pair)
            fix = cur.fetchone()[0]
            correctable_pairs.append(fix)
        print("line", looky(seeline()).lineno, "correctable_pairs:", correctable_pairs)
        # detect primary affected nesting
        print("line", looky(seeline()).lineno, "self.nested_place:", self.nested_place)
        # detect affected sub-nestings
        # NESTED_PLACES HAS TO BE REFACTORED SO THAT ONLY THE PRIMARY NESTING
        #   IS STORED IN THE DATABASE AND THE OTHERS ARE COMPUTED BY PYTHON AS NEEDED.
        #   BETTER YET: STORE ONLY THE PAIRS AND ELIMINATE NESTED PLACES TABLE. SINCE
        #   THE NESTINGS ARE COMPUTED FROM THE PAIRS, STORING THEM AT ALL IS WRONG 
        #   BECAUSE THEY'RE ONLY NEEDED IN THE GUI AND NOT USED TO PERFORM ANY LOGIC,
        #   SO THEY SHOULD BE COMPUTED ON THE FLY FOR THE AUTOFILLS TO USE.
        # update pairs, create new as needed
        # replace primary affected nesting with input
        # replace sub-nestings with new ones
        # change linked values eg fk in finding table
        # update global place lists so they will be current immediately
        self.update_global_place_lists()

        cur.close()
        conn.close()








    def collect_place_ids(self):
        # ids = [[], []]
        ids = {"all": [], "known": []}
        r = 0
        for dkt in self.place_dicts:
            new_id = None
            if len(dkt["id"]) == 0:
                if dkt.get("temp_id") is None:
                    print("line", looky(seeline()).lineno, "something is wrong")
                    return
                else:
                    print("line", looky(seeline()).lineno, "its a new nest")
                    new_id = dkt["temp_id"]
                    ids["all"].append(new_id)
            elif len(dkt["id"]) > 1:
                print("line", looky(seeline()).lineno, "there are still duplicates")
            elif len(dkt["id"]) == 1:
                if dkt.get("temp_id") is None:
                    print("line", looky(seeline()).lineno, "nest is already in database")
                    new_id = dkt["id"][0]
                    ids["all"].append(new_id)
                    ids["known"].append(new_id)
                elif dkt.get("temp_id") is not None:
                    new_id = self.new_place_dialog.radvars[r].get()
                    if new_id != dkt["temp_id"]:
                        ids["all"].append(new_id)
                        ids["known"].append(new_id)
                    else:
                        ids["all"].append(new_id)
                        
                    print("line", looky(seeline()).lineno, "theres both a known and a temp id for a nest")
                else:
                    print("line", looky(seeline()).lineno, "case not handled")
            else:
                print("line", looky(seeline()).lineno, "case not handled")
            # ids.append(new_id)
            r += 1
        self.update_mixed_places(ids)

class NewPlaceDialog():
    def __init__(
            self,
            parent, 
            place_dicts,
            message, 
            title,
            button_labels,
            treebard,
            do_on_ok=None,
            selection=None
):

        self.parent = parent
        self.place_dicts = place_dicts
        self.message = message
        self.title = title
        self.button_labels = button_labels
        self.treebard = treebard
        self.do_on_ok = do_on_ok

        self.got_row = 0
        self.got_nest = None
        self.edit_hint_id = 0
        self.hint_to_edit = None
        self.edit_rows = {}
        self.make_widgets()

    def make_widgets(self):

        def show_message():

            window.columnconfigure(1, weight=1)
            window.rowconfigure(1, weight=1)
            lab = MessageHilited(
                window, text=self.message, justify='left', aspect=500)
            lab.grid(column=1, row=1, sticky='news', ipady=18)

        def ok():
            if self.do_on_ok:
                self.do_on_ok()
            cancel()

        def cancel():
            self.new_places_dialog.destroy()
        size = (
            self.parent.winfo_screenwidth(), self.parent.winfo_screenheight())
        self.new_places_dialog = Toplevel(self.parent)
        self.new_places_dialog.geometry("+84+84")
        self.new_places_dialog.maxsize(
            width=int(size[0] * 0.85), height=int(size[1] * 0.95))
        self.new_places_dialog.columnconfigure(1, weight=1)
        self.new_places_dialog.rowconfigure(4, weight=1)
        canvas = Border(self.new_places_dialog, size=3) # don't hard-code size            
        canvas.title_1.config(text=self.title)
        canvas.title_2.config(text='')

        window = Frame(canvas)
        canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        # DO NOT DELETE THESE LINES, UNCOMMENT IN REAL APP
        # self.treebard.scroll_mouse.append_to_list([canvas, window])
        # self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        window.vsb = Scrollbar(
            self.new_places_dialog, 
            hideable=True, 
            command=canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            self.new_places_dialog, 
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
        buttonbox.grid(column=1, row=3, sticky='se', pady=6)

        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.frm = Frame(window)
        self.frm.grid(column=1, row=2, sticky='news', pady=12)

        show_message()
        self.show_choices()

        resize_scrolled_content(self.new_places_dialog, canvas, window)

        self.new_places_dialog.focus_set()

    def ok_hint(self):
        edit_row = self.edit_rows[self.got_nest]
        new_hint = edit_row.ent.get()
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(update_place_hint, ((new_hint, self.edit_hint_id)))
        conn.commit()
        cur.close()
        conn.close()
        
        self.hint_to_edit.config(text="hint: {}".format(new_hint))
        edit_row.remove_edit_row()

    def make_edit_row(self, parent, row=None):
        edit_row = EditRow(parent, self.ok_hint)
        self.edit_rows[parent] = edit_row

    def grid_edit_row(self, hint):
        edit_row = self.edit_rows[self.got_nest]
        edit_row.grid(column=0, row=self.got_row, sticky='ew', columnspan=2)
        edit_row.lift()
        for child in self.got_nest.winfo_children():
            if child.grid_info()['column'] == 0:
                if child.grid_info()['row'] == self.got_row - 1:
                    self.edit_hint_id = int(child.cget('text').split(': ')[0])
            elif child.grid_info()['column'] == 1:
                if child.grid_info()['row'] == self.got_row:
                    if child.winfo_class() == 'Label':
                        self.hint_to_edit = child
        edit_row.ent.delete(0, 'end')
        edit_row.ent.insert(0, hint)
        edit_row.ent.focus_set()

    def get_clicked_row(self, evt):
        self.got_row = evt.widget.grid_info()['row'] 
        self.got_nest = evt.widget.master

    def on_hover(self, evt):
        evt.widget.config(text='Edit') 

    def on_unhover(self, evt):
        evt.widget.config(text='')

    def show_choices(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.radvars = []
        i = 0
        for dd in self.place_dicts:
            self.var = tk.IntVar()
            # self.var = tk.IntVar(None, 0)
            self.radvars.append(self.var)
            i += 1

        d = 0
        t = 0
        bullet = len(self.place_dicts)
        # configure place_id for query
        for dkt in self.place_dicts:
            add_new_place_option = False
            place_hints = []
            if len(dkt["id"]) == 1:
                if dkt.get("temp_id") is None:
                    place_id = (dkt["id"][0],)
                else:
                    place_id = (dkt["id"][0])
                    add_new_place_option = True
            elif len(dkt["id"]) > 1:
                if dkt.get("temp_id") is not None:
                    add_new_place_option = True
                place_id = dkt["id"]
            elif dkt.get("temp_id") is None:
                place_id = ("none",)
            elif dkt.get("temp_id"):
                # place id will be int type which marks it as a new place
                place_id = dkt["temp_id"]
            else:
                print("line", looky(seeline()).lineno, "case not handled")
            if type(place_id) is int:
                place_hints.append('')
            else:
                for num in place_id:
                    if num == "none":
                        place_hints.append('')
                    else:
                        cur.execute(select_place_hint, (num,))
                        place_hint = cur.fetchone()
                        if place_hint[0] is None:
                            place_hint = ''
                        else: 
                            place_hint = place_hint[0]
                        place_hints.append(place_hint)
            # reconfigure place_id for display
            if type(place_id) is int:
                if dkt["temp_id"] is not None and len(dkt["id"]) > 0:
                    place_hints.append('')
            elif add_new_place_option is True:
                place_hints.append('')
            elif len(place_id) == 1:
                place_id = place_id[0]
            else:
                print("line", looky(seeline()).lineno, "case not handled")
            place_input = dkt["input"]
            place_string = '{}: {}, place ID #{}'.format(
                bullet, place_input, place_id)

            lab = Label(self.frm, text=place_string)
            lab.grid(column=0, row=d, sticky='w')

            self.hint_frm = Frame(self.frm, name="nest{}".format(bullet-1))
            self.hint_frm.grid(column=0, row=d+1, sticky='w', padx=(0,3), columnspan=2)
            self.hint_frm.columnconfigure(0, minsize=48)

            self.make_edit_row(self.hint_frm)

            h = 0
            row = 0
            for hint in place_hints:
                if dkt.get("temp_id") is not None and len(dkt["id"]) > 0:
                    # user will choose between a new ID or one of the existing IDs
                    new_id = dkt["temp_id"]
                    last_idx = len(dkt["id"])
                    if h == last_idx:
                        current_id = new_id
                        if h == 0:
                            self.radvars[t].set(current_id)
                        rad_string = "{}: {} (new place and new place ID)".format(
                            current_id, dkt["input"])
                    else:
                        current_id = dkt["id"][h]
                        if h == 0:
                            self.radvars[t].set(current_id)
                        cur.execute(select_first_nested_place, (current_id,))
                        nesting = cur.fetchone()
                        nesting = [i for i in nesting if i]
                        nesting = ", ".join(nesting)
                        rad_string = "{}: {}".format(current_id, nesting)
                elif dkt.get("temp_id") is not None and len(dkt["id"]) == 0:
                    # user will OK or CANCEL new ID
                    current_id = dkt["temp_id"]
                    if h == 0:
                        self.radvars[t].set(current_id)
                    rad_string = "{}: {} (new place and new place ID)".format(
                        current_id, dkt["input"])
                else:
                    current_id = dkt["id"][h]
                    if h == 0:
                        self.radvars[t].set(current_id)
                    cur.execute(select_first_nested_place, (current_id,))
                    nesting = cur.fetchone()
                    nesting = [i for i in nesting if i]
                    nesting = ", ".join(nesting)
                    rad_string = "{}: {}".format(current_id, nesting)
                rad = RadiobuttonBig(
                    self.hint_frm, 
                    variable=self.radvars[t],
                    value=current_id,
                    text=rad_string, 
                    anchor="w")




# line 825 t, h, current_id: 0 0 833
# line 825 t, h, current_id: 1 0 834
# line 807 t, h, current_id: 2 0 835
# line 800 t, h, current_id: 2 1 845
# line 825 t, h, current_id: 3 0 8



                lab = Label(
                    self.hint_frm, 
                    text="hint: {}".format(hint),
                    anchor='w', bg='red')
                editx = ButtonQuiet(
                    self.hint_frm, 
                    width=2, 
                    command=lambda hint=hint: self.grid_edit_row(hint))

                self.hint_frm.columnconfigure(1, weight=1)
                rad.grid(column=0, row=row, sticky='we', columnspan=2)
                editx.grid(column=0, row=row+1, pady=(0,3), sticky='e')
                lab.grid(column=1, row=row+1, sticky='w', padx=6)

                editx.bind('<Enter>', self.on_hover)
                editx.bind('<Leave>', self.on_unhover)
                editx.bind('<Button-1>', self.get_clicked_row)
                editx.bind('<space>', self.get_clicked_row)
                editx.bind('<FocusIn>', self.on_hover)
                editx.bind('<FocusOut>', self.on_unhover)
                h += 1
                row += 2

            sep = Separator(self.frm, 3)
            sep.grid(column=0, row=d+2, sticky='ew', columnspan=3, pady=(3,0))
            d += 3
            t += 1
            bullet -= 1

        cur.close()
        conn.close()

class EditRow(Frame):
    def __init__(self, master, command, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.ent = Entry(self, width=36)
        spacer = Label(self, width=3)

        ok_butt = Button(
            self,
            text='OK',
            command=command)

        cancel_butt = Button(
            self,
            text='CANCEL',
            command=self.remove_edit_row)
        
        spacer.grid(column=0, row=0)
        self.ent.grid(column=1, row=0, padx=3, pady=3)
        ok_butt.grid(column=2, row=0, padx=6, pady=6)
        cancel_butt.grid(column=3, row=0, padx=6, pady=6)

    def remove_edit_row(self):
        self.grid_forget()

if __name__ == "__main__":

    trials = {
        'a' : "114 Main Street, Paris, Precinct 5, Lamar County, Texas, USA",
        'b' : "114 Main Street, Paris, Bear Lake County, Idaho, USA",
        'c' : "Paris, Tennessee, USA",
        'd' : "Paris, Texas, USA",
        'e' : "Paris",
        'f' : "Maine, Maine, USA",
        'g' : "Glenwood Springs, Garfield County, Colorado, USA",
        'h' : "Paris, France",
        'i' : "Glenwood Springs, USA",
        'j' : "Paris, USA",
        'k' : "Paris",
        'l' : "Seadrift, Calhoun County, Texas, USA",
        'm' : "Hawaii, USA",
        'n' : "Jakarta, Java, Indonesia",
        'o' : "Old Town, Sacramento, California, New Spain, USA",
        'p' : "Blossom, Lamar County, Texas, USA",
        'q' : "Blossom, Precinct 1, Lamar County, Texas, USA",
        'r' : "Maine, Aroostook County, Maine, USA",
        's' : "Maine, Iowa, USA",
        't' : "Sassari, Sassari, Sardegna, Italy",
        'u' : "Elks Lodge, Paris, Precinct 5, Lamar County, Texas, USA",
        'v' : "Elks Lodge, Paris, Bear Lake County, Idaho, USA",
        'w' : "Elks Lodge, Sacramento, Sacramento County, California, USA",
        'x' : "Elks Lodge, Blossom, Lamar County, Texas, USA",
        'y' : "Jerusalem, Israel",
        'z' : "Masada, Israel",
        'aaa' : "Israel",
        'bbb' : "USA",
        'ccc' : "Dupes, Dupes, Dupes",
        'ddd' : "table 5, Elks Lodge, Paris, Precinct 5, Lamar County, Texas, USA",
        'eee' : "table 5, Elks Lodge, Paris, Bear Lake County, Idaho, USA",
        'fff' : "table 5, Elks Lodge, Paris, Precinct 5, Lamar County, Texas, USA",
        'ggg' : "Elks Lodge, Gee Whiz Mall, Maine, Arizona, USA",
        'hhh' : "Paris, Precinct 5, Lamar County, Texas, USA",
        'iii' : "Precinct 5, Lamar County, Texas, USA",
        'jjj' : "Dupe, Dupe, Dupe",
        'kkk' : "Transylvania",
        'lll' : "Blossom, Elma, Erie County, New York, USA",
        'mmm' : "Calhoun County, Texas, USA",
    }

    finding = 1
    nested_place = 271

    def get_final(evt):
        widg = evt.widget
        # final = widg.get()
        # if final != self.initial:
            # self.final = final
            # for row in self.findings:
                # c = 0
                # for col in row[0:-1]:
                    # if col[0] == widg:
                        # self.finding = row[9]
                        # col_num = c
                    # c += 1
        
            # self.update_db(widg, col_num)
        update_db(widg) # will need (widg, col_num) in real one

    def update_db(widg):
        final = widg.get()
        for child in frame.winfo_children():
            child.destroy()
        final = ValidatePlace(root, treebard, final, finding, nested_place)
        j = 0
        for dkt in final.place_dicts:
            lab = Label(
                frame,
                text='{} id#{}'.format(
                    final.place_dicts[j]["input"], final.place_dicts[j]["id"]))
            lab.grid()
            j += 1

            # self.final = ValidatePlace(
                # self.root, 
                # self.treebard,
                # self.final,)

    root = tk.Tk()
    treebard = root # mockup; this isn't what really happens

    entry = EntryAuto(root, width=50, autofill=True)
    EntryAuto.create_lists(place_strings)
    entry.grid()
    entry.focus_set()
    entry.bind("<FocusOut>", get_final, add="+")

    traverse = Entry(root)
    traverse.grid()
    frame = Frame(root)
    frame.grid()
    
    root.mainloop()



# DO LIST

# input to db
# check places_places and nested_places to make sure a bunch of junk hasn't been entered, esp. look for pairs in p_p where id2 is null.
# in the real one, if CANCEL is pressed, the table cell that triggered this procedure should be cleared out so user can start fresh and not get the procedure auto-triggered again from the old data he input.



'''
Cities named Maine in America.	
Maine - North Carolina
Maine - New York
Maine - Minnesota
Maine - Maine
Maine - Iowa
Maine - Arizona

Cities named Maine in Chad.	
Maïné - Guera

Cities named Maine in Pakistan.	
Maine - North-West Frontier

Cities named Maine in Niger.	
Maïné - Maradi

Cities named Maine in France.	
Maine - Poitou-Charentes


'''

# DEV DOCS




'''
New Doc Strings 20210523
Treebard compares user-input nested place strings to place strings stored in
the database to try and figure out which place the user intended. Since the
main goal was to not open the New & Duplicate Places Dialog unnecessarily,
it was late in the game when a major simplification to the code occurred
to me: open the dialog by default and then find simple reasons not to.
Instead of trying to do what had kept me confused till then, which was
to keep the dialog closed by default and test for complicated conditions
which should cause the dialog to open.

PLACE STRING TERMINOLOGY
nest: "Paris" or "France" in "Paris, France"
new nest: a nest that's not in the database yet
single: a nest that occurs in the database in one record only
nesting, nested places, nested place string: "Paris, France"
child: "Paris" in "Paris, France"
parent: "France" in "Paris, France"
orphan: "Paris" in "Paris, Linn County, Iowa" if Linn County is not in the database
inner duplicate: "Maine" in "Maine, Maine, USA"
outer duplicate, duplicate: "Paris" in "Paris, France" and "Paris, Texas"
known: this string exists as a single in the database e.g.
    "Timbuktu", so if user enters "Timbuktu", depending on 
    the context in the nesting, Treebard might guess with   
    reasonable certainty that this is Timbuktu, Mali since
    there's only nest called "Timbuktu" in the database: Timbuktu, Mali. But if
    the user also enters another place by the same name (e.g.
    the crater on Mars named Timbuktu), then "Timbuktu" will
    no longer be treated as a known, and Treebard will have
    to try to figure out which Timbuktu is intended each
    time the user enters the name. Depending on what other 
    nests are in the nesting, a dialog might open for the
    user to explicitly state which Timbuktu to use.

EXPECTATIONS
The goal is to open a duplicate place name dialog for user clarification
but to do so as seldom as possible within reason. Here's an example of
"within reason". User inputs "Paris, Precinct 5, Lamar County, Texas, USA".
Paris is an outer duplicate, Precinct 5 is a new place, and the last three
nests are known. It seems pretty obvious to the user which Paris is meant:
the one he's already entered in Lamar County, Texas. And we could write 
the code to guess that's what he meant, but the more complicated the code gets, the
greater will be our self-loathing at some point in the future when an even
more complicated bit of code has to be added for an even more convoluted
imagined necessity. We don't like to open R U Sure or anything like it,
but entering new places is done all the time because Treebard should not come pre-loaded with everything that Google Maps has ever heard
of. Portability is important and we have only a wee snort of contempt for the kind of
genealogy that is supposed to be all done by machine logic without the user
having to do any research. The internet is filling up with bad data invented
by smarty-pants software. And we don't like bloated, unmaintainable code.
Part of the reason for Treebard to exist is that the code should be usable
by amateur programmers. So for these reasons and others, it is my decision
at this point (after literally months spent writing and re-writing the code
for the new and duplicate places dialog) that the right thing to do is to draw the
line for opening a dialog slightly early rather than slightly late. Treebard will
ask for user clarification slightly more often than some users would like,
in cases where new places are inserted into existing nested place strings which also 
contain duplicate place names.
But I failed to mention the most important reason for not trying to guess
which place out of a set of duplicates is intended: due to circumstances that we can't always predict, Treebard might guess wrong. Whereas if we give the user a chance to input the new place correctly,
in the long run the user will be happier about it. We shouldn't try to predict every eventuality in a misguided attempt to make
the user's decisions for him. But it would also be wrong to allow free
entry of just any old misbegotten place name such as mis-spellings and true duplicates. Somewhere between the two
extremes of "do what you want" and "do what I say", a sane middle-ground is being groped-in-the-dark for as fastidiously as possible.
For example, when entering a new place nested among existing places, the user will be shown a dialog in which the new place has been assigned an ID and barring other complex input, all he has to do is press OK. This dialog seems superfluous depending on your point of view, but from Treebard's stance, the user should have a chance to review and cancel most new place input. The only time Treebard doesn't open a dialog for new place input is when within the nesting that's being input, all of the nests are new input, for example: "Antarctica" or "Pen Hill, Dichotomy County, Fellows Island, North Sea" or "back seat, Geronimo's Cadillac, Indian Territory, The New World" etc.

Design Features:
-- The big place lists are gotten from the database once on load, not each time they're needed. 
-- The big place lists are updated and reloaded each time the database place tables change, so always current.

There are three tables in the database re: places:
1) place table stores place_id and places i.e. the nest (the place string)
2) places_places table stores child-parent pairs. A nest can have more than one parent, and this is a unique feature of Treebard which makes its places data storage and manipulation historically accurate and complex.
3) nested_places stores nestings. Goal is to not look at this table at all for data manipulation in this module, as its reason to exist is to provide autofill strings for place inputs. Since nested_places is a junction table built from data in the first two tables, it would be best if the goals of this module could be met by referencing only the first two tables.

Autofill places are key to our design. Allowing only good data up front is important so user will not have to split and merge places when he finds later that bad data has been allowed into the database. But the validation process should be invisible to the user almost always, unless he's doing something really unusual in which case he can expect to see dialogs. In very unusual cases, the user will want to cancel the dialog and instead input the place nesting manually in the places tab.

Unfortunately, Treebard can't accept place names that contain a comma. Few of these exist, and if a user wants to enter one, he'll have to change the comma to a hyphen or something. We more or less have to use commas to delimit nests within nestings, I don't think there's any way around it, and place names containing commas won't work.

The nested_places table is important. I don't think it denormalizes anything, because 1) each cell contains one value, 2) no data input is repeated except as foreign keys, and 3) in spite of the fact that the columns in the nested_places table are meant to provide ordered values--i.e. the order of the columns is important--it's the most normalized way I could think of to store an autofill string comprised of various concatenated data, so I made the table and it works. You could, if you wanted, use the data in any order you wanted, because there's only one piece of data per table cell. So I don't think it's actually denormalized.

We should pre-populate the database only with currently existing countries, continents and major oceans, and let the user provide the places he actually needs. The places he enters can be used in all his trees. Possibly there should be a global places list for places he wants to use in every tree and a per-tree places list, but I don't want to deal with this. It shouldn't be a problem because the autofill place list will be manipulated to first show recently used places. So if the user has input Zuneida Resort and uses it a lot, it will show up before Albuquerque. If a place called "Aababaca" had to be input to one tree and used once, it can remain harmlessly in a global places table because Treebard will show Albuquerque first if Albuquerque has been used more recently.

The only way to leave out the largest place (e.g. "USA" if user doesn't want to see it on every nested place string) is for the user to not enter it. Treebard disapproves so we shouldn't encourage it. Short versions of country names will be input for USA and USSR only, with their full versions input as a.k.a. All other place names should be spelled out. If some kinda silly official country names like "The Redundant Republic of Featherduster" are input as "Featherduster", it's OK because even if the capitol of Featherduster is called "Featherduster" too, Treebard can tell them apart. So for the most part, the user has a lot of flexibility.

'''

# nested places a.k.a. nested place strings a.k.a. nestings:
# Incomplete nestings get correct but incomplete results. When testing a nesting, if wrong results are obtained, before ripping into the deceptively simple code (which took over 3 months to write), check your nesting. If a nest is missing from a hard-coded test nesting, or if the data in places_places or nested_places is incomplete or incorrect, the good code will give incomplete results. Example: "Paris, Lamar County, Texas, USA" looks right but it's missing "Precinct 5" between Paris and Lamar County (assuming that nest has been previously input), so it won't work up to par. Instead of correctly guessing all the nests, it will open a dialog because it won't be able to guess which "Paris" is intended. In practice, if the user has to have a nesting that doesn't include Precinct 5, he can add it just as easily as the complete nesting. The autofill might not work as conveniently--he might have to type more characters to get to a unique string that will autofill--but it will work. Generally the right way is to use complete nestings if possible, that's how Treebard is designed to work because Autofill and Potentially Multiple Parents for places are integral parts of the Treebard philosophy on how places should work so that place input will be historically accurate yet still convenient and intuitive for the user to do.

# The code works by filtering away duplicates to try to make them singles thus 
#   knowns. The goal is to prevent the dialog from opening unnecessarily.
# I.e. if len(id)>1 the code tries to get it down to 1.
# Or if len(id)==0 a temp_id is made since it's a new nest.
# Also a temp_id is made for an orphan in case it's a new nest.
# When place_dicts is in its final form, its id key(s) are evaluated
#   to see whether or not to open the New & Duplicate Places dialog for user 
#   clarification.

# CASES TO TEST FOR (self.open_dialog = True by default):
#   each test has to be done for each nest:
#   len(id)     temp_id exists        nest state    self.open_dialog
#       0            yes                new            false
#       0             no              undefined (code is lacking)            
#       1            yes             known-or-new       true
#       1             no                known          false
#       >1           yes              dupl-or-new       true
#       >1            no                 dupl          false

# WHAT TO DO ABOUT IT depends on the profile of the whole nesting
#   profile                    self.open_dialog (final)
#   all new                    false
#   all known                  false
#   any dupl                   true
#   some new, some known       false
#   any known-or-new           true
#   any dupl-or-new            true

# Since self.open_dialog is True by default, the only tests that
#   have to be done are those that would change it to False.
#   So we only test for "all new", "all known" and "some new, some known".
#   Instead of setting the boolean default to False and checking for
#   complicated conditions, we set it to True and check for simple stuff.




#   


