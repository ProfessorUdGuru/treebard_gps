# error_messages.py

from tkinter import StringVar
import sqlite3
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
from widgets import (Toplevel, Label, Button, Frame, MessageHilited, Entry)
from styles import config_generic
from files import current_file
import dev_tools as dt
from dev_tools import looky, seeline





def open_error_message(parent, message, title, buttlab):

    def close():
        '''
            See events_table `err_done` for examples of how to override
            this if more needs to be done on closing the error message.
        '''
        msg.destroy()

    msg = Toplevel(parent)
    msg.title(title)
    msg.columnconfigure(0, weight=1)
    msg.rowconfigure(0, weight=1)
    lab = MessageHilited(msg, text=message, justify='left')
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12)
    button = Button(msg, text=buttlab, command=close, width=6)
    button.grid(column=0, row=1, padx=6, pady=(0,12))
    button.focus_set()
    return msg, lab, button

def open_yes_no_message(parent, message, title, ok_lab, cancel_lab):

    def ok():
        cancel()

    def cancel():
        msg.destroy()

    msg = Toplevel(parent)
    msg.title(title)
    msg.columnconfigure(0, weight=1)
    msg.rowconfigure(0, weight=1)
    lab = MessageHilited(msg, text=message, justify='left')
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12, columnspan=2)
    buttonbox = Frame(msg)
    buttonbox.grid(column=0, row=1, sticky='e', padx=(0,12), pady=12)
    ok_butt = Button(buttonbox, text=ok_lab, command=cancel, width=6)
    ok_butt.grid(column=0, row=0, padx=6)
    cancel_butt = Button(buttonbox, text=cancel_lab, command=cancel, width=6)
    cancel_butt.grid(column=1, row=0, padx=6)
    ok_butt.focus_set()
    return msg, lab, ok_butt, cancel_butt, buttonbox

def open_input_message(parent, message, title, ok_lab, cancel_lab, user_input):
    '''
        To avoid a circular import, a simpler version of this (fixed with a 
        neutral color) is available at files.py which should be importable
        to just about any module.
    '''
    def ok():
        cancel()

    def cancel():
        msg.destroy()

    def show():
        gotten = got.get()
        return gotten

    got = StringVar()

    msg = Toplevel(parent)
    msg.title(title)
    msg.columnconfigure(0, weight=1)
    msg.rowconfigure(0, weight=1)
    lab = MessageHilited(msg, text=message, justify='left')
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12, columnspan=2)
    lab2 = Label(msg, text="{} or {}?".format(user_input[0], user_input[1]))
    lab2.grid(column=0, row=1)
    inPut = Entry(msg, textvariable=got)
    inPut.grid(column=1, row=1)
    buttonbox = Frame(msg)
    buttonbox.grid(column=0, row=2, sticky='e', padx=(0,12), pady=12)
    ok_butt = Button(buttonbox, text=ok_lab, command=cancel, width=6)
    ok_butt.grid(column=0, row=0, padx=6)
    cancel_butt = Button(buttonbox, text=cancel_lab, command=cancel, width=6)
    cancel_butt.grid(column=1, row=0, padx=6)
    inPut.focus_set()
    parent.wait_window(msg)
    got = show()
    print("line", looky(seeline()).lineno, "got:", got)
    return user_input, got

places_err = (
    "A place cannot contain itself.\n\nSelect a "
    "chain of places that are nested inside each other.",
)

events_msg = (
    "The same person was used twice.",
    "Please enter a kin type for each person.",
    "A second person must be entered for a couple event.",
    "Offspring events can't be changed to other event types. You "
    "can delete the event and make a new event.",
    "A couple event can't be changed to a non-couple event, or "
        "vice-versa. For example, a marriage can be changed to "
        "a wedding but a death can't be changed to a divorce. "
        "Delete unwanted events and create new ones to "
        "replace them if they're incompatible in this way. To "
        "delete an event, delete the event type in the first column.",
    "An event is about to be deleted. This can't be undone. For "
        "couple events, the event will be deleted for both "
        "partners. For offspring events, the child's birth event "
        "will be deleted, but not the child.",
    "Each person has one birth and one death event. To add more "
        "hypothetical birth or death events, add them as assertions "
        "instead of conclusions. The events table is for conclusions, "
        "but assertions can be added freely by clicking the SOURCES "
        "button at the end of the birth or death event row or by "
        "going directly to the assertions tab if you prefer to make "
        "no conclusions at this time.",
    "A non-offspring event can't be changed to an offspring event. "
        "You can delete the event and make a new event.",
    "Offspring events can't be created directly. Create a new person "
        "and give them parents, and the parents' offspring events "
        "will be created automatically.",
)

names_msg = (
    "This birth name already exists. To create a "
        "new person by the same name, click OK. The "
        "two persons can be merged later if desired.",
    "That name type doesn't exist yet. Create it?",
)

notes_msg = (
    "Any note can be linked to any number of entities.",
)

dates_msg = (
    "One of the words 'and' or 'to' can be used once in a compound date. "
        "Input should be like 'feb 27 1885 to 1886' for 'from 27 Feb 1885 to 1886' "
        "or '1884 and mar 1885' for 'between 1884 and March 1885'.",
    "One month is allowed per date. For compound dates, the two dates have to be "
        "separated by 'and' or 'to'.",
    "For compound dates connected by 'and' or 'to', two months are possible. For "
        "single dates there can only be one month.",
    "If no month is input, no day can be input",
    "Each part of a compound date can have one prefix and one suffix. Each single "
        "date can have one prefix and one suffix. Prefixes include est, abt, bef, aft, "
        "and cal. Suffixes include AD, BC, CE, BCE, NS and OS.",
    "One date includes only one year.",
    "Date input included too many numerical terms. Input months as text, for "
        "example: feb for February, jul for July, may for May, etc.",
    "Each single date can include a maximum of five terms. Each compound date can "
        "include five terms in each part plus a link ('and' or 'to) between the two "
        "parts. The parts within a date can be in any order, for example 'nov 1885 14 "
        "est bc' for 'estimated 14 Nov 1885 BC'.",
    "Day and year are input as numbers. Months are input as abbreviated text "
        "such as mar, sep, dec. The date input seems to be lacking numerical input.",
    "A compound date should include two distinct and complete single dates "
        "separated by 'and' or 'to'. Treebard translates input separated by 'and' into "
        "a range such as 'between 1885 and 1886'. Compound dates separated by 'to' are "
        "translated into a span such as 'from 1912 to Feb 1915'. The input was for two "
        "identical dates. ",
    "That month doesn't have that many days. In leap years, February has 29 days. "
        "Leap years are evenly divisible by 4.",
)

fonts_msg = (
    "Press ALT+P then CTRL+S to resize the scrollbar after changing fonts.",
)

# files_msg = ("Give the tree a unique name. Treebard will use your wording as the title. Treebard will save 'Smith Family Tree' as a file at `{current drive}/treebard_gps/data/smith_family_tree/smith_family_tree.tbd`",)
