# error_messages.py

import sqlite3
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
from widgets import (Toplevel, Label, Button, Frame, Message)
from styles import config_generic
from files import current_file
import dev_tools as dt





def open_error_message(parent, message, title, buttlab):

    def close():
        error.destroy()

    error = Toplevel(parent)
    error.title(title)
    error.columnconfigure(0, weight=1)
    error.rowconfigure(0, weight=1)
    lab = Message(error, text=message, justify='left')
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12)
    button = Button(error, text=buttlab, command=close)
    button.grid(padx=6, pady=(0,12))
    button.focus_set()
    return error, lab

places_err = (
    "A place cannot contain itself.\n\nSelect a "
    "chain of places that are nested inside each other.",

)