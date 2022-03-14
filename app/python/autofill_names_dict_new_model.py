# dict_remove_key_reinsert_change_order

import tkinter as tk
from autofill import EntryAutoPersonHilited
from persons import make_all_names_dict_for_person_select
import dev_tools as dt
from dev_tools import looky, seeline





# since Python 3.7 dict has preserved the order in which keys are inserted, this is a big deal

dkt = {1: "red", 2: "white", 3: "blue", 4: "green", 5: "brown"}

x = dkt.pop(3)
# print(x)
# print(dkt)

# insert removed key at end
dkt[3] = x
# print(dkt)

# sort by keys
dkt = dict(sorted(dkt.items()))
# print(dkt)

# ultimate goal is to sort alphabetically be value, then pop and insert to front
# could use OrderedDict but it's slower than Dict so instead make list, insert, make dict, make list etc

lst = [(1, "red"), (2, "white"), (3, "green"), (4, "blue"), (5, "brown")]

lst = sorted(lst, key=lambda i: i[1])
# print(lst)

first = lst.pop(2)
# print(first)
# print(lst)

lst.insert(0, first)
# print(lst)

dkt = dict(lst)
# print(dkt)

lst = list(dkt.items())
# print(lst)

# in reality there would be a layer of nesting since more information is needed
# want to end up with this...
# people = {
    # 12: {
        # "birth name": "James Norton", "alt name": "James Woodland", 
        # "alt name type": "adopted name", "sort order": "Woodland, James"},
    # 1: {
        # "birth name": "Jeremiah Grimaldo", "alt name": "G-Man", 
        # "alt name type": "nickname", "sort order": "Grimaldo, Jeremiah"}, 
    # 6: {
        # "birth name": "Ronnie Webb", "alt name": "Miss Polly", 
        # "alt name type": "stage name", "sort order": "Webb, Ronnie"}, 
    # 5599: {
        # "birth name": "", "alt name": "Selina Savoy", 
        # "alt name type": "pseudonym", "sort order": "Savoy, Selina"}, 
    # 5: {
        # "birth name": "Donald Webb", "alt name": "Donny Boxer", 
        # "alt name type": "nickname", "sort order": "Webb, Donald"}, 
    # 9898: {
        # "birth name": "John Smith", "alt name": "Smitty", 
        # "alt name type": "nickname", "sort order": "Smith, John"}, 
    # 9999: {
        # "birth name": "John Smith", "alt name": "Mack", 
        # "alt name type": "nickname", "sort order": "Smith, John"}} 
# # ...starting from this:
# keys1 = (12, 1, 6, 5599, 5, 9898, 9999)
# keys2 = ("birth name", "alt name", "alt name type", "sort order")
# values = [
    # ("James Norton", "James Woodland", "adopted name", "Woodland, James"),
    # ("Jeremiah Grimaldo", "G-Man", "nickname", "Grimaldo, Jeremiah"),
    # ("Ronnie Webb", "Miss Polly", "stage name", "Webb, Ronnie"),
    # ("", "Selina Savoy", "pseudonym", "Savoy, Selina"),
    # ("Donald Webb", "Donny Boxer", "nickname", "Webb, Donald"),
    # ("John Smith", "Smitty", "nickname", "Smith, John"),
    # ("John Smith", "Mack", "nickname", "Smith, John"),
# ]

# # inner_dict = list(zip(keys2, values))
# # print(inner_dict)
# inner_dict = []
# for tup in values:
    # indict = dict(zip(keys2, tup))
    # inner_dict.append(indict)
# # print(inner_dict)

# people = dict(zip(keys1, inner_dict))
# print("line", looky(seeline()).lineno, "people:", people)
# print(outer_dict)
# {12: {'birth name': 'James Norton', 'alt name': 'James Woodland', 'alt name type': 'adopted name', 'sort order': 'Woodland, James'}, 1: {'birth name': 'Jeremiah Grimaldo', 'alt name': 'G-Man', 'alt name type': 'nickname', 'sort order': 'Grimaldo, Jeremiah'}, 6: {'birth name': 'Ronnie Webb', 'alt name': 'Miss Polly', 'alt name type': 'stage name', 'sort order': 'Webb, Ronnie'}, 5599: {'birth name': '', 'alt name': 'Selina Savoy', 'alt name type': 'pseudonym', 'sort order': 'Savoy, Selina'}, 5: {'birth name': 'Donald Webb', 'alt name': 'Donny Boxer', 'alt name type': 'nickname', 'sort order': 'Webb, Donald'}}

# people = outer_dict

def update_person_autofill_values():
    people = make_all_names_dict_for_person_select()
    all_names = EntryAutoPersonHilited.create_lists(people)
    for ent in EntryAutoPersonHilited.all_person_autofills:
        ent.values = all_names
    return all_names
    # return people

    

if __name__ == '__main__':

    formats = {"highlight_bg": "bisque"}

    root = tk.Tk()
    root.geometry('+800+300')

    # people = make_all_names_list_for_person_select()        
    # all_names = EntryAutoPersonHilited.create_lists(people) # this will put recently used values to front of list
    people = update_person_autofill_values()
    person_entry = EntryAutoPersonHilited(
        # root, formats, width=30, autofill=True)
        root, formats, width=30, autofill=True, values=people)

    move = tk.Entry(root)

    id_entry = EntryAutoPersonHilited(root, formats, width=6)

    for widg in (person_entry, id_entry):
        widg.config(insertbackground="black", fg="black")

    person_entry.focus_set() 

    EntryAutoPersonHilited.all_person_autofills.extend([person_entry, id_entry])  


    person_entry.grid()
    move.grid()
    id_entry.grid()

    root.mainloop()





