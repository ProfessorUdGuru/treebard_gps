# colorizer

import tkinter as tk
from tkinter import colorchooser
import sqlite3
from widgets import (
    Frame, Canvas, Button, LabelH3, Label, FrameStay, LabelStay, Entry)
from scrolling import Scrollbar
from styles import (
    get_color_schemes, get_color_schemes_plus, 
    get_all_descends, config_generic)
from files import get_current_file
from messages_context_help import color_preferences_swatches_help_msg
from query_strings import (
    update_format_color_scheme, delete_color_scheme, select_color_scheme_current, 
    update_color_scheme_null, insert_color_scheme)
import dev_tools as dt
from dev_tools import looky, seeline




current_file = get_current_file()[0]

class Colorizer(Frame):
    def __init__(self, master, root, rc_menu, formats, 
            tabbook=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.rc_menu = rc_menu
        self.formats = formats
        self.tabbook = tabbook

        # self.formats = make_formats_dict()

        self.old_col = 0
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.root.bind('<Return>', self.apply_scheme)

        self.r_col = {}

        opening_colors = (
            self.formats['bg'], 
            self.formats['highlight_bg'], 
            self.formats['head_bg'], 
            self.formats['fg'])
        self.make_widgets1()
        self.make_widgets2(opening_colors)

    def make_widgets1(self):

        stripview = Frame(self.master)

        self.master.update_idletasks()
        self.swatch_canvas = Canvas(
            stripview, 
            bd=1, highlightthickness=1, 
            highlightbackground=self.formats['highlight_bg'], 
            bg=self.formats['bg'],
            width=840,
            height=118) 
        self.hscroll = Scrollbar(
            stripview, orient='horizontal', command=self.swatch_canvas.xview)
        self.swatch_canvas.configure(xscrollcommand=self.hscroll.set)        

        self.swatch_window = Frame(self.swatch_canvas)

        buttons = Frame(stripview)

        self.try_button = Button(
            buttons, text='TRY', width=7, command=self.config_local)
        self.copy_button = Button(
            buttons, text='COPY', width=7, command=self.copy_scheme)
        self.apply_button = Button(
            buttons, text='APPLY', width=7, command=self.apply_scheme)
        
        self.new_scheme = Frame(self.master)

        # children of self.master
        stripview.grid(column=0, row=0)#, padx=12, pady=12
        self.new_scheme.grid(column=0, row=2, pady=12)

        # children of stripview
        self.swatch_canvas.grid(column=0, row=0, sticky='news')
        self.hscroll.grid(column=0, row=1, sticky="ew")
        buttons.grid(column=0, row=2, sticky='e', pady=(12,0))

        # children of buttons
        self.try_button.grid(column=0, row=0, sticky='e')
        self.copy_button.grid(column=1, row=0, padx=6)
        self.apply_button.grid(column=2, row=0, sticky='w')

        self.make_swatches()

        self.swatch_canvas.create_window(
            0, 0, anchor='nw', window=self.swatch_window)
        self.resize_color_samples_scrollbar()

    def make_widgets2(self, colors):

        def clear_select(evt):
            evt.widget.selection_clear()

        all_schemes = get_color_schemes()

        l_col = [
            'background 1', 'background 2', 'background 3', 'font color']

        self.entries_combos = []
        self.domain_tips = []

        addlab = LabelH3(self.new_scheme, text='New Color Scheme')

        h1 = Label(self.new_scheme, anchor='w', text='DOMAIN')
        h2 = Label(self.new_scheme, anchor='w', text='COLOR')

        j = 2
        for name in l_col:
            lab = Label(self.new_scheme, anchor='w', text=name)
            lab.grid(column=0, row=j, sticky='ew')
            ent = Entry(self.new_scheme, width=12)
            self.r_col[name] = ent
            ent.grid(column=1, row=j, padx=(3,0))
            self.entries_combos.append(ent)
            ent.bind('<FocusOut>', clear_select)
            ent.bind('<Double-Button-1>', self.open_color_chooser)
            self.domain_tips.append(lab)
            j += 1

        self.new_button = Button(
            self.new_scheme,
            text='CREATE SWATCH', 
            command=self.make_new_sample)

        # children of self.new_scheme
        self.new_scheme.columnconfigure(0, weight=1)
        addlab.grid(column=0, row=0, sticky='ew', columnspan=2)
        h1.grid(column=0, row=1, sticky='we')
        h2.grid(column=1, row=1, sticky='we')
        self.new_button.grid(column=0, row=6, columnspan=2, pady=(12,0))

    def resize_color_samples_scrollbar(self):
        self.swatch_window.update_idletasks()                   
        self.swatch_canvas.config(scrollregion=self.swatch_canvas.bbox("all")) 

    def apply_scheme(self, evt=None):
        self.recolorize()

    def recolorize(self):
        color_scheme = []
        for child in self.swatch_window.winfo_children():
            if self.master.focus_get() == child:
                frm = child

        foc = self.root.focus_get()

        if foc.master != self.swatch_window:
            return

        for child in frm.winfo_children():
            color_scheme.append(child['bg'])
            child = child
        color_scheme.append(child['fg'])

        color_scheme = tuple(color_scheme)

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_format_color_scheme, color_scheme)
        conn.commit()
        cur.close()
        conn.close()

        mbg = color_scheme[0]
        hbg = color_scheme[1]
        thbg = color_scheme[2]
        fg = color_scheme[3]

        config_generic(self.root)
        self.root.config(bg=mbg)

    def make_swatches(self):

        all_schemes_plus = get_color_schemes_plus()
        
        y = 0
        for scheme in all_schemes_plus:
            frm = FrameStay(
                self.swatch_window,
                name = '{}{}'.format('cs_', str(scheme[5])),
                bg='lightgray', 
                takefocus=1, 
                bd=1)
            frm.grid(column=y, row=0)
            frm.bind('<FocusIn>', self.change_border_color)
            frm.bind('<FocusOut>', self.unchange_border_color)
            frm.bind('<Key-Delete>', self.delete_sample)

            z = 0
            for color in scheme[0:3]:
                lab = LabelStay(
                    frm, 
                    width=12, 
                    bg=color, 
                    text=color, fg=scheme[3])
                lab.grid(column=y, row=z, ipadx=6, ipady=6)
                lab.bind('<Button-1>', self.config_local)
                self.rc_menu.loop_made[lab] = color_preferences_swatches_help_msg
                z += 1
            y += 1

        self.resize_color_samples_scrollbar()

        self.clear_entries()

    def clear_entries(self):
        for widg in self.new_scheme.winfo_children():
            if widg.winfo_class() == 'Entry':
                widg.delete(0, 'end')

    def detect_colors(self, frm):

        color_scheme = []
        if frm.winfo_class() == 'Label':
            frm = frm.master

        for child in frm.winfo_children():
            color_scheme.append(child['bg'])
            child = child
        color_scheme.append(child['fg'])

        return color_scheme

    def preview_scheme(self, scheme):
        
        trial_widgets = []
        all_widgets_in_tab1 = get_all_descends(
            self.master, trial_widgets)
        all_widgets_in_tab1.append(self.master)

        for widg in (all_widgets_in_tab1):
            if (widg.winfo_class() == 'Label' and 
                widg.winfo_subclass() == 'LabelStay'):
                    pass
            elif (widg in self.new_scheme.winfo_children() and 
                widg.grid_info()['row'] == 0):
                    widg.config(
                        bg=scheme[2],
                        fg=scheme[3])
            elif (widg.winfo_class() == 'Label' and 
                    widg.winfo_subclass() in ('Label', 'LabelH3')):
                        widg.config(
                            bg=scheme[0],
                            fg=scheme[3])
            elif widg.winfo_class() == 'Button':
                widg.config(
                        bg=scheme[1], 
                        fg=scheme[3],
                        activebackground=scheme[2])
            elif widg.winfo_class() == 'Entry':
                widg.config(bg=scheme[1]),
            elif widg in self.swatch_window.winfo_children():
                widg.config(bg='lightgray')
            elif widg.winfo_class() in ('Frame', 'Toplevel', 'Canvas'):
                widg.config(bg=scheme[0])

    def config_local(self, evt=None):

        all_schemes = get_color_schemes()

        self.clear_entries()

        # if double-click
        if evt:
     
            if evt.type == '4':
                evt.widget.master.focus_set()
            color_scheme = self.detect_colors(evt.widget)
            self.preview_scheme(color_scheme)

        # if TRY button
        else:
            for widg in self.new_scheme.winfo_children():

                # if entries not all filled out
                if (widg.winfo_class() == 'Entry' and
                    len(widg.get()) == 0): # prob. shd be break or continue
                        pass

                # if new scheme to try
                if (widg.winfo_class() == 'Entry' and
                    len(widg.get()) > 0):
                        inputs = []
                        inputs = tuple(inputs)

                        # if typed scheme is new
                        if inputs not in all_schemes:
                            self.preview_scheme(inputs)

                        # if scheme already exists
                        else:
                            self.clear_entries()

                # if no sample hilited
                elif self.swatch_window.focus_get().winfo_class() != 'Frame':
                    return
                elif (widg.winfo_class() == 'Entry' and
                    len(widg.get()) == 0):
                            color_scheme = self.detect_colors(
                                self.master.focus_get())
                            self.preview_scheme(color_scheme)

    def change_border_color(self, evt):
        evt.widget.config(bg='white', bd=2)        

    def unchange_border_color(self, evt):
        evt.widget.config(bg='lightgray', bd=1)

    def drop_scheme_from_db(self, frame, scheme):
        id = frame.split('_')[1]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(delete_color_scheme, (id,))
        conn.commit()    
        cur.execute(select_color_scheme_current)
        current_scheme = cur.fetchone()

        if scheme == current_scheme:
            cur.execute(update_color_scheme_null)
            conn.commit()

        cur.close()
        conn.close()    

    def delete_sample(self, evt):
        '''
            Don't allow built-in color schemes to be deleted. 
        '''
        dflt = self.swatch_window.winfo_children()[0]
        drop_me = self.swatch_window.focus_get()
        all_schemes_plus = get_color_schemes_plus()
        color_scheme = tuple(self.detect_colors(drop_me))
        all_schemes = []
        for scheme_plus in all_schemes_plus:
            all_schemes.append(scheme_plus[0:4])
        if color_scheme in all_schemes:
            idx = all_schemes.index(color_scheme)
            if all_schemes_plus[idx][4] == 0:
                drop_name = drop_me.winfo_name()
                self.drop_scheme_from_db(drop_name, color_scheme)
                drop_me.destroy()
                self.resize_color_samples_scrollbar()
                dflt.focus_set()
                fix = []
                for child in self.master.focus_get().winfo_children():
                    fix.append(child['bg']) 
                child = child
                fix.append(child['fg'])
                entries = []
                for child in self.new_scheme.winfo_children():
                    if child.winfo_class() == 'Entry':
                        entries.append(child)
                self.apply_button.invoke()

    def get_new_scheme(self):
        all_schemes = get_color_schemes()
        inputs = []
        for widg in self.new_scheme.winfo_children():
            if widg.winfo_class() == 'Entry':
                inputs.append(widg.get())
        inputs = tuple(inputs)
        for scheme in all_schemes:
            if inputs == scheme:
                return

        self.put_new_scheme_in_db(inputs)

    def put_new_scheme_in_db(self, new_scheme):
        all_schemes = get_color_schemes()
        if new_scheme not in all_schemes:

            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(insert_color_scheme, (new_scheme))
            conn.commit()
            cur.close()
            conn.close()

    def make_new_sample(self):

        back = self.r_col['background 1'].get()
        high = self.r_col['background 2'].get()
        table = self.r_col['background 3'].get()
        fonts = self.r_col['font color'].get()    

        try_these = [
            (back, self.r_col['background 1']), 
            (high, self.r_col['background 2']), 
            (table, self.r_col['background 3']), 
            (fonts, self.r_col['font color'])]

        for tup in try_these:
            if len(tup[0]) == 0:
                return
        
        test_color = Frame(self.root)

        for tup in try_these:
            try:
                test_color.config(bg=tup[0])
            except tk.TclError:
                tup[1].delete(0, tk.END)
                messagebox.showerror(
                    'Color Not Recognized.',
                    'A color was entered that is unknown to the system.')
                return

        self.get_new_scheme()
        for child in self.swatch_window.winfo_children():
            child.destroy()
        self.make_swatches()

    def copy_scheme(self):

        colors = []
        if self.root.focus_get().master == self.swatch_window:
            for child in self.root.focus_get().winfo_children():
                colors.append(child['bg'])
                child=child
            colors.append(child['fg'])

        color_entries = []
        for child in self.new_scheme.winfo_children():
            if child.grid_info()['row'] == 0:
                pass
            elif child.grid_info()['column'] == 1:
                color_entries.append(child)

        place_colors = dict(zip(color_entries, colors))

        for k,v in place_colors.items():
            k.delete(0, 'end')
            k.insert(0, v)

    def open_color_chooser(self, evt):
        chosen_color = colorchooser.askcolor(parent=self.root)[1]
        if chosen_color:
            evt.widget.delete(0, 'end')
            evt.widget.insert(0, chosen_color)




