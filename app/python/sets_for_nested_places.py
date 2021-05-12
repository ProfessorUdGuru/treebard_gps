# sets_for_nested_places

from query_strings import select_place_id, select_all_places
from files import get_current_file
import dev_tools as dt
import sqlite3



'''
call this "Regular Places" emulating "Regular Expressions". A new string will be generated (or list or some readable code) in place of user input, and when user input is completely replaced by readable code, the user input can be correctly stored. "Readable Code" will probably be an ordered list of place ID numbers. Maybe intermediately using a list of dicts with the dict storing trait codes or just a code string, whichever is easier to understand. Performance isn't important because only one place input is done at a time and existing places will be detected first so won't run much code.

Goal: to pinpoint the distinguishing traits of nested place strings so these traits can be coded, searched, and responded to by algorithms that have to tell one nesting from the other without knowing beforehand the unique ID numbers of the nests (nests) or the ID of the nesting itself. User is typing a few characters, autofill is doing or not doing the rest, and user is not expected to know or look up the right ID numbers when entering a nested place, even if there is a duplicate nest such as the Paris in "Paris, France" and "Paris, Tennessee".

Assumptions: 
-- If there's only one stored nesting that matches user input, it's the right one.

Design Features:
-- The place lists are gotten from the database once, not each time they're needed. 
-- The place lists are updated each time the database place tables change, so always current.

Traits of nested place strings aka nested places aka nestings aka input:
-- length (number of nests in a nesting input)
-- same_out : multiple, single, or new (length of id list; nests whose spelling is unique/not unique/missing from db)
-- nest_index (leaf=0, 1, 2, n, root=length-1)
-- same_in (two or more nests within a single nesting are spelled the same)
-- id (from db, a list of IDs matching nest; goal is to filter list down to the right one)

'''

current_file = get_current_file()[0]

# # from database:
# all_place_names = ["114 Main Street", "Paris", "Lamar County", "Texas", "USA", "Bear Lake County", "Idaho", "Tennessee", "Garfield County", "Colorado", "Aspen", "Pitkin County", "Greece", "Arizona", "Europe", "Antarctica", "Ohio", "Washington County", "Paris", "Ohio", "Paris", "Washington County", "Maine", "Maine"]
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
x = "114 Main Street, Paris, Lamar County, Texas, USA"
y = "114 Main Street, Paris, Bear Lake County, Idaho, USA"
z = "Paris, Tennessee, USA"
q = "Paris, Texas, USA"
r = "Paris, Precinct 5, Lamar County, Texas, USA"
s = "Maine, Maine, USA"

place_input = y

def sift_place_input(place_input):
    '''
    User must separate nests with a comma and any number of spaces including 
    no spaces. Nestings will be stored correctly with a comma and one space
    separating nests, and autofill relies on places being typed this way,
    but the validation process doesn't care about spaces, just the comma.

    This method systematically stores the traits of each nest before anything 
    else is done, instead of haphazardly swatting at a moving target with a bunch of
    conditional tests. For example, it might seem lame to store the index when the
    index could be detected at any time, but if it's stored up front then the
    detection procedure won't distract from the procedure for doing something
    with the nestings based on the detected traits. This lets us change the
    position of the nest within the nesting later (e.g. if a new nest is inserted),
    without changing the list of dicts, by changing the value of dkt['index'].
    '''

    def get_matching_ids(nest):
        cur.execute(select_place_id, (nest,))
        ids = cur.fetchall()
        ids = [i[0] for i in ids]
        return ids

    conn = sqlite3.connect(current_file)
    cur = conn.cursor()


    place_dicts = []
    place_list = place_input.split(",")
    place_list = [place_list[i].strip() for i in range(len(place_list))]
    print("place_list is", place_list)

    place_dicts = [
        (
            {
                "nest_index" : i, 
                "id" : get_matching_ids(x),
                "input" : x,
                "same_out" : all_place_names.count(x),
                "same_in" : place_list.count(x)}) 
        for i, x in enumerate(place_list)]

    print("place_dicts is", place_dicts)





    cur.close()
    conn.close()

sift_place_input(place_input)




















# 20210511

lists = []
for stg in (x, y, z):
    lst = stg.split(", ")
    print(lst)
    lists.append(lst)

l = len(set(lists[0]).intersection(lists[1]))
print(l)
l = len(set(lists[0]).intersection(lists[1], lists[2]))
print(l)

f = ["Paris", "Ile-de-France", "France"]

new_places = set(f).difference(unique_place_names)
print(new_places)

a = ["Maine", "Maine", "USA"]
if len(a) != len(set(a)):
    print("Places with same name in single nesting.")

b = ["Sassari", "Sassari", "Sardegna", "Italy"]
c = ["Sassari", "Sardegna", "Italy"]

print(c in b)
print(c == b[1:])
# If applicable, above can be used to rewrite the insert query to nested_places with maybe one line of code?