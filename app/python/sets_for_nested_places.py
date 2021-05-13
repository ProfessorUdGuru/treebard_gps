# sets_for_nested_places

from query_strings import select_place_id, select_all_places
from files import get_current_file
import dev_tools as dt
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
-- If there's only one stored nesting that exactly matches user input, it's the right one, IDs won't be checked.

Design Features:
-- The place lists are gotten from the database once on load, not each time they're needed. 
-- The place lists are updated and reloaded each time the database place tables change, so always current.

Traits of nested place strings aka nested places aka nestings aka input:
-- length (number of nests in a nesting input)
-- same_out : multiple, single, or zero=new (length of id list; nests whose spelling is unique/not unique/missing from db)
-- nest_index (leaf=0, 1, 2, n, root=length of nesting - 1)
-- same_in (two or more nests within a single nesting are spelled the same)
-- id (from db, a list of IDs matching nest; goal is to filter list down to one and it has to be the one the user intended, so if filtered down to none, it has to mean the user intends to enter a new nest)

Things that are always true (so maybe too many traits are defined):
-- same_in <= same_out, so if same_out == 1, don't check same_in, it's irrelevant
-- if id == [], same_out = 0 and same_in = 1

Cases to detect re: nests within the input nesting (one or more case can be true of a nesting) starting with the simplest case:
a) no nests are known or duplicated
b) right nesting is obvious, exactly the same as input, and already in the database
c) one or more largest ancestor(s) known, one or more descendants unknown; no gaps or duplicates

b) right nesting is obvious, parts are the same as input, but other nests are being inserted to it
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

conn = sqlite3.connect(current_file)
cur = conn.cursor()
cur.execute(select_all_places)
all_place_names = [i[0] for i in cur.fetchall()]
cur.close()
conn.close()

# this could be gotten with a SELECT UNIQUE if the first list won't be needed
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
i = "Glenwood Springs, USA" # DON'T ALLOW THIS?
j = "Paris, USA" # DON'T ALLOW THIS?
k = "Paris" # DON'T ALLOW THIS?
l = "Seadrift, Calhoun County, Texas, USA"
m = "Hawaii, USA"
n = "Jakarta, Java, Indonesia"


place_input = m

class ValidatePlace():

    def __init__(self):
        self.place_dicts = []
        self.next_depth = 0

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
            "nest_index" : position of a nest within the nesting, 
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

        self.place_dicts = [
            (
                {
                    "nest_index" : i, 
                    "id" : get_matching_ids(x),
                    "input" : x,
                    "same_out" : all_place_names.count(x),
                    "same_in" : place_list.count(x)}) 
            for i, x in enumerate(place_list)]

        cur.close()
        conn.close()

        self.nest_depth = len(self.place_dicts)

        if get_obvious_nestings() is True:
            print('170 get_obvious_nestings() is True')
            right_nesting = tuple([dkt["id"][0] for dkt in self.place_dicts])
            self.pass_known_place(right_nesting)
        else:
            print('174 get_obvious_nestings() is False')
            new_places = []
            for dkt in self.place_dicts:
                if dkt["same_out"] != 0:
                    break
                else:
                    new_places.append(dkt["input"])

            if len(new_places) == self.nest_depth:
                return self.add_all_new_places(new_places)
            self.sift_place_input()
        
    def sift_place_input(self):
        print("188 self.place_dicts", self.place_dicts)
        g = 0
        last_nest = self.nest_depth - 1
        for dkt in self.place_dicts:
            if (g == 0 and dkt["same_out"] == 0 and 
                    self.place_dicts[last_nest]["same_out"] == 1):
                print('194 dkt is', dkt) # SET A BOOLEAN found_zero = True
                g += 1
            else:
                print('200 keep sifting')

    def add_all_new_places(self, new_places):
        print('193 new_places is', new_places)




    def pass_known_place(self, right_nesting):
        print("right_nesting is", right_nesting)
            

final = ValidatePlace()
final.make_place_dicts(place_input)





















# 20210511

lists = []
for stg in (a, b, c):
    lst = stg.split(", ")
    # print(lst)
    lists.append(lst)

l = len(set(lists[0]).intersection(lists[1]))
# print(l)
l = len(set(lists[0]).intersection(lists[1], lists[2]))
# print(l)

f = ["Paris", "Ile-de-France", "France"]

new_places = set(f).difference(unique_place_names)
# print(new_places)

a = ["Maine", "Maine", "USA"]
# if len(a) != len(set(a)):
    # print("Places with same name in single nesting.")

b = ["Sassari", "Sassari", "Sardegna", "Italy"]
c = ["Sassari", "Sardegna", "Italy"]

# print(c in b)
# print(c == b[1:])
# If applicable, above can be used to rewrite the insert query to nested_places with maybe one line of code?