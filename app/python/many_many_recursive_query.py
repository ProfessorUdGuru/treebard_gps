# many_many_recursive_query [import as mmrq]

import tkinter as tk
from tkinter import ttk
import sqlite3
import files
from widgets import EntryAutofill
from query_strings import (
   select_place_id2, select_count_place_id, select_place)
import dev_tools as dt

current_file = files.get_current_file()[0]

'''
    Terminology: "uppers" is a collection of a
    single item's parent items. "Branch" is a chain of single items in a line of descent. "Leaf" is the current end of a branch. "Initial_id" represents the first item input by the user. "Id_tree" is the end product which contains the IDs and their relationships that are used to create a collection of strings which could be used as values in a combobox or autofill entry. "Stage" is a recursion, a single generation of uppers.

    This class was developed specifically for use in creating strings for 
    nested places like "Arlington, Virginia, USA" but the terminology reflects its generic usefulness by not mentioning place names. For example, the class could be used to create citation strings like "Virginia State Archives, Collected Papers of Ned Frill, Volume 12, Part 2, Chapter 5, page 9, line 40". To keep this code accessible to novice programmers (i.e. so I don't have to learn advanced SQL), the recursion needed has been supplied by two recursive Python functions and no recursion in the SQL. This was not done to avoid using a recursive query on a simple nested relationship, which I know how to do. It was done to avoid creating a recursive query on a many-many table, which I don't know how to do. 

    I used to do 
    this with a simple recursive table that stores each city, township, 
    county, etc. in its own record in a single primary place column 
    with a second column listing a foreign key for the single parent 
    of the primary place in the same record. The FK referenced the 
    primary key of a place in the primary place column. This was 
    easy till I realized that a relatively static place, e.g. "Denver" 
    would have, during its life span, a number of different parents,
    such as differently named townships and counties with frequently
    changing borders. The simple recursive solution doesn't represent 
    how place names really work, and I expect this will be true of
    other nested composite values such as source citations. 

    The trick was to multiply--by the length of the new results list--each branch in the id_tree growing from the results of the previous query. This 
    gives the growing values list the right number of branches so that 
    the new results can be appended to a matching number of prior results. 
    Since values can be repeated in a many-to-many table, I had to keep from running the same query over and over for the same value. So the first step is to get the possible parents of the initial value, which is always one place, and all its possible descendants. A dictionary like {20 : [21, 22, 23]} is saved and the parents of place 20 will not have to be gotten from the database again for this instance. Then the same is done for 21, 22, 23, with a dict of parents saved for each. Repeat on down through the levels till results are null. With these dicts each defined once, there's no more hits on the database for the instance. The result is that you input a place id such as 20, which refers to "Denver" and get a whole collection of values such as "Denver, Arapahoe Co, Colorado, USA" and "Denver, Denver Co, Colorado, USA", etc.

    Place IDs 20 and 24 each have three parents. This chart not only shows how many branches
    should display in the GUI if this code works right, it shows exactly what's in each 
    branch. Trace each of the ten branches down from 20 or up from the bottom. The final 
    results should have two chains with strings representing the ID 18, two chains representing ID 19, and six chains representing ID 24.     
 
                                            20
                                                
                    21                      22                      23

                18      19          24              19         18          24

                7       7       25  7   26          7           7       25  7   26

                8       8       8   8   27          8           8       8   8   27
'''

class ManyManyRecursiveQuery():

    def __init__(self, inwidg, outwidg, initial_id=1):

        self.outwidg = outwidg

        if len(inwidg.get().strip()) != 0:
            self.initial_id = int(inwidg.get().strip())
        else:
            self.initial_id = initial_id

        get_ids = select_place_id2
        self.validate_first = select_count_place_id
        self.get_strings = select_place
        # get_ids = queries[0]
        # self.validate_first = queries[1]
        # self.get_strings = queries[2]

        self.new_id_tree = []
        self.id_tree = [[self.initial_id]]
        self.make_uppers_lists(get_ids)

    def make_uppers_lists(self, get_ids):

        def run_query(id_var):
            '''
                This function is nested so it will run many times
                with the same database connection.
            '''
            cur.execute(get_ids, (id_var,))
            uppers = cur.fetchall()
            self.uppers = [f[0] for f in uppers]

            if id_var is not None:
                d = {id_var:self.uppers}
                self.uppers_dicts.append(d)
            if self.uppers:
                for value in self.uppers:
                    key_in_dict = any(value in d for d in self.uppers_dicts)
                    
                    if key_in_dict is False:
                        run_query(value)
                    else:
                        continue
            else:
                return

        self.uppers_dicts = []

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        run_query(self.initial_id)
        self.get_one_stage_of_values([self.initial_id])
        self.make_show_strings()
        cur.close()
        conn.close()        

    def make_show_strings(self):

        def validate_input():
            cur.execute(self.validate_first, (self.initial_id,))
            count = cur.fetchone()[0]
            return count

        def get_string_with_id(identity):
            cur.execute(self.get_strings, (identity,))
            string_part = cur.fetchone()[0]
            return string_part

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        count = validate_input()

        # # autofillentry version:
        # if count == 0:
            # self.outwidg.values = []

        # combobox version:
        if count == 0:
            self.outwidg.config(values=[])
            return

        final_values_lists = []
        final_strings = []
        print('135 self.id_tree is', self.id_tree)
        for lst in self.id_tree:
            one_part = []
            for identity in lst:
                if identity is None:
                    break
                string_part = get_string_with_id(identity)
                one_part.append(string_part)
            final_values_lists.append(one_part) 
        # print('final_values_lists is', final_values_lists)
        for lst in final_values_lists:
            stg = ', '.join(lst)
            final_strings.append(stg)
            if final_strings == ['unknown']:
                final_strings = []
        print('148 final_strings is', final_strings)

        # # autofillentry version:
        # self.outwidg.values = final_strings

        # combobox version:
        self.outwidg.config(values=final_strings)
        cur.close()
        conn.close()

    def get_one_stage_of_values(self, values_list):
        def get_uppers(leaf):
            uppers = None
            for dkt in self.uppers_dicts:
                if dkt.get(leaf) is None:
                    continue
                else:
                    uppers = dkt.get(leaf)
                    break            
            return uppers  
          
        new_id_tree = []
        f = 0
        for branch in self.id_tree:        
            leaf = branch[len(branch)-1]
            uppers = get_uppers(leaf)
            if uppers is None or len(uppers) == 0:
                '''exit function when no more values are available'''
                return
            for upper in uppers:
                new_branch = list(branch)
                new_branch.append(upper)
                new_id_tree.append(new_branch) 
            f += 1
        self.id_tree = new_id_tree

        for i in range(12):
            self.get_one_stage_of_values(uppers)

if __name__ == '__main__':

    def get_current_place():
        mm = ManyManyRecursiveQuery(ent, combo)

    def clear_combo(evt):
        combo.delete(0, 'end')

    # values = []

    root = tk.Tk()

    ent = tk.Entry(root)
    '''
    Change values list like this: instance.values = [5, 15, 19, 42]. instance.config(textvariable=instance.var) is required
    '''



    # ent = EntryAutofill(root, width = 75)
    # ent.config(textvariable=ent.var)
    ent = ttk.Combobox(root)
    ent.grid()
    ent.bind('<FocusIn>', clear_combo)

    b = tk.Button(
        root, 
        text='Enter ID number above and press',
        command=get_current_place)
    b.grid()

    # combo = ttk.Combobox(root, values=values, width=75)
    combo = ttk.Combobox(root, width=75)
    combo.grid()
    ent.focus_set()

    # queries = (
        # '''
            # SELECT place_id2
            # FROM places_places
            # WHERE place_id1 = ?
        # ''',
        # '''
            # SELECT COUNT (place_id) FROM place WHERE place_id = ?
        # ''',
        # '''
            # SELECT places FROM place WHERE place_id = ?
        # ''')

root.mainloop()

# it just occurred to me that I don't know how to store a nested place once user chooses it. Another table will be needed called findings_places. The columns will reference finding_id and places_places_id. But places_places_id refers to only one part of the place. Would it be possible to add finding_id col to places_places? Doesn't seem to fit. I think what I need is a nested place table. A unique id will identify each unique combination of places chosen and delete them if unchosen(?). The row will also have up to 12 columns which each reference one place_id and the unused columns are null. The findings_places table will then have cols for finding_id and nested_place_id. But wait. Each finding has only one place. A m-m table isn't needed for this part. The place_id col on the finding table could be used but instead of ref'ing place_id it will ref nested_place_id. Then on loading the events table, the stored placename string could be displayed directly and not by storing a list of strings or a concatenated string but by querying the nested_places table and getting each value individually. The concern is to not store more than one Unit in a single table cell. Then when user edits the value in the place row, the nested place row will be created for a new combination of places if it doesn't already exist. There will have to be a Python procedure for editing the nested_places table. The good news is that loading values for autofill place values will come directly from this table, joined to place table so strings will display for stored ids. Typing a new place name will involve storing data in three tables. The place table will get a new row. The nested place table will get a new row. Then the id from the new nested place table row will be stored as FK in place_id col of finding table. But I don't know how to take strings from the user and convert them to IDs. When an existing string is chosen, it won't matter, but when a new string is created, a way of telling what is what will have to be created. First thing to do is to use my new autofillentry to get nested place values out of the nested_places table but first I have to create the nested place table. It seems I will need a procedure for deciding what to store in the table and storing it. Getting it back out is easy, just make the strings using the ids and join them with commas. For now I'll create the table and give it all ten of denver's possible nestings and make it work with an autofillentry. Possibly this many-many-recursive-query class will not be used to display strings at all, but rather to create storable chains of ids. I'll start by cheating some data into a new table and see what happens. But instead of creating a table with 12 cols--which ties me into a 12-value string--and has twelve identical tables that are supposed to be in order and that is not right for relational db, there is not supposed to be a fixed order of the tables--why can't the table just have an id, a place_id fk, and a sort order column? Then if a change is made you might only change the sort order. Sort order could be read off of the results of the m-m-recursive-query. But this won't work for populating a values list for an autofill. The m-m query would have to be redone. So what this 12-col-table really is, is a types table, except that the types are generated by code. I don't think there's any way to do it without putting all twelve cols in order... so the right thing to do is not to have twelve cols but to store a csv and just display it. But then the parts of the string have no meaning so it's back to twelve fk cols, so that for each string its corresponding place id follows it around the code. Too bad the cols have to be read in order but I don't know any way around it. When a new place is made or an old place changed, use self.tree_id to generate the list of ids to be stored.
# change to string input instead of id numbers, which involves:
#   make a list of all possible places on load
#   make a list of last_used places each time a place is used move it to the front of this list
# change the combo into an autofill
# make it work for combobox or autofill by inst mm twice and using a default parameter combobox=False so if combobox=True, see the commented portions where self.outwidg.values = ...
