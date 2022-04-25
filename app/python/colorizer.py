# colorizer.py

import tkinter as tk
from tkinter import colorchooser
from math import ceil
from re import search
import sqlite3
from widgets import (
    Frame, Canvas, Button, LabelH3, Label, FrameStay, LabelStay, Entry,
    FrameHilited2, get_all_descends, configall, Scrollbar,
    make_formats_dict, ALL_WIDGET_CLASSES, open_message)
from files import get_current_file
from messages import colorizer_msg
from messages_context_help import color_preferences_swatches_help_msg
from query_strings import (
    update_current_color_scheme, delete_color_scheme, insert_color_scheme,
    select_all_color_schemes_unhidden, select_all_color_schemes_hidden, 
    update_color_scheme_hide, select_color_scheme_current_id,
    update_current_color_scheme_default)
import dev_tools as dt
from dev_tools import looky, seeline



current_file = get_current_file()[0]
formats = make_formats_dict()
class Colorizer(Frame):
    '''
        The main organization of this class revolves around 
            `self.color_scheme_dicts`
        which is a list of dictionaries, one for each color scheme, and 
            `self.current_swatch`
        which is a nested dict representing one color scheme.
    '''
    def __init__(self, master, root, rc_menu, 
            tabbook=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.rc_menu = rc_menu
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

        self.current_color_scheme = [
            formats["bg"], formats["highlight_bg"], 
            formats["head_bg"], formats["fg"]]

        self.get_current_scheme_id()

        self.make_schemes_dict()
        self.make_widgets()
        self.make_swatches()
        idx = self.get_applied_swatch_index(self.currently_applied_color_scheme)
        self.applied_swatch = self.swatch_window.winfo_children()[idx]        
        self.make_inputs()
        self.update_idletasks()
        self.canvas_height = self.swatch_canvas.winfo_reqheight()

    def make_widgets(self):
        
        self.header = LabelH3(
            self, text="Arrow keys enter & navigate swatches.", anchor="w")
        self.current_display = Label(
            self, text="Currently applied color scheme is ID #{}".format(
                self.currently_applied_color_scheme))
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

        self.current_display.bind("<Button-1>", self.highlight_current_scheme)
        # only key, button, motion, enter, leave, or virtual events 
        #   can be bound here:
        self.sbv.tag_bind("slider", "<ButtonRelease-1>", self.get)

        # children of self
        self.columnconfigure(0, weight=1)
        self.header.grid(column=0, row=0, padx=(12,0), pady=12, sticky="ew")
        self.current_display.grid(column=1, row=0, sticky="e", padx=(0,12))
        swatch_frame.grid(column=0, row=1, columnspan=2, padx=12)
        self.inputs_frame.grid(
            column=0, row=2, columnspan=2, padx=12, pady=12, sticky="ew")

        # children of swatch_frame
        swatch_frame.columnconfigure(0, weight=1)
        swatch_frame.rowconfigure(0, weight=1)
        self.swatch_canvas.grid(column=0, row=0, sticky="news")
        self.sbv.grid(column=1, row=0, sticky="ns")

        self.preview_area = [
            self, self.header, swatch_frame, self.swatch_window, 
            self.inputs_frame, self.sbv, self.current_display]

    def make_inputs(self):

        instructions = "COPY a highlighted swatch to use it as a model for a new color scheme, or TYPE hex colors directly into the inputs, or DOUBLE-CLICK an input to open a color picker. Hex color format is #xxxxxx or #xxx; replace each x with a number or letter a-f."

        explanations = (
            "main background color", 
            "main highlight color", 
            "highlights such as border around scrollbar, background of "
                "pressed button", 
            "fonts and other foreground colors")

        instrux = Label(
            self.inputs_frame,
            text=instructions, 
            wraplength=450,
            anchor="se",
            justify="left")

        new_swatch_frame = FrameHilited2(
            self.inputs_frame, bg=formats["highlight_bg"])
        spacer1 = Frame(new_swatch_frame)
        self.bg1 = Entry(new_swatch_frame, width=9, cursor="hand2")
        self.bg2 = Entry(new_swatch_frame, width=9, cursor="hand2")
        self.bg3 = Entry(new_swatch_frame, width=9, cursor="hand2")
        self.fg1 = Entry(new_swatch_frame, width=9, cursor="hand2")
        spacer2 = Frame(new_swatch_frame)
        new_swatch_frame.columnconfigure(1, weight=1)
        t = 1
        for stg in explanations:
            lab = LabelStay(new_swatch_frame, text=stg, anchor="w")
            lab.grid(column=1, row=t, sticky="ew", ipadx=6, padx=(0,1))
            self.preview_area.append(lab)
            t += 1
        self.copy_button = Button(
            self.inputs_frame, text="COPY COLOR SCHEME", 
            command=self.fill_entries, width=19)
        self.add_button = Button(
            self.inputs_frame, text="ADD COLOR SCHEME", 
            command=self.add_color_scheme, width=19)
        self.apply_button = Button(
            self.inputs_frame, text="APPLY", command=self.apply, width=6)

        # children of self.inputs_frame
        self.inputs_frame.columnconfigure(1, weight=1)
        self.inputs_frame.rowconfigure(2, weight=1)
        instrux.grid(column=0, row=0, sticky="n", rowspan=3)
        new_swatch_frame.grid(column=1, row=0, rowspan=3, padx=(12,0), sticky="ns")
        self.copy_button.grid(column=2, row=0, sticky="ne", padx=(12,0), pady=(4,0))
        self.add_button.grid(column=2, row=1, sticky="ne", padx=(12,0), pady=(6,0))
        self.apply_button.grid(column=2, row=2, sticky="se", padx=(12,0))

        # children of new_swatch_frame
        # for num in range(4):
            # new_swatch_frame.rowconfigure(num, weight=1)
        new_swatch_frame.rowconfigure(0, weight=2)
        new_swatch_frame.rowconfigure(5, weight=3)
        spacer1.grid(column=0, row=0, columnspan=2, sticky="news")
        self.bg1.grid(
            column=0, row=1, padx=self.pad, pady=(self.pad, 0), sticky="ns")
        self.bg2.grid(column=0, row=2, padx=self.pad, sticky="ns")
        self.bg3.grid(column=0, row=3, padx=self.pad, sticky="ns")
        self.fg1.grid(
            column=0, row=4, padx=self.pad, pady=(0, self.pad), sticky="ns")
        spacer2.grid(column=0, row=5, columnspan=2, sticky="news")

        arrow_in_launches = (
            self.bg1, self.bg2, self.bg3, self.fg1, self.copy_button, 
            self.add_button, self.apply_button)
        for widg in arrow_in_launches:
            for event in ("<KeyPress-Up>",):
                widg.bind(event, self.arrow_in_last)
            for event in ("<KeyPress-Down>",):
                widg.bind(event, self.arrow_in_first)
        for widg in arrow_in_launches[4:]:
            for event in ("<KeyPress-Up>", "<KeyPress-Left>"):
                widg.bind(event, self.arrow_in_last)
            for event in ("<KeyPress-Down>", "<KeyPress-Right>"):
                widg.bind(event, self.arrow_in_first)

        self.preview_area.extend(
            [instrux, self.copy_button, self.bg1, self.bg2, self.bg3, self.fg1,  
                new_swatch_frame, self.apply_button, self.add_button, spacer1,
                spacer2])

        self.INPUTS = (self.bg1, self.bg2, self.bg3, self.fg1)
        for widg in self.INPUTS:
            widg.bind("<KeyRelease>", self.validate_hex_colors)
            widg.bind("<Double-Button-1>", self.open_color_chooser)
            widg.bind("<space>", self.open_color_chooser)

    def get_current_scheme_id(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_color_scheme_current_id)
        self.currently_applied_color_scheme = cur.fetchone()[0]
        cur.close()
        conn.close()

    def make_schemes_dict(self):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_color_schemes_unhidden)
        self.unhidden_color_schemes = cur.fetchall()
        cur.close()
        conn.close()

        self.color_scheme_dicts = []
        keys = ("id", "bg", "highlight", "head", "fg", "built_in", "hidden")
        for tup in self.unhidden_color_schemes:
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
                self.swatch_window, bg=formats["highlight_bg"], takefocus=1)
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
            (len(self.unhidden_color_schemes) / self.swatches_across))) * self.swatch_height
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

    def preview(self, typed_colors=None):
        if typed_colors:
            bg, highlight_bg, head_bg, fg = typed_colors       
        else:
            bg = self.current_swatch["scheme"]["bg"]
            highlight_bg = self.current_swatch["scheme"]["highlight_bg"]
            head_bg = self.current_swatch["scheme"]["head_bg"]
            fg = self.current_swatch["scheme"]["fg"]
        for widg in self.preview_area:
            cls = widg.winfo_class()
            if cls == "Label":
                if widg.winfo_subclass() == "LabelStay":
                    row = widg.grid_info()["row"] - 1
                    if row == 0:
                        widg.config(bg=bg, fg=fg)
                    elif row == 1:
                        widg.config(bg=highlight_bg, fg=fg)
                    elif row == 2:
                        widg.config(bg=head_bg, fg=fg)
                    elif row == 3:
                        widg.config(bg=fg, fg=bg)
                    text = widg.cget("text")
                    widg.config(text=text)
                else:
                    widg.config(bg=bg)
            elif cls == "Frame":
                if widg.winfo_subclass() != "FrameHilited2":
                    widg.config(bg=bg)
                else:
                    widg.config(bg=head_bg)
            elif cls in ("Button", "Entry", "Canvas"):
                widg.config(bg=highlight_bg)
                if cls == "Button":
                    widg.config(activebackground=head_bg)
                elif cls == "Entry":
                    widg.config(insertbackground=fg)
            if cls not in ("Frame", "Canvas", "Label"):
                widg.config(fg=fg)
            elif cls == "Label" and widg.winfo_subclass() != "LabelStay":
                widg.config(fg=fg)

        self.sbv.itemconfig(self.sbv.thumb, fill=bg, outline=head_bg)
        self.previewed = (bg, highlight_bg, head_bg, fg)

    def highlight(self, evt):
        widg = evt.widget
        widg.config(bg="orange", bd=self.pad)
        widg.grid_configure(padx=0, pady=0)
        idx = 0
        for child in self.swatch_window.winfo_children():
            if child == widg:
                iD = idx
                break
            idx += 1
        idx = self.color_scheme_dicts[iD]["id"]
        self.make_current_swatch_dict(widg, idx)
        self.preview()

    def unhighlight(self, evt):
        widg = evt.widget
        widg.config(bg=formats["highlight_bg"], bd=0)
        widg.grid_configure(padx=self.pad, pady=self.pad)

    def highlight_current_scheme(self, evt):
        iD = int(evt.widget.cget("text").split("id# ")[1])
        idx = self.get_applied_swatch_index(iD)
        self.applied_swatch = self.swatch_window.winfo_children()[idx]
        self.applied_swatch.config(bg="chartreuse", bd=self.pad)
        self.applied_swatch.grid_configure(padx=0, pady=0)

    def get_applied_swatch_index(self, iD):
        q = 0
        for dkt in self.color_scheme_dicts:
            if dkt["id"] == iD:
                idx = q
                break
            else:
                pass
            q += 1
        return idx

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

                Arrow traversal currently works better than Tab traversal. 
                Tab can enter and leave the swatch area, which is useful, but
                when using Tab traversal, the autoscroll doesn't work yet when
                going from the end of the last visible row to the next 
                (non-visible) row. It's on the do list.

                Any of the arrow keys enter the swatch area, from other focused 
                widgets on the page except the new color Entries. Arrows don't 
                traverse out of the swatch area, just round and round. To get 
                out of the swatch area, use Tab or the mouse.
            '''

            self.update_idletasks()
            column = widg.grid_info()["column"]
            row = widg.grid_info()["row"]
            swatch_top = widg.winfo_rooty()
            swatch_bottom = swatch_top + self.swatch_height
            up1_swatch_top = swatch_top - self.swatch_height
            down1_swatch_bottom = swatch_bottom + self.swatch_height
            down_ratio = swatch_top + widget_ratio / window_height
            up_ratio = swatch_top - widget_ratio / window_height
            self.last_visible_row = self.visible_rows - 1
           
            if sym == "Right":
                if widg == self.swatch_last:
                    self.scroll_up()
                elif column == self.last_column:
                    if (row == self.last_visible_row and 
                            self.last_visible_row != self.last_row):
                        self.scroll_down()          
            elif sym == "Left":
                if widg == self.swatch_first:
                    self.scroll_down()
                elif column == 0:
                    if (row == self.top_visible_row and 
                            self.top_visible_row != 0):
                        self.scroll_up() 
            elif sym == "Down":
                if self.current_swatch["last"] is True:
                    self.scroll_up()
                elif down1_swatch_bottom > canvas_bottom:
                    self.scroll_down()
            elif sym == "Up":
                if row == 0:
                    self.scroll_down()
                elif up1_swatch_top < canvas_top:
                    self.scroll_up()

        sym = evt.keysym
        widg = evt.widget
        if sym not in ("Up", "Down", "Right", "Left"):
            if sym == "Delete":
                self.axe_color_scheme(widg)
                return
            else:
                return

        canvas_top = self.swatch_canvas.winfo_rooty()
        window_height = self.swatch_window.winfo_reqheight()
        canvas_bottom = canvas_top + self.canvas_height
        widget_ratio = self.swatch_height / window_height

        for direx in self.DIREX:
            if sym == direx:
                self.current_swatch[direx].focus_set()
        autoscroll(sym, widg) 

    def scroll_up(self):
        self.swatch_canvas.yview_moveto(0.0)
        self.top_visible_row = 0
        self.last_visible_row = self.visible_rows - 1 

    def scroll_down(self):
        self.swatch_canvas.yview_moveto(1.0)
        self.top_visible_row = self.last_row - self.visible_rows + 1
        self.last_visible_row = self.last_row        

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

    def make_current_swatch_dict(self, widg, iD):
        grid = widg.grid_info()
        column = grid["column"]
        row = grid["row"]
        up, right, down, left, last = self.get_adjacent_widgets(widg, column, row)

        self.current_swatch["id"] = iD
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

    def arrow_in_first(self, evt):
        self.swatch_first.focus_set()
        self.swatch_canvas.yview_moveto(0.0)

    def arrow_in_last(self, evt):
        self.swatch_last.focus_set()
        self.swatch_canvas.yview_moveto(1.0)

    def fill_entries(self):
        colors = (
            self.current_swatch["scheme"]["bg"], 
            self.current_swatch["scheme"]["highlight_bg"], 
            self.current_swatch["scheme"]["head_bg"], 
            self.current_swatch["scheme"]["fg"])
        a = 0
        for widg in self.INPUTS:
            widg.delete(0, 'end')
            widg.insert(0, colors[a])
            a += 1        

    def apply(self, evt=None):
        color_scheme = (
            self.current_swatch["scheme"]["bg"], 
            self.current_swatch["scheme"]["highlight_bg"], 
            self.current_swatch["scheme"]["head_bg"], 
            self.current_swatch["scheme"]["fg"])
        idx = self.get_applied_swatch_index(self.currently_applied_color_scheme)
        self.applied_swatch = self.swatch_window.winfo_children()[idx] 
        self.applied_swatch.config(bg=formats["highlight_bg"], bd=0)
        self.applied_swatch.grid_configure(padx=self.pad, pady=self.pad)

        # get id for above selected color_scheme and change self.currently_applied_color_scheme to that id
        self.currently_applied_color_scheme = self.current_swatch["id"]

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        cur.execute(update_current_color_scheme, (self.currently_applied_color_scheme,))
        conn.commit()
        cur.close()
        conn.close()
        self.current_display.config(
            text="Currently applied color scheme is id# {}".format(
                self.currently_applied_color_scheme))

        new_formats = make_formats_dict()

        for klass in ALL_WIDGET_CLASSES:
            klass.formats = new_formats 

        configall(self.root, new_formats)
        self.root.config(bg=color_scheme[0])

    def validate_hex_colors(self, evt=None, chooser=False):
        if evt:
            sym = evt.keysym
            if sym not in ("numbersign", "BackSpace", "Delete"):
                if len(sym) != 1:
                    return
        spelt = False
        hexx = None
        typed_colors = []
        for widg in self.INPUTS:
            typed_colors.append(widg.get().strip())
        if evt or chooser is True: # KeyRelease or color chooser dialog
            valid_colors = 0
        else: # COPY button is pressed
            valid_colors = 3
        for stg in typed_colors:
            hexx = search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', stg)
            if hexx is None and stg not in COLOR_STRINGS:
                return
            elif hexx is not None:
                valid_colors += 1
            elif stg.lower() in COLOR_STRINGS:                
                spelt = True
                valid_colors += 1
            if valid_colors == 4 and (len(stg) in (4, 7) or spelt is True):
                try:
                    self.preview(typed_colors=typed_colors)
                except tk.TclError:
                    pass # the error is real but it's being handled

    def open_color_chooser(self, evt):
        chosen_color = colorchooser.askcolor(parent=self.root)[1]
        if chosen_color:
            evt.widget.delete(0, 'end')
            evt.widget.insert(0, chosen_color)
            self.validate_hex_colors(chooser=True)

    def add_color_scheme(self):

        in_unhidden = False
        in_hidden = False
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_all_color_schemes_hidden)
        hidden_color_schemes = cur.fetchall()
        for scheme in self.unhidden_color_schemes:
            if self.previewed[0:] == scheme[1:5]:
                in_unhidden = True
                break
        for scheme in hidden_color_schemes:
            if self.previewed[0:] == scheme[1:5]:
                in_hidden = True
                break
        if in_unhidden:
            open_message(self.root, colorizer_msg[0], "Non-Unique Color Scheme", "OK")
            cur.close()
            conn.close()
            return
        elif in_hidden:
            open_message(self.root, colorizer_msg[1], "Hidden Color Scheme", "OK")
            cur.close()
            conn.close()
            return
        else:
            cur.execute(insert_color_scheme, self.previewed)
            conn.commit()

        self.redraw_swatches(autodown=True)

        cur.close()
        conn.close()

    def redraw_swatches(self, autodown=False):
        self.clear_inputs()
        for child in self.swatch_window.winfo_children():
            child.destroy()
        self.make_schemes_dict()
        self.make_swatches()
        self.update_idletasks()
        self.canvas_height = self.swatch_canvas.winfo_reqheight()
        if autodown is True:
            self.scroll_down()
            self.swatch_last.focus_set()
        else:
            self.scroll_up()
            self.swatch_first.focus_set()

    def axe_color_scheme(self, widg):

        def delete_scheme():
            cur.execute(delete_color_scheme, (id_del,))
            conn.commit()            

        def hide_scheme():
            cur.execute(update_color_scheme_hide, (id_del,))
            conn.commit()

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        a = 0
        for dkt in self.color_scheme_dicts:
            if dkt["id"] == self.current_swatch["id"]:
                id_del = dkt["id"]
                built_in = dkt["built_in"]
                break
            a += 1
        if built_in == 0:
            delete_scheme()
        elif built_in == 1:
            hide_scheme()
        if id_del == self.currently_applied_color_scheme:
            cur.execute(update_current_color_scheme_default)
            conn.commit()
            self.currently_applied_color_scheme = 1
            # config_generic(self.root)
            configall(self.root, formats)

        self.redraw_swatches()

        cur.close()
        conn.close()        

    def clear_inputs(self):
        for widg in (self.bg1, self.bg2, self.bg3, self.fg1):
            widg.delete(0, 'end')

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

COLOR_STRINGS = [
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 
    'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 
    'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 
    'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 
    'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 
    'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 
    'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
    'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 
    'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 
    'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 
    'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 
    'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 
    'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 
    'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 
    'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 
    'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 
    'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 
    'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
    'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 
    'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 
    'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 
    'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 
    'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 
    'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 
    'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 
    'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 
    'wheat', 'white', 'whitesmoke', 'yellow']






