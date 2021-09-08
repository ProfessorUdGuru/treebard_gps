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
    button = Button(msg, text=buttlab, command=close)
    button.grid(padx=6, pady=(0,12))
    button.focus_set()
    return msg, lab, button

places_err = (
    "A place cannot contain itself.\n\nSelect a "
    "chain of places that are nested inside each other.",

)

event_table_err = (
    "The same person was used twice.",
    "Please enter a kin type for each person.",
    "A second person must be entered for a couple event.",

)
