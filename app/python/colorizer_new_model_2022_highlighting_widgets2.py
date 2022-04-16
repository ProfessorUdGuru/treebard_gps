# colorizer_new_model_2022_highlighting_widgets2

# version 2: the last version successfully used instance variables but this one will use class variables. The goal is to change the colors and fonts in every instance of a class with one command, and to persist the changes in the db so the app opens up with the colors it was last given. 

# The old colorizer has extra work to do for widgets that highlight when you point at them (etc) ie special event widgets, widgets that respond to events by changing color or font. Nothing else in Treebard is user-customizable but this feature is important. Having added a co-highlighting feature to the events and families tables, there are now many widgets each independently running a make_formats_dict() function whenever the user changes colors. And when the app loads so it now loads much slower. As usual, having just made the autofill widget respond to events, it doesn't work yet when you change color schemes. It still uses the old color scheme. I've had this problem every time I create a new widget that highlights and it's time to refactor this functionality from scratch now that it's slowing the loading of the app way down. I will be starting from scratch on the whole colorizing scheme since I was brand new to coding when I wrote the first, second and third version, and now that I have 4 years of experience I have hopes that I will write a better functionality if I start from scratch, than I would if I were building on the old rickety model. The colorizer itself (colorizer.py) is newly refactored and as far as I know the database system is fine, but the methodology for actually getting every widget in the app to instantly change color schemes, even if it's a widget that responds to events, has to be redone.

import tkinter as tk
import sqlite3
from widgets import (
    Label, Button, LabelHilited3, LabelButtonText, LabelMovable, LabelStay,
    ButtonBigPic, Entry, Frame, LabelHilited)
# from styles import make_formats_dict
from window_border import Border    
from persons import EntryAutoPerson
from autofill import EntryAuto
from custom_combobox_widget import Combobox
from custom_tabbed_widget import LabelTab
from toykinter_widgets import Separator
from scrolling import Scrollbar, resize_scrolled_content   
from files import get_current_file
from query_strings import (
    select_color_scheme_current_id, select_color_scheme_by_id, select_format_font_scheme)
import dev_tools as dt
from dev_tools import looky, seeline






NEUTRAL_COLOR = '#878787'
ALL_WIDGET_CLASSES = (
    Label, Button, LabelHilited3, LabelButtonText, LabelMovable, LabelStay,
    ButtonBigPic, Entry, Frame, EntryAuto, EntryAutoPerson, Border, Combobox, 
    Separator, LabelTab, Combobox, LabelHilited, Scrollbar)
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
bg_fg_selectBgHead_selectFg_insertBgFg = ("EntryAutoPerson", "EntryAuto", )
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
bgHilite_fg_fontIn_selectBgHead_selectFg_insertBgFg = (
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

def get_opening_settings():
           
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_color_scheme_current_id)
    color_scheme_id = cur.fetchone()
    if color_scheme_id is None:
        cur.execute(select_opening_settings)
        user_formats = cur.fetchone()
    else:
        user_formats = get_current_formats(color_scheme_id[0])
    cur.close()
    conn.close()
    return user_formats
  
def make_formats_dict():
    """ To add a style, add a string to the end of keys list
        and a line below values.append...
    """
    prefs_to_use = list(get_opening_settings())
    prefs_to_use.insert(5, 'dejavu sans mono')
    keys = [
        # background, foreground
        'bg', 'highlight_bg', 'head_bg', 'fg', 
        # standard fonts
        'output_font', 'input_font',
        # heading fonts
        'heading1', 'heading2', 'heading3', 'heading4', 
        # other fonts
        'status', 'boilerplate', 'show_font', 'titlebar_0',
        'titlebar_1', 'titlebar_2', 'titlebar_3',
        'titlebar_hilited_0', 'titlebar_hilited_1', 
        'titlebar_hilited_2', 'titlebar_hilited_3',
        'unshow_font', 'tab_font']
    values = []

    values.append(prefs_to_use[0])
    values.append(prefs_to_use[1])
    values.append(prefs_to_use[2])
    values.append(prefs_to_use[3])
    values.append((prefs_to_use[4], prefs_to_use[6]))
    values.append((prefs_to_use[5], prefs_to_use[6]))
    values.append((prefs_to_use[4], prefs_to_use[6] * 2, 'bold'))
    values.append((prefs_to_use[4], int(prefs_to_use[6] * 1.5), 'bold'))
    values.append((prefs_to_use[4], int(prefs_to_use[6] * 1.125), 'bold'))
    values.append((prefs_to_use[4], int(prefs_to_use[6] * 0.75), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 0.83)))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 0.66)))
    values.append((prefs_to_use[5], prefs_to_use[6], 'italic'))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 0.66), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 0.75), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 1.00), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 1.25), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 0.66)))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 0.75)))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 1.00)))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * 1.25)))
    values.append((prefs_to_use[5], int(prefs_to_use[6] * .75), 'italic'))
    values.append((prefs_to_use[4], int(prefs_to_use[6] * 0.75)))

    formats = dict(zip(keys, values))
    return formats

def configall(master, formats):
    def config_bg_fg(widg):
        widg.config(bg=formats["bg"], fg=formats["fg"])
    def config_bg_fg_activeBgHilite_activeFg_selectColorBg(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], 
            activebackground=formats["highlight_bg"],
            activeforeground=formats["fg"], selectcolor=formats["bg"])
    def config_bg_fg_activeBgHilite_activeFg_selectColorHilite(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], 
            activebackground=formats["highlight_bg"],
            activeforeground=formats["fg"], selectcolor=formats["highlight_bg"])
    def config_bg_fg_fontBoilerplate_activeBgHead(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=formats["boilerplate"], activebackground=formats["head_bg"])
    def config_bg_fg_fontH2(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], font=formats["heading2"])
    def config_bg_fg_fontH3(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], font=formats["heading3"])
    def config_bg_fg_fontIn(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], font=formats["input_font"])
    def config_bg_fg_fontIn_activeBgHead(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], font=formats["input_font"],
            activebackground=formats["head_bg"])
    def config_bg_fg_fontOut(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], 
            font=formats["output_font"])
    def config_bg_fg_fontOut_activeBgHead_activeFg(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=formats["output_font"],
            activebackground=formats["head_bg"],
            activeforeground=formats["fg"])
    def config_bg_fg_fontOut_activeBgHead_troughColorHilite(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=formats["output_font"],
            activebackground=formats["head_bg"],
            troughcolor=formats["highlight_bg"])
    def config_bg_fg_fontOut_activeBgHilite_activeFg_selectColorHilite(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=formats["output_font"],
            activebackground=formats["highlight_bg"],
            activeforeground=formats["fg"],
            selectcolor=formats["highlight_bg"])
    def config_bg_fg_fontStatus(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], font=formats["status"])
    def config_bg_fg_selectBgHead_selectFg_insertBgFg(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"],
            font=formats["input_font"],
            selectbackground=formats["head_bg"],
            selectforeground=formats["fg"],
            insertbackground=formats["fg"])
    def config_bg_fgHilite(widg):
        widg.config(bg=formats["bg"], fg=formats["highlight_bg"])
    def config_bgFg_fgBg_fontOut(widg):
        widg.config(
            bg=formats["fg"], fg=formats["bg"], font=formats["output_font"])
    def config_bgHead(widg):
        widg.config(bg=formats["head_bg"])
    def config_bgHead_fg_fontStatus(widg):
        widg.config(
            bg=formats["head_bg"], fg=formats["fg"],
            font=formats["status"])
    def config_bgHilite(widg):
        widg.config(bg=formats["highlight_bg"])
    def config_bgHilite_fg_activeBgFg_activeFgBg(widg):
        widg.config(
            bg=formats["highlight_bg"], fg=formats["fg"],
            activebackground=formats["fg"],
            activeforeground=formats["bg"])
    def config_bgHilite_fg_fontH3(widg):
        widg.config(
            bg=formats["highlight_bg"], fg=formats["fg"],
            font=formats["heading3"])
    def config_bgHilite_fg_fontIn(widg):
        widg.config(
            bg=formats["highlight_bg"], fg=formats["fg"],
            font=formats["input_font"])
    def config_bgHilite_fg_fontOut(widg):
        widg.config(
            bg=formats["highlight_bg"], fg=formats["fg"],
            font=formats["output_font"])            
    def config_bgHilite_fg_fontIn_selectBgHead_selectFg_insertBgFg(widg):
        widg.config(
            bg=formats["highlight_bg"], fg=formats["fg"],
            font=formats["input_font"], selectbackground=formats["head_bg"],
            selectforeground=formats["fg"], insertbackground=formats["fg"])
    def config_bgOnly(widg):
        widg.config(bg=formats["bg"])

    for klass in ALL_WIDGET_CLASSES:
        klass.formats = formats # the key to everything
    ancestor_list = []
    all_widgets_in_root = get_all_descends(master, ancestor_list)
    for widg in (all_widgets_in_root):
        subclass = widg.winfo_subclass()

        if subclass in bg_fg:
            config_bg_fg(widg)            
        elif subclass in bg_fg_activeBgHilite_activeFg_selectColorBg:
            config_bg_fg_activeBgHilite_activeFg_selectColorBg(widg)
        elif subclass in bg_fg_activeBgHilite_activeFg_selectColorHilite:
            config_config_bg_fg_activeBgHilite_activeFg_selectColorHilite(widg)
        elif subclass in bg_fg_fontBoilerplate_activeBgHead:
            config_bg_fg_fontBoilerplate_activeBgHead(widg)
        elif subclass in bg_fg_fontH2:
            config_bg_fg_fontH2(widg)
        elif subclass in bg_fg_fontH3:
            config_bg_fg_fontH3(widg)
        elif subclass in bg_fg_fontIn:
            config_bg_fg_fontIn(widg)
        elif subclass in bg_fg_fontIn_activeBgHead:
            config_bg_fg_fontIn_activeBgHead(widg)
        elif subclass in bg_fg_fontOut:
            config_bg_fg_fontOut(widg)
        elif subclass in bg_fg_fontOut_activeBgHead_activeFg:
            config_bg_fg_fontOut_activeBgHead_activeFg(widg)
        elif subclass in bg_fg_fontOut_activeBgHead_troughColorHilite:
            config_bg_fg_fontOut_activeBgHead_troughColorHilite(widg)
        elif subclass in bg_fg_fontOut_activeBgHilite_activeFg_selectColorHilite:
            config_bg_fg_fontOut_activeBgHilite_activeFg_selectColorHilite(widg)
        elif subclass in bg_fg_fontStatus:
            config_bg_fg_fontStatus(widg)
        elif subclass in bg_fg_selectBgHead_selectFg_insertBgFg:
            config_bg_fg_selectBgHead_selectFg_insertBgFg(widg)
            if subclass == "EntryAutoPerson":
                EntryAutoPerson.highlight_bg = formats["highlight_bg"]
                EntryAutoPerson.bg = formats["bg"]
        elif subclass in bg_fgHilite:
            config_bg_fgHilite(widg)
        elif subclass in bgFg_fgBg_fontOut:
            config_bgFg_fgBg_fontOut(widg)
        elif subclass in bgHead_fg_fontStatus:
            config_bgHead_fg_fontStatus(widg)
        elif subclass in bgHilite:
            config_bgHilite(widg)
        elif subclass in bgHilite_fg_activeBgFg_activeFgBg:
            config_bgHilite_fg_activeBgFg_activeFgBg(widg)
        elif subclass in bgHilite_fg_fontH3:
            config_bgHilite_fg_fontH3(widg)
        elif subclass in bgHilite_fg_fontIn:
            config_bgHilite_fg_fontIn(widg)
        elif subclass in bgHilite_fg_fontOut:
            config_bgHilite_fg_fontOut(widg)
            if subclass == LabelHilited:
                LabelHilited.highlight_bg = formats["highlight_bg"]
                LabelHilited.bg = formats["bg"]
            elif subclass == LabelHilited:
                LabelMovable.highlight_bg = formats["highlight_bg"]
                LabelMovable.head_bg = formats["head_bg"]
        elif subclass in bgHilite_fg_fontIn_selectBgHead_selectFg_insertBgFg:
            config_bgHilite_fg_fontIn_selectBgHead_selectFg_insertBgFg(widg)
        elif subclass in bgOnly:
            config_bgOnly(widg)

        elif widg.winfo_class() == 'Frame':
            if widg.winfo_subclass() == 'Combobox':
                widg.colorize()

    root.config(bg=formats["bg"])

formats = make_formats_dict

def recolorize():
    new_scheme = int(ent_colors.get())
    new_font = ent_font.get()
    new_font_size = ent_font_size.get()
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    cur.execute(
        '''
            UPDATE format 
            SET (output_font, font_size) = 
                (?, ?)
            WHERE format_id = 1
        ''',
        (new_font, new_font_size))
    conn.commit()
    cur.execute(
        '''
            UPDATE current
            SET color_scheme_id = ?
            WHERE current_id = 1
        ''',
        (new_scheme,))
    conn.commit()
    cur.close()
    conn.close()
    formats = make_formats_dict()
    for klass in ALL_WIDGET_CLASSES:
        klass.formats = formats 

    configall(root, formats)
    resize_scrolled_content(root, canvas, window)

# get rid of this when working on types branch
def get_current_formats(color_scheme_id):   
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_color_scheme_by_id, (color_scheme_id,))
    color_scheme = list(cur.fetchone())
    cur.execute(select_format_font_scheme)
    font_scheme = list(cur.fetchone()[0:2])
    user_formats = color_scheme + font_scheme
    cur.close()
    conn.close()
    return user_formats

if __name__ == "__main__":

    formats = make_formats_dict()
    def make_scrollbars():

        vsb = Scrollbar(
            root, 
            hideable=True, 
            command=canvas.yview,
            width=20)
        hsb = Scrollbar(
            root, 
            hideable=True, 
            width=20, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=hsb.set, 
            yscrollcommand=vsb.set)
        vsb.grid(column=2, row=4, sticky='ns')
        hsb.grid(column=1, row=5, sticky='ew')

    def make_widgets():

        make_scrollbars()

        scridth = 20
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)

    root = tk.Tk()

    canvas = Border(root, root, formats)
    window = Frame(canvas)
    canvas.create_window(0, 0, anchor='nw', window=window)
    make_widgets()

    l1 = Label(window, text="enter color scheme ID")

    sep0 = Separator(window)
    ent_colors = Entry(window)
    l5 = Label(window, text="enter font")
    l6 = Label(window, text="enter font size")

    ent_font = EntryAuto(window)
    ent_font_size = EntryAuto(window)

    sep1 = Separator(window, height=5)

    ent2 = EntryAutoPerson(window, width=60)
    ent2.insert(0, "It's important to not be blinded by your computer screen.")

    ent3 = EntryAutoPerson(window, width=60)
    ent3.insert(0, "It's convenient to be able to read the words on the screen.")

    lh3_1 = LabelHilited3(window, text="These two labels are used in dropdown menu...")
    lh3_2 = LabelHilited3(window, text="...so they have to respond to events.")
    combo1 = Combobox(window, root)
    combo2 = Combobox(window, root)
    lt1 = LabelTab(window, text="Used for notebook tabs")
    lt2 = LabelTab(window, text="Used for notebook tabs")
    fm = Frame(window)
    mv1 = LabelMovable(fm, text="movable1")
    mv2 = LabelMovable(fm, text="movable2")
    mv3 = LabelMovable(fm, text="movable3")
    mv4 = LabelMovable(fm, text="movable4")
    mv5 = LabelMovable(fm, text="movable5")
    bp1 = ButtonBigPic(window, text="should have a picture in it")
    bp2 = ButtonBigPic(window, text="should have a picture in it")
    lbt1 = LabelButtonText(window, text="button made from label", width=24)
    lbt2 = LabelButtonText(window, text="button made from label", width=24)
    stay = LabelStay(window, bg="hotpink", text="this should never change color")

    button = Button(window, text="RECOLORIZE", command=recolorize)

    l1.grid(column=0, row=0, pady=6)
    ent_colors.grid(column=1, row=0, pady=6)
    sep0.grid(column=0, row=1, pady=6, columnspan=2, sticky="ew")
    l5.grid(column=0, row=2, pady=6)
    l6.grid(column=0, row=3, pady=6)
    ent_font.grid(column=1, row=2, pady=6)
    ent_font_size.grid(column=1, row=3, pady=6)
    sep1.grid(pady=6, columnspan=2, sticky="ew")
    ent2.grid(pady=6, columnspan=2)
    ent3.grid(pady=6, columnspan=2)
    lh3_1.grid(pady=6)
    lh3_2.grid(pady=6)
    combo1.grid(pady=6)
    combo2.grid(pady=6)
    lt1.grid(pady=6)
    lt2.grid(pady=6)
    fm.grid(pady=6)
    mv1.grid(column=0, row=0, padx=3)
    mv2.grid(column=1, row=0, padx=3)
    mv3.grid(column=2, row=0, padx=3)
    mv4.grid(column=3, row=0, padx=3)
    mv5.grid(column=4, row=0, padx=3)
    bp1.grid(pady=6)
    bp2.grid(pady=6)
    lbt1.grid(pady=6)
    lbt2.grid(pady=6)
    stay.grid(pady=6)   

    button.grid(pady=6)

    configall(root, formats)
    resize_scrolled_content(root, canvas, window)
    root.mainloop()

# DO LIST

# LabelButtonText and title bar don't change to new color till you click them
# combobox doesn't colorize, maybe because the LabelHilited arrow is inside the Combobox class
# same with LabelHilited3? didn't try yet but it's used inside the Dropdown class do prob has to be handled inside the class
# finish all config_ functions, then break big ones up so instead of one function with a long name and a lot of stuff in it, a widg with lots of options will run two or three small functions and the repetition as well as the number of functions will be cut way back
# go thru all modules and get rid of as many formats = make_formats_dict() runs as possible
# when everything works, rename this module styles.py and retest
# move query strings to other module




    # # ************* special event widgets ********************

    # def config_labelhilited(lab):
        # '''
            # When used for Combobox arrow, it has to respond to events.
        # '''
        # lab.formats = formats 
        # lab.config(
            # bg=formats['highlight_bg'],
            # fg=formats['fg'],
            # font=formats['output_font']) 

    # def config_labelhilited3(lab):
        # '''
            # When used for dropdown menu labels, it has to respond to events.
        # '''
        # lab.formats = formats 
        # lab.config(
            # bg=formats['highlight_bg'],
            # fg=formats['fg'],
            # font=formats['input_font'])

    # def config_labelbuttontext(lab):
        # lab.formats = formats
        # lab.config(
            # bg=formats['bg'],
            # fg=formats['fg'],
            # font=formats['input_font'])            

    # def config_labeltab(lab):
        # lab.formats = formats
        # if lab.chosen is False:
            # lab.config(
                # bg=formats['highlight_bg'],
                # fg=formats['fg'],
                # font=formats['tab_font'])
        # else:
            # lab.config(
                # bg=formats['bg'],
                # fg=formats['fg'],
                # font=formats['tab_font'])

    # def config_labelmovable(lab):
        # lab.formats = formats
        # lab.config(
            # bg=formats['highlight_bg'], 
            # fg=formats['fg'],
            # font=formats['output_font'])

    # def config_button_bigpic(widg):
        # widg.formats = formats
        # widg.config(bg=formats['bg'], fg=formats['highlight_bg'])

    # def config_border(widg):
        # widg.formats = formats
        # widg.config(bg=formats['head_bg'], fg=formats['fg'])
        # widg.colorize_border()

    # def config_entryauto(ent):
        # ent.formats = formats
        # ent.config(
            # bg=formats['bg'], fg=formats['fg'],
            # font=formats['input_font'], insertbackground=formats['fg'])

# for entryautoperson see class X

    # # *****************end of special event widgets******************

        # elif widg.winfo_class() == 'Frame':

            # if widg.winfo_subclass() == 'Combobox':
                # widg.colorize()


        # elif widg.winfo_class() == 'Canvas':

            # if widg.winfo_subclass() == 'Scrollbar':
                # # to figure out where all the scrollbars are:
                # # print("line", looky(seeline()).lineno, "widg:", widg)
                # widg.colorize()

            # elif widg.winfo_subclass() == 'Border':
                # config_border(widg)

    # def config_separator(sep):
        # ''' 
            # has 3 frames with 3 different colors
            # so needs its own reconfigure method 
        # '''
        # sep.colorize()




