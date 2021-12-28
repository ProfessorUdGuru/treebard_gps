# autofill.py

# EntryAutofill is shown for comparison, it's not to be used; 
#   this module is about EntryAuto which is defined below

import tkinter as tk
from widgets import EntryUnhilited
# from styles import make_formats_dict
import dev_tools as dt
from dev_tools import looky, seeline





# formats = make_formats_dict()

class EntryAuto(EntryUnhilited):
    '''
        To use this class, after instantiating it, you have to call 
        EntryAuto.create_lists(all_items). Other than getting all_items
        (e.g. from a database query), the class is self-contained.        
    '''

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
        # self.formats = formats
        self.autofill = autofill
        self.values = values

        # self.config(
            # bg=self.formats['bg'], 
            # fg=self.formats['fg'], 
            # font=self.formats['input_font'], 
            # insertbackground=self.formats['fg'])

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
            runs on every key release; filters out most non-alpha-numeric 
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
    traverse.config(textvariable=traverse.var)

    place_values = EntryAuto.create_lists(all_items)

    autofill2 = EntryAuto(root, autofill=True, width=40, bg="steelblue", values=place_values)
    autofill2.grid()
    root.mainloop()






