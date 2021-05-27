# sets_for_nested_places

import tkinter as tk
from widgets import (
    Toplevel, Frame, Button, Label, RadiobuttonBig, MessageHilited, 
    Entry, ButtonQuiet, Separator)
from query_strings import (
    select_all_nested_places, select_place, select_place_id, 
    select_place_nickname, select_all_places, select_all_places_places, )
from files import get_current_file
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
import dev_tools as dt
from dev_tools import looky, seeline
import sqlite3





'''
New Doc Strings 20210523
Treebard compares user-input place strings to place strings stored in
the database to try and figure out which place the user intended.

PLACE STRING TERMINOLOGY
nest: "Paris" or "France" in "Paris, France"
nesting, nested places, nested place string: "Paris, France"
single: a nest that occurs in the database in one record only
inner duplicate: "Maine" in "Maine, Maine, USA"
outer duplicate: "Paris" in "Paris, France" and "Paris, Texas"
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
of. Portability is important and we have only a bored snort of contempt for the kind of
genealogy that is supposed to be all done by machine logic without the user
having to do any research. The internet is filling up with bad data invented
by smarty-pants software. And we don't like bloated, unmaintainable code.
Part of the reason for Treebard to exist is that the code should be usable
by amateur programmers. So for these reasons and others, it is my decision
at this point (after literally months spent writing and re-writing the code
for the duplicate places dialog) that the right thing to do is to draw the
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
*********
call this "Regular Places" emulating "Regular Expressions". A new string will be generated (or list or some readable code) in place of user input, and when user input is completely replaced by readable code, the user input can be correctly stored. "Readable Code" will probably be an ordered list of place ID numbers. Maybe intermediately using a list of dicts with the dict storing trait codes or just a code string, whichever is easier to understand. Performance isn't important because only one place input is done at a time and existing places will have been detected first so this modal dialog won't run much code while open.

Goal: to pinpoint the distinguishing traits of one nested place string input so these traits can be coded, searched, and responded to by algorithms that have to tell one nesting from the other without knowing beforehand the unique ID numbers of the nests (nests) or the ID of the nesting itself, if any. User is typing a few characters, autofill is doing or not doing the rest, and user is not expected to know or look up the right ID numbers when entering a nested place, even if there is a duplicate nest such as the Paris in "Paris, France" and "Paris, Tennessee".

Terminology:
-- nest: single place e.g. "Paris" in "Paris, Ile-de-France, France"
-- nesting, nested place, nested place string: e.g. "Paris, Ile-de-France, France"
-- parent, child, ancestor: Paris is child of Ile-de-France and descendant of France (means the same as Paris is nested in Ile-de-France)
-- leaf, view, node: Paris is the smallest place, it is the leaf; France is the largest place, it is the view; the other nodes (nests) are between them.

Assumptions: 
-- If there's exactly one stored nesting that exactly matches user input, it's the right one, IDs won't be checked. That means no nest in the nesting can have a duplicate  (e.g. if one of the nests is Paris, this won't apply here.)

Design Features:
-- The big place lists are gotten from the database once on load, not each time they're needed. 
-- The big place lists are updated and reloaded each time the database place tables change, so always current.

Traits of nested place strings aka nested places aka nestings aka input:
-- length (number of nests in a nesting input)
-- same_out : single, multiple, or zero=new (length of id list; nests whose spelling is unique/not unique/missing from db)
-- same_in (two or more nests within a single nesting are spelled the same)
-- id (from db, a list of IDs matching nest; goal is to filter list down to one and it has to be the one the user intended, so if itfilters down to none, it has to mean the user intends to enter a new nest)

Things that are always true (so maybe too many traits are defined):
-- same_in <= same_out, so if same_out == 1, don't check same_in, it's irrelevant
-- if id == [], same_out = 0 and same_in = 1
-- if insert_juxta is True, insert_multi is also True

Cases to detect re: nests within the input nesting; one or more case can be true of a nesting so the simplest cases are eliminated first; 0 = no matches so the nest is absent from the database; 1 = exactly one match so in some simple cases this means the ID is known. Starting from the simplest case:
a) no nests are known or duplicated, e.g. (0, 0, 0) or (0) or (0, 0) etc.
b) right nesting is obvious, exactly the same as input, and already in the database, e.g. (1, 1, 1, 1, 1) or (1) or (1, 1) etc.
c) one or more largest ancestor(s) known, one or more descendant(s) unknown; no gaps or duplicates; e.g. (0, 0, 0, 1), (0, 1, 1), (0, 0, 1) etc. but not (0, 1, 0) or (0, 0, 1, 0, 1) or (0, 2, 1) etc.
d) right nesting is obvious, parts are the same as input, but other nests are being inserted to it

c) right nesting is obvious, parts are the same as input, but nest(s) have been omitted from it
d) one or more nests are known
e) one or more nests are new
f) one or more nests are in the database by duplicate spellings so right ID(s) are unknown
g) two or more nests within the nesting are spelled the same
h) all nests except the largest ancestor are unknown
i) all nests except the two largest ancestors are unknown
j) one or more nests are known but the largest ancestor is unknown
i) only one nest is input and it's known
j) only one nest is input and it's duplicate
k) only one nest is input and it's unknown
l) a parent has two children by the same name

The strategy is to know what traits the nesting has and what cases it represents before doing any work on it. If its match in the database is obvious, don't do any work on it. The goal is to know which nesting (in the database) is matched or partly matched so nestings in the database can  be edited, added or deleted.

There are three tables in the database re: places:
1) place table stores place_id and nest (the place string)
2) places_places table stores child-parent pairs. A nest can have more than one parent.
3) nested_places stores nestings. Goal is to not look at this table at all as its reason to exist is to provide autofill strings for place inputs. Since it's build from data in the first two tables, it would be best if the goals of this module could be met by referencing only the first two tables.

Starting from the simplest case (case a), validation only runs till the right nesting is found. If the right nesting can't be found, a Duplicate Place Name dialog or other dialog will open to request user confirmation or additional input. The goal is to almost never open such a dialog.

Autofill places are key to our design. Allowing only good data up front is important so user will not have to split and merge places when he finds later that bad data has been allowed in. But the validation process should be invisible to the user almost always, unless he's doing something really unusual in which case he can expect to see dialogs.

The nested_places table is important. I don't think it denormalizes anything, because 1) each cell contains one value, 2) no data input is repeated except as foreign keys, and 3) in spite of the fact that the columns in the nested_places table are meant to provide ordered values--i.e. the order of the columns is important--it's the most normalized way I could think of to store an autofill string comprised of various concatenated data, so I made the table and it works.

We should pre-populate the database only with currently existing countries, continents and major oceans, and let the user provide the places he actually needs. The places he enters can be used in all his trees.

The only way to leave out the largest place (e.g. "USA" if user doesn't want to see it on every nested place string) is for the user to not enter it. Treebard disapproves so we shouldn't encourage it. Short versions of country names will be input for USA and USSR only, with their full versions input as a.k.a. All other place names should be spelled out.

'''

current_file = get_current_file()[0]

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

def get_all_places_places():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_places_places)
    places_places = cur.fetchall()
    cur.close()
    conn.close()
    return places_places

place_strings = make_autofill_strings()
nested_place_ids = get_autofill_places()
places_places = get_all_places_places()

conn = sqlite3.connect(current_file)
cur = conn.cursor()
cur.execute(select_all_places)
all_place_names = [i[0] for i in cur.fetchall()]
cur.close()
conn.close()

unique_place_names = set(all_place_names)

print(len(unique_place_names), len(all_place_names))

# sample inputs in lieu of widgets:
a = "114 Main Street, Paris, Lamar County, Texas, USA"
b = "114 Main Street, Paris, Bear Lake County, Idaho, USA"
c = "Paris, Tennessee, USA"
d = "Paris, Texas, USA"
e = "Paris, Precinct 5, Lamar County, Texas, USA"
f = "Maine, Maine, USA"
g = "Glenwood Springs, Garfield County, Colorado, USA"
h = "Paris, France"
i = "Glenwood Springs, USA" # allow this 
j = "Paris, USA" # allow this but the duplicate's ID is unguessable so there will be a dialog
k = "Paris" # ditto
l = "Seadrift, Calhoun County, Texas, USA"
m = "Hawaii, USA"
n = "Jakarta, Java, Indonesia"
o = "Old Town, Sacramento, California, New Spain, USA"
p = "Blossom, Lamar County, Texas, USA"
q = "Blossom, Precinct 1, Lamar County, Texas, USA"
r = "Maine, Aroostook County, Maine, USA"
s = "Maine, Iowa, USA"
t = "Sassari, Sassari, Sardegna, Italy"
u = "McDonalds, Paris, Precinct 5, Lamar County, Texas, USA"
v = "McDonalds, Paris, Bear Lake County, Idaho, USA"
w = "McDonalds, Sacramento, Sacramento County, California, USA" # this one exists
x = "McDonalds, Blossom, Lamar County, Texas, USA" # this McDonalds doesn't exist
y = "Jerusalem, Israel"
z = "Masada, Israel"
aaa = "Israel"
bbb = "USA"
ccc = "Dupes, Dupes, Dupes"
ddd = "table 5, McDonalds, Paris, Lamar County, Texas, USA"
eee = "table 5, McDonalds, Paris, Bear Lake County, Idaho, USA"
fff = "table 5, McDonalds, Paris, Precinct 5, Lamar County, Texas, USA"
ggg = "McDonalds, Gee Whiz Mall, Maine, Arizona, USA"

place_input = a # fff # u # e

class ValidatePlace():

    def __init__(self, view, treebard, place_input):

        self.view = view
        self.treebard = treebard
        self.place_input = place_input
        self.place_dicts = []
        self.temp_places = []
        self.temp_places_places = []

        self.new_places = False
        self.inner_duplicates = False
        self.outer_duplicates = False

        self.make_place_dicts()
        self.see_whats_needed()
        self.open_duplicate_places_dialog()

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

        def catch_new_dupes():
            '''
                In case a new place is intended when a same-named place exists
                once in the database; so the existing place won't be used
                if a new place was intended. Compares existing singles to
                entered nests.
            '''

            b = 0
            for dkt in self.place_dicts:
                if b == len(self.place_dicts) - 1:
                    return                 
                if len(dkt["id"]) == 1:
                    child = dkt["id"][0]         
                    parents = self.place_dicts[b + 1]["id"] # [78]
                    cur.execute(
                        '''
                            SELECT place_id2 
                            FROM places_places
                            WHERE place_id1 = ?
                        ''',
                        (child,))
                    parent_list = [i[0] for i in cur.fetchall()]
                    ok = False
                    for i in parent_list:
                        for j in parents:
                            if i == j:
                                ok = True
                    if ok is False:
                        dkt["id"] = []
                b += 1

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
        catch_new_dupes()
        cur.close()
        conn.close()

    def see_whats_needed(self):
        for dkt in self.place_dicts:
            if len(dkt["id"]) == 0:
                self.new_places = True
            elif len(dkt["id"]) > 1 and dkt["inner_dupe"] is False:
                self.outer_duplicates = True
            elif len(dkt["id"]) > 1 and dkt["inner_dupe"] is True:
                self.inner_duplicates = True

        if self.new_places is True:
            self.make_new_places()
        if self.inner_duplicates is True:
            self.handle_inner_duplicates()
        if self.outer_duplicates is True:
            self.handle_outer_duplicates()

    def make_new_places(self):
        '''
            The place IDs should be decided for new places before anything
            else is done. This way, there will be consistency and it's all
            being done at once. Otherwise, when a procedure is interrupted
            because a place ID is needed, if the ID were made on the fly
            at that time, it would require an extra hit to the database and
            the code would be more confusing due to a scattered procedure.
        '''

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute("SELECT MAX(place_id) FROM place")
        temp_id = cur.fetchone()[0] + 1

        for dkt in self.place_dicts:
            if len(dkt["id"]) == 0:              
                dkt["temp_id"] = temp_id
                temp_id += 1
        cur.close()
        conn.close()

    def handle_inner_duplicates(self):
        '''
            This will handle one pair of inner duplicates. If there are three
            nests in the same nesting with exactly the same name, the code can
            be extended. If there is more than one pair of inner duplicates
            in the same nesting, the code can be extended. For now, tell the
            user to find unique historically correct names for the places. 
            Open a dialog if too many duplicates, and make no changes to the 
            database.
        '''

        def handle_non_contiguous_dupes():
            # leave this here for now in case it's needed
            pass

        inner_dupes_idx = []
        i = 0
        for nest in self.place_list:
            if self.place_list.count(nest) > 1:
                same = nest
                inner_dupes_idx.append(i)
                if len(inner_dupes_idx) > 2:
                    duplicate_error = Toplevel(self.view)
                    duplicate_error.title("Too many duplicates, find unique names.")
                    return
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
            print("line", looky(seeline()).lineno, "dkt", dkt)
            for tup in selected_ids:
                if tup[0] == b:
                    dkt["id"] = [tup[1]]
            b += 1

    def handle_outer_duplicates(self):

        def pinpoint_child(parent, children):
            conn = sqlite3.connect(current_file)
            cur = conn.cursor()

            cur.execute(
                '''
                    SELECT place_id1
                    FROM places_places
                    WHERE place_id2 = ?
                ''',
                (parent,))
            possible_children = [i[0] for i in cur.fetchall()]
            
            cur.close()
            conn.close()

            st = set(possible_children).intersection(children)
            child = list(st)

            return child

        def seek_child():
            u = 0
            parent = None
            child = None
            for dkt in self.place_dicts:
                if len(dkt["id"]) == 1:
                    parent = dkt["id"][0]
                else:
                    u += 1
                    continue

                if parent is not None and len(self.place_dicts[u - 1]["id"]) != 1:
                    children = tuple(self.place_dicts[u - 1]["id"])
                    child = pinpoint_child(parent, children)
                    self.place_dicts[u - 1]["id"] = child
                    return
                else:
                    u += 1
                    continue

        for dkt in self.place_dicts:
            seek_child()

    def open_duplicate_places_dialog(self):
        open_dialog = False
        dialog_values = []
        for dkt in self.place_dicts:
            if len(dkt["id"]) != 1:
                if dkt.get("temp_id") is None:
                    print("line", looky(seeline()).lineno, "dkt['id']", dkt["id"])
                    dialog_values.append([dkt["input"], dkt["id"]])
                    open_dialog = True

                else:
                    known = 0
                    nests = 0
                    new = None
                    for dkt in self.place_dicts:
                        if len(dkt["id"]) == 1:
                            known += 1
                        elif len(dkt["id"]) == 0:
                            new = nests
                        nests += 1
                    if known > nests - 2:
                        # self.make_new_place(new, self.place_dicts)
                        open_dialog = True
                
        if open_dialog is True:
            new_place_dialog = NewPlaceDialog(
                self.view,
                self.place_input,
                'Duplicate place names have been stored. Use which one?', 
                'Duplicate Place Names Dialog',
                ('OK', 'Cancel'),
                self.treebard,
                do_on_ok=self.input_places_to_db,
                selection=dkt['id'])


            for val in dialog_values:
                lab = Label(new_place_dialog, text=val)
                lab.grid()

    def input_places_to_db(self):
        print("line", looky(seeline()).lineno, "self.place_dicts", self.place_dicts)


    def make_new_place(self, position, nesting):
        '''
            Add one new nest to the database if there's only one new place to make.
            Always add places one at a time, passing the updated dict each time.
            So if more than one new place is to be made, run this function over
            with the dict updated first to reflect what's actually in the database
            at that moment.
        '''

        print("line", looky(seeline()).lineno, "position, nesting", position, nesting)
        # line 506 position, nesting 0 [{'id': [], 'input': '114 Main Street', 'temp_id': 808}, {'id': [30], 'input': 'Paris', 'inner_dupe': False}, {'id': [78], 'input': 'Lamar County'}, {'id': [29], 'input': 'Texas'}, {'id': [8], 'input': 'USA'}]    

class NewPlaceDialog():
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

    def make_widgets(self):

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
        # DO NOT DELETE THESE LINES, UNCOMMENT IN REAL APP
        # self.treebard.scroll_mouse.append_to_list([canvas, window])
        # self.treebard.scroll_mouse.configure_mousewheel_scrolling()

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

        


if __name__ == "__main__":

    from widgets import Toplevel, Label

    view = tk.Tk()
    treebard = view # mockup; this isn't what really happens

    final = ValidatePlace(view, treebard, place_input)
    j = 0
    for dkt in final.place_dicts:
        lab = Label(
            view,
            text='{} id#{}'.format(
                final.place_dicts[j]["input"], final.place_dicts[j]["id"]))
        lab.grid()
        j += 1
    
    view.mainloop()
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



# DO LIST

# dlg shd open for case a-- new place followed by an outer dupe followed by knowns

# test all cases before starting on the dialog; dialog should open for new places unless the new places are not duplicates and there are no complicating factors in which case the new place should just be made silently
# move query strings to module

# when entering a single place there will always be a dialog unless the place is new to the db    

# New thoughts 20210523
# Don't use the temp lists, the info is already stored in dict, make key for child and parent
# Deal with edge cases immediately as soon as there's an ID for each nest

# Starting over 20210518, it's still too complicated to finish
# Take care of one nest at a time. Define each nest completely. 
# Make new places FIRST like this:
#   Get max ID from places table, increment for each new place
#   populate a temp_new_places list, a temp_places_places list, and a temp_nested_places list if needed
#   If a CANCEL button is clicked on a dialog the temp lists have done no harm
#   otherwise the three place tables can be updated on SUBMIT. 
#   Make dict key temp_id so empty id key can still trigger db update.
# Don't deal with duplicates till everything is known about every nest in the nesting.
# Start another minified model and keep it minified.
# Edge cases should make it easier, not harder, to find matches. How many places are there named "Maine, Maine"? Do them first.
# When a single ID or temp_id exists for each nest, stop. Test after each id assignment.

