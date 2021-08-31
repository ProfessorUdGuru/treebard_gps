# nested_place_strings.py

''' 
    Nestings are created on load, so are available for use by an autofill 
    entry.
'''

import tkinter as tk
from tkinter import ttk
import sqlite3
from files import current_file
from widgets import Entry, Button
from autofill import EntryAuto
from query_strings import (
   select_place_id2, select_count_place_id, select_place, select_all_place_ids)
from styles import config_generic    
import dev_tools as dt
from dev_tools import looky, seeline







'''
    Terminology:
        --nest: any single place; can be a child and/or parent of another nest.
        --uppers: a collection of a single nest's parent items. 
        --branch: a chain of single items in a line of nested hierarchy. 
        --leaf: the current end of a branch, which is really a root, but I 
            didn't want yet another usage for the word "root" in Tkinter. 
        --initial_id: the first item input by the user. 
        --id_tree: the end product which contains the IDs and their 
            relationships that are used to create a collection of nestings.
        --nesting: nested place string representing the place IDs in an id_tree 
            which could be used as values in a combobox or autofill entry.

    This class was developed specifically for use in creating strings for 
    nested places like "Arlington, Virginia, USA" but there might be other
    usages. For example, the class could be used to create re-usable citation 
    strings like "Virginia State Archives, Collected Papers of Ned Frill, 
    Volume 9, Part 2, Chapter 5, page 9, line 40". If so, the user could input
    that whole string by typing a "v".

    To keep this code accessible to novice programmers (i.e. so I don't have 
    to learn advanced SQL such as Common Table Expressions), the recursion 
    needed has been supplied by code with no recursion in the SQL. This was 
    not done to avoid using a recursive query on a simple nested relationship, 
    which I know how to do. It was done to avoid creating a recursive query on 
    a many-to-many table, which I don't know how to do. 

    A single self-referencing table could store each city, township, county, 
    etc. in its own record in a single primary place column with a second 
    column listing a foreign key for the single parent of the primary place 
    in the same record. The FK would reference the primary key of a place in 
    the primary place column. But the nesting of a place is not that simple
    in the real world. For example, Dallas, Texas, has occupied the same basic 
    spot on the map during its life span, but it's had a number of 
    different parents. Currently it occupies parts of four different counties.
    But when it first came into being, it wasn't even in the United States of
    America, but rather in a place called the Republic of Texas. The simple 
    self-referencing table doesn't represent how places really work.

    One useful trick early in this lengthy process of planning this code
    was to multiply--by the length of the new results list--each branch in the 
    id_tree growing from the results of the previous query. This gives the 
    growing values list the right number of branches so that the new results 
    can be appended to a matching number of prior results. Since values can be 
    repeated in a many-to-many table, I had to keep from running the same query 
    over and over for the same value. So the first step is to get the possible 
    parents of the initial value, which is always one place, and all its 
    possible descendants. A dictionary like {20 : [21, 22, 23]} is saved and 
    the parents of place 20 will not have to be gotten from the database again 
    for this instance. Then the same is done for 21, 22, 23, with a dict of 
    parents saved for each. Repeat on down through the levels till results are 
    null. The intended result is that you input a place id such as 20, which 
    refers to "Denver" and get a whole collection of values such as "Denver, 
    Arapahoe Co, Colorado, USA" and "Denver, Denver Co, Colorado, USA", etc.

    In reality, detecting null parents to stop the search was more complicated 
    than it sounds. Since there can be more than one parent, nulls and branches
    had to be counted to make sure every branch ended in a null, before ending 
    the search. Otherwise, "Dallas, Collin County, Texas, USA" would have been 
    cut short at two nests when the null ending "Dallas, Republic of Texas" was 
    found. I had yet to take this into account when I created the chart below, 
    which was otherwise fairly helpful in trying to visualize how many branches
    would need to be made. In reality, all nestings that start from a given 
    initial_id will not be the same length.

    In the chart below, place IDs 20 and 24 each have three parents. This chart 
    not only shows how many branches should display in the GUI if this code 
    works right, it shows exactly what's in each branch. Trace each of the ten 
    branches down from 20 or up from the bottom. The final results should have 
    two chains with strings starting from 18, two chains starting from 19, and 
    six chains starting from 24.     
 
                                    20
                                             
            21                      22                      23

        18      19          24              19         18          24

        7       7       25  7   26          7           7       25  7   26

        8       8       8   8   27          8           8       8   8   27
'''

class ManyManyRecursiveQuery():
    '''
        This class has widget references built into it.
    '''

    final_strings = []

    def __init__(self, inwidg=None, outwidg=None, initial_id=1):

        self.outwidg = outwidg

        if inwidg is not None and len(inwidg.get().strip()) != 0:
            self.initial_id = int(inwidg.get().strip())
        else:
            self.initial_id = initial_id
        self.new_id_tree = []
        self.id_tree = [[self.initial_id]]
        self.final = []
        self.final_id_list = []
        self.radio_text = []
        self.make_uppers_lists()

    def make_uppers_lists(self):

        def run_query(id_var):
            '''
                This function is nested so it will run many times
                with the same database connection.
            '''            
            cur.execute(select_place_id2, (id_var,))
            uppers = cur.fetchall()
            self.uppers = [f[0] for f in uppers]
            if id_var is not None:
                dikt = {id_var:self.uppers}
                self.uppers_dicts.append(dikt)
            if self.uppers:
                for upper in self.uppers:
                    key_in_dict = any(upper in dikt for dikt in self.uppers_dicts)
                    
                    if key_in_dict is False:
                        run_query(upper)
                    else:
                        continue
            else:
                return

        self.uppers_dicts = []

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_place, (self.initial_id,))
        result = cur.fetchone()
        if result is None:
            if self.outwidg:
                self.outwidg.config(values=[])
            return
        run_query(self.initial_id)
        self.get_one_stage_of_values([self.initial_id])
        self.make_show_strings()
        cur.close()
        conn.close()  

    def get_one_stage_of_values(self, values_list):
        '''
            Starting with the initial value input, e.g. 130 for "Dallas",
            130 is currently/temporarily the leaf in the branch [130] so all 
            parents for 130 are found. Those parents [129, 138, 141, 142, 145] 
            then go through the same process. Branches will be made for each 
            possible lineage such as 
                [130, 129, None] for "Dallas, Republic of Texas, no parent"
            and the null will stop the search. The search will proceed then to
            build a branch starting [130, 138...]. This might finally end up
            as "Dallas, Dallas County, Texas, USA, None".

            The simple version: with the last ID in a chain as the dict key, 
            we're looking for the next value. If one is found, it will be 
            appended. If it's not a null, we'll then look for ITS parent. If it 
            is a null we'll stop looking but still complete the other chains of 
            IDs till each of them ends with a null.

            If you print `dkt.get(leaf)` and you get back `[None]`, that is a 
            dict value, but if you get back `None`, it means there's no such 
            key. 
        '''
        def get_uppers(leaf):
            uppers = None
            for dkt in self.uppers_dicts:
                if dkt.get(leaf) is None:
                    continue
                else:
                    uppers = dkt.get(leaf)
                    break            
            return uppers 
      
        none_count = 0
        new_id_tree = []
        f = 0
        for branch in self.id_tree: 
            leaf = branch[len(branch) - 1]
            uppers = get_uppers(leaf)

            if uppers is None:
                '''exit function when no more values are available'''
                list_count = len(self.id_tree)

                for lst in self.id_tree:
                    if lst[len(lst) - 1] is None:
                        self.final.append(lst)
                        none_count += 1

                if none_count == list_count:
                    self.final_id_list = self.final
                    return 
            else:
                for upper in uppers:
                    new_branch = list(branch)
                    new_branch.append(upper)
                    new_id_tree.append(new_branch) 
            f += 1

        self.id_tree = new_id_tree
        # Running one recursion builds up the whole nesting,
        #  which was a surprise. I had been running this in
        #  a loop when I accidentally discovered it was done
        #  after running one recursion.
        self.get_one_stage_of_values(uppers)      

    def make_show_strings(self):

        def validate_input():
            cur.execute(select_count_place_id, (self.initial_id,))
            count = cur.fetchone()[0]
            return count

        def get_string_with_id(identity):
            cur.execute(select_place, (identity,))
            string_part = cur.fetchone()[0]
            return string_part

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        count = validate_input()
        if count == 0:
            if self.outwidg:
                self.outwidg.config(values=[])
            return
        final_values_lists = []
        for lst in self.final_id_list:
            one_part = []
            k = 2
            for identity in lst:
                if identity is None:
                    break
                string_part = get_string_with_id(identity)
                one_part.append(string_part)
                if k == len(lst):
                    final_values_lists.append(one_part) 
                k += 1

        for lst in final_values_lists:
            stg = ', '.join(lst)
            if stg == 'unknown':
                stg = ''
            ManyManyRecursiveQuery.final_strings.append(stg)

        # single nesting for radiobutton label
        if self.outwidg is None:
            self.radio_text = stg

        cur.close()
        conn.close()

def make_all_nestings(query):
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    
    cur.execute(query)
    all_ids = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    for item_id in all_ids:
        ManyManyRecursiveQuery(initial_id=item_id)
    return ManyManyRecursiveQuery.final_strings

def make_new_nesting(query, idnum):
    ManyManyRecursiveQuery(initial_id=idnum)
    return ManyManyRecursiveQuery.final_strings

if __name__ == '__main__':

    def get_current_place():
        mm = ManyManyRecursiveQuery(id_in, combo)

    def clear_combo(evt):
        combo.delete(0, 'end')

    all_items = ["hello", "help", "hellfire-and-brimstone", 
        "health", "health & welfare"]

    all_items = make_all_nestings(select_all_place_ids)

    root = tk.Tk()

    auto = EntryAuto(root, autofill=True, width=75)
    auto.grid(column=0, row=0, columnspan=2)
    EntryAuto.create_lists(all_items)

    id_in = Entry(root)
    id_in.grid(column=0, row=1)
    id_in.bind('<FocusIn>', clear_combo)

    b = Button(
        root, 
        text='Enter ID number (left). Press here to make values for combobox.',
        command=get_current_place)
    b.grid(column=1, row=1)

    combo = ttk.Combobox(root, width=75)
    combo.grid(column=0, row=2, columnspan=2)
    auto.focus_set()

    config_generic(root)

    root.mainloop()




