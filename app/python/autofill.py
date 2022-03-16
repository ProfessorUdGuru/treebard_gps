# autofill.py

import tkinter as tk
from widgets import EntryUnhilited, Radiobutton, Button, Frame, LabelHeader
from window_border import Dialogue
import dev_tools as dt
from dev_tools import looky, seeline





class EntryAutoPerson(EntryUnhilited):
    '''
        To use this class, after instantiating it, you have to call 
        EntryAuto.create_lists(all_items). Other than getting all_items
        (e.g. from a database query), and updating the values list when
        a new value is added, the class is self-contained.        
    '''

    all_person_autofills = []

    def create_lists(all_items):
        """ Run this whenever autofill entries are being created to get the 
            values for the autofill. After values change, run something like
            update_person_autofill_values() which runs this function and 
            updates the values of all the autofill entries.

            Keeps a temporary list during one app session which will 
            prioritize the autofill values with the most recently used values
            given priority over the alphabetical list of the values not used in
            the current session.

            The `prepend_match()` method is used in conjuction with this 
            to add the most recently used value to the very front of the list.

            Since this function and the list `all_person_autofills` comprise a 
            class-level procedure, values used and moved to the front of the 
            list by one input will become available as first match to all the 
            other inputs too, until the app is closed. Next time the app opens,
            a fresh list of recently-used autofill values will be started.
        """
        key_list = list(all_items.items())
        recent_items = []
        all_items_unique = []

        for item in key_list:
            if item not in recent_items:
                all_items_unique.append(item)
        final_items = dict(recent_items + all_items_unique)
        return final_items

    def __init__(self, master, autofill=False, values=None, *args, **kwargs):
        EntryUnhilited.__init__(self, master, *args, **kwargs)
        self.master = master
        self.autofill = autofill
        self.values = values

        self.pos = 0
        self.current_id = None
        self.current_is_dupe = False
        self.hits = None

        if autofill is True:
            self.bind("<KeyPress>", self.detect_pressed)
            self.bind("<KeyRelease>", self.get_typed)
            self.bind("<FocusOut>", self.prepend_match, add="+")
            self.bind("<FocusIn>", self.deselect, add="+")

    def detect_pressed(self, evt):
        '''
            runs on every key press
        '''
        if self.autofill is False:
            return
        key = evt.keysym
        if len(key) == 1:
            self.pos = self.index('insert')
            keep = self.get()[0:self.pos]
            self.delete(0, 'end')
            self.insert(0, keep)

    def get_typed(self, evt):
        """ Run on every key release. Filter out most non-alpha-numeric 
            keys. Run the functions not triggered by events.
        """
        def do_it():
            hits = self.match_string()
            self.show_hits(hits, self.pos)

        self.current_id = None
        if self.autofill is False:
            return
        key = evt.keysym
        # Allow alphanumeric characters.
        if len(key) == 1:
            do_it()
        # Allow number signs, hyphens and apostrophes (#, -, ').
        elif key in ('numbersign', 'minus', 'quoteright'):
            do_it()
        # Open the PersonAdd dialog with the "+" stripped off the input.
        elif key == "plus":
            pass
        else:
            pass

    def match_string(self):
        """ Match typed input to birth name, or alt name if no birth name. """
        def match_alt_string():
            for key,val in self.values.items():
                for k,v in val.items():
                    if k == "alt name":
                        if v.lower().startswith(got.lower()):
                            if (v, key) not in hits:
                                hits.append((v, key))

        hits = []
        got = self.get()

        for key,val in self.values.items():
            for k,v in val.items():
                if k == "birth name":
                    if len(v) == 0:
                        match_alt_string()
                    elif v.lower().startswith(got.lower()):
                        if (v, key) not in hits:
                            hits.append((v, key))
        return hits

    def show_hits(self, hits, pos):
        cursor = pos + 1
        if len(hits) != 0:
            if len(hits) > 1:
                first = hits[0][0]
                self.current_is_dupe = False
                for hit in hits:
                    if hit[0] == first:
                        self.current_is_dupe = True
                        self.hits = hits
                    else:
                        self.current_is_dupe = False
                        break
                # if self.current_is_dupe:
                    # radval = self.open_dupe_dialog(hits)
                    # self.delete(0, 'end')
                    # self.insert(0, radval[0])
                    # self.current_id = radval[1]
                else:
                    self.delete(0, 'end')
                    self.insert(0, hits[0][0])
                    self.current_id = hits[0][1]
            else:
                self.delete(0, 'end')
                self.insert(0, hits[0][0])
                self.current_id = hits[0][1]
        self.icursor(cursor)

    def open_dupe_dialog(self, hits):

        def ok_dupe_name():
            cancel_dupe_name()
    
        def search_dupe_name():
            cancel_dupe_name()

        def cancel_dupe_name():
            dupe_name_dlg.destroy()

        self.right_id = tk.IntVar()
        dupe_name_dlg = Dialogue(self)

        lab = LabelHeader(
            dupe_name_dlg.window, justify='left', wraplength=450)
        lab.grid(column=0, row=0, padx=12, pady=12, ipadx=6, ipady=6)

        radfrm = Frame(dupe_name_dlg.window)
        radfrm.grid(column=0, row=1)

        r = 0
        for hit in hits:
            name, iD = [hit[0], str(hit[1])]
            rdo = Radiobutton(
                radfrm, text="{}  #{}".format(name, iD), 
                variable=self.right_id, value=r)
            rdo.grid(column=0, row=r)
            if r == 0:
                rdo.select()
                rdo.focus_set()
                lab.config(text="Which {}?".format(name))
            r += 1
        
        buttons = Frame(dupe_name_dlg.window)
        buttons.grid(column=0, row=2, pady=12, padx=12)
        dupe_name_ok = Button(buttons, text="OK", command=ok_dupe_name, width=7)
        dupe_name_ok.grid(column=0, row=0, sticky="e", padx=(0,12))
        search_name = Button(buttons, text="SEARCH DUPE NAME", command=search_dupe_name)
        search_name.grid(column=1, row=0, sticky="e", padx=(0,12))
        dupe_name_cancel = Button(buttons, text="CANCEL", command=cancel_dupe_name, width=7)
        dupe_name_cancel.grid(column=2, row=0, sticky="e", padx=0)

        dupe_name_dlg.canvas.title_1.config(text="Duplicate Stored Names")
        dupe_name_dlg.canvas.title_2.config(text="")

        dupe_name_dlg.resize_window()
        self.wait_window(dupe_name_dlg)
        return hits[self.show_current_id()]

    def show_current_id(self):
        return self.right_id.get()

    def prepend_match(self, evt):
        """ Determine which ID was used to fill in a value. Move the autofill
            value corresponding with that ID to the front of the valus list.
        """
        content = self.get()
        if self.current_id in self.values:
            key_list = list(self.values.items())
            u = 0
            for tup in key_list:
                if tup[0] == self.current_id:
                    idx = u
                    break
                u += 1
            used = key_list.pop(idx)
            key_list.insert(0, used)
            self.values = dict(key_list)

    def deselect(self, evt):
        '''
            This callback was added because something in the code for this 
            widget caused the built-in replacement of selected text with 
            typed text to stop working. So if you tabbed into an autofill entry
            that already had text in it, the text was all selected as expected 
            but if you typed, the typing was added to the end of the existing 
            text instead of replacing it, which is unexpected. Instead of 
            finding out why this is happening, I added this callback so that 
            tabbing into a filled-out autofill will not select its text. This 
            might be better since the value in the field is not often changed 
            and should not be easy to change by mistake.
        '''
        self.select_clear()

class EntryAuto(EntryUnhilited):
    '''
        To use this class, after instantiating it, you have to call 
        EntryAuto.create_lists(all_items). Other than getting all_items
        (e.g. from a database query), the class is self-contained.        
    '''

    all_person_autofills = []

    def create_lists(all_items):
        recent_items = []
        all_items_unique = []

        for item in all_items:
            if item not in recent_items:
                all_items_unique.append(item)
        final_items = recent_items + all_items_unique
        return final_items

    def __init__(self, master, autofill=False, values=None, *args, **kwargs):
        EntryUnhilited.__init__(self, master, *args, **kwargs)
        self.master = master
        self.autofill = autofill
        self.values = values

        if autofill is True:
            self.bind("<KeyPress>", self.detect_pressed)
            self.bind("<KeyRelease>", self.get_typed)
            self.bind("<FocusOut>", self.prepend_match, add="+")
            self.bind("<FocusIn>", self.deselect, add="+")

    def detect_pressed(self, evt):
        '''
            runs on every key press
        '''
        if self.autofill is False:
            return
        key = evt.keysym
        if len(key) == 1:
            self.pos = self.index('insert')
            keep = self.get()[0:self.pos]
            self.delete(0, 'end')
            self.insert(0, keep)

    def get_typed(self, evt):
        '''
            Run on every key release; filters out most non-alpha-numeric 
            keys; runs the functions not triggered by events.
        '''
        def do_it():
            hits = self.match_string()
            self.show_hits(hits, self.pos)

        if self.autofill is False:
            return
        key = evt.keysym
        # allow alphanumeric characters
        if len(key) == 1:
            do_it()
        # allow hyphens and apostrophes
        elif key in ('minus', 'quoteright'):
            do_it()
        # look for other chars that should be allowed in nested names
        else:
            pass

    def match_string(self):
        hits = []
        got = self.get()
        use_list = self.values
        for item in use_list:
            if item.lower().startswith(got.lower()):
                hits.append(item)
        return hits

    def show_hits(self, hits, pos):
        cursor = pos + 1
        if len(hits) != 0:
            self.delete(0, 'end')
            self.insert(0, hits[0])
            self.icursor(cursor)

    def prepend_match(self, evt):
        content = self.get()
        if content in self.values:
            idx = self.values.index(content)
            del self.values[idx]
            self.values.insert(0, content)

    def deselect(self, evt):
        '''
            This callback was added because something in the code for this 
            widget caused the built-in replacement of selected text with 
            typed text to stop working. So if you tabbed into an autofill entry
            that already had text in it, the text was all selected as expected 
            but if you typed, the typing was added to the end of the existing 
            text instead of replacing it, which is unexpected. Instead of 
            finding out why this is happening, I added this callback so that 
            tabbing into a filled-out autofill will not select its text. This 
            might be better since the value in the field is not often changed 
            and should not be easy to change by mistake.
        '''
        self.select_clear()

class EntryAutoHilited(EntryAuto):
    def __init__(self, master, formats, *args, **kwargs):
        EntryAuto.__init__(self, master, *args, **kwargs)

        self.config(bg=formats["highlight_bg"])

class EntryAutoPersonHilited(EntryAutoPerson):
    def __init__(self, master, formats, *args, **kwargs):
        EntryAutoPerson.__init__(self, master, *args, **kwargs)

        self.config(bg=formats["highlight_bg"])

if __name__ == "__main__":

    from widgets import Entry

    all_items = [
        "Flagstaff, Coconino County, Arizona",
        "Fond du Lac, USA",
        "Fort Pierce, USA",
        "Fort Morgan, USA",
        "Flagstaff, USA",
        "Fairmont, USA",
        "Fitchburg, USA",
        "Falmouth, USA",
        "Flagstaff, Arizona, USA",
        "Fairbanks, USA",
        "Florissant, USA",
        "Florence, USA",
        "Fairfax, USA",
        "Farmington, USA",
        "Fayetteville, USA",
        "Fort Kent, USA",
        "Forrest City, USA",
        "Freeport, USA",
        "Fort Benton, USA",
        "Fort Barbour, UK",
        "Fort Worth, USA",
        "Fort Lee, USA",
        "Florida, USA",
        "Flemington, Italy",
        "Frederick, USA",
        "Findlay, USA",
        "Fredericksburg, USA",
        "Fairfield, USA",
        "Fernandina Beach, USA",
        "Ferguson, USA",
        "Fallon, USA",
        "Fitzgerald, USA",
        "Franklin, USA",
        "Fort Valley, USA",
        "Fulton, USA",
    ]

    root = tk.Tk()

    autofill = EntryAuto(root, autofill=True, width=40, bg="steelblue")
    autofill.grid()
    autofill.focus_set()

    traverse = Entry(root, bg="tan")
    traverse.grid()
    traverse.autofill = True
    traverse.values = all_items
    # traverse.config(textvariable=traverse.var)

    place_values = EntryAuto.create_lists(all_items)

    autofill2 = EntryAuto(root, autofill=True, width=40, bg="steelblue", values=place_values)
    autofill2.grid()
    root.mainloop()






