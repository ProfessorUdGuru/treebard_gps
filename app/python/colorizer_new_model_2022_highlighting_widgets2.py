# colorizer_new_model_2022_highlighting_widgets2

# version 2: the last version successfully used instance variables but this one will use class variables. The goal is to change the colors and fonts in every instance of a class with one command, and to persist the changes in the db so the app opens up with the colors it was last given. 

# The old colorizer has extra work to do for widgets that highlight when you point at them (etc) ie special event widgets, widgets that respond to events by changing color or font. Nothing else in Treebard is user-customizable but this feature is important. Having added a co-highlighting feature to the events and families tables, there are now many widgets each independently running a make_formats_dict() function whenever the user changes colors. And when the app loads so it now loads much slower. As usual, having just made the autofill widget respond to events, it doesn't work yet when you change color schemes. It still uses the old color scheme. I've had this problem every time I create a new widget that highlights and it's time to refactor this functionality from scratch now that it's slowing the loading of the app way down. I will be starting from scratch on the whole colorizing scheme since I was brand new to coding when I wrote the first, second and third version, and now that I have 4 years of experience I have hopes that I will write a better functionality if I start from scratch, than I would if I were building on the old rickety model. The colorizer itself (colorizer.py) is newly refactored and as far as I know the database system is fine, but the methodology for actually getting every widget in the app to instantly change color schemes, even if it's a widget that responds to events, has to be redone.

import tkinter as tk
import sqlite3
from widgets import Label, Button
from styles import make_formats_dict
from families import EntryAutoPerson
from autofill import EntryAuto
from files import get_current_file
import dev_tools as dt
from dev_tools import looky, seeline







bg_fg = ("LabelFrame",)
bg_fg_activeBgHilite_activeFg_selectColorBg = ("Checkbutton", )
bg_fg_activeBgHilite_activeFg_selectColorHilite = ("Radiobutton", )
bg_fg_fontBoilerplate_activeBgHead = ("ButtonQuiet", )
bg_fg_fontH2 = ("LabelH2", )
bg_fg_fontH3 = ("LabelH3", )
bg_fg_fontIn = ("LabelEntry", "LabelButtonText", "LabelButtonText", )
bg_fg_fontIn_activeBgHead = ("ButtonPlain", )
bg_fg_fontOut = ("Label", "MessageCopiable", )
bg_fg_fontOut_activeBgHead_activeFg = ("Button",)
bg_fg_fontOut_activeBgHead_troughColorHilite = ("Scale",)
bg_fg_fontOut_activeBgHilite_activeFg_selectColorHilite = ("RadiobuttonBig", )
bg_fg_fontStatus = ("LabelStatusbar",)
bg_fg_fontSize_selectBgHead_selectFg_insertBgFg = ("X", "EntryAutoPerson", "EntryAuto", )
bg_fgHilite = ("ButtonBigPic", )
bgFg_fgBg_fontOut = ("LabelNegative",)
bgHead = ("FrameHilited2", "DropdownMenu", )
bgHead_fg_fontStatus = ("LabelTip2",)
bgHilite = (
    "FrameHilited", "FrameHilited3", "FrameHilited4", 
    "ToplevelHilited", "CanvasHilited", "TitleBarButtonSolidBG", )
bgHilite_fg_activeBgFg_activeFgBg = ("ButtonFlatHilited",)
bgHilite_fg_fontH3 = ("LabelHeader",)
bgHilite_fg_fontIn = ("LabelHilited3",)
bgHilite_fg_fontOut = ("LabelHilited", "LabelMovable", )
bgHilite_fg_selectBgHead_selectFg_insertBgFg = (
    "Entry", "Text", "EntryAutoHilited", )
bgOnly = (
    "Frame", "Canvas", "Toplevel", "FrameHilited6", "Border", "NotesDialog", 
    "Dialogue", "TabBook", "PersonSearch", "RolesDialog", "EditRow",
    "InputMessage", "Gallery", )

def get_all_descends (ancestor, deep_list):
    ''' 
        So all widgets can be configured at once, this lists every widget in 
        the app by running recursively.
    '''

    lst = ancestor.winfo_children()        
    for item in lst:
        deep_list.append(item)
        get_all_descends(item, deep_list)
    return deep_list

def configall(master):
    def config_bg_fg(widg):
        pass

    def config_bg_fg_activeBgHilite_activeFg_selectColorBg(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], 
            activebackground=formats["highlight_bg"],
            activeforeground=formats["fg"], selectcolor=formats["bg"])




    def config_bg_fg_fontOut(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], 
            font=(formats["output_font"], formats["font_size"]))
    def config_bg_fg_fontOut_activeBgHead_activeFg(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=(formats["output_font"], formats["font_size"]),
            activebackground=formats["head_bg"],
            activeforeground=formats["fg"])



    def config_bg_fg_fontSize_selectBgHead_selectFg_insertBgFg(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=(formats["input_font"], formats["font_size"]),
            selectbackground=formats["head_bg"],
            selectforeground=formats["fg"],
            insertbackground=formats["fg"])



    def config_bgOnly(widg):
        widg.config(bg=formats["bg"])


    formats = make_formats_dict()
    for klass in (X, Label, Button, EntryAuto, EntryAutoPerson):
        klass.formats = formats # the key to everything
    ancestor_list = []
    all_widgets_in_root = get_all_descends(master, ancestor_list)
    for widg in (all_widgets_in_root):
        subclass = widg.winfo_subclass()

        if subclass in bg_fg:
            config_bg_fg(widg)            
        elif subclass in bg_fg_activeBgHilite_activeFg_selectColorBg:
            config_bg_fg_activeBgHilite_activeFg_selectColorBg(widg)

# bg_fg_activeBgHilite_activeFg_selectColorHilite
# bg_fg_fontBoilerplate_activeBgHead
# bg_fg_fontH2
# bg_fg_fontH3
# bg_fg_fontIn
# bg_fg_fontIn_activeBgHead
        elif subclass in bg_fg_fontOut:
            config_bg_fg_fontOut(widg)
        elif subclass in bg_fg_fontOut_activeBgHead_activeFg:
            config_bg_fg_fontOut_activeBgHead_activeFg(widg)
# bg_fg_fontOut_activeBgHead_troughColorHilite
# bg_fg_fontOut_activeBgHilite_activeFg_selectColorHilite
# bg_fg_fontStatus
        elif subclass in bg_fg_fontSize_selectBgHead_selectFg_insertBgFg:
            config_bg_fg_fontSize_selectBgHead_selectFg_insertBgFg(widg)
            if subclass == "X":
                X.bg_hilite = formats["highlight_bg"]
                X.bg = formats["bg"]
# bg_fgHilite
# bgFg_fgBg_fontOut
# bgHead
# bgHead_fg_fontStatus
# bgHilite
# bgHilite_fg_fontH3
# bgHilite_fg_fontIn
# bgHilite_fg_fontOut
# bgHilite_fg_selectBgHead_selectFg_insertBgFg
# bgOnly

        elif subclass in bgOnly:
            config_bgOnly(widg)
    root.config(bg=formats["bg"])

def get_default_formats():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(
        '''
            SELECT default_bg, default_highlight_bg, default_head_bg, default_fg, default_output_font, default_font_size, default_input_font
            FROM format 
            WHERE format_id = 1
        ''')
    default_scheme = cur.fetchone()
    cur.close()
    conn.close()
    formats = {}
    (
        formats["bg"], formats["highlight_bg"], formats["head_bg"], 
        formats["fg"], formats["output_font"], formats["font_size"],
        formats["input_font"]) = default_scheme
    return formats


formats = get_default_formats()

class X(EntryAutoPerson):
    formats = formats
    bg_hilite = formats["highlight_bg"]
    bg = formats["bg"]
    def __init__(self, master, *args, **kwargs):
        EntryAutoPerson.__init__(self, master, *args, **kwargs)

        # self.bg_hilite = X.formats["highlight_bg"]
        # self.bg = X.formats["bg"]

        self.config(bg=X.formats["bg"], fg=X.formats["fg"], 
            insertbackground=X.formats["fg"], selectbackground=X.formats["head_bg"], 
            font=(X.formats["input_font"], X.formats["font_size"]))            
        self.bind("<Enter>", self.highlight)
        self.bind("<Leave>", self.unhighlight)

    def highlight(self, evt):
        self.config(bg=X.bg_hilite)

    def unhighlight(self, evt):
        self.config(bg=X.bg)

def make_formats_dict():

    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(
        '''
            SELECT bg, highlight_bg, head_bg, fg, output_font, font_size, input_font
            FROM format 
            WHERE format_id = 1
        ''')
    scheme = cur.fetchone()
    cur.close()
    conn.close()
    formats = {}
    (
        formats["bg"], formats["highlight_bg"], formats["head_bg"], 
        formats["fg"], formats["output_font"], formats["font_size"],
        formats["input_font"]) = scheme
    return formats

def recolorize():
    new_bg = ent_bg.get()
    new_highlight_bg = ent_highlight_bg.get()
    new_head_bg = ent_head_bg.get()
    new_fg = ent_fg.get()
    new_font = ent_font.get()
    new_font_size = ent_font_size.get()
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    cur.execute(
        '''
            UPDATE format 
            SET (bg, highlight_bg, head_bg, fg, output_font, font_size) = 
                (?, ?, ?, ?, ?, ?)
            WHERE format_id = 1
        ''',
        (new_bg, new_highlight_bg, new_head_bg, new_fg, new_font, new_font_size))
    conn.commit()
    cur.close()
    conn.close()
    X.formats = make_formats_dict() 

    configall(root)

if __name__ == "__main__":

    root = tk.Tk()

    l1 = Label(root, text="select bg")
    l2 = Label(root, text="select highlight bg")
    l3 = Label(root, text="select head bg")
    l4 = Label(root, text="select fg")
    l5 = Label(root, text="select font")
    l6 = Label(root, text="select font size")

    ent_bg = EntryAuto(root)

    ent_highlight_bg = EntryAuto(root)

    ent_head_bg = EntryAuto(root)

    ent_fg = EntryAuto(root)

    ent_font = EntryAuto(root)

    ent_font_size = EntryAuto(root)

    ent2 = X(root, width=60)
    ent2.insert(0, "It's important to not be blinded by your computer screen.")

    ent3 = X(root, width=60)
    ent3.insert(0, "It's convenient to be able to read the words on the screen.")

    button = Button(
        root, text="RECOLORIZE", command=recolorize)


    l1.grid(column=0, row=0, pady=6)
    l2.grid(column=0, row=1, pady=6)
    l3.grid(column=0, row=2, pady=6)
    l4.grid(column=0, row=3, pady=6)
    l5.grid(column=0, row=4, pady=6)
    l6.grid(column=0, row=5, pady=6)
    ent_bg.grid(column=1, row=0, pady=6)
    ent_highlight_bg.grid(column=1, row=1, pady=6)
    ent_head_bg.grid(column=1, row=2, pady=6)
    ent_fg.grid(column=1, row=3, pady=6)
    ent_font.grid(column=1, row=4, pady=6)
    ent_font_size.grid(column=1, row=5, pady=6)
    ent2.grid(pady=6, columnspan=2)
    ent3.grid(pady=6, columnspan=2)
    button.grid(pady=6)

    root.config(bg=X.formats["bg"])
    configall(root)
    root.mainloop()

# DO LIST

# add fontIn to any tuple name and func name that uses input font and add FontOut to any tuple name and func name that uses output font, and in the function use font_size also
# add to this test module all the special event widgets, 2 of each




