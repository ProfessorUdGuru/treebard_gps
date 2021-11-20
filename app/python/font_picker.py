# font_picker.py

import tkinter as tk
from tkinter import font
import sqlite3
from files import get_current_file
from query_strings import update_format_font, select_format_font_scheme
from widgets import Label, Frame, Scale, Button
from styles import make_formats_dict, config_generic
from messages import open_message, fonts_msg
from scrolling import resize_scrolled_content    
from custom_combobox_widget import Combobox
import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

class FontPicker(Frame):
    def __init__(self, master, root, main, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.main = main
        self.all_fonts = sorted(font.families())
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_format_font_scheme)
        font_scheme = list(cur.fetchone())
        cur.close()
        conn.close()
        copy = []
        z = 0
        for i in font_scheme[0:2]:
            if i is None:
                copy.append(font_scheme[z + 2])
            else:
                copy.append(font_scheme[z])
            z += 1
        self.font_scheme = copy
        self.make_widgets()

    def make_widgets(self):

        def combobox_selected(combo):
            self.output_sample.config(font=(self.all_fonts[combo.current], self.fontSize))
            self.update_idletasks()  

        sample = Frame(self)

        self.output_sample = Label(
            sample,
            text="Sample Output Text ABCDEFGHxyz 0123456789 iIl1 o0O")

        self.fontSizeVar = tk.IntVar()
        self.fontSize = self.font_scheme[1]

        self.font_size = Scale(
            self,
            from_=8.0,
            to=26.0,
            tickinterval=6.0,
            label="Text Size",
            orient="horizontal",
            length=200,
            variable=self.fontSizeVar,
            command=self.show_font_size)
        print("line", looky(seeline()).lineno, "self.font_size, self.fontSize:", self.font_size, self.fontSize)
        self.font_size.set(self.fontSize)
 
        lab = Label(self, text="Select Output Font")
        self.cbo = Combobox(
            self, self.root, values=self.all_fonts, 
            height=500, scrollbar_size=12)
        lab.grid(column=0, row=2, pady=(24,6))
        self.cbo.grid(column=0, row=3, pady=(6, 20))

        self.apply_button = Button(
            self,
            text="APPLY",
            command=self.apply)

        sample.grid(column=0, row=0)
        self.output_sample.grid(padx=24, pady=20)
        self.font_size.grid(column=0, row=1, pady=24)
        self.apply_button.grid(column=0, row=4, sticky="e", padx=(0,24), pady=(0,24))

        Combobox.combobox_selected = combobox_selected

    def apply(self):
        self.font_scheme[1] = self.fontSizeVar.get()
        if len(self.cbo.get()) != 0:
            self.font_scheme[0] = self.cbo.get()
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_format_font, tuple(self.font_scheme))
        conn.commit()
        cur.close()
        conn.close()

        # Running redraw() anywhere in this block of code doesn't help, but if 
        #   run manually via ctrl+s it resizes the scrollbar correctly--why? 
        #   The sb isn't tall enough EVEN IF MAKING FONT SMALLER but ok on reload. 
        #   HINT: clicking APPLY button messes up the scrollbar EVEN IF NO CHANGE 
        #   IS MADE TO FONT SIZE. So that should help find the bug.
        #   HINT 2: CTRL+S also does nothing unless the Person Tab is active.
        # self.main.findings_table.redraw()
        # Try again after fixing all missing stuff in config_generic re: fonts
        config_generic(self.root)
        resize_scrolled_content(self.root, self.main.master, self.main)

        msg0 = open_message(
            self, 
            fonts_msg[0], 
            "Redraw-on-Font-Change Bug", 
            "OK")
        msg0[0].grab_set()
        msg0[1].config(aspect=400)

    def show_font_size(self, evt):
        self.fontSize = self.fontSizeVar.get()

if __name__ == "__main__": 

    root = tk.Tk()

    t = FontPicker(root, root, main=None)
    t.grid()

    q = Label(root, text="This text represents everything outside of the "
        "font picker.\n It changes when you click the APPLY button.")
    q.grid(padx=24, pady=48)

    config_generic(root)

    root.mainloop()