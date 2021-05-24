# sets_for_nested_places

import tkinter as tk
from query_strings import (
    select_place_id, select_all_places, select_place_id1, select_place_id2,
    select_all_places_places, select_all_nested_places, select_place, )
from files import get_current_file
import dev_tools as dt
from dev_tools import looky, seeline
import sqlite3





'''
New Doc Strings 20210523
TERMINOLOGY
nest: "Paris" or "France" in "Paris, France"
nesting, nested places, nested place string: "Paris, France"
inner duplicate: "Maine" in "Maine, Maine, USA"
outer duplicate: "Paris" in "Paris, France" and "Paris, Texas"
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
u = "McDonalds, Paris, Lamar County, Texas, USA"
v = "McDonalds, Paris, Bear Lake County, Idaho, USA"
w = "McDonalds, Sacramento, California, USA" # this one exists
x = "McDonalds, Blossom, Lamar County, Texas, USA" # this one doesn't exist
y = "Jerusalem, Israel"
z = "Masada, Israel"
aaa = "Israel"
bbb = "USA"
ccc = "Dupes, Dupes, Dupes"


place_input = u # u # v
class ValidatePlace():

    def __init__(self, view, place_input):

        self.view = view
        self.place_input = place_input
        self.single = None
        self.multiple = None
        self.place_dicts = []
        self.temp_places = []
        self.temp_places_places = []
        self.make_place_dicts()
        self.make_new_places()
        self.handle_inner_duplicates()
        self.handle_outer_duplicates()



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

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.place_list = self.place_input.split(",")
        self.place_list = [self.place_list[i].strip() for i in range(len(self.place_list))]
        self.length = len(self.place_list)

        self.place_dicts = [
            (
                { 
                    "id" : get_matching_ids(x),
                    "input" : x
}) 
            for x in self.place_list]

        cur.close()
        conn.close()



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
        new_id = cur.fetchone()[0] + 1

        for dkt in self.place_dicts:
            if len(dkt["id"]) == 0:
                # print("line", looky(seeline()).lineno, "is", dkt)                
                dkt["temp_id"] = new_id
                new_id += 1
            else:
                print("line", looky(seeline()).lineno, "is", dkt)
                 

        cur.close()
        conn.close()
        # print("line", looky(seeline()).lineno, "is", self.place_dicts)                

    def handle_inner_duplicates(self):
        '''
            This will handle one pair of inner duplicates. If there are three
            nests in the same nesting with exactly the same name, the code can
            be extended. If there is more than one pair of inner duplicates
            in the same nesting, the code can be extended. For now, tell the
            user to find some historically correct names for the places that
            aren't exactly the same. Open a dialog if too many duplicates, 
            and make no changes to the database.
        '''

        def handle_non_contiguous_dupes():
            print("line", looky(seeline()).lineno, "is", inner_dupes_idx)
            # this shd not be needed, 
            # just delete the return after the call, 
            # prob delete the func, maybe set a bool
            # just leave this here for now in case it's needed
            # if so then likely it needs to be run later
            # after right_pair is known

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
        if abs(inner_dupes_idx[0] - inner_dupes_idx[1]) != 1:# not needed?
            handle_non_contiguous_dupes()
            # return

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
                    dkt["id"] = tup[1]
            b += 1

    def handle_outer_duplicates(self):

        def seek_identifiable_pair():
            if self.single_found is False:
                seek_single()
            elif self.multiple_found is False:
                seek_multiple()
            else:
                redefine_duplicate()

        def seek_single():
            print("line", looky(seeline()).lineno, "self.ids_reversed[self.idx]", self.ids_reversed[self.idx])
            if len(self.ids_reversed[self.idx]) == 1:
                self.single = self.ids_reversed[self.idx]
                self.single_found = True
                self.idx += 1
                seek_identifiable_pair()
            

        def seek_multiple():
            print("line", looky(seeline()).lineno, "self.ids_reversed[self.idx:]", self.ids_reversed[self.idx])
            if len(self.ids_reversed[self.idx]) > 1:
                self.multiple = self.ids_reversed[self.idx]
                self.multiple_found = True
                seek_identifiable_pair()
            else:
                self.idx += 1
                self.single_found = False
                seek_identifiable_pair()


        def redefine_duplicate():
            print("line", looky(seeline()).lineno, "self.single, self.multiple", self.single, self.multiple)

        self.idx = 0
        self.single_found = False
        self.multiple_found = False
        self.ids_reversed = list(self.place_dicts)
        self.ids_reversed.reverse()
        self.ids_reversed = [dkt["id"] for dkt in self.ids_reversed]
        seek_identifiable_pair()

            

            
        
        
            

if __name__ == "__main__":

    from widgets import Toplevel, Label

    view = tk.Tk()

    final = ValidatePlace(view, place_input)
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

