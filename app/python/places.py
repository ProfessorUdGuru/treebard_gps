# sets_for_nested_places

from query_strings import (
    select_place_id, select_all_places, select_place_id1, select_place_id2,
    select_all_places_places, select_all_nested_places, select_place, )
from files import get_current_file
import dev_tools as dt
from dev_tools import looky, seeline
import sqlite3


'''
call this "Regular Places" emulating "Regular Expressions". A new string will be generated (or list or some readable code) in place of user input, and when user input is completely replaced by readable code, the user input can be correctly stored. "Readable Code" will probably be an ordered list of place ID numbers. Maybe intermediately using a list of dicts with the dict storing trait codes or just a code string, whichever is easier to understand. Performance isn't important because only one place input is done at a time and existing places will have been detected first so this modal dialog won't run much code while open.

Goal: to pinpoint the distinguishing traits of one nested place string input so these traits can be coded, searched, and responded to by algorithms that have to tell one nesting from the other without knowing beforehand the unique ID numbers of the nests (nests) or the ID of the nesting itself, if any. User is typing a few characters, autofill is doing or not doing the rest, and user is not expected to know or look up the right ID numbers when entering a nested place, even if there is a duplicate nest such as the Paris in "Paris, France" and "Paris, Tennessee".

Terminology:
-- nest: single place e.g. "Paris" in "Paris, Ile-de-France, France"
-- nesting, nested place, nested place string: e.g. "Paris, Ile-de-France, France"
-- parent, child, ancestor: Paris is child of Ile-de-France and descendant of France (means the same as Paris is nested in Ile-de-France)
-- leaf, root, node: Paris is the smallest place, it is the leaf; France is the largest place, it is the root; the other nodes (nests) are between them.

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
r = "Paris, Maine, Maine, USA"
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


place_input = v # u # v

class ValidatePlace():

    def __init__(self):
        self.place_dicts = []
        self.all_same_out = []
        self.next_depth = 0
        self.insert_first = False
        self.insert_last = False
        self.insert_multi = False
        self.insert_juxta = False
        
    def sift_place_input(self):
        '''
            Runs when place_dicts is complete if right nesting is not known.
        '''
        self.detect_0_1_series()
        self.detect_insertions()


    def make_place_dicts(self, place_input):
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

        def get_obvious_nestings():
            for dkt in self.place_dicts:
                if dkt['same_out'] != 1:
                    return False
            return True

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        place_list = place_input.split(",")
        place_list = [place_list[i].strip() for i in range(len(place_list))]
        self.length = len(place_list)

        self.place_dicts = [
            (
                { 
                    "id" : get_matching_ids(x),
                    "input" : x,
                    "same_out" : all_place_names.count(x),
                    "same_in" : place_list.count(x)}) 
            for w, x in enumerate(place_list)]

        self.all_same_out = [dkt["same_out"] for dkt in self.place_dicts]#line 238 is [3, 22, 1, 1, 1]
        self.duplicates = 0
        for num in self.all_same_out:
            if num > 1:
                self.duplicates += 1
        for num in self.all_same_out:
            if num > 1:
                self.filter_duplicates()
                break
        self.finish_making_dict()

        cur.close()
        conn.close()

        if get_obvious_nestings() is True:
            right_nesting = tuple([dkt["id"][0] for dkt in self.place_dicts])
            self.pass_known_place(right_nesting)
        else:
            new_places = []
            for dkt in self.place_dicts:
                if dkt["same_out"] != 0:
                    break
                else:
                    new_places.append(dkt["input"])

            if len(new_places) == self.length:
                return self.add_all_new_places(new_places)
            self.sift_place_input()

    def filter_duplicates(self):
        '''
            Case 1: find ID when there is also a duplicate nest inside the 
                nesting i.e. dkt["same_in"] > 1 besides a duplicate nest 
                outside the nesting i.e. dkt["same_out"] > 1.
            Case 2: find ID when the duplicate place is also duplicated 
                inside the nesting i.e. dkt["same_out"] > dkt["same_in"]
            Case 3: find ID when there are new places to input.
            Case 4: find IDs of more than one duplicate place.
            Case 5: find ID when there are no new places to input except a 
                single duplicate place name whose ID is not known because it's
                a duplicate string.
        '''
        j = 0
        for dkt in self.place_dicts:
            if dkt["same_out"] > 1 and dkt["same_in"] > 1:
                if dkt["same_out"] > dkt["same_in"]:
                    self.handle_duplex_duplicates()
                    break
                elif dkt["same_out"] == dkt["same_in"]:
                    self.handle_duplicates_within_nest()
                    break
            elif len(dkt["id"]) == 0:
                self.handle_duplicates_and_new_place()
                break
            elif self.duplicates > 1:
                self.handle_multiple_duplicates()
                break
            elif self.duplicates == 1:
                self.handle_one_duplicate(dkt, j)                
                break
            else:
                print("something else not handled", dkt)
            j += 1


    def handle_one_duplicate(self, dkt, j):
        '''
            Duplicate countries? Israel for example. Two different epochs, 
            two different countries. The two should technically be named
            differently but not all users are that technically inclined.
        '''

        def get_child_parent(combos, side):
            '''
                Normally duplicate place name input is clarified by finding the 
                ID of the ambiguous place's parent, but in the rare case when 
                the last/largest nest is a duplicate, the ambiguous place has 
                no parent so its child's ID has to be found. The variable 
                `side` refers to the left index (0) of the child/parent pair or 
                the right index (1). Set intersection is used to filter out 
                unmatching pairs from the places_places table. Sets are 
                unordered but it doesn't matter because we already know what 
                order the nests are in.
            '''
            right_pair = None
            for st in combos:
                for pair in places_places:
                    isect = st.intersection(pair)
                    if len(isect) > 1: 
                        right_pair = pair
            if right_pair:
                dkt["id"] = [right_pair[side]]
            else:
                dkt["id"] = []
                if j == 0: self.insert_first = True
                self.insert_one_nest()

        def assign_vars_to_pair(last=False, idx=0):
            if last is False:
                id1 = dkt["id"]
                id2 = self.place_dicts[j + 1]["id"]                
            else:
                id1 = self.place_dicts[j - 1]["id"]
                id2 = dkt["id"]
            combos = [set([p, q]) for p in id1 for q in id2]
            get_child_parent(combos, idx)    

        if j < self.length - 1:
            assign_vars_to_pair()
        elif self.length > 1 and j == self.length - 1:
            assign_vars_to_pair(last=True, idx=1)
        elif self.length == 1:
            if self.all_same_out[j] == 1:
                right_nesting = (dkt["id"],)
                self.pass_known_place(right_nesting)
            else:
                self.open_duplicate_places_dialog()
                j += 1
        else:
            print("some condition not handled")
            j += 1 

    def handle_multiple_duplicates(self):
        '''
            Figure out which duplicate nest has a known parent; if neither, 
            look for a known child; the one w/ known parent or child is done 
            first. If neither have a known parent or child, open dialog.
        '''
        def seek_unique_and_multiple():
            nonlocal single
            print('362 num is', num)
            multidx = None
            prev = profile[single - 1];print("line", looky(seeline()).lineno, "is", prev)
            nekst = profile[single + 1];print("line", looky(seeline()).lineno, "is", nekst)
            if nekst > 1:
                print('374')
                multidx = single + 1
                print("line", looky(seeline()).lineno, "is", single, multidx)
                return single-1, multidx-1
            elif prev > 1:
                print('378')
                multidx = single - 1
                print("line", looky(seeline()).lineno, "is", multidx, single)
                return multidx-1, single-1


        # goal:
        # find first unique id
        # see if it has a multiple next to it
        # if not, find the next unique
        # after finding the first multiple that's next to a unique, find the next unique (etc)


        profile = list(self.all_same_out)
        profile.append(0)
        profile.insert(0, 0);print("line", looky(seeline()).lineno, "is", profile)
        single = 0
        for num in profile:
            if num != 1:
                single += 1
                continue
            else:
                pair = seek_unique_and_multiple()
                print("line", looky(seeline()).lineno, "is", pair)
                print("line", looky(seeline()).lineno, "is", self.place_dicts[pair[0]]["id"], self.place_dicts[pair[1]]["id"])
                # self.handle_one_duplicate(self.place_dicts[single], multidx)
            single += 1 
# TRY TO fix handle_one_duplicate() to PASS THE PAIR OF IDs TO handle_one_duplicate() , NOTHING ELSE
# because that's what I have here


     

    def handle_duplicates_and_new_place(self):
        print('252 self.place_dicts is', self.place_dicts)

    def handle_duplex_duplicates(self):
        '''
            One or more matches is in database besides the two or more matches
            within the nesting that was input.
        '''
        print('259 self.place_dicts is', self.place_dicts)

    def handle_duplicates_within_nest(self):
        print('262 self.place_dicts is', self.place_dicts)

    def finish_making_dict(self):
        '''
            Can't be done till duplicates are filtered down to one and the
            correct place_id for each duplicate is known, even if a duplicate
            place dialog has to open first.
        '''
        u = 0
        for dkt in self.place_dicts:
            child = None
            parent = None
            if u != 0:
                child = tuple(self.place_dicts[u-1]["id"])
            if u != self.length - 1:
                parent = tuple(self.place_dicts[u+1]["id"])
            dkt["child"] = child
            dkt["parent"] = parent
            u += 1 
        print("line", looky(seeline()).lineno, "is", self.place_dicts)

    def detect_0_1_series(self):
        for num in self.all_same_out:
            if num not in (0, 1):
                return
        if self.place_dicts[0]["same_out"] != 0:
            return
        if self.place_dicts[self.length - 1]["same_out"] != 1:
            return
        if self.length == 2:
            return self.handle_0_1_series()
        mids = [dkt["same_out"] for dkt in self.place_dicts[1:-1]]
        zeros = True
        for num in mids:
            if num == 1: zeros = False 
            if zeros is False:
                if num == 0:
                    print('too bad')
                    return
        self.handle_0_1_series()

    def detect_insertions(self):
        '''
            Nesting contains only obvious matches and new places (1s and 0s), 
            with one or more new place inserted between obvious matches, e.g. 
            lists of same_outs that fit this criteria: (1, 0, 1, 1), 
            (0, 1, 0, 1, 1, 1), (1, 0, 1, 0, 1), (0, 1, 1, 0) etc. 

            Special case `insert_first` is when nest0 is a new place 
                (dkt["same_out"] = 0). 
            Special case `insert_last` is when the last nest is a new place 
                (largest place is being added). 
            Special case `insert_multi` is when there are more than one single 
                zeros e.g. (1, 0, 1, 0, 1). 
            Special case `insert_juxta` is when two or more nests are inserted 
                next to each other e.g. (1, 0, 0, 1).
        '''
        insert_one = False
        all = self.all_same_out
        if all.count(0) > 1: self.insert_multi = True
        elif all.count(0) == 1: insert_one = True
        if all[0] == 0: self.insert_first = True
        if all[len(all)-1] == 0: self.insert_last = True
        all_strings = [str(i) for i in all]
        if "00" in "".join(all_strings): self.insert_juxta = True

        if (    self.insert_first is False and
                self.insert_last is False and
                self.insert_multi is False and
                self.insert_juxta is False): 
            if insert_one is True:
                self.handle_insertions()

    def handle_0_1_series(self):
        '''
            One or more new nests (dkt["same_out"] = 0) precede one or 
            more obvious existing places (dkt["same_out"] = 1) with no gaps 
            between existing places, e.g. (0, 0, 0, 1, 1).
        '''
        print("341 self.place_dicts is", self.place_dicts)

    def handle_insertions(self):
        '''
            "Paris, Texas, USA" is already in the database but user input is
            "Paris, Lamar County, Texas, USA". To insert "Lamar County", three
            database tables have to be updated, but before that, other input
            traits have to be detected.
        '''

        if self.insert_multi is False:
            print("352 running")
            self.insert_one_nest()
        elif (self.insert_juxta is True and 
                self.insert_first is False and self.insert_last is False):
            self.insert_adjacent_nests()
        elif self.insert_first is True:
            self.insert_first_nest_plus()
        elif self.insert_last is True:
            self.insert_last_nest_plus()
        else:
            print("insertion not needed or not handled")

    def insert_one_nest(self):
        '''
            Only one nest has no match.
        '''

        if self.insert_first is True:
            print("445 self.place_dicts is", self.place_dicts)
        elif self.insert_last is True:
            print("447 self.place_dicts is", self.place_dicts)
        else:
            print("449 self.place_dicts is", self.place_dicts)

    def insert_first_nest_plus(self):
        '''
            First nest and other nest(s) have no match.
        '''

        if self.insert_juxta is True:
            print("382 self.place_dicts is", self.place_dicts)
        else:
            print("384 self.place_dicts is", self.place_dicts)

    def insert_last_nest_plus(self):
        '''
            Last nest and other nest(s) have no match.
        '''

        if self.insert_juxta is True:
            print("392 self.place_dicts is", self.place_dicts)
        else:
            print("394 self.place_dicts is", self.place_dicts)

    def insert_adjacent_nests(self):
        '''
            Two or more adjacent nests have no match.
        '''
        print("400 self.place_dicts is", self.place_dicts)

    def add_new_place(self, nest):

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        cur.execute(insert_place_new, (nest,))
        conn.commit()

        cur.execute('SELECT seq FROM SQLITE_SEQUENCE WHERE name = "place"')
        new_place_id = cur.fetchone()[0]

        cur.close()
        conn.close()
        
        return new_place_id  

    def add_all_new_places(self, new_places):
        print('420 new_places is', new_places)

    def pass_known_place(self, right_nesting):
        print("543 right_nesting is", right_nesting)

    def open_duplicate_places_dialog(self):
        '''
            If Treebard can't guess what nesting the user intended based on user
            input, open a dialog for clarification. (Move the class here from the
            superceded places.py module and rename this module places.py.)
        '''
        print("line", looky(seeline()).lineno, "is", "opening dupe places dlg")
            

final = ValidatePlace()
final.make_place_dicts(place_input)

























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

# search each of the dict keys and delete the ones that are tracked but not being used. First get everything working right.