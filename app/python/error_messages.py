# error_messages.py

# import tkinter as tk
import sqlite3
from window_border import Border
from scrolling import Scrollbar, resize_scrolled_content
from widgets import (Toplevel, Label, Button, Frame)
from styles import ThemeStyles
from files import get_current_file
import dev_tools as dt




current_file = get_current_file()[0]
ST = ThemeStyles()

def open_error_message(parent, message, title, buttlab):

    def close():
        error.destroy()

    error = Toplevel(parent)
    error.title(title)
    error.columnconfigure(0, weight=1)
    error.rowconfigure(0, weight=1)
    lab = Message(error, text=message, justify='left')
    lab.grid(column=0, row=0, sticky='news', padx=3, pady=3)
    button = Button(error, text=buttlab, command=close)
    button.grid(padx=3, pady=3)
    button.focus_set()

# duplicate_places_with_duplicate_parents = (
    # "There are too many levels of identically-named but different places "
    # "in the database. Use nicknames for all but one of the levels till more " 
    # "code is written to handle this case.\n\n"
    # "Example: Two places named 'OK Ranch' existed somewhere and both "
    # "were in places called 'Pickens Township' but these were two "
    # "different townships. Due to two levels of duplicate nestings, "
    # "unique nicknames will have to be used for either the ranches "
    # "or the townships till code is written to handle this kind of duplex "
    # "duplication in nested places.")