# right_click_menu

import tkinter as tk
from styles import config_generic
from widgets import Toplevel, LabelStylable, Button
import dev_tools as dt



def make_rc_menus(
        rcm_widgets, 
        rc_menu,
        rcm_msg):
    '''
        To include a widget in the right-click context help, list the widget
        in rcm_widgets in the instance and store each widget's message 
        and title in message_strings.py. Example of usage from notes.py: near
        bottom of make_widgets() i.e. after making all widgets, do this...

            rcm_widgets = (self.subtopic_input.ent, self.note_input.text)
            rcm.make_rc_menus(
                rcm_widgets, 
                self.rc_menu, 
                ms.note_dlg_msg)

        ...and in __init__ right before calling make_widgets() do this...

        self.rc_menu = rcm.RightClickMenu(self.root)
    '''

    rc_menu.help_per_context = dict(zip(rcm_widgets, rcm_msg))
    
    for widg in rcm_widgets:
        widg.bind("<Button-3>", rc_menu.attach_rt_clk_menu)
        
    for k,v in rc_menu.loop_made.items():
        k.bind("<Button-3>", rc_menu.attach_rt_clk_menu)
        rc_menu.help_per_context[k] = v

class RightClickMenu(tk.Menu):

    def __init__(self, master, *args, **kwargs):
        tk.Menu.__init__(self, master, *args, **kwargs)

        self.master = master
        self.message = ''
        self.help_title = ''
        self.widg = None
        self.help_per_context = {}
        self.config(tearoff=0)

        self.loop_made = {}

        self.add_command(label='Copy', command=self.copy)
        self.add_command(label='Paste', command=self.paste)
        self.add_separator()
        self.add_command(label='Context Help', command=self.context_help)
        # # EXAMPLE don't delete, this is how you config() the menu items
        # #     post-constructor, or do it in the instance, see below.
        # self.entryconfigure('Copy', state='disabled')

    def copy(self):
        print('Copied')

    def paste(self):
        print('Pasted')

    def context_help(self):
        help = Toplevel(self.master)
        help.title(self.help_title)
        text = LabelStylable(
            help,
            width=75)
        text.grid(padx=24, pady=24)
        text.insert('end', self.message)
        off = Button(help, text='Done', command=help.destroy)
        off.grid(padx=24, pady=24, sticky='e')
        config_generic(help)
        off.focus_set()

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


