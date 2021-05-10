# date_validation_model_refactor

# sample widgets which give input to a dates validation class and get modified input back out

import tkinter as tk
from tkinter import ttk
import sqlite3
import widgets as wdg
from styles import ThemeStyles, make_formats_dict
import dev_tools as dt

ST = ThemeStyles()
formats = make_formats_dict()

class DateError(wdg.Toplevel):
    def __init__(self, message, widg, *args, **kwargs):
        wdg.Toplevel.__init__(self, *args, **kwargs)

        self.widg = widg
        self.title('Date Error')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frm = wdg.FrameHilited(self)
        lab = wdg.LabelHilited(frm, text=message)
        close = wdg.Button(self, text='OK', command=self.close)       

        frm.grid(column=0, row=0, padx=24, pady=(24,0), sticky='news')
        lab.grid(column=0, row=0, padx=24, pady=24)
        close.grid(column=0, row=1, pady=12)
        close.focus_set()
        self.grab_set()

        ST.config_generic(self)
        utes.center_window(self)

    def highlight_error(self):
        '''
            Detect whether input is from wdg.EntryLabel, tk.Entry,
            ttk.Combobox, wdg.Entry, or tk.Text.
        '''

        kind = self.widg.winfo_class()
        if kind == 'Label':
            # uncomment when entrylabel fixed to unplace 
            #    instead of destroy the placed Entry:
            # self.widg.ent.select_range(0, 'end') # DO NOT DELETE
            pass
        elif kind in ('Entry', 'Combobox'):
            self.widg.select_range(0, 'end')
        elif kind == 'Text':
            pass
        elif kind == 'Frame':
            self.widg.ent.select_range(0, 'end')
        self.widg.focus_set()

    def close(self):
        self.grab_release()
        self.highlight_error()
        self.destroy()

ERRORS = (
    "Date has too many terms.",
    "Repeated word in date.",
    "Year must be between 1 and 9999.",
    "Date contains conflicting information.",
    "Date is incomplete.",
    "Date is blank.",
    "Undatelike word.",
    "Too many numerical terms.",
    "Too many years input.",
    "'?' is used wrong.",
    "4-digit year required e.g. input '12 AD' as '0012'",
    "One suffix and one prefix maximum.",
    "Years have 4 digits ('1884', '0912'),\n"
        "days have 1 or 2 ('12', '02', '2'),\n"
        "and months have none ('ja', 'fe', 'mar', 'ap', 'may', etc.).",
    "The date doesn't exist.")

class ValidDate():
    def __init__(self, widg):

        self.widg = widg
        self.intake = intake

    def run_validator(self):
        '''
            Write this method in full as a flow chart for all actions
            before writing any other code.
        '''

        valid_date = self.get_widg_type(widg, finding_id=None)

    def get_widg_type(self, widg, finding_id=None):
        ''' validate date string, take appropriate action '''
        kind = widg.winfo_class()
        if kind == 'Label':
            date_in = widg.cget('text')
        elif kind in ('TCombobox', 'Entry'):
            date_in = widg.get()
        elif kind == 'Frame':
            date_in = widg.ent.get()
        elif kind == 'Text':
            date_in = widg.get(1.0, 'end')
        date_out = validate_date(date_in, widg)
        if len(date_out) == 0:
            return
        if kind == 'Label':
            widg.config(text=date_out)
        elif kind in ('TCombobox', 'Entry'):
            widg.delete(0, 'end')
            widg.insert(0, date_out)
        elif kind == 'Frame':
            widg.ent.delete(0, 'end')
            widg.ent.insert(0, date_out)
        elif kind == 'Text':
            widg.delete(1.0, 'end')
            widg.insert(1.0, date_out)
        store_date_db(date_out) # model only
        # store_valid_date(date_out, make_date_sorter.sorter, finding_id)

        return date_out # not needed in model



if __name__ == '__main__': 

    finding_id = 5555  

    def use_input(intake, widg):
        ''' for EntryLabel '''
        validate.run_validator(widg)

    def get_event(evt):
        ''' for widgets other than EntryLabel '''
        widg = evt.widget
        validate.run_validator(widg) 

    date_in = ''
    validate = ValidDate


    root = tk.Tk()
    root.geometry('+10+600')

    label = wdg.Label(
        root, 
        text='Dates validation procedure must work equally\n'
             'from any kind of input widget')
    label.grid(columnspan=3, pady=24)

    simple = wdg.Entry(root)
    simple.grid(column=0, row=1)
    simple.insert(0, '1810 10 18')
    simple.focus_set()

    mostring = wdg.Entry(root)
    mostring.grid(column=1, row=1)
    mostring.insert(0, '1912 4 jan')

    clarif3 = wdg.Entry(root)
    clarif3.grid(column=2, row=1)
    clarif3.insert(0, '11 oct 0012 ad to 1884 bc')

    clarif2 = wdg.Entry(root)
    clarif2.grid(column=3, row=1)
    clarif2.insert(0, '1811 4 3')

    ranje = wdg.Entry(root)
    ranje.grid(column=4, row=1)
    ranje.insert(0, '1822 and 1818')

    span = wdg.Entry(root)
    span.grid(column=5, row=1)
    span.insert(0, '1815 to 1808')

    span1 = wdg.Entry(root)
    span1.grid(column=6, row=1)
    span1.insert(0, '? to 1818')

    span2 = wdg.Entry(root)
    span2.grid(column=7, row=1)
    span2.insert(0, '1822 to ?')

    label2 = wdg.Label(root, text='EntryLabel:', takefocus=1)
    label2.grid(column=0, row=3)

    entrylabel = wdg.EntryLabel(root, use_input)
    entrylabel.grid(column=1, row=3)
    entrylabel.config(text='1500')

    conn = sqlite3.connect('c:/treebard_gps/app/python/test_date_in_out.db')
    cur = conn.cursor()
    cur.execute('SELECT dates FROM date_test WHERE date_test_id = 1')
    stored_date = cur.fetchone()[0]
    entrylabel.config(text=stored_date)

    label3 = wdg.Label(root,text='Combobox:', takefocus=1)
    label3.grid(column=0, row=4)

    combobox = wdg.ClickAnywhereCombo(root)
    combobox.grid(column=1, row=4)
    combobox.insert(0, '1499')

    label4 = wdg.Label(root,text='Text:', takefocus=1)
    label4.grid(column=0, row=5)

    text = wdg.Text(root, width=40, height=1)
    text.grid(column=1, row=5, columnspan=2)
    text.insert(1.0, '1601')

    show = wdg.Label(root)
    show.grid(column=0, row=6, columnspan=2)

    widgets = [simple, mostring, clarif3, clarif2, ranje, span, span1, span2]

    u = 0
    for widg in widgets:
        button = wdg.Button(
            root, 
            text='Validate', 
            command=lambda widg=widg: validate.run_validator(widg))
        button.grid(column=u, row=2)
        u += 1 

    def focus_next_window(event):
        event.widget.tk_focusNext().focus()
        return("break")

    text.bind("<Tab>", focus_next_window)
    for widg in (combobox, text):
        widg.bind('<FocusOut>', get_event)

    ST.config_generic(root)

    root.mainloop()






# DO LIST

# BEFORE STARTING refactor EntryLabel to unplace instead of destroy so that focusing out does not destroy, bec. if user input is bad, the focus needs to be returned to EntryLabel, replace the word input with intake
# keep portions of the work distinct from each other eg consider validity of input first and issue all error messages and return stoppages in one method where nothing else is done
# use a table of contents as a central operations method with shows what order things are done in, basically convert a flow chart into a list of function calls. Each one has input as a parameter and returns a final value which the next method then uses as a parameter
# use instance vars only where parameters and return values won't work or become difficult
# store encoded
# Replace tuples like not in ('bet', 'bet.'...) with variables for the tuple
# MAKE date code string, start with ad for suffix by default so it's never blank, and for code use 'from' 'to' 'and' 'bet'
# Add 9 cols to date_format db table for default_date_formats, default_abt, etc. and query them to get vals instead of hard-coding vals
# Try fixing all the old dates that still display as iso, using the gui only
# make date inputs work on date prefs tab, replace this line:
    # self.date_test.validate_date_or_not(input, widg)
# make date input work in new event maker where it says this:         date_test.classify_one_date(
# move this code to dates.py and refactor as needed till it works in findings table, search table? and date prefs tab, if necessary make the validator a class 
# delete extra db tables re date settings. 
# Rewrite right click menu topics and statustips for date settings


# Put in main do list under dates: Not retyping a year less than 4 digits is not currently allowed, which is an exception to the policy that "if it can be displayed in a formatted date, then it can be left there after some edit is made." But from 1884 B.C.E. to Oct 11, 12 C.E. for example gets an error bec. 12 is not four digits. I don't want to change this now because it's an edge case. It will only happen if 1) the person is actually inputting years < 999 and 2) the user wants to edit such a date. It stores fine if input as a 4-digit year eg 0012 and the error message that comes up is correct. I'm leaving it for now.