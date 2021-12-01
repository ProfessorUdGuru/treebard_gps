# many_many_recursive_query

import tkinter as tk
from tkinter import ttk
import sqlite3
from files import get_current_file
from widgets import EntryAutofill
from query_strings import (
   select_place_id2, select_count_place_id, select_place, select_all_place_ids)
import dev_tools as dt
from dev_tools import looky, seeline







'''
    Terminology: "uppers" is a collection of a
    single item's parent items. "Branch" is a chain of single items in a line of descent. "Leaf" is the current end of a branch. "Initial_id" represents the first item input by the user. "Id_tree" is the end product which contains the IDs and their relationships that are used to create a collection of strings which could be used as values in a combobox or autofill entry. "Stage" is a recursion, a single generation of uppers.

    This class was developed specifically for use in creating strings for 
    nested places like "Arlington, Virginia, USA" but the terminology reflects its generic usefulness by not mentioning place names. For example, the class could be used to create citation strings like "Virginia State Archives, Collected Papers of Ned Frill, Volume 9, Part 2, Chapter 5, page 9, line 40". To keep this code accessible to novice programmers (i.e. so I don't have to learn advanced SQL such as Common Table Expressions), the recursion needed has been supplied by recursive Python function(s) and no recursion in the SQL. This was not done to avoid using a recursive query on a simple nested relationship, which I know how to do. It was done to avoid creating a recursive query on a many-many table, which I don't know how to do. 

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

    One trick early in this lengthy groping-in-the-dark was to multiply--by the length of the new results list--each branch in the id_tree growing from the results of the previous query. This 
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
    '''
        This class had widget references built into it.
    '''
    def __init__(self, inwidg=None, outwidg=None, initial_id=1):

        self.outwidg = outwidg

        if len(inwidg.get().strip()) != 0:
            self.initial_id = int(inwidg.get().strip())
        else:
            self.initial_id = initial_id
        self.new_id_tree = []
        self.id_tree = [[self.initial_id]]
        self.final = []
        self.final_id_list = []
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

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_place, (self.initial_id,))
        result = cur.fetchone()
        if result is None:
            return
        run_query(self.initial_id)
        self.get_one_stage_of_values([self.initial_id])
        self.make_show_strings()
        cur.close()
        conn.close()  

    def get_one_stage_of_values(self, values_list):
        '''

            In the code I'm using `leaf` for root since `root` is being used in
            Tkinter already. It just refers to the last item in a list. 
            Topmost ancestor or `leaf` is found by inserting a null in the
            database for a nest that has no parent. The null leaf stops
            the search. The same idea can be used in a simpler recursive db 
            query but in this case we're querying a many-to-many db table
            and I don't know how to do that recursively so I invented this
            alternate way to drive myself crazy instead of figuring out the
            purely SQL solution.

            Starting with the initial value input, e.g. 130 for "Dallas",
            130 is currently/temporarily the leaf in the branch [130] so all parents for 130 are 
            found. Those parents [129, 138, 141, 142, 145] then go through
            the same process. Branches will be made for each possible lineage
            such as [130, 129, None] for "Dallas, Republic of Texas, no parent"
            and the null will stop the search. The search will proceed then to
            build a branch starting [130, 138...]. This might finally end up
            as "Dallas, Dallas County, Texas, USA, None".

            The finishing touch on this procedure was to stop the search for 
            only the one branch when that branch gets a null parent, instead
            of stopping the search altogether at the first null, which is how
            a simple recursive nested parent would be found. But we have to 
            learn how to deal accurately in entities that have multiple parents, otherwise 
            all the branches will be stunted to the same length as 
            [130, 129, None]. This was done by creating yet another list to
            hold finished branches while branches still being searched can be
            searched until each finds a null leaf. By popping branches out of the list being searched when their null
            is found, the search automatically stops when the original list is empty.

            Coming
            back to this code after a long absence I finally grew back into an
            understanding of it by reminding myself that `leaf` is the last ID
            in the CURRENT/GROWING list of IDs, and `dkt.get(leaf)` is the value that
            corresponds to `leaf` as the key, or else it's None. If you print
            `dkt.get(leaf)` and you get back `[None]`, that is a dict value, but
            if you get back `None`, it means there's no such key. The simple version:
            with the last ID in a chain as the dict key, we're looking for the next
            value. If one is found, it will be appended. If it's not a null, we'll
            then look for ITS parent. If it is a null we'll stop looking but still
            complete the other chains of IDs till each of them ends with a null.
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
        # running one recursion builds up the whole nesting
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
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        count = validate_input()
        if count == 0:
            self.outwidg.config(values=[])
            return

        final_values_lists = []
        final_strings = []
        for lst in self.final_id_list:
            one_part = []
            for identity in lst:
                if identity is None:
                    break
                string_part = get_string_with_id(identity)
                one_part.append(string_part)
            final_values_lists.append(one_part) 
        for lst in final_values_lists:
            stg = ', '.join(lst)
            final_strings.append(stg)
            if final_strings == ['unknown']:
                final_strings = []
        self.outwidg.config(values=final_strings)
        cur.close()
        conn.close()

if __name__ == '__main__':

    def get_current_place():
        mm = ManyManyRecursiveQuery(ent, combo)

    def clear_combo(evt):
        combo.delete(0, 'end')

    root = tk.Tk()

    ent = tk.Entry(root)
    ent.grid()
    ent.bind('<FocusIn>', clear_combo)

    b = tk.Button(
        root, 
        text='Enter ID number above. Press here to make values for combobox.',
        command=get_current_place)
    b.grid()

    combo = ttk.Combobox(root, width=75)
    combo.grid()
    ent.focus_set()

    root.mainloop()


# use above to generate nestings on load and store the nesting for use by autofills
#   get all places from place table
#   from each place generate its possible nestings
#   store each nesting in a Python list
#   test with autofill
#   when editing places do it over




