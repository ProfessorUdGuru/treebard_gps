# colorizer

import tkinter as tk
from tkinter import colorchooser
from math import ceil
import sqlite3
from widgets import (
    Frame, Canvas, Button, LabelH3, Label, FrameStay, LabelStay, Entry)
from scrolling import Scrollbar
from styles import get_all_descends, config_generic
from files import get_current_file
from messages_context_help import color_preferences_swatches_help_msg
from query_strings import (
    update_format_color_scheme, delete_color_scheme, select_color_scheme_current, 
    update_color_scheme_null, insert_color_scheme, select_all_color_schemes_unhidden)
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

        self.pad = 2

        self.make_schemes_dict()
        self.make_widgets()
        self.make_swatches()
        self.make_inputs()

    def make_widgets(self):
        header = LabelH3(self, text="Arrow keys enter & navigate swatches.", anchor="w")
        swatch_frame = Frame(self)
        self.swatch_canvas = Canvas(swatch_frame, height=500)
        sbv = Scrollbar(
            swatch_frame, 
            command=self.swatch_canvas.yview,
            hideable=True)
        self.swatch_canvas.config(yscrollcommand=sbv.set)

        self.swatch_window = Frame(self.swatch_canvas)
        self.swatch_canvas.create_window(
            0, 0, anchor="nw", window=self.swatch_window)

        self.inputs_frame = Frame(self)

        # children of self
        self.columnconfigure(0, weight=1)
        header.grid(column=0, row=0, padx=(12,0), pady=12, sticky="ew")
        swatch_frame.grid(column=0, row=1, padx=12)
        self.inputs_frame.grid(column=0, row=2, padx=12, pady=12, sticky="ew")

        # children of swatch_frame
        swatch_frame.columnconfigure(0, weight=1)
        swatch_frame.rowconfigure(0, weight=1)
        self.swatch_canvas.grid(column=0, row=0, sticky="news")
        sbv.grid(column=1, row=0, sticky="ns")

    def make_schemes_dict(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_color_schemes_unhidden)
        self.all_color_schemes = cur.fetchall()
        cur.close()
        conn.close()

        self.color_scheme_dicts = []
        keys = ("id", "bg", "highlight", "head", "fg", "built_in", "hidden")
        for tup in self.all_color_schemes:
            values = tup
            dkt = dict(zip(keys, values))
            self.color_scheme_dicts.append(dkt)
        self.color_scheme_dicts = sorted(
            self.color_scheme_dicts, key=lambda i: i["id"])

    def make_swatches(self):
        last = len(self.color_scheme_dicts) - 1
        stop = False
        w = 0
        c = 1
        r = 0
        for dkt in self.color_scheme_dicts:
            frm = FrameStay(
                self.swatch_window, bg=self.formats["highlight_bg"], takefocus=1)
            frm.grid(column=c-1, row=r, padx=self.pad, pady=self.pad)
            frm.bind("<FocusIn>", self.highlight)
            frm.bind("<FocusOut>", self.unhighlight)
            bg = dkt["bg"]
            highlight = dkt["highlight"]
            head = dkt["head"]
            fg = dkt["fg"]
            lab0 = LabelStay(frm, text=bg, bg=bg, fg=fg, width=10)
            lab1 = LabelStay(
                frm, text=highlight, bg=highlight, fg=fg, width=10)
            lab2 = LabelStay(frm, text=head, bg=head, fg=fg, width=10)
            lab3 = LabelStay(frm, text=fg, bg=fg, fg=bg, width=10)
            lab0.grid(column=0, row=0)
            lab1.grid(column=0, row=1)
            lab2.grid(column=0, row=2)
            lab3.grid(column=0, row=3)
            if stop is False:
                stop = True
                sample_lab = lab0
                self.swatch1 = frm
                self.update_idletasks()
                unit_width = sample_lab.winfo_reqwidth() + (self.pad * 2)
                unit_height = self.swatch1.winfo_reqheight() + (self.pad * 2)
                swatches_width = self.master.master.winfo_reqwidth()
                swatches_across = int(swatches_width / unit_width)
            if w == last:
                self.swatch_last = frm

            if c % swatches_across == 0:
                c = c - swatches_across + 1
            else:
                c += 1
            if (w + 1) % swatches_across == 0:
                r += 1
            w += 1

        canvas_width = unit_width * swatches_across
        scroll_height = int(ceil(
            (len(self.all_color_schemes) / swatches_across))) * unit_height
        self.swatch_canvas.config(
            width=canvas_width,
            height=unit_height * 3, 
            scrollregion=(0, 0, canvas_width, scroll_height))

    def highlight(self, evt):
        self.current_swatch = evt.widget
        evt.widget.config(bg=self.formats["fg"], bd=self.pad)
        evt.widget.grid_configure(padx=0, pady=0)
        self.traverse()

    def traverse(self):
        self.current_scheme = []
        for child in self.current_swatch.winfo_children():
            self.current_scheme.append(child.cget("text"))
        print("line", looky(seeline()).lineno, "self.current_scheme:", self.current_scheme)
        print("line", looky(seeline()).lineno, "self.current_swatch.tk_focusNext():", self.current_swatch.tk_focusNext())       

    def unhighlight(self, evt):
        evt.widget.config(bg=self.formats["highlight_bg"], bd=0)
        evt.widget.grid_configure(padx=self.pad, pady=self.pad)

    def make_inputs(self):

        instructions = '''
            Copy the current swatch to use it as a model for a new color scheme,
            or type hex colors directly into the inputs, or double-click an
            input to open a color picker. Hex color format is #xxxxxx.
        '''
        instrux = Label(
            self.inputs_frame,
            text=instructions, 
            wraplength=600,
            anchor="se",
            justify="right")

        new_swatch_frame = FrameStay(
            self.inputs_frame, bg=self.formats["highlight_bg"])
        copy_button = Button(
            self.inputs_frame, text="COPY", command=self.fill_entries, width=6)
        bg1 = Entry(new_swatch_frame, width=9)
        bg2 = Entry(new_swatch_frame, width=9)
        bg3 = Entry(new_swatch_frame, width=9)
        fg1 = Entry(new_swatch_frame, width=9)
        spacer = Frame(self.inputs_frame)
        apply_button = Button(
            self.inputs_frame, text="APPLY", command=self.apply, width=6)

        # children of self.inputs_frame
        self.inputs_frame.columnconfigure(3, weight=1)
        # self.inputs_frame.rowconfigure(0, weight=1)
        instrux.grid(column=0, row=0, sticky="n")
        new_swatch_frame.grid(column=1, row=0, padx=(12,0), sticky="s")
        copy_button.grid(column=2, row=0, padx=(12,0), sticky="sw")
        spacer.grid(column=3, row=0, sticky="ew")
        apply_button.grid(column=4, row=0, sticky="se")

        # children of new_swatch_frame
        bg1.grid(column=0, row=0, padx=self.pad, pady=(self.pad, 0))
        bg2.grid(column=0, row=1, padx=self.pad)
        bg3.grid(column=0, row=2, padx=self.pad)
        fg1.grid(column=0, row=3, padx=self.pad, pady=(0, self.pad))

        for widg in (bg1, bg2, bg3, fg1, copy_button, apply_button):
            for event in ("<KeyPress-Up>", "<KeyPress-Left>"):
                widg.bind(event, self.arrow_in_last)
            for event in ("<KeyPress-Down>", "<KeyPress-Right>"):
                widg.bind(event, self.arrow_in_first)

    def arrow_in_first(self, evt):
        self.swatch1.focus_set()
        self.swatch_canvas.yview_moveto(0.0)

    def arrow_in_last(self, evt):
        self.swatch_last.focus_set()
        self.swatch_canvas.yview_moveto(1.0)

    def fill_entries(self):
        pass

    def apply(self):
        pass


    def open_color_chooser(self, evt):
        chosen_color = colorchooser.askcolor(parent=self.root)[1]
        if chosen_color:
            evt.widget.delete(0, 'end')
            evt.widget.insert(0, chosen_color)




