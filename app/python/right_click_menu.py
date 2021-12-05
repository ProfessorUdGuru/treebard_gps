# right_click_menu

import tkinter as tk
from styles import config_generic
from messages import open_message
from widgets import LabelStylable, Button
import dev_tools as dt
from dev_tools import looky, seeline



def make_rc_menus(rcm_widgets, rc_menu, rcm_msg):
    '''
        To include a widget in the right-click context help, list the widget
        in rcm_widgets in the instance and store each widget's message 
        and title in messages_context_help.py. Example of usage from notes.py: near
        bottom of make_widgets() i.e. after making all widgets, do this...
            `rcm_widgets = (self.subtopic_input.ent, self.note_input.text)`
            `make_rc_menus(
                rcm_widgets, 
                self.rc_menu, 
                note_dlg_help_msg)`
        ...and in `__init__` before calling `make_widgets()` do this...
            `self.rc_menu = RightClickMenu(self.root)`
        ... and import to the module where rcm widgets are accessible:
            `from right_click_menu import RightClickMenu, make_rc_menus`

        Use this if the widgets were made in a loop and should all have the 
        same right-click message:

        In the loop where the widgets such as `editx` are made:
            `self.rc_menu.loop_made[editx] = role_edit_help_msg`

        At the bottom of messages_context_help.py, store the message and
        dialog title, e.g.:
            `role_edit_help_msg = (
                'Clicking the Edit button will open a row of edit inputs... ', 
                'Roles Dialog: Edit Existing Role Button')`

        Import the message & title text to the module where it will be used:
            `from messages_context_help import role_edit_help_msg`

        The normal procedure described above this loopy one still needs to be
        done even if there are no normal widgets in the module (widgets made
        one-at-a-time instead of in a loop. In this case `rcm_widgets` and
        `note_dlg_help_msg` can both = `()` but they have to exist.
    '''
    rc_menu.help_per_context = dict(zip(rcm_widgets, rcm_msg))
    
    for widg in rcm_widgets:
        widg.bind("<Button-3>", rc_menu.attach_rt_clk_menu)

    for k,v in rc_menu.loop_made.items():
        k.bind("<Button-3>", rc_menu.attach_rt_clk_menu)
        rc_menu.help_per_context[k] = v

class RightClickMenu(tk.Menu):
    '''
        This is how you config() the menu items post-constructor, or do it in 
        the instance, see below:
        self.entryconfigure('Copy', state='disabled')
    '''

    def __init__(self, master, *args, **kwargs):
        tk.Menu.__init__(self, master, *args, **kwargs)

        self.master = master
        self.message = ''
        self.help_title = ''
        self.widg = None
        self.config(tearoff=0)

        self.help_per_context = {}
        self.loop_made = {}

        self.add_command(label='Copy', command=self.copy)
        self.add_command(label='Paste', command=self.paste)
        self.add_separator()
        self.add_command(label='Context Help', command=self.context_help)

    def copy(self):
        print('Copied')

    def paste(self):
        print('Pasted')

    def context_help(self):
        msg = open_message(
            self.master, 
            self.message, 
            self.help_title, 
            "DONE")

    def attach_rt_clk_menu(self, evt):
        self.widg = evt.widget
        self.post(evt.x_root, evt.y_root)
        for k,v in self.help_per_context.items():
            if k == self.widg:
                self.message = v[0]
                self.help_title = v[1]

        self.widg.update_idletasks()

    def detect_text(self, evt):
        ''' 
            When the dropdown menu overlaps a second widget
            that also responds to this evt, it can take an extra 
            brain clearing click to get this to work right. 
        '''

        clikt = evt.widget
        if (len(self.help_per_context[clikt][0]) == 0 and 
                len(self.help_per_context[clikt][1]) == 0):
            self.disable_context_help()
        else:
            self.enable_context_help()

    def disable_context_help(self):
        self.entryconfigure('Context Help', state='disabled')

    def enable_context_help(self):
        self.entryconfigure('Context Help', state='normal')


