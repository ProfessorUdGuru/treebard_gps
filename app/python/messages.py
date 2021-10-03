# error_messages.py

import sqlite3
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
from widgets import (Toplevel, Label, Button, Frame, MessageHilited)
from styles import config_generic
from files import current_file
import dev_tools as dt





def open_error_message(parent, message, title, buttlab):

    def close():
        '''
            See events_table `err_done` for an example of how to override
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
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12)
    buttonbox = Frame(msg)
    buttonbox.grid(column=0, row=1, sticky='e', padx=(0,12), pady=12)
    ok_butt = Button(buttonbox, text=ok_lab, command=cancel, width=6)
    ok_butt.grid(column=0, row=0, padx=6)
    cancel_butt = Button(buttonbox, text=cancel_lab, command=cancel, width=6)
    cancel_butt.grid(column=1, row=0, padx=6)
    ok_butt.focus_set()
    return msg, lab, ok_butt, cancel_butt

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


)

names_msg = (
    "This birth name already exists. To create a "
    "new person by the same name, click OK. The "
    "two persons can be merged later if desired.",

)
