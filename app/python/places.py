# places.py (starting over 20210809)


''' It's possible that correcting-by-defect is the solution
 but I doubt it. The system is too complex to be solved by a
 complex algorithm. Any system that attempts to track the 
 details of this problem will fail sooner or later, because
 as more cases come up it will get harder and harder to improve,
 maintain or even understand. What's needed is a revolution in
 thought, which starts with a simple idea and stays with a simple
 idea. That idea is a compromise and it will be put into play by
 analyzing the input string as a string and dealing with it as
 a string. It's obvious that keeping the dialog from opening in
 some complex cases but not others is a hairsplitting waste of 
 energy and will just complicate
 the code more and more to no end. There should be very few
 criteria as to whether a case is or is not too complex to 
 accept input without a dialog. Fooling around with 'maybe this
 but maybe that' is not worth the trouble because the result is
 a house of cards built upon incomplete information. As more
 cases come up, the whole thing needs to be redone or else 
 fixing one thing will break another. So a decision needs to be
 made when a string is input and no questions asked. The only 
 way to solve this problem is to start over again on the duplicate
 and new places dialog. I have no choice, because the result of 
 each fix is a more and more patched-up non-algorithm of spaghetti.
 At this point the code resembles that game 'pick-up-stix' where
 you dump a bunch of lightweight sticks into a tangled pile and
 each player has a color. He has to pick up all his sticks first
 without moving any stick except the one he's currently picking
 up. It's fun because it's nearly impossible. Coding should not 
 be quite that impossible because I am now in the usual predicament
 of trying to super-analyze code I never quite understood even when
 I wrote it months ago. I'm starting over.'''
                    

import tkinter as tk
from widgets import (
    Toplevel, Frame, Button, Label, RadiobuttonBig, MessageHilited, 
    Entry, ButtonQuiet)
from place_autofill import EntryAuto
from toykinter_widgets import Separator
from nested_place_strings import make_all_nestings, ManyManyRecursiveQuery
from query_strings import (
    select_place_id, 
    select_place_hint, select_all_places, select_all_places_places, 
    select_finding_places_nesting, update_place_hint, select_place_id2, 
    select_max_place_id, select_place_id1, update_finding_places_finding_id,
    insert_place_new_with_id, insert_nested_pair, insert_finding_places,
    select_finding_places_id, select_places_places_id, select_all_place_ids)
from files import current_file
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
import dev_tools as dt
from dev_tools import looky, seeline
import sqlite3






def get_all_places_places():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_places_places)
    places_places = cur.fetchall()
    cur.close()
    conn.close()
    return places_places

def make_global_place_lists():
    place_strings = make_all_nestings(select_all_place_ids)
    places_places = get_all_places_places()
    return place_strings, places_places

place_strings, places_places = make_global_place_lists()

conn = sqlite3.connect(current_file)
cur = conn.cursor()
cur.execute(select_all_places)
all_place_names = [i[0] for i in cur.fetchall()]
cur.close()
conn.close()

unique_place_names = set(all_place_names) 

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
        self.add_new_place_option = False

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
        self.new_places_dialog.geometry("+120+24")
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
        self.lay_out_radios()

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

    def lay_out_radios(self):
        '''
            Make a new place dialog the same way for every place, then for
            certain qualifying (unambiguous) cases, don't open the dialog.
        '''
        self.radvars = []
        i = 0
        for dd in self.place_dicts:
            self.var = tk.IntVar()
            self.radvars.append(self.var)
            i += 1

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        for dkt in self.place_dicts:
            dkt["hint"] = ['']
            for num in dkt["id"]:
                cur.execute(select_place_hint, (num,))
                place_hint = list(cur.fetchone())
                if place_hint[0] is None:
                    place_hint[0] = ''
                else:
                    print("line", looky(seeline()).lineno, "case not handled")
                # dkt["hint"].append(place_hint[0])
                dkt["hint"].insert(0, place_hint[0])
            
        cur.close()
        conn.close()

        self.bullet = len(self.place_dicts) - 1
        self.rowdx = 0
        self.vardx = 0
        for dkt in self.place_dicts:
            self.make_radiobuttons(dkt)


    def make_radiobuttons(self, dkt):
        if len(dkt["id"]) > 0:
            nest_ids =  dkt["id"]
        else:
            nest_ids = dkt["temp_id"]
        place_string = '{}: {}, place ID #{}'.format(
            self.bullet, dkt["input"], nest_ids)

        lab = Label(self.frm, text=place_string)
        lab.grid(column=0, row=self.rowdx, sticky='w')

        self.hint_frm = Frame(self.frm, name="nest{}".format(self.bullet-1))
        self.hint_frm.grid(column=0, row=self.rowdx+1, sticky='w', padx=(0,3), columnspan=2)
        self.hint_frm.columnconfigure(0, minsize=48)

        self.make_edit_row(self.hint_frm)
        self.radx = 0
        row = 0
        for hint in dkt["hint"]:
            if len(dkt["id"]) > 0:
                new_id = dkt["temp_id"]
                last_idx = len(dkt["id"])
                if self.radx == last_idx:
                    self.current_id = new_id
                    self.select_first_radio()
                    rad_string = "{}: {} (new place and new place ID)".format(
                        self.current_id, dkt["input"])
                else:
                    self.current_id = dkt["id"][self.radx]
                    self.select_first_radio()
                    nesting = ManyManyRecursiveQuery(
                        initial_id=self.current_id).final_strings
                    rad_string = "{}: {}".format(self.current_id, nesting)
            elif len(dkt["id"]) == 0:
                self.current_id = dkt["temp_id"]
                self.select_first_radio()
                rad_string = "{}: {} (new place and new place ID)".format(
                    self.current_id, dkt["input"])
            else:
                print("line", looky(seeline()).lineno, "what does this do?")
                self.current_id = dkt["id"][self.radx]
                self.select_first_radio()
                nesting = ManyManyRecursiveQuery(
                    initial_id=self.current_id).final_strings
                rad_string = "{}: {}".format(self.current_id, nesting)

            rad = RadiobuttonBig(
                self.hint_frm, 
                variable=self.radvars[self.vardx],
                value=self.current_id,
                text=rad_string, 
                anchor="w")

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
            lab.grid(column=1, row=row+1, sticky='w', padx=6)
            editx.grid(column=0, row=row+1, pady=(0,3), sticky='e')

            editx.bind('<Enter>', self.on_hover)
            editx.bind('<Leave>', self.on_unhover)
            editx.bind('<Button-1>', self.get_clicked_row)
            editx.bind('<space>', self.get_clicked_row)
            editx.bind('<FocusIn>', self.on_hover)
            editx.bind('<FocusOut>', self.on_unhover)
            self.radx += 1
            row += 2

        sep = Separator(self.frm, 3)
        sep.grid(column=0, row=self.rowdx+2, sticky='ew', 
            columnspan=3, pady=(3,0))
        self.rowdx += 3
        self.vardx += 1
        self.bullet -= 1

    def select_first_radio(self):
        if self.radx == 0:
            self.radvars[self.vardx].set(self.current_id)





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

class ValidatePlace():

    def __init__(self, root, treebard, place_input, finding, nested_place):

        self.root = root
        self.treebard = treebard
        self.place_input = place_input
        self.finding = finding
        self.nested_place = nested_place

        self.place_list = []
        self.place_dicts = []
        self.new = False
        self.dupes = False

        self.see_whats_needed()

    def see_whats_needed(self):

        def get_matching_ids(nest):
            cur.execute(select_place_id, (nest,))
            ids = cur.fetchall()
            ids = [i[0] for i in ids] 
            if len(ids) == 0: self.new = True
            elif len(ids) > 1: self.dupes = True
            return ids

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        self.place_list = self.place_input.split(",")
        self.place_list = [self.place_list[i].strip() for i in range(len(self.place_list))]
        self.length = len(self.place_list)

        self.place_dicts = [
            (
                { 
                    "id" : get_matching_ids(nest),
                    "input" : nest}) 
            for nest in self.place_list]
        cur.close()
        conn.close()

        self.make_new_places()
        print("line", looky(seeline()).lineno, "self.new, self.dupes:", self.new, self.dupes)
        if self.new is True or self.dupes is True:
            self.new_place_dialog = NewPlaceDialog(
                self.root,
                self.place_dicts,
                "Clarify place selections where there is not exactly one ID "
                "number.\n\nPress the EDIT button to add or edit hints for "
                "duplicate place names or any place name.\n\nWhen entering "
                "new place names, ID numbers have been assigned which you can "
                "just OK.\n\nIf the options are not exactly right, press CANCEL "
                "and use the Places Tab to create or edit the place.", 
                "New and Duplicate Places Dialog",
                ("OK", "CANCEL"),
                self.treebard,
                do_on_ok=self.collect_place_ids)

    def make_new_places(self):
        '''
            A temp_id is assigned to each nest in case the user needs to make
            a new place by the name input, even if some place(s) by that name
            already exist in the database.

            The temp_ids all have to be assigned at the same time so that each
            number is unique, then entry to the database has to be done all
            at the same time while this information is still correct. After
            the max ID is obtained from the database, no db transactions can
            occur which insert to any of the place tables till these temp IDs
            are either used or discarded.
        '''
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_max_place_id)
        temp_id = cur.fetchone()[0] + 1
        for dkt in self.place_dicts:
            dkt["temp_id"] = temp_id
            temp_id += 1
        cur.close()
        conn.close()

    def collect_place_ids(self):
        print("line", looky(seeline()).lineno, "self.place_dicts:", self.place_dicts)
        r = 0
        for dkt in self.place_dicts:
            dkt["id"] = self.new_place_dialog.radvars[r].get()
            r += 1

        print("line", looky(seeline()).lineno, "self.place_dicts:", self.place_dicts)

# ALL KNOWN PLACES, NO DUPES: dialog doesn't open; dialog opens for all other cases:

# ALL KNOWN, SOME OUTER DUPES
# line 492 self.place_dicts: [{'id': [860, 861, 862, 864], 'input': 'Motel 6'}, {'id': [728, 792], 'input': 'Reno'}, {'id': [708], 'input': 'Nevada'}, {'id': [8], 'input': 'USA'}]
# line 498 self.place_dicts: [{'id': 864, 'input': 'Motel 6'}, {'id': 728, 'input': 'Reno'}, {'id': 708, 'input': 'Nevada'}, {'id': 8, 'input': 'USA'}]

# ALL KNOWN, SOME INNER DUPES
# line 492 self.place_dicts: [{'id': [15, 679], 'input': 'Sassari'}, {'id': [15, 679], 'input': 'Sassari'}, {'id': [14], 'input': 'Sardegna'}, {'id': [12], 'input': 'Italy'}]
# line 498 self.place_dicts: [{'id': 15, 'input': 'Sassari'}, {'id': 679, 'input': 'Sassari'}, {'id': 14, 'input': 'Sardegna'}, {'id': 12, 'input': 'Italy'}]

# ALL KNOWN, SOME INNER & SOME OUTER DUPES


# SOME NEW & SOME KNOWN, NO DUPES
# line 492 self.place_dicts: [{'id': [], 'input': 'Abd', 'temp_id': 867}, {'id': [], 'input': 'Def', 'temp_id': 868}, {'id': [], 'input': 'Geh', 'temp_id': 869}, {'id': [116], 'input': 'Iowa'}, {'id': [8], 'input': 'USA'}]
# line 498 self.place_dicts: [{'id': 867, 'input': 'Abd', 'temp_id': 867}, {'id': 868, 'input': 'Def', 'temp_id': 868}, {'id': 869, 'input': 'Geh', 'temp_id': 869}, {'id': 116, 'input': 'Iowa'}, {'id': 8, 'input': 'USA'}]

# SOME NEW & SOME KNOWN, SOME OUTER DUPES = ok

# SOME NEW & SOME KNOWN, SOME INNER DUPES = ok

# SOME NEW & SOME KNOWN, SOME INNER & SOME OUTER DUPES = ok

# ALL NEW, NO DUPES = ok

# ALL NEW, SOME OUTER DUPES
# NOT GOOD ENOUGH, NEEDED TO INPUT NEW BUT NO OPTION RAD

# ALL NEW, SOME INNER DUPES

# ALL NEW, SOME INNER & SOME OUTER DUPES


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
                    final.place_list[j], final.place_list[j]))
            lab.grid()
            j += 1

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


