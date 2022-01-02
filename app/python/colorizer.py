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

        self.current_swatch = {
            "widget": None, "id": 0, "column": 0, "row": 0, "Up": None, 
            "Down": None, "Left": None, "Right": None, "last": False, 
            "scheme": {"bg": "", "highlight_bg": "", "head_bg": "", "fg": ""}}
        self.visible_rows = 3
        self.top_visible_row = 0
        self.DIREX = ("Up", "Right", "Down", "Left")

        self.bind("<Map>", self.arrow_in_first)

        self.pad = 2

        # self.preview_area = []

        self.make_schemes_dict()
        self.make_widgets()
        self.make_swatches()
        self.make_inputs()
        self.update_idletasks()
        self.canvas_height = self.swatch_canvas.winfo_reqheight()

    def make_widgets(self):
        
        header = LabelH3(self, text="Arrow keys enter & navigate swatches.", anchor="w")
        swatch_frame = Frame(self)
        self.swatch_canvas = Canvas(swatch_frame)
        self.sbv = Scrollbar(
            swatch_frame, 
            command=self.swatch_canvas.yview,
            hideable=True)
        self.swatch_canvas.config(yscrollcommand=self.sbv.set)

        self.swatch_window = Frame(self.swatch_canvas)
        self.swatch_canvas.create_window(
            0, 0, anchor="nw", window=self.swatch_window)

        self.inputs_frame = Frame(self)
        # only key, button, motion, enter, leave, or virtual events 
        #   can be bound here:
        self.sbv.tag_bind("slider", "<ButtonRelease-1>", self.get)

        # children of self
        self.columnconfigure(0, weight=1)
        header.grid(column=0, row=0, padx=(12,0), pady=12, sticky="ew")
        swatch_frame.grid(column=0, row=1, padx=12)
        self.inputs_frame.grid(column=0, row=2, padx=12, pady=12, sticky="ew")

        # children of swatch_frame
        swatch_frame.columnconfigure(0, weight=1)
        swatch_frame.rowconfigure(0, weight=1)
        self.swatch_canvas.grid(column=0, row=0, sticky="news")
        self.sbv.grid(column=1, row=0, sticky="ns")

        self.preview_area = [
            self, header, swatch_frame, self.swatch_window, 
            self.inputs_frame, self.sbv]

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
        qty = len(self.color_scheme_dicts)
        last = qty - 1
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
            frm.bind("<KeyPress>", self.traverse)      
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
            for lab in (lab0, lab1, lab2, lab3):
                lab.bind("<Button-1>", self.select)
            if stop is False:
                stop = True
                self.size_up(lab0, frm, qty)

            if w == last:
                self.swatch_last = frm
            if c % self.swatches_across == 0:
                c = c - self.swatches_across + 1
            else:
                c += 1
            if (w + 1) % self.swatches_across == 0:
                r += 1
            w += 1

        canvas_width = self.swatch_width * self.swatches_across
        scroll_height = int(ceil(
            (len(self.all_color_schemes) / self.swatches_across))) * self.swatch_height
        self.swatch_canvas.config(
            width=canvas_width,
            height=self.swatch_height * self.visible_rows, 
            scrollregion=(0, 0, canvas_width, scroll_height))

    def select(self, evt):
        evt.widget.master.focus_set()

    def size_up(self, sample_lab, sample_swatch, qty):
        self.swatch_first = sample_swatch
        self.update_idletasks()
        self.swatch_width = sample_lab.winfo_reqwidth() + (self.pad * 2)
        self.swatch_height = self.swatch_first.winfo_reqheight() + (self.pad * 2)
        row_width = self.master.master.winfo_reqwidth()
        self.swatches_across = int(row_width / self.swatch_width)
        self.last_row = self.swatches_across - (qty % self.swatches_across) - 1
        self.last_column = self.swatches_across - 1

    def preview(self):
        bg = self.current_swatch["scheme"]["bg"]
        highlight_bg = self.current_swatch["scheme"]["highlight_bg"]
        head_bg = self.current_swatch["scheme"]["head_bg"]
        fg = self.current_swatch["scheme"]["fg"]
        for widg in self.preview_area:
            cls = widg.winfo_class()
            if cls in ("Frame", "Label"):
                widg.config(bg=bg)
            elif cls in ("Button", "Entry", "Canvas"):
                widg.config(bg=highlight_bg)
                if cls == "Button":
                    widg.config(activebackground=head_bg)
            if cls not in ("Frame", "Canvas"):
                widg.config(fg=fg)
        self.sbv.itemconfig(self.sbv.thumb, fill=bg, outline=head_bg)

    def highlight(self, evt):
        widg = evt.widget
        widg.config(bg=self.formats["fg"], bd=self.pad)
        widg.grid_configure(padx=0, pady=0)
        self.make_swatch_dict(widg)
        children = widg.winfo_children()
        self.preview()

    def unhighlight(self, evt):
        evt.widget.config(bg=self.formats["highlight_bg"], bd=0)
        evt.widget.grid_configure(padx=self.pad, pady=self.pad)

    def traverse(self, evt):
        def autoscroll(sym, widg):
            '''
                The window position can't be used, because the window is 
                scrolling. Have to use the canvas position. The canvas is
                the port into the scrollregion. The window and scrollregion
                can/should be the same size, and the canvas smaller, like a 
                peep-hole.

                In spite of the fact that self.top_visible_row is only 
                referenced in this function, it has to be an instance variable 
                so the last value will persist till the next time the 
                function is called. 
            '''
            def scroll_up():
                self.swatch_canvas.yview_moveto(0.0)
                self.top_visible_row = 0
                last_visible_row = self.visible_rows - 1 

            def scroll_down():
                self.swatch_canvas.yview_moveto(1.0)
                self.top_visible_row = self.last_row - self.visible_rows + 1
                last_visible_row = self.last_row 

            self.update_idletasks()
            column = widg.grid_info()["column"]
            row = widg.grid_info()["row"]
            swatch_top = widg.winfo_rooty()
            swatch_bottom = swatch_top + self.swatch_height
            up1_swatch_top = swatch_top - self.swatch_height
            down1_swatch_bottom = swatch_bottom + self.swatch_height
            down_ratio = swatch_top + widget_ratio / window_height
            up_ratio = swatch_top - widget_ratio / window_height
            last_visible_row = self.visible_rows - 1
           
            if sym == "Right":
                if widg == self.swatch_last:
                    scroll_up()
                elif column == self.last_column:
                    if (row == last_visible_row and 
                            last_visible_row != self.last_row):
                        scroll_down()          
            elif sym == "Left":
                if widg == self.swatch_first:
                    scroll_down()
                elif column == 0:
                    if (row == self.top_visible_row and 
                            self.top_visible_row != 0):
                        scroll_up() 
            elif sym == "Down":
                if self.current_swatch["last"] is True:
                    scroll_up()
                elif down1_swatch_bottom > canvas_bottom:
                    scroll_down()
            elif sym == "Up":
                if row == 0:
                    scroll_down()
                elif up1_swatch_top < canvas_top:
                    scroll_up()

        sym = evt.keysym
        widg = evt.widget
        if sym not in ("Up", "Down", "Right", "Left"):
            return

        canvas_top = self.swatch_canvas.winfo_rooty()
        window_height = self.swatch_window.winfo_reqheight()
        canvas_bottom = canvas_top + self.canvas_height
        widget_ratio = self.swatch_height / window_height

        for direx in self.DIREX:
            if sym == direx:
                self.current_swatch[direx].focus_set()
        autoscroll(sym, widg)        

    def get_adjacent_widgets(self, widg, column, row):
        '''
            When a swatch comes into focus, create a dict of its relevant data.
        '''

        catalog = widg.master.winfo_children()

        right = widg.tk_focusNext()            
        left = widg.tk_focusPrev()
        self.last_row = self.swatch_last.grid_info()["row"]
        maxrow_lite = self.last_row - 1
        maxcol_lastrow = self.swatch_last.grid_info()["column"]
                
        rightcol = column + 1
        leftcol = column - 1
        uprow = row - 1
        downrow = row + 1
        last = False       

        if row == self.last_row:
            downrow = 0
            last = True
        elif row == maxrow_lite:
            if column > maxcol_lastrow:
                downrow = 0
                last = True
        elif row == 0:
            if column <= maxcol_lastrow:
                uprow = self.last_row
            else:
                uprow = maxrow_lite

        if column == self.last_column:
            rightcol = 0
        elif column == 0:
            leftcol = self.last_column

        for child in catalog:
            if child == widg: continue
            grid = child.grid_info()
            newcol = grid["column"]
            newrow = grid["row"]
            if (newcol == rightcol and newrow == row + 1 and 
                    column == self.last_column):
                right = child
            elif newcol == leftcol and newrow == row - 1 and column == 0:
                left = child
            elif newrow == uprow and newcol == column:
                up = child
            elif newrow == downrow and newcol == column:
                down = child 

        if widg is self.swatch_first:
            left = self.swatch_last
        elif widg is self.swatch_last:
            right = self.swatch_first

        return up, right, down, left, last

    def make_swatch_dict(self, widg):
        grid = widg.grid_info()
        column = grid["column"]
        row = grid["row"]
        up, right, down, left, last = self.get_adjacent_widgets(widg, column, row)

        self.current_swatch["widget"] = widg
        self.current_swatch["column"] = column
        self.current_swatch["row"] = row
        self.current_swatch["Up"] = up
        self.current_swatch["Right"] = right
        self.current_swatch["Down"] = down
        self.current_swatch["Left"] = left
        self.current_swatch["last"] = last
        d = 0
        for child in self.current_swatch["widget"].winfo_children():
            if d == 0:
                self.current_swatch["scheme"]["bg"] = child.cget("text")
            elif d == 1:
                self.current_swatch["scheme"]["highlight_bg"] = child.cget("text")
            elif d == 2:
                self.current_swatch["scheme"]["head_bg"] = child.cget("text")
            elif d == 3:
                self.current_swatch["scheme"]["fg"] = child.cget("text")
            d += 1

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

        new_swatch_frame = Frame(
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

        self.preview_area.extend(
            [instrux, copy_button, bg1, bg2, bg3, fg1, spacer, 
                new_swatch_frame, apply_button])

    def arrow_in_first(self, evt):
        self.swatch_first.focus_set()
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

    def get(self, evt):
        '''
            Haven't tried doing anything with this yet. Move it to Scrollbar
            class in scrolling.py instead of making it an instance attribute.
        '''
        trough_height = self.canvas_height
        thumb_top = self.sbv.coords('slider')[1]
        thumb_bottom = self.sbv.coords('slider')[3]
        thumb_height = thumb_bottom - thumb_top
        trough_traverse_height = trough_height - thumb_height
        ratio = thumb_top / trough_traverse_height
        print("line", looky(seeline()).lineno, "ratio:", ratio)




