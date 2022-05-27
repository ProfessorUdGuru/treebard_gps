# widgets.py

import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from tkinter import font
from files import (
    get_current_file, app_path, global_db_path, set_closing,
    handle_new_tree_event, handle_open_event, save_as, save_copy_as, 
    rename_tree, close_tree, exit_app, get_recent_files,
    new_file_path, change_tree_title, set_current_file, save_recent_tree)
from scrolling import resize_scrolled_content
from utes import center_dialog
from query_strings import ( 
    select_color_scheme_current_id, select_color_scheme_by_id,
    select_format_font_scheme, select_format_font_size, delete_links_links_name,
    select_current_person, select_name_with_id, select_all_names_ids,
    select_all_person_ids, select_image_id, select_max_person_id,    
    insert_images_elements, select_name_type_id, insert_name, 
    select_all_images, select_all_name_types, insert_person_new,
    select_person_gender, select_max_name_type_id, insert_name_type_new,
    insert_image_new, select_name_with_id_any, select_birth_names_ids,
    insert_finding_birth_new_person, update_format_font,
    select_current_person_id, delete_name_person, delete_findings_roles_person,
    select_name_id_by_person_id, delete_links_links_person,
    update_finding_person_1_null, update_finding_person_2_null,
    delete_finding_person, delete_claims_roles_person, delete_person,
    update_claims_persons_1_null, update_claims_persons_2_null,
    delete_images_elements_person, delete_claim_person, select_name_sorter,
    select_name_type_sorter_with_id, select_all_names, update_current_person,
    select_name_type_hierarchy, select_opening_settings,
    select_closing_state_recent_files, update_closing_state_recent_files) 
from messages_context_help import person_add_help_msg
from messages import persons_msg, opening_msg
from images import get_all_pics 
import dev_tools as dt
from dev_tools import looky, seeline 









# formerly in styles.py
# print('formats is', formats)
# formats is {'bg': '#34615f', 'highlight_bg': '#4a8a87', 'head_bg': '#486a8c', 'fg': '#b9ddd9', 'output_font': ('courier', 16), 'input_font': ('tahoma', 16), 'heading1': ('courier', 32, 'bold'), 'heading2': ('courier', 24, 'bold'), 'heading3': ('courier', 17, 'bold'), 'heading4': ('courier', 13, 'bold'), 'status': ('tahoma', 13), 'boilerplate': ('tahoma', 10), 'show_font': ('tahoma', 16, 'italic'), 'titlebar_0': ('tahoma', 10, 'bold'), 'titlebar_1': ('tahoma', 14, 'bold'), 'titlebar_2': ('tahoma', 16, 'bold'), 'titlebar_3': ('tahoma', 20, 'bold'), 'titlebar_hilited_0': ('tahoma', 10), 'titlebar_hilited_1': ('tahoma', 14), 'titlebar_hilited_2': ('tahoma', 16), 'titlebar_hilited_3': ('tahoma', 20), 'unshow_font': ('tahoma', 14, 'italic')}

INPUT_FONT = "dejavu sans mono"

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
    """ If the tree is brand new, get treebard's default color scheme. """
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_color_scheme_current_id)
    color_scheme_id = cur.fetchone()
    if color_scheme_id is None:
        cur.close()
        conn.close()
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute(select_opening_settings)
        default_formats = list(cur.fetchone())
        cur.close()
        conn.close()
        return default_formats
    else:
        cur.execute(select_color_scheme_by_id, color_scheme_id)
        color_scheme = list(cur.fetchone())
        cur.execute(select_format_font_scheme)
        font_scheme = list(cur.fetchone()[0:2])
        user_formats = color_scheme + font_scheme
        user_formats.insert(5, INPUT_FONT)
        # user_formats = color_scheme + [INPUT_FONT] + font_scheme
        cur.close()
        conn.close()
        return user_formats

# # get rid of this when working on types branch
# def get_current_formats(color_scheme_id):   
    # current_file = get_current_file()[0]
    # conn = sqlite3.connect(current_file)
    # cur = conn.cursor()
    # cur.execute(select_color_scheme_by_id, (color_scheme_id,))
    # color_scheme = list(cur.fetchone())
    # cur.execute(select_format_font_scheme)
    # font_scheme = list(cur.fetchone()[0:2])
    # user_formats = color_scheme + [INPUT_FONT] + font_scheme
    # cur.close()
    # conn.close()
    # return user_formats
  
def make_formats_dict():
    """ To add a style, add a string to the end of keys list
        and a line below values.append...
    """
    prefs_to_use = list(get_opening_settings())
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
formats = make_formats_dict()

def configall(master, formats):
    def config_activeBgHead(widg):
        widg.config(activebackground=formats["head_bg"])
    def config_activeBgHilite(widg):
        widg.config(activebackground=formats["highlight_bg"])
    def config_activeFg(widg):
        widg.config(activeforeground=formats["fg"])
    def config_bg_fg(widg):
        widg.config(bg=formats["bg"], fg=formats["fg"])
    def config_bgHead(widg):
        widg.config(bg=formats["head_bg"])
    def config_bgHilite(widg):
        widg.config(bg=formats["highlight_bg"])
    def config_bgOnly(widg):
        widg.config(bg=formats["bg"])
    def config_fg(widg):
        widg.config(fg=formats["fg"])
    def config_fontBoilerplate(widg):
        widg.config(font=formats["boilerplate"])
    def config_fontH2(widg):
        widg.config(font=formats["heading2"])
    def config_fontH3(widg):
        widg.config(font=formats["heading3"])
    def config_fontIn(widg):
        widg.config(font=formats["input_font"])
    def config_fontOut(widg):
        widg.config(font=formats["output_font"])
    def config_insertBgFg(widg):
        widg.config(insertbackground=formats["fg"])
    def config_selectBgHead(widg):
        widg.config(selectbackground=formats["head_bg"])
    def config_selectFg(widg):
        widg.config(selectforeground=formats["fg"])
    def config_selectColorBg(widg):
        widg.config(selectcolor=formats["bg"])
    def config_selectColorHilite(widg):
        widg.config(selectcolor=formats["highlight_bg"])
    def config_troughColorHilite(widg):
        widg.config(troughcolor=formats["highlight_bg"])
    def config_highlightcolorHead(widg):
        widg.config(highlightcolor=formats["head_bg"])
    def config_highlightbackground(widg):
        widg.config(highlightbackground=formats["bg"])

    def config_buttonflathilited(widg):
        widg.config(
            bg=formats["highlight_bg"], fg=formats["fg"],
            activebackground=formats["fg"],
            activeforeground=formats["bg"])

    def config_bg_fgHilite(widg):
        widg.config(bg=formats["bg"], fg=formats["highlight_bg"])

    def config_entryauto(widg):
        widg.config(
            bg=formats["bg"], 
            fg=formats["fg"],
            font=formats["input_font"],
            selectbackground=formats["head_bg"],
            selectforeground=formats["fg"],
            insertbackground=formats["fg"])

    def config_bg_fg_fontStatus(widg):
        widg.config(
            bg=formats["bg"], fg=formats["fg"], font=formats["status"])

    def config_separator(sep):
        """ Has 3 frames with 3 different colors
            so uses its own reconfigure method.
        """
        sep.colorize()

    def config_combobox(widg):
        widg.config(bg=formats["bg"]) 
        widg.entry.config(
            bg=formats["bg"], fg=formats["fg"],
            font=formats["input_font"],
            selectbackground=formats["head_bg"],
            selectforeground=formats["fg"],
            insertbackground=formats["fg"])            

    def config_scrollbar(widg):
        widg.config(bg=formats["head_bg"])
        widg.itemconfig(
            widg.thumb, fill=formats["bg"], outline=formats["highlight_bg"])
            
    def config_labelstatusbar(widg):
        widg.config(
            bg=formats["bg"],
            fg=formats["fg"],
            font=formats["status"])

    def config_labeltab(widg):
        if widg.chosen is False:
            widg.config(bg=formats["highlight_bg"])
        else:
            widg.config(bg=formats["bg"])
        widg.config(fg=formats["fg"], font=formats["tab_font"])

    def config_labelmovable(widg):
        widg.config( 
            bg=LabelMovable.highlight_bg, 
            fg=LabelMovable.fg, 
            font=LabelMovable.output_font)

    def config_labelbuttontext(widg):
        widg.config(
            bg=LabelButtonText.bg,
            fg=LabelButtonText.fg,
            font=LabelButtonText.input_font)

    def config_labeldots(widg):
        widg.config(
            bg=LabelDots.bg,
            fg=LabelDots.fg,
            font=LabelDots.heading3)

    def config_labelhilited3(widg):
        widg.config(
            bg=LabelHilited3.highlight_bg,
            fg=LabelHilited3.fg,
            font=LabelHilited3.input_font)

    def config_border(widg):
        widg.config(bg=Border.bg)

    root = None
    if master.winfo_name() in (".", "tk"):
        root = master
    
    for klass in ALL_WIDGET_CLASSES:
        klass.formats = formats
    ancestor_list = []
    all_widgets_in_root = get_all_descends(master, ancestor_list)
    for widg in (all_widgets_in_root):
        # if widg.winfo_class() != "Toplevel": # still using tk.Toplevel for tips 
            # subclass = widg.winfo_subclass()
        # else:
            # subclass = "Toplevel"
        subclass = widg.winfo_subclass()
        if subclass in bg_fg:
            config_bg_fg(widg)  
        if subclass in activeBgHilite:
            config_activeBgHilite(widg)
        if subclass in activeFg:
            config_activeFg(widg)
        if subclass in selectColorBg:
            config_selectColorBg(widg)
        if subclass in selectColorHilite:
            config_selectColorHilite(widg)
        if subclass in fontBoilerplate:
            config_fontBoilerplate(widg)
        if subclass in activeBgHead:
            config_activeBgHead(widg)
        if subclass in fontH2:
            config_fontH2(widg)
        if subclass in fontH3:
            config_fontH3(widg)
        if subclass in fontIn:
            config_fontIn(widg)
        if subclass in fG:
            config_fg(widg)
        if subclass in fontOut:
            config_fontOut(widg)
        if subclass in troughColorHilite:
            config_troughColorHilite(widg)
        if subclass in bgHead:
            config_bgHead(widg)
        if subclass in bgHilite:
            config_bgHilite(widg)
        if subclass in selectBgHead:
            config_selectBgHead(widg)
        if subclass in selectFg:
            config_selectFg(widg)
        if subclass in insertBgFg:
            config_insertBgFg(widg)
        if subclass in bgOnly:
            config_bgOnly(widg)
        if subclass in highlightcolorHead:
            config_highlightcolorHead(widg)
        if subclass in highlightbackground:
            config_highlightbackground(widg)

        elif subclass == "ButtonBigPic":
            config_bg_fgHilite(widg)
            ButtonBigPic.bg = formats["bg"]
            ButtonBigPic.fg = formats["highlight_bg"]

        elif subclass == "ButtonFlatHilited":
            config_buttonflathilited(widg)

        elif subclass in bg_fg and subclass in fontStatus:
            if subclass == "LabelStatusbar":
                LabelStatusbar.bg = formats["bg"]
                LabelStatusbar.fg = formats["fg"]
                LabelStatusbar.status = formats["status"]
            config_bg_fg_fontStatus(widg)

        elif subclass in ("EntryAutoPerson", "EntryAuto"):
            EntryAutoPerson.highlight_bg = formats["highlight_bg"]
            EntryAutoPerson.bg = formats["bg"]
            EntryAutoPerson.fg=formats["fg"]
            EntryAutoPerson.font=formats["input_font"]
            EntryAutoPerson.selectbackground=formats["head_bg"]
            EntryAutoPerson.selectforeground=formats["fg"]
            EntryAutoPerson.insertbackground=formats["fg"]
            config_entryauto(widg)

        elif subclass == "ComboArrow":
            ComboArrow.highlight_bg = formats["highlight_bg"]
            ComboArrow.fg = formats["fg"]
            ComboArrow.output_font = formats["output_font"] 
            ComboArrow.head_bg = formats["head_bg"]
        
        elif subclass == "DropdownMenu":
            DropdownMenu.bg = formats["bg"]
            DropdownMenu.highlight_bg = formats["highlight_bg"]
            DropdownMenu.head_bg = formats["head_bg"]

        elif subclass == "LabelHilited3":
            LabelHilited3.bg = formats["bg"]
            LabelHilited3.highlight_bg = formats["highlight_bg"]
            LabelHilited3.fg = formats["fg"]
            LabelHilited3.input_font = formats["input_font"]
            config_labelhilited3(widg)

        elif subclass == "Separator": 
            Separator.color1=formats['head_bg'], 
            Separator.color2=formats['highlight_bg'], 
            Separator.color3=formats['bg']           
            config_separator(widg)

        elif subclass == "Combobox":
            Combobox.highlight_bg = formats["highlight_bg"]
            Combobox.head_bg = formats["head_bg"]
            Combobox.bg = formats["bg"]
            config_combobox(widg)

        elif subclass == "Scrollbar":
            Scrollbar.slidercolor = formats["bg"]
            Scrollbar.troughcolor = formats["head_bg"]
            Scrollbar.bordercolor = formats["highlight_bg"]
            config_scrollbar(widg)

        elif subclass == "LabelTab":
            LabelTab.bg = formats["bg"]
            LabelTab.fg = formats["fg"]
            LabelTab.highlight_bg = formats["highlight_bg"]
            LabelTab.font = formats["tab_font"]
            config_labeltab(widg)

        elif subclass == "LabelMovable":
            LabelMovable.highlight_bg = formats["highlight_bg"]
            LabelMovable.head_bg = formats["head_bg"]
            LabelMovable.output_font = formats["output_font"]
            config_labelmovable(widg)

        elif subclass == "LabelButtonText":
            LabelButtonText.bg = formats["bg"]
            LabelButtonText.fg = formats["fg"]
            LabelButtonText.head_bg = formats["head_bg"]
            LabelButtonText.input_font = formats["input_font"]
            config_labelbuttontext(widg)

        elif subclass == "LabelDots":
            LabelDots.bg = formats["bg"]
            LabelDots.fg = formats["fg"]
            LabelDots.head_bg = formats["head_bg"]
            LabelDots.heading3 = formats["heading3"]
            config_labeldots(widg)

        elif subclass == "Border":
            Border.head_bg = formats["head_bg"]
            Border.fg = formats["fg"]
            Border.bg = formats["bg"]
            config_border(widg)

    if root:
        root.config(bg=formats["bg"])

# formerly in widgets.py

NEUTRAL_COLOR = '#878787'

class Framex(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' 
            Like built-in tkinter method
            w.winfo_class() except it gets subclass names.
        '''
        subclass = type(self).__name__
        return subclass

class FrameStay(Framex):
    ''' 
        Frame background color will not change when color scheme changes.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        pass

class Frame(Framex):
    ''' 
        Frame background color changes when color scheme changes. 
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'])

class FrameTest(Framex):
    ''' 
        Frame background color can be altered for testing/visibility. 
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg='orange')

class FrameTest2(Framex):
    ''' 
        Frame background color can be altered for testing/visibility. 
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg='green')

class FrameTitleBar(Framex):
    ''' 
        Frame hilited by border and a different background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=NEUTRAL_COLOR)


class FrameHilited(Framex):
    ''' 
        Frame hilited by groove border and background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'], bd=3, relief='groove')

class FrameHilited2(Framex):
    ''' 
        Frame hilited by border and a different background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['head_bg'])

class FrameHilited3(Framex):
    ''' 
        Frame hilited by different background color but not border.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'])

class FrameHilited4(Framex):
    ''' 
        Frame hilited by sunken border and background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'], bd=2, relief='sunken')

class FrameHilited6(Framex):
    ''' 
        Frame hilited by sunken border only.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.bd = 2
        self.config(bg=formats['bg'], bd=self.bd, relief='sunken')

class LabelFramex(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' 
            Like built-in tkinter method
            w.winfo_class() except it gets subclass names.
        '''
        subclass = type(self).__name__
        return subclass

class LabelFrame(LabelFramex):
        def __init__(self, master, *args, **kwargs):
            LabelFramex.__init__(self, master, *args, **kwargs)

            self.config(
                bg=formats['bg'], 
                fg=formats['fg'], 
                font=formats['output_font']) 
      
class Labelx(tk.Label):
    def __init__(self, master, *args, **kwargs):
        tk.Label.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        ''' a method that works like built-in tkinter method
            w.winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

class Label(Labelx):
    ''' 
        If this subclass is detected it will be reconfigured
        according to user preferences. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['bg'], 
            fg=formats['fg'],
            font=formats['output_font'])

class LabelSearch(Label): 
    """ Label for search results column cells. """

    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        self.config(anchor='w')

class LabelTest(Labelx):
    ''' 
        Color can be changed for testing/visibility. 
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg='purple', 
            fg=formats['fg'],
            font=formats['output_font'])
 
class LabelHeader(Labelx):
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['heading3'],
            bd=1,
            relief='raised')

class LabelHilited3(Labelx):
    ''' 
        Like Label with a different background and a monospaced sans-serif font. 
        Because it's monospaced, this font is ideal for places such as dropdown
        menus where a single label needs to have both flush left and flush right
        text with variable space in the middle keeping both strings flush. 
    '''
    formats = formats
    fg = formats["fg"]
    highlight_bg = formats["highlight_bg"]
    bg = formats["bg"]
    input_font = formats["input_font"]
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=LabelHilited3.highlight_bg, 
            fg=LabelHilited3.fg,
            font=LabelHilited3.input_font)

class LabelEntry(Labelx):
    ''' 
        Like Label but with input font. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'], 
            fg=formats['fg'],
            font=formats['input_font']
)

class LabelTip2(Labelx):
    ''' 
        Like Label with a different background. For tooltips. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['head_bg'], 
            fg=formats['fg'],
            font=formats['status'], bd=1, relief='solid') 

class LabelNegative(Labelx):
    ''' 
        Usual bg and fg reversed. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['fg'], 
            fg=formats['bg'],
            font=formats['output_font'])

class LabelH2(Labelx):
    ''' 
        For large subheadings. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['bg'], 
            fg=formats['fg'],
            font=formats['heading2'])

class LabelH3(Labelx):
    ''' 
        For small subheadings. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['bg'], 
            fg=formats['fg'],
            font=formats['heading3'])

class LabelButtonText(Labelx):
    """ A label that looks and works like a button. Displays text.
    """
    formats = formats
    bg = formats["bg"] 
    head_bg = formats["head_bg"]
    input_font = formats["input_font"]
    fg = formats["fg"]    
    def __init__(self, master, width=8, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            anchor='center',
            borderwidth=1, 
            relief='raised', 
            takefocus=1,
            bg=formats['bg'],
            width=width,
            font=formats['input_font'],
            fg=formats['fg'])

        self.bind('<FocusIn>', self.show_focus)
        self.bind('<FocusOut>', self.unshow_focus)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_unhover)

    def show_focus(self, evt):
        self.config(borderwidth=2)

    def unshow_focus(self, evt):
        self.config(borderwidth=1)

    def on_press(self, evt):
        self.config(relief='sunken', bg=LabelButtonText.head_bg)

    def on_release(self, evt):
        self.config(relief='raised', bg=LabelButtonText.bg)

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

class LabelDots(Labelx):
    """ Display clickable dots if there's more info, no dots if none. 
    """
    formats = formats
    bg = formats["bg"] 
    head_bg = formats["head_bg"]
    heading3 = formats["heading3"]
    fg = formats["fg"]
    def __init__(
            self, 
            master,
            dialog_class,
            treebard,
            person_autofill_values=None,
            *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.master = master
        self.dialog_class = dialog_class
        self.treebard = treebard
        self.person_autofill_values = person_autofill_values

        self.current_person = None        
        self.root = master.master

        self.finding_id = None
        self.header = []

        self.config(
            anchor='center',
            borderwidth=1, 
            relief='raised', 
            takefocus=1,
            bg=formats['bg'],
            width=5,
            font=formats['heading3'],
            fg=formats['fg'])

        self.bind('<Button-1>', self.open_dialog)
        self.bind('<Return>', self.open_dialog)
        self.bind('<space>', self.open_dialog)

        self.bind('<FocusIn>', self.show_focus)
        self.bind('<FocusOut>', self.unshow_focus)
        self.bind('<Button-1>', self.on_press, add="+")
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_unhover)

    def show_focus(self, evt):
        self.config(borderwidth=2)

    def unshow_focus(self, evt):
        self.config(borderwidth=1)

    def on_press(self, evt):
        self.config(relief='sunken', bg=LabelDots.head_bg)

    def on_release(self, evt):
        self.config(relief='raised', bg=LabelDots.bg)

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

    def open_dialog(self, evt):
        dlg = self.dialog_class(
            self.master, 
            self.finding_id, 
            self.header, 
            self.current_person,
            self.treebard,
            pressed=evt.widget,
            person_autofill_values=self.person_autofill_values)

class LabelTitleBar(Labelx):
    ''' 
        Like Label for fine print. Can be sized independently
        of other font sizes so users who want larger fonts 
        elsewhere can keep titles tiny if they want. Used for 
        window titlebar and menu strip since people are
        so used to Windows' tiny fonts on these widgets that some
        people will not want to see the font get bigger even if 
        they can't read it. 
    '''

    def __init__(self, master, size='tiny', *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=NEUTRAL_COLOR, fg=formats['fg'])
 
        if size == 'tiny':
            self.config(font=formats['titlebar_0'])
        elif size == 'small':
            self.config(font=formats['titlebar_1'])
        elif size == 'medium':
            self.config(font=formats['titlebar_2'])
        elif size == 'large':
            self.config(font=formats['titlebar_3'])

class LabelMenuBarTest(LabelTitleBar):
    '''
        Color can be changed for testing/visibility.
    '''

    def __init__(self, master, size='tiny',  *args, **kwargs):
        LabelTitleBar.__init__(self, master,**options)

        self.config(bg='blue')

        self.bind('<Enter>', self.enrise)
        self.bind('<Leave>', self.flatten)
        self.bind('<Button-1>', self.sink)

        if size == 'tiny':
            self.config(font=formats['titlebar_hilited_0'])
        elif size == 'small':
            self.config(font=formats['titlebar_hilited_1'])
        elif size == 'medium':
            self.config(font=formats['titlebar_hilited_2'])
        elif size == 'large':
            self.config(font=formats['titlebar_hilited_3'])

    def enrise(self, evt):
        evt.widget.config(relief='raised')

    def flatten(self, evt):
        evt.widget.config(relief='flat')

    def sink(self, evt):
        evt.widget.config(relief='sunken')
       
class LabelStay(Labelx):
    ''' 
        If this subclass is detected its background won't be reconfigured. 
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        pass

class LabelMovable(Labelx):
    ''' 
        A label that can be moved to a different grid position
        by trading places with another widget on press of an
        arrow key. The master can't contain anything but LabelMovables. 
        The ipadx, ipady, padx, pady, and sticky grid options can
        be used as long as they're the same for every LabelMovable in
        the master. With some more coding, columnspan and rowspan
        could be set too but as is the spans should be left at
        their default values which is 1.
    '''
    formats = formats
    output_font = formats["output_font"]
    highlight_bg = formats["highlight_bg"]
    fg = formats["fg"]
    def __init__(self, master, first_column=0, first_row=0, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.master = master
        self.first_column = first_column
        self.first_row = first_row
        self.config(
            takefocus=1, 
            bg=formats["highlight_bg"], 
            fg=formats["fg"], 
            font=formats["output_font"])
        self.bind('<FocusIn>', self.highlight_on_focus)
        self.bind('<FocusOut>', self.unhighlight_on_unfocus)
        self.bind('<Key>', self.locate)
        self.bind('<Key>', self.move)

    def locate(self, evt):
        ''' 
            Get the grid position of the two widgets that will
            trade places.
        '''

        self.mover = evt.widget

        mover_dict = self.mover.grid_info()
        self.old_col = mover_dict['column']
        self.old_row = mover_dict['row']
        self.ipadx = mover_dict['ipadx']
        self.ipady = mover_dict['ipady']
        self.pady = mover_dict['pady']
        self.padx = mover_dict['padx']
        self.sticky = mover_dict['sticky']        

        self.less_col = self.old_col - 1
        self.less_row = self.old_row - 1
        self.more_col = self.old_col + 1
        self.more_row = self.old_row + 1

        self.last_column = self.master.grid_size()[0] - 1
        self.last_row = self.master.grid_size()[1] - 1

    def move(self, evt):
        ''' 
            Determine which arrow key was pressed and make the trade. 
        '''

        def move_left():
            if self.old_col > self.first_column:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.less_col and 
                            child.grid_info()['row'] == self.old_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.less_col, row=self.old_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky)

        def move_right():
            if self.old_col < self.last_column:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.more_col and 
                            child.grid_info()['row'] == self.old_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.more_col, row=self.old_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky) 

        def move_up():
            if self.old_row > self.first_row:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.old_col and 
                            child.grid_info()['row'] == self.less_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.old_col, row=self.less_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky)

        def move_down():
            if self.old_row < self.last_row:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.old_col and 
                            child.grid_info()['row'] == self.more_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.old_col, row=self.more_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky)

        self.locate(evt)

        keysyms = {
            'Left' : move_left,
            'Right' : move_right,
            'Up' : move_up,
            'Down' : move_down}

        for k,v in keysyms.items():
            if evt.keysym == k:
                v()

        self.fix_tab_order()

    def fix_tab_order(self):
        new_order = []
        for child in self.master.winfo_children():
            new_order.append((
                child, 
                child.grid_info()['column'], 
                child.grid_info()['row']))
            new_order.sort(key=lambda i: (i[1], i[2])) 
        for tup in new_order:
            widg = tup[0]
            widg.lift()        

    def highlight_on_focus(self, evt):        
        evt.widget.config(bg=LabelMovable.head_bg)

    def unhighlight_on_unfocus(self, evt):        
        evt.widget.config(bg=LabelMovable.highlight_bg)

class Buttonx(tk.Button):
    def __init__(self, master, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' a method that works like built-in tkinter method
            w.winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

# BUTTONS should not use a medium background color because the highlightthickness
    # and highlightcolor options don't work and the button highlight focus might not
    # be visible since Tkinter or Windows is choosing the color of the focus highlight
    # and it can't be made thicker.
class Button(Buttonx):
    ''' Includes tk.Button in the colorizer scheme. '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            font=(formats['output_font']),
            overrelief=tk.GROOVE, 
            activebackground=formats['head_bg'],
            bg=formats['bg'],
            fg=formats['fg'])

class ButtonBigPic(Buttonx):
    ''' 
        Used for top_pic on person tab and tree decoration on opening_dialog.
    '''
    formats = formats
    bg = formats["bg"]
    fg = formats["highlight_bg"]
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            bd=0, 
            relief="flat",
            bg=formats['bg'],  
            fg=formats['highlight_bg'],
            cursor='hand2')
        self.bind('<FocusIn>', self.highlight)
        self.bind('<FocusOut>', self.unhighlight)

    def highlight(self, evt):
        self.config(bg=ButtonBigPic.fg)

    def unhighlight(self, evt):
        self.config(bg=ButtonBigPic.bg)

class ButtonFlatHilited(Buttonx):
    '''
        A button with no relief or border.
    '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['highlight_bg'],
            relief='flat',
            fg=formats['fg'],
            activebackground=formats['fg'], # bg color while pressed
            activeforeground=formats['bg'], # fg color while pressed
            overrelief='flat', # relief when hovered by mouse
            bd=0) # prevents sunken relief while pressed
        self.grid_configure(sticky='ew') 

        def highlight(self, evt):
            self.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'],
                activebackground=formats['fg'],
                activeforeground=formats['bg'])

class ButtonPlain(Buttonx):
    ''' Used for icon menu '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            font=(formats['input_font']),
            bd=0, 
            activebackground=formats['head_bg'],
            bg=formats['bg'],  
            fg=formats['fg'],
            cursor='hand2')
        self.bind('<FocusIn>', self.highlight)
        self.bind('<FocusOut>', self.unhighlight)

    def highlight(self, evt):
        self.config(bg=formats['head_bg'])

    def unhighlight(self, evt):
        self.config(bg=formats['bg'])

class ButtonQuiet(Buttonx):
    ''' Same color as background, no text. '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            text='',
            width=3,
            overrelief=tk.GROOVE, 
            activebackground=formats['head_bg'],
            bg=formats['bg'],  
            fg=formats['fg'],
            font=formats['boilerplate'])
    
class Entryx(tk.Entry):
    def __init__(self, master, *args, **kwargs):
        tk.Entry.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' a method that works like built-in tkinter method
            w.winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

class Entry(Entryx):
    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        
        self.config(
            bg=formats['highlight_bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'],
            selectforeground=formats["fg"],
            selectbackground=formats["head_bg"]) 
            

# class EntryUnhilited(Entryx):
    # '''
        # Looks like a Label.
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Entryx.__init__(self, master, *args, **kwargs)
        
        # self.config(
            # bd=0,
            # bg=formats['bg'], 
            # fg=formats['fg'], 
            # font=formats['input_font'], 
            # insertbackground=formats['fg'])

class Textx(tk.Text):
    def __init__(self, master, *args, **kwargs):
        tk.Text.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Text(Textx):
    def __init__(self, master, *args, **kwargs): 
        Textx.__init__(self, master, *args, **kwargs)

        self.config(
            wrap='word', 
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['input_font'],
            insertbackground=formats['fg'])

        self.bind("<Tab>", self.focus_next_window)
        self.bind("<Shift-Tab>", self.focus_prev_window)

    # make the Text widget use tab key for traversal like other widgets
    # I think return('break') prevents the built-in binding to Tab
    def focus_next_window(self, evt):
        evt.widget.tk_focusNext().focus()
        return('break')

    def focus_prev_window(self, evt):
        evt.widget.tk_focusPrev().focus()
        return('break')

class MessageCopiable(Textx):
    ''' 
        To use as a Label whose text can be selected 
        with mouse, set the state to disabled after 
        constructing the widget and giving it text. 
        Enable temporarily to change color or text, for example.
    '''

    def __init__(self, master, *args, **kwargs):
        Textx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'],
            fg=formats['fg'],
            borderwidth=0, 
            wrap='word',
            state='disabled',
            font=(formats['output_font']),  
            takefocus=0)
       
    def set_height(self):
        # answer is wrong first time thru mainloop so update:
        self.update_idletasks()
        lines = self.count('1.0', 'end', 'displaylines')
        self.config(height=lines)

        self.tag_configure('left', justify='left')
        self.tag_add('left', '1.0', 'end')
        self.config(state='disabled')
    # How to use:
    # www = MessageCopiable(root, width=32)
    # www.insert(1.0, 
        # 'Maecenas quis elit eleifend, lobortis turpis at, iaculis '
        # 'odio. Phasellus congue, urna sit amet posuere luctus, mauris '
        # 'risus tincidunt sapien, vulputate scelerisque ipsum libero at '
        # 'neque. Nunc accumsan pellentesque nulla, a ultricies ex '
        # 'convallis sit amet. Etiam ut sollicitudi felis, sit amet '
        # 'dictum lacus. Mauris sed mattis diam. Pellentesque eu malesuada '
        # 'ipsum, vitae sagittis nisl Morbi a mi vitae nunc varius '
        # 'ullamcorper in ut urna. Maecenas auctor ultrices orci. '
        # 'Donec facilisis a tortor pellentesque venenatis. Curabitur '
        # 'pulvinar bibendum sem, id eleifend lorem sodales nec. Mauris '
        # 'eget scelerisque libero. Lorem ipsum dolor sit amet, consectetur '
        # 'adipiscing elit. Integer vel tellus nec orci finibus ornare. '
        # 'Praesent pellentesque aliquet augue, nec feugiat augue posuere ')
    # www.grid()
    # www.set_height()
        
class Checkbuttonx(tk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        tk.Checkbutton.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Checkbutton(Checkbuttonx):
    def __init__(self, master, *args, **kwargs):
        Checkbuttonx.__init__(self, master, *args, **kwargs)
        ''' 
            To see selection set the selectcolor 
            option to either bg or highlight_bg.
        '''
        self.config(
            bg=formats['bg'],
            fg=formats['fg'], 
            activebackground=formats['highlight_bg'],
            selectcolor=formats['bg'], 
            padx=6, pady=6) 
       
class Radiobuttonx(tk.Radiobutton):
    def __init__(self, master, *args, **kwargs):
        tk.Radiobutton.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass 

class Radiobutton(Radiobuttonx):
    def __init__(self, master, *args, **kwargs):
        Radiobuttonx.__init__(self, master, *args, **kwargs)
        ''' 
            To see selection set the selectcolor 
            option to either bg or highlight_bg.
        '''
        self.config(
            bg=formats['bg'],
            fg=formats['fg'], 
            activebackground=formats['highlight_bg'],
            selectcolor=formats['highlight_bg'], 
            padx=6, pady=6) 

class RadiobuttonBig(Radiobutton):
    def __init__(self, master, *args, **kwargs):
        Radiobutton.__init__(self, master, *args, **kwargs)
        ''' 
            If the main content of a dialog is a set of radiobuttons,
            use standard text size.
        '''
        self.config(font=formats['output_font'])

class Toplevelx(tk.Toplevel):
    '''
        All my toplevels have to declare a master whether they need one or not.
        This keeps the code consistent and symmetrical across all widgets,
        even though Tkinter doesn't require a master for its Toplevel.
    '''

    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        subclass = type(self).__name__
        return subclass

class Toplevel(Toplevelx):
    def __init__(self, master, *args, **kwargs):
        Toplevelx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'])

class ToplevelHilited(Toplevelx):
    formats = formats
    highlight_bg = formats["highlight_bg"]
    bg = formats["bg"]
    def __init__(self, *args, **kwargs):
        Toplevelx.__init__(self, *args, **kwargs)
        self.config(bg=formats['highlight_bg'])

class Scalex(tk.Scale):
    def __init__(self, master, *args, **kwargs):
        tk.Scale.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Scale(Scalex):
    def __init__(self, master, *args, **kwargs):
        Scalex.__init__(self, master, *args, **kwargs)
        
        self.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['output_font'],
            troughcolor=formats['highlight_bg'],
            activebackground=formats['head_bg'],
            highlightthickness=1,
            highlightcolor=formats["head_bg"],
            highlightbackground=formats["bg"]) 

class Canvasx(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Canvas(Canvasx):
    def __init__(self, master, *args, **kwargs):
        Canvasx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'], bd=0, highlightthickness=0)

class CanvasHilited(Canvasx):
    def __init__(self, master, *args, **kwargs):
        Canvasx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['highlight_bg'], bd=0, highlightthickness=0)

# from window_border.py

def close(evt):
    dlg = evt.widget.winfo_toplevel()
    if dlg.winfo_name() == 'tk':
        set_closing()
        dlg.quit()
    else:
        dlg.grab_release()
        dlg.destroy()

class Border(Canvas):
    pool = []
    formats = formats
    head_bg = formats["head_bg"]
    fg = formats["fg"]
    def __init__(
            self, master, root, menubar=False, 
            ribbon_menu=False, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        '''
            This class replaces root and dialog borders with custom borders. 

            Since this custom "Toykinter" border is part of the app instead 
            of being controlled by Windows, its use allows clicks on the title 
            bar to be responded to with standard Tkinter configuration methods 
            and other Python code. 

            This class can't use Treebard as a master since Treebard is the 
            whole app and is only instantiated once, so this class has to use 
            its host toplevel as parent. Setting font size should change the 
            size of fonts, title bar, and max/min/quit buttons. The settings 
            are 3, 4, 7, or 11 pixels. The size shown is linked to changes in 
            font size (in progress--user still has to switch to person tab and
            redraw() to see change).

            The hard part to remember when using this is that the parts of the
            border including the canvas itself (`self` in the class) are gridded
            in this class. This causes confusion because I'm always trying to
            figure out where to grid the canvas and how to set columnconfigure()
            and rowconfigure() but it's already done here since it has to be
            the same wherever it's used. Also the dropdown menu and icon menu
            occupy rows 2 and 3 whether they're used or not, and they're only
            used in the root window.
        '''

        self.master = master # toplevel
        self.root = root
        self.menubar = menubar
        self.ribbon_menu = ribbon_menu

        self.set_title_bar_size()

        self.changing_values = None
        self.maxxed = False

        self.make_widgets()

        self.BORDER_PARTS = (
            self.title_bar, self.title_frame, self.logo, self.title_1, 
            self.title_1b, self.title_2, self.txt_frm, self.buttonbox, 
            self.border_top, self.border_left, self.border_right, 
            self.border_bottom)

        Border.pool.append(self)
        if self.master.winfo_name() != "tk":
            self.master.bind("<Destroy>", self.clean_pool)
        self.colorize_border()

    def clean_pool(self, evt):
        '''
            Delete destroyed toplevel from list and highlight the title bar
            of the toplevel that's uppermost in the window stacking order.
        '''
        widg = evt.widget
        if (widg.winfo_class() == "Canvas" and 
                widg.winfo_subclass() == "Border"):
            idx = Border.pool.index(widg)
            del Border.pool[idx]
        if len(Border.pool) != 0: # hack to use Dialogue class in misc test module
            Border.pool[0].colorize_border()

    def set_title_bar_size(self):
        sizes = { 
            3 : ['tiny', 20, 0.25], 
            4 : ['small', 25, 0.75], 
            7 : ['medium', 31, 0.25], 
            11 : ['large', 45, 1.0]}

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.execute(select_format_font_size)
        result = cur.fetchone()
        if result is None:
            font_size = (12, 12)
        else:
            font_size = result
        # font_size = cur.fetchone()
        cur.close()
        conn.close()
        if font_size[0] is None:
            font_size = font_size[1]
        else:
            font_size = font_size[0]
        if font_size < 11:
            self.size = 3
        elif font_size < 14:
            self.size = 4
        elif font_size < 20:
            self.size = 7
        elif font_size < 31:
            self.size = 11         

        for k,v in sizes.items():
            if self.size == k:
                self.icon_size = v[0]
                self.offset_x = v[1]
                self.rel_y = v[2]

    def make_widgets(self):

        self.border_top = FrameTitleBar(
            self.master, height=3, name='top')
        self.title_bar = FrameTitleBar(self.master)

        self.menu_frame = FrameHilited3(self.master)
        self.ribbon_frame = FrameHilited3(self.master)

        self.border_left = FrameTitleBar(self.master, width=3, name='left')
        self.border_right = FrameTitleBar(self.master, width=3, name='right')

        self.statusbar = StatusbarTooltips(self.master)

        self.border_bottom = FrameTitleBar(
            self.master, height=3, name='bottom')

        self.border_top.config(cursor='sb_v_double_arrow')
        self.border_left.config(cursor='sb_h_double_arrow')
        self.border_right.config(cursor='sb_h_double_arrow')
        self.border_bottom.config(cursor='sb_v_double_arrow')

        # children of toplevel i.e. self.master
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(4, weight=1)
        self.border_top.grid(column=0, row=0, columnspan=4, sticky='ew')
        self.title_bar.grid(column=1, row=1, columnspan=2, sticky='ew')
        if self.menubar is True:
            self.menu_frame.grid(column=1, row=2, columnspan=2, sticky='ew')
        if self.ribbon_menu is True:
            self.ribbon_frame.grid(column=1, row=3, columnspan=2, sticky='w')
        self.grid(column=1, row=4, sticky='news')
        self.border_left.grid(column=0, row=1, rowspan=6, sticky='ns')
        self.border_right.grid(column=3, row=1, rowspan=6, sticky='ns')
        self.statusbar.grid(column=1, row=6, columnspan=2, sticky='ew')
        self.border_bottom.grid(column=0, row=7, columnspan=4, sticky='ew')

        self.config(cursor='arrow')

        # children of self.title_bar
        self.title_bar.columnconfigure(0, weight=1)
        self.title_bar.columnconfigure(1, weight=0)
        self.title_frame = FrameTitleBar(self.title_bar)
        self.buttonbox = FrameTitleBar(self.title_bar)

        self.title_frame.pack(side='left')
        self.buttonbox.place(relx=1.0, x=-100, rely=0.125, y=-2)

        # children of self.title_frame
        self.logo = TitleBarButtonSolidBG(
            self.title_frame,
            icon='logo',
            icon_size=self.icon_size)

        self.txt_frm = FrameTitleBar(self.title_frame)
        self.logo.pack(side='left', pady=(0,3), padx=(0,12))
        self.txt_frm.pack(side='left')

        # children of text_frm
        self.title_1 = LabelTitleBar(
            self.txt_frm, 
            size=self.icon_size,
            text='Toykinter Demo')
        self.title_1b = FrameTitleBar(self.txt_frm, width=36)
        self.title_2 = LabelTitleBar(
            self.txt_frm,
            size=self.icon_size, 
            text='for all ages')

        self.title_1.grid(column=0, row=0)
        self.title_1b.grid(column=1, row=0, sticky='ew')
        self.title_2.grid(column=2, row=0)

        # children of self.buttonbox
        self.minn = TitleBarButton(
            self.buttonbox, icon='min', icon_size=self.icon_size)
        self.maxx = TitleBarButton(
            self.buttonbox, icon='max', icon_size=self.icon_size)
        self.restore = TitleBarButton(
            self.buttonbox, icon='restore', icon_size=self.icon_size)
        self.quitt = TitleBarButton(
            self.buttonbox, icon='quit', icon_size=self.icon_size)

        self.minn.grid(column=0, row=0, sticky='w')
        self.maxx.grid(
            column=1, row=0, sticky='w', padx=(0,3))
        self.restore.grid(
            column=1, row=0, sticky='w', padx=(0,3))
        self.restore.grid_remove()
        self.quitt.grid(
            column=2, row=0, sticky='e', 
            padx=(0, self.size))

        self.master.update_idletasks()
        to_the_left = self.buttonbox.winfo_reqwidth()
        self.buttonbox.place(relx=1.0, x=-to_the_left, rely=0.125, y=-2 * self.rel_y)

        self.master.bind('<Map>', self.hide_windows_titlebar)
        self.minn.bind('<Button-1>', self.minimize)
        self.maxx.bind('<Button-1>', self.toggle_max_restore)
        self.restore.bind('<Button-1>', self.toggle_max_restore)
        self.quitt.bind('<Button-1>', close)
        x = [i.bind(
            '<Map>', 
            self.recolorize_on_restore) for i in (self.minn, self.quitt)]

        for widg in (
                self.title_bar, self.title_frame, self.logo, self.title_1, 
                self.title_1b, self.title_2, self.txt_frm, self.buttonbox):
            widg.bind('<B1-Motion>', self.move_window)
            widg.bind('<Button-1>', self.get_pos)
            widg.bind('<Double-Button-1>', self.toggle_max_restore) 

        for widg in (
                self.border_top, self.border_left, 
                self.border_right, self.border_bottom):
            widg.bind('<Button-1>', self.start_edge_sizer)
            widg.bind('<B1-Motion>', self.stop_edge_sizer)
            widg.bind('<ButtonRelease-1>', self.stop_edge_sizer)

    def recolorize_on_restore(self, evt):
        evt.widget.config(bg=NEUTRAL_COLOR)

    def move_window(self, evt):
        ''' Drag the window by the title frame
        '''
        self.master.update_idletasks()
        x_mouse_move_screen = evt.x_root
        y_mouse_move_screen = evt.y_root
        new_x = x_mouse_move_screen + self.adjust_x
        new_y = y_mouse_move_screen + self.adjust_y

        evt.widget.winfo_toplevel().geometry('+{}+{}'.format(new_x, new_y))

    def get_pos(self, evt):
        ''' Prepare to drag the window by the title frame. '''
        evt.widget.winfo_toplevel().lift()
        self.colorize_border()
        
        left_edge = self.master.winfo_rootx()
        top_edge = self.master.winfo_rooty()
        x_click_screen = evt.x_root
        y_click_screen = evt.y_root

        self.adjust_x = left_edge - x_click_screen
        self.adjust_y = top_edge - y_click_screen

    def toggle_max_restore(self, evt):
        '''
            When window is maximized, change window border button
            to restore down and vice versa. Have to return the
            Windows title bar first or Tkinter won't let it be
            maximized.
        '''

        if self.maxxed is False:
            self.maxxed = True
            self.init_geometry = evt.widget.winfo_toplevel().geometry()
            self.maxx.grid_remove()
            self.restore.grid()
            self.restore.config(bg=NEUTRAL_COLOR)
            self.maximize(evt)
        elif self.maxxed is True:
            self.maxxed = False
            self.restore.grid_remove()
            self.maxx.grid()
            self.maxx.config(bg=NEUTRAL_COLOR)
            self.restore_down(evt)

    def minimize(self, evt):
        '''
            Withdraw so return of Windows titlebar isn't visible.
            Return Windows titlebar so window can be iconified.
        '''        
        dlg = evt.widget.winfo_toplevel()
        dlg.withdraw()
        self.master.update_idletasks()
        dlg.overrideredirect(0)
        dlg.iconify()

    def hide_windows_titlebar(self, evt):
        self.update_idletasks()
        self.master.overrideredirect(1)

    def split_geometry_string(self, window):
        xy = window.geometry().split('+')
        wh = xy.pop(0).split('x')
        return int(wh[0]), int(wh[1]), int(xy[0]), int(xy[1])
       
    def maximize(self, evt):
        dlg = evt.widget.winfo_toplevel()
        self.master.update_idletasks()
        dlg.overrideredirect(0)
        dlg.attributes('-fullscreen', True)

    def restore_down(self, evt):
        dlg = evt.widget.winfo_toplevel()
        dlg.attributes('-fullscreen', False)
        dlg.geometry(self.init_geometry)

    def start_edge_sizer(self, evt):

        def pass_values():
            values =  (
                resizee, init_geometry, click_down_x, click_down_y, 
                orig_pos_x, orig_pos_y)
            return values

        resizee = evt.widget.winfo_toplevel()
        init_geometry = resizee.geometry()
        
        (click_down_x, click_down_y) = resizee.winfo_pointerxy()

        orig_pos_x = resizee.winfo_rootx()
        orig_pos_y = resizee.winfo_rooty()

        self.changing_values = pass_values()

    def stop_edge_sizer(self, evt):

        values = self.changing_values
        resizee = values[0]
        init_geometry = values[1]
        click_down_x = values[2]
        click_down_y = values[3]
        orig_pos_x = values[4]
        orig_pos_y = values[5]

        click_up_x = click_down_x  
        click_up_y = click_down_y
        new_pos_x = orig_pos_x
        new_pos_y = orig_pos_y

        klikt = evt.widget 

        xy = init_geometry.split('+')
        wh = xy.pop(0).split('x')

        new_w = orig_wd = int(wh[0])
        new_h = orig_ht = int(wh[1])  

        click_up_x = resizee.winfo_pointerx() 
        click_up_y = resizee.winfo_pointery()

        dx = click_down_x - click_up_x
        dy = click_down_y - click_up_y
        if klikt.winfo_name() == 'left':
            new_w = orig_wd + dx
            new_pos_x = orig_pos_x - dx
        elif klikt.winfo_name() == 'right':
            new_w = orig_wd - dx
        elif klikt.winfo_name() == 'top':
            new_h = orig_ht + dy
            new_pos_y = orig_pos_y - dy
        elif klikt.winfo_name() == 'bottom':
            new_h = orig_ht - dy

        if new_w < 10:
            new_w = 10
        if new_h < 10:
            new_h = 10
        resizee.geometry('{}x{}+{}+{}'.format(
            new_w, new_h, new_pos_x, new_pos_y))

    def colorize_border(self):
        '''
            Runs whenever title bar is clicked, called in get_pos().
        '''
        for widg in self.BORDER_PARTS:
            widg.config(bg=Border.head_bg)
        for widg in (self.title_1, self.title_2):
            widg.config(fg=Border.fg)
        for border in Border.pool:
            if border != self:
                for widg in border.BORDER_PARTS:
                    widg.config(bg=NEUTRAL_COLOR)                    
            else:
                # Move active toplevel to the top of the list so it will be 
                #   highlighted by clean_pool() when a toplevel is destroyed.
                idx = Border.pool.index(border)
                Border.pool.insert(0, Border.pool.pop(idx))

class TitleBarButton(Labelx):
    formats = formats
    bg = formats["bg"] 
    head_bg = formats["head_bg"]

    def __init__(self, master, icon='', icon_size='tiny', *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        '''
            The icons are 32x32 but they can be set to any integer size
            between 12 and 32 and a thumbnail will be displayed if less 
            than 32. But sizes between 22 and 30 make a bad X for some
            reason. Sizes 12, 16, 21, and 32 look best so I've hard-coded
            it with those four size options only. (Using Pillow...)

            This class is for buttons with transparent backgrounds so it
            uses my standard neutral color #878787 which doesn't change.
            For buttons with darker colors filling the whole button, 
            #a8afc4 might show as a bright border contrasting too much
            with the image on the button, so a class has been inherited
            from this one which has a darker background color.
        '''

        font_icon_file = {
            'tiny' : (
                10, '{}images/icons/{}_{}.png'.format(app_path, icon, 12)), 
            'small' : (
                12, '{}images/icons/{}_{}.png'.format(app_path, icon, 17)), 
            'medium' : (
                14, '{}images/icons/{}_{}.png'.format(app_path, icon, 21)), 
            'large' : (
                18, '{}images/icons/{}_{}.png'.format(app_path, icon, 32))}

        for k,v in font_icon_file.items():
            if icon_size == k:
                icon_size = v[0]
                file = v[1]
        img = Image.open(file)
        self.tk_img = ImageTk.PhotoImage(img, master=master)

        self.config(
            font=('arial', icon_size, 'bold'), 
            bd=2, 
            relief='raised',
            bg=NEUTRAL_COLOR,
            image=self.tk_img)

        self.bind('<FocusIn>', self.show_focus)
        self.bind('<FocusOut>', self.unshow_focus)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_unhover)

    def show_focus(self, evt):
        self.config(borderwidth=2)

    def unshow_focus(self, evt):
        self.config(borderwidth=1)

    def on_press(self, evt):
        self.config(relief='sunken', bg=TitleBarButton.head_bg)

    def on_release(self, evt):
        self.config(relief='raised', bg=TitleBarButton.bg)

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

class TitleBarButtonSolidBG(TitleBarButton):
    def __init__(self, master, *args, **kwargs):
        TitleBarButton.__init__(self, master, *args, **kwargs)
        '''
            For buttons with a solid image and darker color
            backgrounds so a bright border doesn't show through
            around the edge of the image.
        '''
        self.config(bg=formats['highlight_bg'])

class Dialogue(Toplevel):
    '''
        Generic unscrolled dialogue with Toykinter border. Border class is a
        Canvas which is gridded in its home class. Rows are reserved for the
        menu bar and icon ribbon menu although usually not used so they are
        False by default, but their unused rows have to be taken into account
        when gridding their siblings in rows. This is used for error messages 
        and one-button dialogs which don't change size and won't scroll.
    '''
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.withdraw()
        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, master)
        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)
        self.formats = make_formats_dict()

    def resize_window(self):
        """ Call this to show the dialog. Added to requested width and height 
            are allowances for widgets not in self.window such as borders, 
            title bar, and status bar.
        """
        self.update_idletasks()    
        width = self.window.winfo_reqwidth() + 6
        height = self.window.winfo_reqheight() + 42
        self.geometry("{}x{}".format(width, height))
        center_dialog(self)

        configall(self, self.formats)
        self.deiconify()

class EntryAuto(Entryx):
    '''
        To use this class, after instantiating it, you have to call 
        EntryAuto.create_lists(all_items). Other than getting all_items
        (e.g. from a database query), the class is self-contained. 

        To extend this class, rule number 1 is don't try doing logic on a
        string being autofilled until the typing/autofilling is done and
        focus is out of the widget. See EntryAutoPerson in persons.py.
    '''

    all_person_autofills = []
    formats = formats
    bg = formats["bg"]
    fg = formats["fg"]
    insertbackground = formats["fg"]
    selectbackground = formats["head_bg"]
    selectforeground = formats["fg"]
    font = formats["input_font"]

    def create_lists(all_items):
        """ Ignore this, it's made to use a simple list. Until it's customized
            for the dict that is used for name values, this won't work for
            person autofills. It currently works for events and places.
        """
        recent_items = []
        all_items_unique = []

        for item in all_items:
            if item not in recent_items:
                all_items_unique.append(item)
        final_items = recent_items + all_items_unique
        return final_items

    def __init__(self, master, autofill=False, values=None, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        self.master = master
        self.autofill = autofill
        self.values = values

        self.config(
            bd=0,
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'],
            selectbackground=formats["head_bg"],
            selectforeground=formats["fg"])

        if autofill is True:
            self.bind("<KeyPress>", self.detect_pressed)
            self.bind("<KeyRelease>", self.get_typed)
            self.bind("<FocusOut>", self.prepend_match, add="+")
            self.bind("<FocusIn>", self.deselect, add="+")

    def detect_pressed(self, evt):
        '''
            runs on every key press
        '''
        if self.autofill is False:
            return
        key = evt.keysym
        if len(key) == 1:
            self.pos = self.index('insert')
            keep = self.get()[0:self.pos]
            self.delete(0, 'end')
            self.insert(0, keep)

    def get_typed(self, evt):
        '''
            Run on every key release; filters out most non-alpha-numeric 
            keys; runs the functions not triggered by events.
        '''
        def do_it():
            hits = self.match_string()
            self.show_hits(hits, self.pos)

        if self.autofill is False:
            return
        key = evt.keysym
        # prevent CTRL+S from filling anything in; also keeps the first
        #   typed character from filling anything in if it's an "s"; sorry.
        if key in ("s", "S"):
            return
        # allow alphanumeric characters
        if len(key) == 1:
            do_it()
        # allow hyphens and apostrophes
        elif key in ('minus', 'quoteright'):
            do_it()
        # look for other chars that should be allowed in nested names
        else:
            pass

    def match_string(self):
        hits = []
        got = self.get()
        use_list = self.values
        for item in use_list:
            if item.lower().startswith(got.lower()):
                hits.append(item)
        return hits

    def show_hits(self, hits, pos):
        cursor = pos + 1
        if len(hits) != 0:
            self.delete(0, 'end')
            self.insert(0, hits[0])
            self.icursor(cursor)

    def prepend_match(self, evt):
        content = self.get()
        if content in self.values:
            idx = self.values.index(content)
            del self.values[idx]
            self.values.insert(0, content)

    def deselect(self, evt):
        '''
            This callback was added because something in the code for this 
            widget caused the built-in replacement of selected text with 
            typed text to stop working. So if you tabbed into an autofill entry
            that already had text in it, the text was all selected as expected 
            but if you typed, the typing was added to the end of the existing 
            text instead of replacing it, which is unexpected. Instead of 
            finding out why this is happening, I added this callback so that 
            tabbing into a filled-out autofill will not select its text. This 
            might be better since the value in the field is not often changed 
            and should not be easy to change by mistake.
        '''
        self.select_clear()

class EntryAutoHilited(EntryAuto):
    def __init__(self, master, *args, **kwargs):
        EntryAuto.__init__(self, master, *args, **kwargs)
        self.config(bg=formats["highlight_bg"])

""" These two autofill inputs are based on simpler code in autofill.py. """
class EntryAutoPerson(Entryx):
    """ To use this class, each person autofill input has to be given the 
        ability to use its newest values with a line like this: 
            `EntryAutoPerson.all_person_autofills.append(person_entry)`.
        Then, after instantiating a class that uses autofills, you have to call 
        `EntryAuto.create_lists(all_items)`. After values change, run something 
        like `update_person_autofill_values()`.        
    """
    all_person_autofills = []
    formats = formats
    highlight_bg = formats["highlight_bg"]
    bg = formats["bg"]
    font = formats["input_font"]
    fg = formats["fg"]
    insertbackground = formats["fg"]
    selectforeground = formats["fg"]
    selectbackground = formats["head_bg"]
    def create_lists(all_items):
        """ Keeps a temporary list during one app session which will 
            prioritize the autofill values with the most recently used values
            given priority over the alphabetical list of the values not used in
            the current session.

            The `prepend_match()` method is used in conjunction with this 
            to add the most recently used value to the very front of the list.

            Since this function and the list `all_person_autofills` comprise a 
            class-level procedure, values used and moved to the front of the 
            list by one input will become available as first match to all the 
            other inputs too, until the app is closed. Next time the app opens,
            a fresh list of recently-used autofill values will be started.
        """
        key_list = list(all_items.items())
        recent_items = []
        all_items_unique = []

        for item in key_list:
            if item not in recent_items:
                all_items_unique.append(item)
        final_items = dict(recent_items + all_items_unique)
        return final_items

    def __init__(self, master, autofill=False, values=None, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        self.master = master
        self.autofill = autofill
        self.values = values
        self.pos = 0
        self.current_id = None
        self.filled_name = None
        self.hits = None

        if autofill is True:
            self.bind("<KeyPress>", self.detect_pressed)
            self.bind("<KeyRelease>", self.get_typed)
            self.bind("<FocusOut>", self.prepend_match, add="+")
            self.bind("<FocusIn>", self.deselect, add="+")
        
        self.config(
            bd=0,
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'],
            selectbackground=formats["head_bg"], 
            selectforeground=formats["fg"])  
         
        self.bind("<Enter>", self.highlight)
        self.bind("<Leave>", self.unhighlight)

    def highlight(self, evt):
        self.config(bg=EntryAutoPerson.highlight_bg)

    def unhighlight(self, evt):
        self.config(bg=EntryAutoPerson.bg)

    def detect_pressed(self, evt):
        """ Run on every key press.
        """
        if self.autofill is False:
            return
        key = evt.keysym
        if len(key) == 1:
            self.pos = self.index('insert')
            keep = self.get()[0:self.pos].strip("+")
            self.delete(0, 'end')
            self.insert(0, keep)

    def get_typed(self, evt):
        """ Run on every key release. Filter out most non-alpha-numeric 
            keys. Run the functions not triggered by events.
        """
        def do_it():
            hits = self.match_string()
            self.show_hits(hits, self.pos)

        self.current_id = None
        if self.autofill is False:
            return
        key = evt.keysym
        # prevent CTRL+S from filling anything in; also keeps the first
        #   typed character from filling anything in if it's an "s"; sorry.
        if key in ("s", "S"):
            return
        # Allow alphanumeric characters.
        if len(key) == 1:
            do_it()
        # Allow number signs, hyphens and apostrophes (#, -, ').
        elif key in ('numbersign', 'minus', 'quoteright'):
            do_it()
        # Open the PersonAdd dialog with the "+" stripped off the input.
        elif key == "plus":
            content = self.get()
            idx = content.index("+")
            fixed = content.replace("+", "")
            self.delete(0, "end")
            self.insert(0, "{}+".format(fixed))

    def match_string(self):
        """ Match typed input to names already stored in hierarchical order. """

        hits = []
        got = self.get()

        for k, v in self.values.items():
            for dkt in v:
                if dkt["name"].lower().startswith(got.lower()):
                    if (dkt, k) not in hits:
                        
                        hits.append((dkt, k))
        return hits

    def show_hits(self, hits, pos):
        cursor = pos + 1
        if len(hits) != 0:
            self.current_id = hits[0][1]
            self.filled_name = hits[0][0]["name"]
            self.delete(0, 'end')
            self.insert(0, self.filled_name)
        self.icursor(cursor)
        self.hits = hits

    def open_dupe_dialog(self, hits):

        def ok_dupe_name():
            self.delete(0, "end")
            dupe_name_dlg.destroy()
    
        def search_dupe_name():
            self.delete(0, "end")
            dupe_name_dlg.destroy()

        def cancel_dupe_name():
            nonlocal dupe_name_dlg_cancelled
            dupe_name_dlg_cancelled = True
            self.delete(0, "end")
            dupe_name_dlg.destroy()

        dupe_name_dlg_cancelled = False
        self.right_id = tk.IntVar()
        dupe_name_dlg = Dialogue(self)

        lab = LabelHeader(
            dupe_name_dlg.window, justify='left', wraplength=450)
        lab.grid(column=0, row=0, padx=12, pady=12, ipadx=6, ipady=6)

        radfrm = Frame(dupe_name_dlg.window)
        radfrm.grid(column=0, row=1)
        r = 0
        for hit in hits:
            dkt, iD = hit
            name, name_type, used_by, dupe_name = (
                dkt["name"], dkt["name type"], dkt["used by"], dkt["dupe name"])
            if len(used_by) != 0:
                used_by = ", name used by {}".format(used_by)
            rdo = Radiobutton(
                radfrm, text="person #{} {} ({}){} ".format(iD, name, name_type, used_by), 
                variable=self.right_id, value=r, anchor="w")
            rdo.grid(column=0, row=r, sticky="ew")
            if r == 0:
                rdo.select()
                rdo.focus_set()
                lab.config(text="Which {}?".format(name))
            r += 1
     
        buttons = Frame(dupe_name_dlg.window)
        buttons.grid(column=0, row=2, pady=12, padx=12)
        dupe_name_ok = Button(buttons, text="OK", command=ok_dupe_name, width=7)
        dupe_name_ok.grid(column=0, row=0, sticky="e", padx=(0,12))
        search_name = Button(buttons, text="SEARCH DUPE NAME", command=search_dupe_name)
        search_name.grid(column=1, row=0, sticky="e", padx=(0,12))
        dupe_name_cancel = Button(buttons, text="CANCEL", command=cancel_dupe_name, width=7)
        dupe_name_cancel.grid(column=2, row=0, sticky="e", padx=0)

        dupe_name_dlg.canvas.title_1.config(text="Duplicate Stored Names")
        dupe_name_dlg.canvas.title_2.config(text="")

        dupe_name_dlg.resize_window()
        self.wait_window(dupe_name_dlg)
        if dupe_name_dlg_cancelled is False:
            selected = self.right_id.get()
            return hits[selected]

    def prepend_match(self, evt):
        """ Determine which ID was used to fill in a value. Move the autofill
            value corresponding with that ID to the front of the valus list.
        """
        content = self.get()
        if self.current_id in self.values:
            key_list = list(self.values.items())
            u = 0
            for tup in key_list:
                if tup[0] == self.current_id:
                    idx = u
                    break
                u += 1
            used = key_list.pop(idx)
            key_list.insert(0, used)
            self.values = dict(key_list)

    def deselect(self, evt):
        '''
            This callback was added because something in the code for this 
            widget caused the built-in replacement of selected text with 
            typed text to stop working. So if you tabbed into an autofill entry
            that already had text in it, the text was all selected as expected 
            but if you typed, the typing was added to the end of the existing 
            text instead of replacing it, which is unexpected. Instead of 
            finding out why this is happening, I added this callback so that 
            tabbing into a filled-out autofill will not select its text. This 
            might be better since the value in the field is not often changed 
            and should not be easy to change by mistake.
        '''
        self.select_clear()

class EntryAutoPersonHilited(EntryAutoPerson):
    """ Override event handling from parent class. """
    def __init__(self, master, *args, **kwargs):
        EntryAutoPerson.__init__(self, master, *args, **kwargs)
        self.config(bg=formats["highlight_bg"])
    def highlight(self, evt):
        pass
    def unhighlight(self, evt):
        pass

# from custom_combobox_widget.py
class Combobox(FrameHilited3):
    hive = []
    formats = formats
    highlight_bg = formats["highlight_bg"]
    head_bg = formats["head_bg"]
    bg = formats["bg"]

    def __init__(
            self, 
            master, 
            root, 
            callback=None,
            height=480, 
            values=[], 
            scrollbar_size=24, 
            *args, **kwargs):
        FrameHilited3.__init__(self, master, *args, **kwargs)
        '''
            This is a replacement for ttk.Combobox.
        '''

        self.master = master
        self.callback = callback
        self.root = root
        self.height = height
        self.values = values
        self.scrollbar_size = scrollbar_size

        self.buttons = []
        self.selected = None
        self.result_string = ''

        self.entered = None
        self.lenval = len(self.values)
        self.owt = None
        self.scrollbar_clicked = False
        self.typed = None

        self.screen_height = self.winfo_screenheight()
        self.config(bd=0)

        # simulate <<ComboboxSelected>>:
        self.var = tk.StringVar()
        self.var.trace_add('write', lambda *args, **kwargs: self.combobox_selected()) 

        # simulate ttk.Combobox.current()
        self.current = 0

        self.make_widgets()
        self.master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')

        # self.root.bind('<Configure>', self.hide_all_drops) # DO NOT DELETE
        # Above binding closes dropdown if Windows title bar is clicked, it
        #   has no other purpose. But it causes minor glitches e.g. if a
        #   dropdown button is highlighted and focused, the Entry has to be
        #   clicked twice to put it back into the alternating drop/undrop
        #   cycle as expected. Without this binding, the click on the title
        #   bar lowers the dropdown below the root window which is good 
        #   enough for now. To get around it, use the Border class in 
        #   window_border.py instead of the built-in Windows title bar that
        #   comes with Tkinter.

        # expose only unique methods of Entry e.g. not self.config (self is a
        #   Frame and the Entry, Toplevel, Canvas, and window have to be 
        #   configured together) so to size the entry use 
        #   instance.config_drop_width(72)
        self.insert = self.entry.insert
        self.delete = self.entry.delete
        self.get = self.entry.get

    def make_widgets(self):
        self.entry = Entry(self, textvariable=self.var)
        self.arrow = ComboArrow(self, text='\u25BC', width=2)

        self.entry.grid(column=0, row=0)
        self.arrow.grid(column=1, row=0)

        self.update_idletasks()
        self.width = self.winfo_reqwidth()

        self.drop = ToplevelHilited(self, bd=0)
        self.drop.bind('<Destroy>', self.clear_reference_to_dropdown)
        self.drop.withdraw()
        Combobox.hive.append(self.drop)
        for widg in (self.master, self.drop):
            widg.bind('<Escape>', self.hide_all_drops, add='+')

        self.drop.grid_columnconfigure(0, weight=1)
        self.drop.grid_rowconfigure(0, weight=1)

        self.canvas = CanvasHilited(self.drop)
        self.canvas.grid(column=0, row=0, sticky='news')

        self.scrollv_combo = Scrollbar(
            self.drop, hideable=True, command=self.canvas.yview, 
            width=self.scrollbar_size)
        self.canvas.config(yscrollcommand=self.scrollv_combo.set)
        self.content = Frame(self.canvas)

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure('all', weight=1)

        self.scrollv_combo.grid(column=1, row=0, sticky='ns') 

        self.entry.bind('<KeyPress>', self.open_or_close_dropdown)
        self.entry.bind('<Tab>', self.open_or_close_dropdown)

        for widg in (self.entry, self.arrow):
            widg.bind('<Button-1>', self.open_or_close_dropdown, add='+')
    
        self.arrow.bind('<Button-1>', self.focus_entry_on_arrow_click, add='+')
       
        for frm in (self, self.content):
            """ Bind arrow events to frames to make arrow label highlight on
                click or focus in. I don't remember why it had to be done this
                way, but changing it to run a local callback breaks the 
                highlighting.
            """
            frm.bind('<FocusIn>', self.arrow.highlight_arrow)
            frm.bind('<FocusOut>', self.arrow.unhighlight_arrow)

        self.drop.bind('<FocusIn>', self.focus_dropdown)
        self.drop.bind('<Unmap>', self.unhighlight_all_drop_items)

        self.current_combo_parts = [self, self.entry, self.arrow, self.scrollv_combo]
        for part in self.current_combo_parts:
            part.bind('<Enter>', self.unbind_combo_parts, add="+")
            part.bind('<Leave>', self.rebind_combo_parts, add="+")
        self.config_values(self.values)

        configall(self.drop, Combobox.formats)
        # config_generic(self.drop)

    def unbind_combo_parts(self, evt):
        self.master.unbind_all('<ButtonRelease-1>')

    def rebind_combo_parts(self, evt):
        self.master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')

    def unhighlight_all_drop_items(self, evt):
        for child in self.content.winfo_children():
            child.config(bg=Combobox.highlight_bg)

    def clear_reference_to_dropdown(self, evt):
        dropdown = evt.widget
        if dropdown in Combobox.hive:
            idx = Combobox.hive.index(dropdown)
            del Combobox.hive[idx]  
            dropdown = None

    def config_values(self, values):
        '''
            The vertical scrollbar, when there is one, overlaps the 
            dropdown button highlight but both still work. To change
            this, the button width can be changed when the scrollbar
            appears and disappears.
        '''
        if len(values) == 0: return
        # RE: above return line; NOT SURE WHY THIS WAS NEEDED alert:
        #   had to add this line after adding `if self.fit_height <= self.height:`
        #   at bottom of this method, which had to be added so dropdowns
        #   could be less than default height. Possibly this has to do with the
        #   difference between running a Combobox in a dialog vs. in a tab on the
        #   root window. I say this because this method seems to be running too
        #   early (before there are any values) and if that happens, the new 
        #   line below sets height to 0. Seems to be working now that this 
        #   method is not allowed to run twice.
        # a sample button is made to get its height, then destroyed
        b = ButtonFlatHilited(self.content, text='Sample')
        one_height = b.winfo_reqheight()
        self.fit_height = one_height * len(values)

        self.values = values
        self.lenval = len(self.values)

        for button in self.buttons:
            button.destroy()
        self.buttons = []

        host_width = self.winfo_reqwidth()
        self.window = self.canvas.create_window(
            0, 0, anchor='nw', window=self.content, width=host_width)
        self.canvas.config(scrollregion=(0, 0, host_width, self.fit_height))
        c = 0
        for item in values:
            bt = ButtonFlatHilited(self.content, text=item, anchor='w')
            bt.grid(column=0, row=c, sticky='ew')  
            for event in ('<Button-1>', '<Return>', '<space>'):
                bt.bind(event, self.get_clicked, add='+')
            bt.bind('<Enter>', self.highlight_button)
            bt.bind('<Leave>', self.unhighlight_button)
            bt.bind('<Tab>', self.tab_out_of_dropdown_fwd)
            bt.bind('<Shift-Tab>', self.tab_out_of_dropdown_back)
            bt.bind('<KeyPress>', self.traverse_on_arrow)
            bt.bind('<FocusOut>', self.unhighlight_button)
            bt.bind('<FocusOut>', self.get_tip_widg, add='+')
            bt.bind('<FocusIn>', self.get_tip_widg)
            bt.bind('<Enter>', self.get_tip_widg, add='+')
            bt.bind('<Leave>', self.get_tip_widg, add='+')
            self.buttons.append(bt)
            c += 1
        for b in self.buttons:
            b.config(command=self.callback)
        if self.fit_height <= self.height:
            self.height = self.fit_height

    def get_tip_widg(self, evt):
        '''
            '10' is FocusOut, '9' is FocusIn
        '''
        if self.winfo_reqwidth() <= evt.widget.winfo_reqwidth():
            widg = evt.widget
            evt_type = evt.type
            if evt_type in ('7', '9'):
                self.show_overwidth_tip(widg)
            elif evt_type in ('8', '10'):
                self.hide_overwidth_tip()

    def show_overwidth_tip(self, widg):
        '''
            Instead of a horizontal scrollbar, if a dropdown item doesn't all
            show in the space allotted, the full text will appear in a tooltip
            on highlight. Most of this code is borrowed from Michael Foord.
        '''
        text=widg.cget('text')
        if self.owt:
            return
        x, y, cx, cy = widg.bbox()
        x = x + widg.winfo_rootx() + 32
        y = y + cy + widg.winfo_rooty() + 32
        self.owt = ToplevelHilited(self)
        self.owt.wm_overrideredirect(1)
        l = LabelTip2(self.owt, text=text) 
        l.pack(ipadx=6, ipady=3)
        self.owt.wm_geometry('+{}+{}'.format(x, y))

    def hide_overwidth_tip(self):    
        tip = self.owt
        self.owt = None
        if tip:
            tip.destroy() 

    def focus_entry_on_arrow_click(self, evt):
        self.focus_set()
        self.entry.select_range(0, 'end')  

    def hide_other_drops(self):
        for dropdown in Combobox.hive:
            if dropdown != self.drop:
                dropdown.withdraw()

    def hide_all_drops(self, evt=None):
        for dropdown in Combobox.hive:
            dropdown.withdraw()

    def close_dropdown(self, evt):
        '''
            Runs only on ButtonRelease-1.

            In the case of a destroyable combobox in a dialog, after the
            combobox is destroyed, this event will cause an error because
            the dropdown no longer exists. I think this is harmless so I
            added the try/except to pass on it instead of figuring out how
            to prevent the error.
        '''
        widg = evt.widget
        if widg == self.scrollv_combo:
            self.scrollbar_clicked = True
        try:
            self.drop.withdraw()
        except tk.TclError:
            pass

    def config_drop_width(self, new_width):
        self.entry.config(width=new_width)
        self.update_idletasks()
        self.width = self.winfo_reqwidth()
        self.drop.geometry('{}x{}'.format(self.width, self.height)) 
        self.scrollregion_width = new_width
        self.canvas.itemconfigure(self.window, width=self.width)
        self.canvas.configure(scrollregion=(0, 0, new_width, self.fit_height))

    def open_or_close_dropdown(self, evt=None):
        if evt is None:
            # dropdown item clicked--no evt because of Button command option
            if self.callback:
                self.callback(self.selected)
            self.drop.withdraw()
            return
        if len(self.buttons) == 0:
            return
        evt_type = evt.type
        evt_sym = evt.keysym
        if evt_sym == 'Tab':
            self.drop.withdraw()
            return
        elif evt_sym == 'Escape':
            self.hide_all_drops()
            return
        first = None
        last = None
        if len(self.buttons) != 0:
            first = self.buttons[0]
            last = self.buttons[len(self.buttons) - 1]
        # self.drop.winfo_ismapped() gets the wrong value
        #   if the scrollbar was the last thing clicked
        #   so drop_is_open has to be used also.
        if evt_type == '4':
            if self.drop.winfo_ismapped() == 1:
                drop_is_open = True
            elif self.drop.winfo_ismapped() == 0:
                drop_is_open = False
            if self.scrollbar_clicked is True:
                drop_is_open = True
                self.scrollbar_clicked = False
            if drop_is_open is True:
                self.drop.withdraw() 
                drop_is_open = False
                return
            elif drop_is_open is False:
                pass
        elif evt_type == '2':
            if evt_sym not in ('Up', 'Down'):
                return
            elif first is None or last is None:
                pass
            elif evt_sym == 'Down':
                first.config(bg=Combobox.bg)
                first.focus_set()
                self.canvas.yview_moveto(0.0)
            elif evt_sym == 'Up':
                last.config(bg=Combobox.bg)
                last.focus_set()
                self.canvas.yview_moveto(1.0)

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        combo_height = self.winfo_reqheight()

        self.fit_height = self.content.winfo_reqheight()
        self.drop.wm_overrideredirect(1)
        fly_up = self.get_vertical_pos(combo_height, evt)
        if fly_up[0] is False:            
            y = y + combo_height
        else:
            y = fly_up[1]
       
        self.drop.geometry('{}x{}+{}+{}'.format(
            self.width, self.height, x, y)) 
        self.drop.deiconify() 
        self.hide_other_drops()

    def get_vertical_pos(self, combo_height, evt):
        fly_up = False
        vert_pos = evt.y_root - evt.y
        clearance = self.screen_height - (vert_pos + combo_height)
        if clearance < self.height:
            fly_up = True

        return (fly_up, vert_pos - self.height)

    def highlight_button(self, evt):
        for widg in self.buttons:
            widg.config(bg=Combobox.highlight_bg)
        widget = evt.widget
        widget.config(bg=Combobox.bg)
        self.selected = widget
        widget.focus_set()

    def unhighlight_button(self, evt):
        x, y = self.winfo_pointerxy()
        hovered = self.winfo_containing(x,y)
        if hovered in self.buttons:
            evt.widget.config(bg=Combobox.highlight_bg)

    def hide_drops_on_title_bar_click(self, evt):
        x, y = self.winfo_pointerxy()
        hovered = self.winfo_containing(x,y)

    def focus_dropdown(self, evt):
        for widg in self.buttons:
            widg.config(takefocus=1)

    def handle_tab_out_of_dropdown(self, go):

        for widg in self.buttons:
            widg.config(takefocus=0)

        self.entry.delete(0, 'end')
        self.entry.insert(0, self.selected.cget('text'))
        self.drop.withdraw()
        self.entry.focus_set()
        if go == 'fwd':
            goto = self.entry.tk_focusNext()
        elif go == 'back':
            goto = self.entry.tk_focusPrev()
        goto.focus_set()

    def tab_out_of_dropdown_fwd(self, evt):
        self.selected = evt.widget
        self.handle_tab_out_of_dropdown('fwd')

    def tab_out_of_dropdown_back(self, evt):
        self.selected = evt.widget
        self.handle_tab_out_of_dropdown('back')

    def get_clicked(self, evt):

        self.selected = evt.widget
        self.current = self.selected.grid_info()['row']
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.selected.cget('text')) 
        self.entry.select_range(0, 'end')
        self.open_or_close_dropdown()  

    def get_typed(self):
        self.typed = self.var.get()    

    def highlight_on_traverse(self, evt, next_item=None, prev_item=None):

        evt_type = evt.type
        evt_sym = evt.keysym # 2 is key press, 4 is button press

        for widg in self.buttons:
            widg.config(bg=Combobox.highlight_bg)
        if evt_type == '4':
            self.selected = evt.widget
        elif evt_type == '2' and evt_sym == 'Down':
            self.selected = next_item
        elif evt_type == '2' and evt_sym == 'Up':
            self.selected = prev_item

        self.selected.config(bg=Combobox.bg)
        self.widg_height = int(self.fit_height / self.lenval)
        widg_screenpos = self.selected.winfo_rooty()
        widg_listpos = self.selected.winfo_y()
        win_top = self.drop.winfo_rooty()
        win_bottom = win_top + self.height
        win_ratio = self.height / self.fit_height
        list_ratio = widg_listpos / self.fit_height
        widg_ratio = self.widg_height / self.fit_height
        up_ratio = list_ratio - win_ratio + widg_ratio

        if widg_screenpos > win_bottom - 0.75 * self.widg_height:
            self.canvas.yview_moveto(float(list_ratio))
        elif widg_screenpos < win_top:
            self.canvas.yview_moveto(float(up_ratio))
        self.selected.focus_set()

    def traverse_on_arrow(self, evt):
        if evt.keysym not in ('Up', 'Down'):
            return
        widg = evt.widget
        sym = evt.keysym
        self.widg_height = int(self.fit_height / self.lenval)
        self.update_idletasks()
        next_item = widg.tk_focusNext()
        prev_item = widg.tk_focusPrev()

        if sym == 'Down':
            if next_item in self.buttons:
                self.highlight_on_traverse(evt, next_item=next_item)
            else:
                next_item = self.buttons[0]
                next_item.focus_set()
                next_item.config(bg=Combobox.bg)
                self.canvas.yview_moveto(0.0)

        elif sym == 'Up':
            if prev_item in self.buttons:
                self.highlight_on_traverse(evt, prev_item=prev_item)
            else:
                prev_item = self.buttons[self.lenval-1]
                prev_item.focus_set()
                prev_item.config(bg=Combobox.bg)
                self.canvas.yview_moveto(1.0)        

    def callback(self):
        '''
            A function specified on instantiation.
        '''
        # print('this will not print if overridden (callback)')
        pass

    def combobox_selected(self):
        '''
            A function specified on instantiation will run when
            the selection is made. Similar to ttk's <<ComboboxSelected>>
            but instead of binding to a virtual event.
        '''
        # print('this will not print if overridden (combobox_selected)')
        pass

class ComboArrow(Labelx):
    head_bg = formats["head_bg"]
    fg = formats["fg"]
    output_font = formats["output_font"]
    highlight_bg = formats["highlight_bg"]
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs) 
        self.config(
            bg=ComboArrow.highlight_bg, 
            fg=ComboArrow.fg,
            font=ComboArrow.output_font)

    def highlight_arrow(self, evt):
        self.config(bg=ComboArrow.head_bg)

    def unhighlight_arrow(self, evt):
        self.config(bg=ComboArrow.highlight_bg)

# from custom_tabbed_widget.py

'''
    Replaces ttk.Notebook. Tabs can be displayed on the bottom of the main
    frame, instead of the top. 

    This is a Frame that can be gridded anywhere. No scrollbar needed, because
    tabbed widgets are meant to retain a fixed size and the space they are in
    has a scrollbar of its own. The space they are in should not resize, so set
    `minx` and `miny` to accommodate the tab with the biggest content.
'''

class LabelTab(Labelx):
    formats = formats
    bg = formats["bg"]
    fg = formats["fg"]
    highlight_bg = formats["highlight_bg"]
    tab_font = formats["tab_font"]
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)    
        self.config(font=formats['tab_font'])
        self.chosen = False
        if self.chosen is False:
            self.config(
                bg=formats['bg'], fg=formats['fg'], font=formats["tab_font"])
        else: 
            self.config(
                bg=formats['highlight_bg'], fg=formats["fg"], 
                font=formats["tab_font"]) 

class TabBook(Framex):
    def __init__(
            self, master, root=None, side='nw', bd=0, tabwidth=13, 
            selected='', tabs=[],  minx=0.90, miny=0.85, case='title', 
            takefocus=1, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        '''
            The tab is the part that sticks out with the title 
            you click to activate the page which holds that 
            tab's content. To add widgets grid them with 
            instance.store[page] as the master. For example: 
            inst.store['place'] where 'place' is a string from 
            the original tabs parameter (list of tuples containing
            tab title and accelerator e.g.:
            `[('images', 'I'), ('attributes', 'A')]`). The default
            value of `selected` should not be an empty string since
            a string here is not optional, it has to be the title
            of one of the tabs, the one that is to be open by default. 
            `minx` and `miny` are minimum sizes as proportions of the
            screen size.
        '''

        self.master = master
        self.side = side
        self.bd = bd
        self.tabwidth = tabwidth
        self.selected = selected
        self.minx = self.master.winfo_screenwidth() * minx
        self.miny = self.master.winfo_screenheight() * miny
        self.case = case
        self.takefocus = takefocus
        
        self.tabdict = {}
        for tab in tabs:
            self.tabdict[tab[0]] = [tab[1]]

        self.store = {}
        
        self.active = None
        self.make_widgets() 
        self.open_tab_alt(root)

    def make_widgets(self):
        self.tab_base = Frame(self)
        self.border_base = FrameHilited2(self)
        self.notebook = Frame(self.border_base)
        self.tab_frame = FrameHilited2(self.tab_base)
        self.tabless = Frame(self.tab_base)
        self.spacer = Frame(self.tabless)
        self.top_border = FrameHilited2(self.tabless, height=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.notebook.columnconfigure(0, weight=1, minsize=self.minx)
        self.notebook.rowconfigure(0, weight=1, minsize=self.miny)

        self.grid_tabs()  

        c = 0
        for tab in self.tabdict:
            lab = LabelTab(
                self.tab_frame,
                width=int(self.tabwidth),
                takefocus=self.takefocus)  
            if c == 0:
                lab.chosen = True
            if self.case == 'title':
                lab.config(text=tab.title())   
            elif self.case == 'lower':
                lab.config(text=tab.lower())    
            elif self.case == 'upper':
                lab.config(text=tab.upper())     
            self.tabdict[tab].append(lab)

            if self.side in ('ne', 'nw'):
                lab.grid(column=c, row=0, padx=1, pady=(1, 0))
            elif self.side in ('se', 'sw'):
                lab.grid(column=c, row=0, padx=1, pady=(0, 1))

            lab.bind('<Button-1>', self.make_active)
            lab.bind('<FocusIn>', self.highlight_tab)
            lab.bind('<FocusOut>', self.unhighlight_tab)
            lab.bind('<Key-space>', self.make_active)
            lab.bind('<Key-Return>', self.make_active)
            lab.bind('<ButtonRelease-1>', self.unhighlight_tab)
            create_tooltip(lab, 'Alt + {}'.format(self.tabdict[tab][0]))
            page = Frame(self.notebook)
            page.grid(column=0, row=0, sticky='news')
            page.grid_remove()
            self.tabdict[tab].append(page)
            self.store[tab] = page
            c += 1

        # The next 4 lines are copied in font_picker so make them a method.
        selected_page = self.tabdict[self.selected][2] # page
        selected_page.grid()
        self.active = self.tabdict[self.selected][1] # tab
        self.make_active()

    def grid_tabs(self):

        if self.side in ('nw', 'ne'):
            pady = (0, 1)
            tab_row = 0
            body_row = 1
            spacer_row = 0
            border_row = 1

        elif self.side in ('sw', 'se'):
            pady=(1, 0)
            tab_row = 1
            body_row = 0
            spacer_row = 1
            border_row = 0

        if self.side in ('nw', 'sw'):
            tab_col = 0
            tabless_col = 1                

        elif self.side in ('ne', 'se'):
            tab_col = 1
            tabless_col = 0                

        # self.notebook switches pady
        self.notebook.grid(column=0, row=0, padx=1, pady=pady, sticky='news')
        # self.tab_base and borderbase switch rows
        self.tab_base.grid(column=0, row=tab_row, sticky='news')
        self.tab_base.grid_columnconfigure(tabless_col, weight=1)
        self.tab_base.grid_rowconfigure(0, weight=1)
        self.border_base.grid(column=0, row=body_row, sticky='news')
        # self.tab_frame and self.tabless switch cols
        self.tab_frame.grid(column=tab_col, row=0, sticky='ew')
        self.tabless.grid(column=tabless_col, row=0, sticky='news')
        self.tabless.grid_columnconfigure(0, weight=1)
        self.tabless.grid_rowconfigure(spacer_row, weight=1)
        # self.spacer and self.top_border switch rows
        self.spacer.grid(column=0, row=tab_row, sticky='ns')
        self.top_border.grid(column=0, row=border_row, sticky='ew') 

    def highlight_tab(self, evt):
        # accelerators don't work if notebook not visible
        if evt.widget in self.store.values():
            evt.widget.config(fg='yellow')

    def unhighlight_tab(self, evt):
        # accelerators don't work if notebook not visible
        if evt.widget in self.store.values():
            evt.widget.config(fg=LabelTab.fg)

    def make_active(self, evt=None):
        ''' Open the selected tab & reconfigure it to look open. '''

        # position attributes are needed in the instance
        self.posx = self.winfo_rootx()
        self.posy = self.winfo_rooty()    

        # if this method is not running on load
        if evt:
            self.active = evt.widget
            self.active.focus_set()

            # if evt was alt key accelerator
            if (evt.widget is self.master or 
                    evt.keysym not in ('space', 'Return')):

                for k,v in self.tabdict.items():
                    if evt.keysym in (v[0], v[0].lower()):
                        self.active = v[1]
                        self.active.focus_set()
                        
            # if evt was spacebar, return key, or mouse button
            elif evt.type in ('2', '4'):
                self.active.config(fg=LabelTab.fg)

            # remove all pages and regrid the right one
            for k,v in self.tabdict.items():
                if self.active == v[1]:
                    for widg in self.tabdict.values():
                        widg[2].grid_remove()
                    v[2].grid()
        
        # unhighlight all tabs
        for tab in self.tabdict.values():
            tab[1].config(
                bg=LabelTab.highlight_bg,
                font=LabelTab.tab_font)

        # detect which tab is active and set its tab.chosen attribute to True
        #   so config_generic will give it the right background color when
        #   color_scheme is changed
        for tab in self.tabdict.values():    
            if tab[1] == self.active:
                tab[1].chosen = True
            else:
                tab[1].chosen = False

        # highlight active tab; doesn't work on load due to config_generic()
        #   but does work on user-initiated events
        self.active.config(
            bg=LabelTab.bg,
            font=LabelTab.tab_font)
        # remove all pages and regrid the right one
        for v in self.tabdict.values():
            if self.active == v[1]:
                for widg in self.tabdict.values():
                    widg[2].grid_remove()
                v[2].grid()

    def open_tab_alt(self, root_window):
        ''' Bindings for notebook tab accelerators. '''

        for k,v in self.tabdict.items():
            key_combo_upper = '<Alt-Key-{}>'.format(v[0])  
            root_window.bind(key_combo_upper, self.make_active)
            key_combo_lower = '<Alt-Key-{}>'.format(v[0].lower()) 
            root_window.bind(key_combo_lower, self.make_active)

            unkey_combo_upper = '<Alt-KeyRelease-{}>'.format(v[0])            
            root_window.bind_all(unkey_combo_upper, self.unhighlight_tab)
            unkey_combo_lower = '<Alt-KeyRelease-{}>'.format(v[0].lower()) 
            root_window.bind_all(unkey_combo_lower, self.unhighlight_tab)

# from toykinter_widgets.py

class LabelStatusbar(Labelx):
    formats = formats
    bg = formats["bg"]
    fg = formats["fg"]
    status = formats["status"]
    """ Statusbar messages on focus-in to individual widgets,
        tooltips in statusbars, and replacement for ttk.Sizegrip.
    """
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=LabelStatusbar.bg, 
            fg=LabelStatusbar.fg,
            font=LabelStatusbar.status)

class StatusbarTooltips(Frame):
    '''
        To use this:
        In self.make_widgets()...
            some_statusbar = StatusbarTooltips(self)
            some_statusbar.grid(column=0, row=2, sticky='ew') # use last row in toplevel
            visited = (
                (self.widget1, 
                    'status bar message on focus in', 
                    'tooltip message on mouse hover.'),
                (self.widget2, 
                    'status bar message on focus in', 
                    'tooltip message on mouse hover.'))        
            run_statusbar_tooltips(
                visited, 
                some_statusbar.status_label, 
                some_statusbar.tooltip_label)
        If parent is a Toplevel and you don't want the Toplevel to be resizable,
        use resizer=False when instantiating the Statusbar and add this:
            dialog.resizable(False, False) --that's width and height in that order.

    '''

    def __init__(self, master, resizer=True, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master # root or toplevel
        self.sizer = Sizer(self.master)

        self.grid_columnconfigure(0, weight=1)
        # With custom window border, you can't use the otherwise 
        #   desirable option bd=2, relief='sunken' for a border on statusbar
        #   because edge grabber for resizing is below statusbar 
        #   so border looks wrong there. Instead put a Separator 
        #   above the statusbar frame.
        frm = Frame(self, bd=0)
        frm.grid(column=0, row=0, sticky='news')
        frm.grid_columnconfigure(0, weight=1)
        self.status_label = LabelStatusbar(
            frm, cursor='arrow', anchor='w')
        self.tooltip_label = LabelStatusbar(
            frm, bd=2, relief='sunken', anchor='e')

        if resizer is True:
            self.sizer.place(relx=1.0, x=-3, rely=1.0, anchor='se')
            self.sizer.bind('<Button-1>', self.sizer.get_pos)
        self.status_label.grid(column=0, row=0, sticky='w')

class Sizer(Label):
    def __init__(self, master, icon='sizer_15_dark', *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        ''' 
            SE corner gripper/resizer. Replaces ttk.Sizegrip. The master has to 
            be the toplevel window being resized. Since it's placed, not    
            gridded, it will overlap so the statusbar tooltips had to be moved 
            to the left with padding. This has been built into the toykinter
            statusbar.
        '''
        self.master = master
        self.click_x = 0
        self.click_y = 0
        file = '{}images/icons/{}.png'.format(app_path, icon)
        img = Image.open(file)
        self.tk_img = ImageTk.PhotoImage(img, master=self.master)

        self.config(
            bd=0, 
            cursor='size_nw_se',
            image=self.tk_img)

    def get_pos(self, evt):

        def resize_se(event):
            x_on_move = event.x_root
            y_on_move = event.y_root
            dx = x_on_move - click_x
            dy = y_on_move - click_y
            new_w = orig_w + dx
            new_h = orig_h + dy

            if new_w < 10:
                new_w = 10
            if new_h < 10:
                new_h = 10
            self.master.geometry('{}x{}'.format(new_w, new_h))

        orig_geom = self.master.geometry()
        orig_geom = orig_geom.split('+')[0].split('x')
        orig_w = int(orig_geom[0])
        orig_h = int(orig_geom[1])
        click_x = evt.x_root
        click_y = evt.y_root

        self.bind('<B1-Motion>', resize_se)

class Separator(Framex):
    """ Horizontal separator like ttk.Separator but 
        can be sized and utilize the user-selected colors.
    """
    formats = formats
    color1=formats['head_bg'], 
    color2=formats['highlight_bg'], 
    color3=formats['bg']

    def __init__(
        self, master, height=3, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        Separator.color1=Separator.formats['head_bg'], 
        Separator.color2=Separator.formats['highlight_bg'], 
        Separator.color3=Separator.formats['bg'],

        self.height = int(height/5)

        self.make_widgets()

    def make_widgets(self):

        if self.height > 0:
            self.line1 = FrameStay(
                self, bg=Separator.color1, height=self.height)
            self.line1.grid(column=0, row=0, sticky='ew')

            self.line2 = FrameStay(
                self, bg=Separator.color2, height=self.height)
            self.line2.grid(column=0, row=1, sticky='ew')

            self.line3 = FrameStay(
                self, bg=Separator.color3, height=self.height)
            self.line3.grid(column=0, row=2, sticky='ew')

            self.line4 = FrameStay(
                self, bg=Separator.color2, height=self.height)
            self.line4.grid(column=0, row=4, sticky='ew')

            self.line5 = FrameStay(
                self, bg=Separator.color1, height=self.height)
            self.line5.grid(column=0, row=5, sticky='ew')
        else:
            self.line1 = FrameStay(
                self, bg=Separator.color1, height=self.height)
            self.line1.grid(column=0, row=0, sticky='ew')

            self.line2 = FrameStay(
                self, bg=Separator.color2, height=self.height)
            self.line2.grid(column=0, row=1, sticky='ew')

            self.line3 = FrameStay(
                self, bg=Separator.color3, height=self.height)
            self.line3.grid(column=0, row=2, sticky='ew')

        self.colorize()

    def colorize(self):
        if self.height > 0:
            self.line1.config(bg=Separator.color1)
            self.line2.config(bg=Separator.color2)
            self.line3.config(bg=Separator.color3)
            self.line4.config(bg=Separator.color2)
            self.line5.config(bg=Separator.color1)
        else:
            self.line1.config(bg=Separator.color1)
            self.line2.config(bg=Separator.color2)
            self.line3.config(bg=Separator.color3)

# from scrolling.py

'''
	One purpose of this module is to tell right here how to make a canvas and 
    scrollbar do different things under a variety of circumstances.
 
    I wrote this because I needed a cheat sheet, not because I'm an expert.

    I. MAKE SCROLLBARS:

        sbv = Scrollbar(
            toplevel, 
            command=canvas.yview,
            hideable=True)
        canvas.config(yscrollcommand=sbv.set)

        sbh = Scrollbar(
            toplevel, 
            orient='horizontal', 
            command=canvas.xview, 
            hideable=True)
        canvas.config(xscrollcommand=sbh.set)

    A scrollbar and its canvas are always siblings, e.g. in the above example, 
    the parent of the canvas would also be `toplevel`.

    The class is a custom "Toykinter" widget based on the Tkinter API so using 
    it is almost identical to using the Tkinter scrollbar except that it can be 
    easily configured like any Tkinter widget instead of using Windows system 
    colors. Also it is optionally hideable; default for that option is False. 
    The complication with the hideable scrollbar is that it needs a place to be
    when it appears, so an offset--a blank space the same size as the hidden 
    scrollbar--was added to the required size of the window. Then a spacer 
    was added to the north and west edges of the window to balance this out. 
    These procedures increase the size of the window to prevent the scrollbar 
    from appearing before it's needed. The offset spacer or scrollbar width is 
    "scridth".

    II. CANVAS, SCROLLBAR AND WINDOW SIZING:

    There are several things that can have dimensions so I think of them as a stack
    with the toplevel (root or dialog) on bottom:

        toplevel
        scrollregion
        canvas
        window (content frame)

    The canvas is a widget, gridded, packed or placed like any other widget.

    What I'm calling a "content frame" is a single frame covering the whole 
    canvas, so that
    when the canvas is scrolled, the effect is that the content and all its 
    widgets are being scrolled. Since this frame is not gridded but created 
    by canvas.create_window(), in my code where it says 'window' this should be
    a reference to a content frame in a canvas. If there will be objects drawn 
    on the canvas instead of widgets in a content frame, give the canvas a size 
    with its width and height options. But if there will be a content frame, 
    ignore the canvas width and height options.

    The scrollregion can be visualized as an area behind the canvas, at least 
    as large as the canvas, which can be slid around with only part of it 
    visible at one time. The scrollregion can be panned by dragging with the 
    mouse or arrow keys, or scrolled with scrollbars or the mousewheel. 

    A. RESIZABLE CANVAS

    The root window and some toplevel windows need to have dynamically varying 
    contents. The scrollregion is set to autosize to all the canvas' contents 
    (bounding box or bbox), which is just the content frame in this case.

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        canvas = Canvas(root)
        content = Frame(canvas) # don't grid
        canvas.grid(column=0, row=0, sticky='news')
        content_window = canvas.create_window(0, 0, anchor='nw', window=content)
        canvas.config(scrollregion=canvas.bbox('all')) 

        def resize_canvas(event):
            root.update_idletasks()
            if event.width > content.winfo_reqwidth():
                canvas.itemconfigure(content_window, width=event.width)

        canvas.bind('<Configure>', resize_canvas)

    The toplevel could also be resized this way when its contents change. This way
    instead of resizing automatically when contents change, you have to know when
    contents will change and call the function at that time:

        def resize_scrolled_content(toplevel, canvas):
            toplevel.update_idletasks()
            canvas.config(scrollregion=canvas.bbox('all'))
            page_x = canvas.content.winfo_reqwidth()
            page_y = canvas.content.winfo_reqheight()
            toplevel.geometry('{}x{}'.format(page_x, page_y))

    B. NESTED CANVAS WITH A FIXED SIZE

    Within a toplevel whether it's got its own full-size scrolled area or not, 
    a smaller scrolled area of a fixed size could be contained. In this case, 
    the scrollregion doesn't get set to bbox('all') but to a fized size at 
    least the size of the canvas. The resizing methods are not needed here.

        canvas = Canvas(root, width=500, height=750)
        content = Frame(canvas) # don't grid
        canvas.create_window(0, 0, anchor='nw', window=content)
        canvas.config(scrollregion=(0, 0, 900, 1000)) 

    Instead of hard-coding the width and height of the scrollregion, the 
    required width and height of the canvas contents can be detected so 
    the size of the scrollregion is the exact size it needs to be. The 
    canvas width and height should be set to any size smaller than the 
    scrollregion but won't go below a minimum size that's built into Tkinter.

    C. DROPDOWN WINDOW WITH A FIXED WIDTH   

    A toplevel without a border can be used as a dropdown window, for example 
    in a custom-made combobox, and provided with a vertical scrollbar. Its 
    width will be fixed to that of a host, for example the entry widget in a 
    combobox. The scrollregion height will be calculated to fit the vertical 
    contents. The window height is left to resize to its contents.

    In this example, self is the combobox, i.e. a frame that holds the combobox
    entry and arrow.

        host = self.Entry(self)
        host.grid()
        host_width = self.winfo_reqwidth()
        self.window = self.canvas.create_window(
            0, 0, anchor='nw', window=self.content, width=host_width)
        self.canvas.config(scrollregion=(0, 0, host_width, self.fit_height))

    D. SCROLLING WITH THE MOUSEWHEEL

    Another purpose of this module is to provide a class that coordinates the 
    various scrolled canvases so the right one is scrolled with the mousewheel.

    Each canvas should scroll when the mouse is over that canvas, so a 
    collection of canvases is kept and the mousewheel callback is bound to 
    each canvas. The class is self-contained so all you have to do is 1) 
    instantiate it ahead of any reference to any function that will open a 
    participating toplevel, 2) for root and each participating toplevel, run a 
    method to list the canvases, and 3) for root and each participating 
    toplevel, run a method to configure canvas and window. For 2) above, if 
    the toplevel is resizable, it's listed in a sublist of [canvas, window]. 
    For non-resizable canvases, only the canvas is listed and resizable=False.
    For 3) above, if the root canvas is being configured, in_root=True. This
    effort not only takes care of mousewheel scrolling among a variety of dialogs,
    but also automatically removes references to destroyed toplevels from the 
    list to prevent errors. Besides that, it takes care of resizing window and
    scrollbar in case a dialog changes size for some reason.

        scroll_mouse = MousewheelScrolling(root, canvas)

        scroll_mouse.append_to_list([canvas, canvas.content])
        scroll_mouse.append_to_list(canvas3, resizable=False)
        scroll_mouse.configure_mousewheel_scrolling(in_root=True)

        scroll_mouse.append_to_list([canvas2, canvas2.content])
        scroll_mouse.configure_mousewheel_scrolling()

    E. WHAT ABOUT A SCROLLED CANVAS CLASS?

    I tried making a scrolled canvas class but it was a bag of worms because 
    it abstracted the creation of scrollbars away from the overall design of
    the GUI, becoming an annoyance rather than a tool. It made it seem 
    unnecessary to understand how to make scrollbars, and yet to ever extend 
    the code, the opposite is true. It required extra lines of code which were 
    not Tkinterish, and the end result was more work, not less. But the Scrollbar,
    MousewheelScrolling, and Combobox classes below are the bee's knees, as well as 
    the Border class which is in window_border.py.

'''
class Scrollbar(Canvas):
    '''
        A scrollbar is gridded as a sibling of what it's scrolling. Set the 
        command attribute during construction; it's a python keyword argument 
        but not a Tkinter option so vscroll.config(command=self.yview) won't 
        work. This scrollbar works well and can be made any size or color. It's
        lacking the little arrows at the ends of the trough.

        The `get()` method for this class isn't finished but has been started in
        colorizer.py. It should be moved here instead of making it as an
        instance attribute.
    '''
    formats = formats
    slidercolor = formats['bg']
    troughcolor = formats['head_bg']
    bordercolor = formats['highlight_bg']
    
    def __init__(
        self, master, width=16, orient='vertical', 
            hideable=False, **kwargs):

        self.command = kwargs.pop('command', None)
        Canvas.__init__(self, master, **kwargs)

        self.width = width
        self.orient = orient
        self.hideable = hideable

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0

        self.new_start_y = 0
        self.new_start_x = 0
        self.first_y = 0
        self.first_x = 0

        if orient == 'vertical':
            self.config(width=width)
        elif orient == 'horizontal':
            self.config(height=width)

        self.config(bg=Scrollbar.troughcolor, bd=0, highlightthickness=0)

        self.thumb = self.create_rectangle(
            0, 0, 1, 1, 
            fill=Scrollbar.slidercolor, 
            width=1,    # this is border width
            outline=Scrollbar.bordercolor, 
            tags=('slider',))
        self.bind('<ButtonPress-1>', self.move_on_click)

        self.bind('<ButtonPress-1>', self.start_scroll, add='+')
        self.bind('<B1-Motion>', self.move_on_scroll)
        self.bind('<ButtonRelease-1>', self.end_scroll)

    def set(self, lo, hi):
        '''
            For resizing & repositioning the slider. The hideable
            scrollbar portion is by Fredrik Lundh, one of Tkinter's authors.
        '''

        lo = float(lo)
        hi = float(hi)

        if self.hideable is True:
            if lo <= 0.0 and hi >= 1.0:
                self.grid_remove()
                return
            else:
                self.grid()

        self.height = self.winfo_height()
        width = self.winfo_width()

        if self.orient == 'vertical':
            x0 = 0
            y0 = max(int(self.height * lo), 0)
            x1 = width - 1
            y1 = min(int(self.height * hi), self.height)
        elif self.orient == 'horizontal':
            x0 = max(int(width * lo), 0)
            y0 = 0
            x1 = min(int(width * hi), width)
            y1 = self.height -1

        self.coords('slider', x0, y0, x1, y1)
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def move_on_click(self, event):
        if self.orient == 'vertical':
            y = event.y / self.winfo_height()
            if event.y < self.y0 or event.y > self.y1:
                self.command('moveto', y)
            else:
                self.first_y = event.y
        elif self.orient == 'horizontal':
            x = event.x / self.winfo_width()
            if event.x < self.x0 or event.x > self.x1:
                self.command('moveto', x)
            else:
                self.first_x = event.x

    def start_scroll(self, event):
        if self.orient == 'vertical':
            self.last_y = event.y 
            self.y_move_on_click = int(event.y - self.coords('slider')[1])
        elif self.orient == 'horizontal':
            self.last_x = event.x 
            self.x_move_on_click = int(event.x - self.coords('slider')[0])

    def end_scroll(self, event):
        if self.orient == 'vertical':
            self.new_start_y = event.y
        elif self.orient == 'horizontal':
            self.new_start_x = event.x

    def move_on_scroll(self, event):

        jerkiness = 3

        if self.orient == 'vertical':
            if abs(event.y - self.last_y) < jerkiness:
                return
            delta = 1 if event.y > self.last_y else -1
            self.last_y = event.y
            self.command('scroll', delta, 'units')
            mouse_pos = event.y - self.first_y
            if self.new_start_y != 0:
                mouse_pos = event.y - self.y_move_on_click
            self.command('moveto', mouse_pos/self.winfo_height()) 
        elif self.orient == 'horizontal':
            if abs(event.x - self.last_x) < jerkiness:
                return
            delta = 1 if event.x > self.last_x else -1
            self.last_x = event.x
            self.command('scroll', delta, 'units')
            mouse_pos = event.x - self.first_x
            if self.new_start_x != 0:
                mouse_pos = event.x - self.x_move_on_click
            self.command('moveto', mouse_pos/self.winfo_width()) 

class ScrolledText(Framex):
    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.text = Text(self)
        self.text.grid(column=0, row=0)
        self.ysb = Scrollbar(
            self, 
            width=16,
            orient='vertical', 
            hideable=True,
            command=self.text.yview)
        self.text.configure(yscrollcommand=self.ysb.set, wrap="word")
        self.ysb.grid(column=1, row=0, sticky='ns')

# from dropdown.py

'''
    Replaces Tkinter Menu. Unlike Tkinter's dropdown menu, this widget
        --is used and configured like other Tkinter widgets.
        --doesn't use Windows colors.

    Currently this dropdown menu only uses the mouse, but it could be 
    improved to use keyboard navigation also.

    I just found out, long after creating a replacement for the Windows border
    and putting it on all my main dialogs and the root window, that the 
    Tkinter dropdown menu doesn't even work with my "Toykinter" border. Not
    that I wanted to use tkinter.Menu anyway since its colors can't be changed 
    (maybe depending on the Windows theme in use). Tkinter's dropdown menu 
    doesn't use any of Tkinter's geometry managers (`grid`, `pack` or `place`),
    since it's assumed that the menu is always going to be right below the
    Windows title bar. Since the Toykinter title bar is gridded like any other
    widget, the Tkinter menu bar attaches above the Toykinter title bar and I 
    doubt there's anything that can be done about it, but it doesn't matter, I 
    just had to write a little code, like everyone does in HTML anyway when 
    they need a dropdown menu for a web app.

    At this time I'm keeping it as simple as possible by making the dropdown
    menu respond only to mouse events. To me this seems like the right way
    to use a dropdown menu since I want to tab through GUI functionalities
    quickly to get to the right one, without having to first tab through a 
    bunch of icons and text menu items. Normally I'd rather type than
    click, but prior efforts to make a dropdown menu that works with both mouse
    and keyboard got bogged down in conflicting events and focus handling.

    This widget is hard-coded to handle three levels of menu items: 1) The 
    Labels permanently gridded horizontally across the menu bar; 2) the first
    dropdown that pops open or closed on click and hover events; 3) the second 
    dropdown which flies out to the right of its parent.

    Since there will never be more than one set of `drop0`, `drop1`, and `drop2`
    open at a time, only one set exists. Each of the three drops is a permanent 
    widget which is withdrawn, deiconified and populated with destroyable labels 
    as needed.

    The dropdown is a Toplevel window since it's the only Tkinter widget that
    is made to overlap other widgets without pushing them to the side.
    The Toplevel also doesn't rely on `grid`, `pack` or `place`. Instead, the 
    Toplevel dropdown uses the geometry() method to appear next to its host 
    widget. If the window moves, the dropdown is withdrawn.
'''
IMPORT_TYPES = (
    ("From Treebard", "", ""), 
    ("From GEDCOM", "", ""))

EXPORT_TYPES = (
    ("To Treebard", "", ""), 
    ("To GEDCOM", "", ""))

MOD_KEYS = ("Ctrl", "Alt", "Shift", "Ctrl+Alt", "Ctrl+Shift", "Alt+Shift")

def placeholder(evt=None, name=""):
    print('menu test:', name.upper()) 
    print('evt:', evt) 

class DropdownMenu(FrameHilited2):
    formats = formats
    bg = formats["bg"]
    highlight_bg = formats["highlight_bg"]
    head_bg = formats["head_bg"]
    def __init__(
            self, master, root, treebard, callback=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master 
        self.root = root
        self.treebard = treebard
        self.callback = callback

        self.recent_trees = []

        self.drop1_is_open = False
        self.drop2_is_open = False
        self.expand = False 

        self.clicked = None

        self.host1 = None
        self.drop_delay = 250
        self.ipady = 3
        self.screen_height = self.winfo_screenheight()

        self.drop1 = ToplevelHilited(self, bd=1, relief="raised")
        self.drop2 = ToplevelHilited(self, bd=1, relief="raised")
        self.current_file = ""

        self.drop_items = {
            "file": (
                ("new", lambda evt, root=self.root, tbard=self.treebard, 
                    openfunx=open_input_message2, 
                    msg=opening_msg: handle_new_tree_event(
                        evt, root, tbard, openfunx, msg),
                    "n"),
                ("open", lambda evt, tbard=self.treebard: handle_open_event(
                    evt, tbard), "..."),
                ("save", lambda evt, name="save (redraw)": placeholder(evt, name), "s"),
                ("save as", lambda evt, root=self.root: save_as(evt, root), "CAs"),
                ("save copy as", lambda evt: save_copy_as(), "t"),
                ("rename", lambda evt, root=self.root: rename_tree(evt, root), "h"),
                ("recent trees", lambda evt: self.show_recent_trees(evt), 
                    ">", self.recent_trees),
                ("import tree", self.show_list, ">", IMPORT_TYPES),
                ("export tree", self.show_list, ">", EXPORT_TYPES),
                ("close", lambda evt, tbard=self.treebard: close_tree(evt, tbard), ""),
                ("exit", lambda evt, root=self.root: exit_app(evt, root), "")),

            "edit": (
                ("cut", lambda evt, name="cut": placeholder(evt, name), "x"), 
                ("copy", lambda evt, name="copy": placeholder(evt, name), "c"), 
                ("paste", lambda evt, name="paste": placeholder(evt, name), "v")),

            "elements": (
                ("add person", 
                    lambda evt, name="add person": placeholder(evt, name), ""),
                ("add place", 
                    lambda evt, name="add place": placeholder(evt, name), ""),
                ("add event",
                    lambda evt, name="add event": placeholder(evt, name), ""),
                ("add assertion", 
                    lambda evt, name="add assertion": placeholder(evt, name), ""),
                ("add source",  
                    lambda evt, name="add source": placeholder(evt, name), ""),
                ("add image",  
                    lambda evt, name="add image": placeholder(evt, name), ""),),

            "output": (
                ("charts", 
                    lambda evt, name="charts": placeholder(evt, name), ""),
                ("reports", 
                    lambda evt, name="reports": placeholder(evt, name), ""),),

            "research": (
                ("do list", 
                    lambda evt, name="do list": placeholder(evt, name), ""),
                ("add research goals", 
                    lambda evt, name="research goals": placeholder(evt, name), ""),
                ("contacts",
                    lambda evt, name="contacts": placeholder(evt, name), ""),
                ("correspondence",  
                    lambda evt, name="correspondence": placeholder(evt, name), ""),),

            "tools": (
                ("relationship calculator", 
                    lambda evt, name="relationship calculator": placeholder(evt, name), ""), 
                ("date calculator",  
                    lambda evt, name="date calculator": placeholder(evt, name), ""), 
                ("dupes & matches detector",  
                    lambda evt, name="dupes & matches detector": placeholder(evt, name), ""), 
                ("unlikelihood detector",  
                    lambda evt, name="unlikelihood detector": placeholder(evt, name), ""), 
                ("certainty calculator",  
                    lambda evt, name="certainty calculator": placeholder(evt, name), "")),  

            "help": (
                ("about treebard", 
                    lambda evt, name="about treebard": placeholder(
                        evt, name), ""),
                ("users' manual",  
                    lambda evt, name="users' manual": placeholder(
                        evt, name), ""),
                ("genealogy tips & tricks", 
                    lambda evt, name="genealogy tips & tricks": placeholder(
                        evt, name), ""),
                ("treebard website",
                    lambda evt, name="treebard website": placeholder(
                        evt, name), ""),
                ("forum & blog", 
                    lambda evt, name="forum & blog": placeholder(
                        evt, name), ""),
                ("help search",  
                    lambda evt, name="help search": placeholder(
                        evt, name), ""),
                ("contact",
                    lambda evt, name="contact": placeholder(
                        evt, name), ""),
                ("feature requests", 
                    lambda evt, name="feature requests": placeholder(
                    evt, name), ""),
                ("source code",  
                    lambda evt, name="source code": placeholder(
                        evt, name), ""),
                ("donations",  
                    lambda evt, name="donations": placeholder(
                        evt, name), ""),)}

        self.make_drop0()

        for drop in (self.drop1, self.drop2):
            drop.wm_overrideredirect(1)
            drop.withdraw()
        
        self.root.bind("<Button-1>", self.close_drop_on_click, add="+")

    def make_drop0(self):
        d = 0
        for key in self.drop_items:
            lab = LabelHilited3(self, text=key.title(), bd=1)
            lab.grid(column=d, row=0, ipadx=6, ipady=self.ipady)
            lab.bind('<Button-1>', self.open_drop1_on_click)
            lab.bind('<Enter>', self.make_border)
            lab.bind('<Leave>', self.flatten_border)
            lab.bind('<Enter>', self.open_drop1_on_hover, add="+")
            lab.bind('<Leave>', self.open_drop1_on_hover, add="+")
            d += 1

    def make_drop1(self, evt):
        for child in self.drop1.winfo_children():
            child.destroy()
        self.host1 = widg = evt.widget
        cmd = widg.cget("text").lower()
        for k,v in self.drop_items.items():
            if cmd == k:
                format_strings = []
                text = ""
                lengths = []
                widgets = []
                row = 0
                for lst in self.drop_items[cmd]:
                    lab = LabelHilited3(self.drop1, text=lst[0].title())
                    symval = lst[2]
                    if symval == ">":
                        text = "{}    >".format(lst[0].title())
                    elif symval == "...":
                        text = "{}...    {}".format(lst[0].title(), " ")
                    elif len(symval) != 0:
                        if symval.startswith("CA"):
                            symval = symval[2]
                            mod_key = MOD_KEYS[3]
                        else:
                            mod_key = MOD_KEYS[0]
                        text = "{}    {}+{}".format(lst[0].title(), mod_key, symval.upper())
                    elif len(symval) == 0:
                        text = "{}    ".format(lst[0].title())
                    else:
                        print("line", looky(seeline()).lineno, "case not handled:")

                    lab.grid(column=0, row=row, sticky='ew')
                    self.bind_command(lab, text, v[row])
                    format_strings.append(text)
                    lengths.append(len(text))
                    widgets.append(lab)
                    row += 1
                self.fix_strings(
                    lengths, self.drop_items[cmd], format_strings, widgets)
     
        self.position_drop1()
        self.drop1.deiconify()

    def fix_strings(self, lengths, stringslist, format_strings, widgets):
        maxx = max(lengths)
        j = 0
        for lst in stringslist:
            rightsym = False
            if len(lst[2]) != 0:
                rightsym = True
            if rightsym:
                diff = maxx - lengths[j] + 4
            else:
                diff = maxx - lengths[j]
            stgs = format_strings[j].split("    ")
            new_string = "{}{}{}".format(stgs[0], " " * (diff), stgs[1])

            if not rightsym:
                new_string = "{}    ".format(new_string)
            widgets[j].config(text=new_string, width=maxx + 4)
            j += 1

    def bind_command(self, lab, text, v_row): 
        lab.bind('<Enter>', self.highlight)
        lab.bind('<Leave>', self.unhighlight)
        lab.bind("<Enter>", self.detect_drop2, add="+")
        lab.bind("<Leave>", self.close_drop2, add="+")
        lab.bind("<ButtonRelease-1>", self.close_drop_on_click, add="+")
        if ">" in text:
            return
        lab.bind("<Button-1>", v_row[1], add="+")

    def highlight(self, evt):
        evt.widget.config(bg=LabelHilited3.bg)

    def unhighlight(self, evt):
        evt.widget.config(bg=LabelHilited3.highlight_bg)

    def detect_drop2(self, evt):    

        def run_drop_delay(delay):
            self.after(delay, self.make_drop2, evt, row, sym, text)            

        widg = evt.widget
        row = widg.grid_info()['row']
        text = widg.cget('text').lower()
        for k,v in self.drop_items.items():
            if k != self.clicked:
                break
            if ">" in text:
                if v[row][0] == text.rstrip(">").rstrip():
                    sym = ">"
                    run_drop_delay(self.drop_delay)
                    break
            else:
                self.expand = False
                self.close_drop2()

    def show_recent_trees(self, evt):
        def populate_drop2_recent_files():
            x = 0
            for i in range(20):
                lab = LabelHilited3(self.drop2, anchor="w")
                if len(recent_files) >= x + 1:
                    lab.config(text=recent_files[x])
                    lab.grid(sticky='ew')
                    lab.bind("<ButtonRelease-1>", use_recent_tree, add="+")
                    lab.bind('<Enter>', self.highlight)
                    lab.bind('<Leave>', self.unhighlight)
                else:
                    break
                x += 1   

        def use_recent_tree(event):
            nonlocal recent_files
            close_tree(treebard=self.treebard)
            tree_title = event.widget.cget("text")
            current_file = "{}.tbd".format(tree_title.replace(" ", "_").lower())
            set_current_file(current_file)            
            save_recent_tree(tree_title, recent_files)
            for child in self.drop2.winfo_children():
                child.destroy()
            populate_drop2_recent_files()
            change_tree_title(self.treebard)
            self.treebard.make_main_window() 
            configall(self.root, formats)             

        recent_files = get_recent_files() 
        populate_drop2_recent_files()

    def show_list(self, list_to_use):
        format_strings = []
        text = ""
        lengths = []
        widgets = []
        row = 0
        for lst in list_to_use:
            lab = LabelHilited3(self.drop2, text=lst[0].title())
            symval = lst[2]
            if symval == ">":
                text = "{}    >".format(lst[0].title())
            elif symval == "...":
                text = "{}...    {}".format(lst[0].title(), " ")
            elif len(symval) != 0:                
                if symval.startswith("AA"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[0]
                elif symval.startswith("SS"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[1]
                elif symval.startswith("CA"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[2]
                elif symval.startswith("CS"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[3]
                elif symval.startswith("AS"):
                    symval = symval[2]
                    mod_key = MOD_KEYS[4]
                else:
                    mod_key = MOD_KEYS[5]
                text = "{}    {}+{}".format(lst[0].title(), mod_key, symval.upper())
            elif len(symval) == 0:
                text = "{}    {}".format(lst[0], " ")
            else:
                print("line", looky(seeline()).lineno, "case not handled:")

            lab.grid(column=0, row=row, sticky='w')
            lab.bind('<Enter>', self.highlight)
            lab.bind('<Leave>', self.unhighlight)
            lab.bind("<Button-1>", self.close_drop_on_click, add="+")
            format_strings.append(text)
            lengths.append(len(text))
            widgets.append(lab)
            row += 1

        self.fix_strings(
            lengths, list_to_use, format_strings, widgets)

    def make_drop2(self, evt, row, sym, text):
        for child in self.drop2.winfo_children():
            child.destroy()
        self.host2 = evt.widget
        for k,v in self.drop_items.items():
            row = 0
            for lst in v:
                text = text.split("    ")[0]
                if text == v[row][0]:
                    v[row][1](v[row][3])
                row += 1
        self.position_drop2()
        self.drop2.deiconify()
        self.drop2_is_open = True
        self.expand = True

    def position_drop2(self):
        self.drop2.geometry("+{}+{}".format(
            self.drop1.winfo_rootx() - 3 + self.drop1.winfo_reqwidth(), 
            self.host2.winfo_rooty())) 

    def close_drop2(self, evt=None):
        if self.drop1_is_open is True and self.expand is True:
            return

        def withdraw_drop2():
            self.drop2.withdraw()
            for child in self.drop2.winfo_children():
                child.destroy()

        def run_drop_delay(delay):
            self.after(delay, withdraw_drop2)

        run_drop_delay(self.drop_delay)
        self.drop2_is_open = False
        self.expand = False

    def position_drop1(self):
        app_west = self.root.winfo_rootx()
        app_north = self.root.winfo_rooty()
        west = self.host1.winfo_rootx()
        north = (
            self.host1.winfo_rooty() + self.host1.winfo_reqheight() + 
                (self.ipady * 2))
        self.drop1.geometry("+{}+{}".format(west, north))

    def open_drop1_on_click(self, evt):
        if self.drop1_is_open is True:
            if self.drop1_is_open is False:
                return
            if self.drop2_is_open is True and self.expand is False:
                return
            for child in self.drop1.winfo_children():
                child.destroy()
            self.drop1_is_open = False
            self.expand = False
            self.make_border(evt) 
            self.drop1.withdraw()
            return
        self.make_drop1(evt)
        self.clicked = evt.widget.cget("text").lower()
        self.drop1_is_open = True
        self.make_border(evt)  

    def open_drop1_on_hover(self, evt):
        if self.drop1_is_open is False:
            return
        self.make_drop1(evt)
        self.clicked = evt.widget.cget("text").lower() 

    def make_border(self, evt):
        if self.drop1_is_open is True:
            evt.widget.config(relief="sunken")
        elif self.drop1_is_open is False:
            evt.widget.config(relief="raised")

    def flatten_border(self, evt):
        evt.widget.config(relief="flat")

    def close_drop_on_click(self, evt):
        '''
            Handle miscellaneous clicks that should or should not close 
            the dropdown.
        '''        
        def close_it():
            self.drop1.withdraw()
            self.drop2.withdraw()
            self.drop1_is_open = False
            self.drop2_is_open = False
            self.expand = False

        if self.drop1_is_open is False:
            return

        if evt.widget.master != self:
            widg = evt.widget
            if widg.winfo_class() == "Label":
                text = widg.cget("text")
                if ">" not in text:
                    close_it()               
            else:
                close_it()

# from error_messages
def open_message(master, message, title, buttlab, inwidg=None):

    def close():
        """ Override this if more needs to be done on close. """        
        msg.destroy()
    msg = Dialogue(master)
    msg.canvas.title_1.config(text=title)
    msg.canvas.title_2.config(text="")
    lab = LabelHeader(
        msg.window, text=message, justify='left', wraplength=600)
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12, ipadx=6, ipady=3)
    button = Button(msg.window, text=buttlab, command=close, width=6)
    button.grid(column=0, row=1, padx=6, pady=(0,12))
    button.focus_set()
    msg.resize_window()

    return msg, lab, button

def open_input_message2(master, message, title, ok_lab, cancel_lab):
    '''
        For more primary-level input vs. error-level input.
    '''

    def ok():
        cancel()

    def cancel():
        msg.destroy()
        master.grab_set()

    def show():
        gotten = got.get()
        return gotten

    got = tk.StringVar()

    msg = Dialogue(master)
    msg.grab_set()
    msg.canvas.title_1.config(text=title)
    msg.canvas.title_2.config(text="")
    lab = LabelHeader(
        msg.window, text=message, justify='left', 
        font=("courier", 14, "bold"), wraplength=450)
    lab.grid(
        column=0, row=0, sticky='news', padx=12, pady=12, 
        columnspan=2, ipadx=6, ipady=3)
    inPut = Entry(
        msg.window, textvariable=got, width=48, 
        font=("dejavu sans mono", 14))
    inPut.grid(column=0, row=1, padx=12)
    buttonbox = Frame(msg.window)
    buttonbox.grid(column=0, row=2, sticky='e', padx=(0,12), pady=12)
    ok_butt = Button(
        buttonbox, text=ok_lab, command=cancel, width=7)
    ok_butt.grid(column=0, row=0, padx=6, sticky='e')
    cancel_butt = Button(
        buttonbox, text=cancel_lab, command=cancel, width=7)
    cancel_butt.grid(column=1, row=0, padx=6, sticky='e')
    inPut.focus_set()

    configall(msg, formats)
    msg.resize_window()
    master.wait_window(msg)
    gotten = show()
    return gotten

FONTS_THAT_MATCH_HEIGHT_OF_DEJAVU_SANS_MONO = ('alef', 'consolas', 'corbel light', 'courier', 'courier new', 'david clm', 'david libre', 'dejavu sans light', 'frank ruehl clm', 'frank ruhl hofshi', 'gabriola', 'gentium basic', 'gentium book basic', 'georgia', 'ink free', 'microsoft tai le', 'mingliu-extb', 'miriam clm', 'miriam mono clm', 'ms gothic', 'ms pgothic', 'ms serif', 'ms ui gothic', 'sansita', 'sansita black', 'sansita black italic', 'sansita extrabold', 'sansita light', 'sansita light italic', 'sansita medium', 'sansita medium italic', 'segoe script', 'simsun-extb', 'terminal', 'times new roman')

DEFAULT_OUTPUT_FONT = "courier"

class FontPicker(Frame):
    def __init__(self, master, root, main, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.main = main
        self.all_fonts = FONTS_THAT_MATCH_HEIGHT_OF_DEJAVU_SANS_MONO
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

        sample = Frame(self)

        self.output_sample = Label(
            sample,
            text="Sample Output Text ABCDEFGHxyz 0123456789 iIl1 o0O")

        self.label_sample = Label(sample, text="Sample Label Text")
        self.entry_sample = EntryAutoPerson(sample)
        self.entry_sample.insert(0, "Sample Input Text")

        self.fontSizeVar = tk.IntVar()
        self.font_size = self.font_scheme[1]

        self.font_sizer = Scale(
            self,
            from_=8.0,
            to=26.0,
            tickinterval=6.0,
            label="Text Size",
            orient="horizontal",
            length=200,
            variable=self.fontSizeVar,
            command=self.show_font_size)
        self.font_sizer.set(self.font_size)
 
        lab = Label(self, text="Select Output Font")
        self.cbo = Combobox(
            self, self.root, values=self.all_fonts, 
            height=500)

        message = ("Input font is dejavu sans mono. Its size can be changed. "
            "Output or label font can be changed with the combobox selection. "
            "The sample widgets at the top show a preview, or press APPLY to "
            "change font family and/or size for the whole application.",)
        instrux = Label(self, text=message[0], wraplength=640, justify="left")

        buttons = Frame(self)
        self.preview_button = Button(
            buttons, text="PREVIEW", command=self.preview_font, width=8)
        self.apply_button = Button(
            buttons, text="APPLY", command=self.apply_font, width=8)

        # children of self
        sample.grid(column=0, row=0)
        self.font_sizer.grid(column=0, row=1, pady=24)
        lab.grid(column=0, row=2, pady=(24,6))
        self.cbo.grid(column=0, row=3, pady=(6, 20))
        instrux.grid(column=0, row=4, padx=12)
        buttons.grid(column=0, row=5, pady=12, sticky="e")

        # children of sample
        self.output_sample.grid(column=0, row=0, padx=24, pady=20)
        self.label_sample.grid(column=0, row=1, sticky="e")
        self.entry_sample.grid(column=1, row=1, sticky="w")

        # children of buttons
        self.preview_button.grid(column=0, row=0, pady=12)
        self.apply_button.grid(column=1, row=0, pady=12) 

    def apply_font(self):
        self.font_scheme[1] = self.fontSizeVar.get()
        if len(self.cbo.get()) != 0:
            self.font_scheme[0] = self.cbo.get()
        else:
            self.font_scheme[0] = DEFAULT_OUTPUT_FONT
        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_format_font, tuple(self.font_scheme))
        conn.commit()
        cur.close()
        conn.close()
        self.formats = make_formats_dict()

        # These 5 lines are copied from TabBook class so could be 
        #   made a method there instead. The person tab scrollbar
        #   won't resize correctly unless it's made the active tab first.
        main_tabbook = self.main.main_tabs
        person_tab = main_tabbook.tabdict["person"][2] # page
        person_tab.grid()
        main_tabbook.active = main_tabbook.tabdict["person"][1] # tab
        main_tabbook.make_active()

        redraw_person_tab(
            main_window=self.main, 
            current_person=self.main.current_person, 
            current_name=self.main.current_person_name)

    def preview_font(self):
        selected = self.cbo.get()
        if selected not in self.all_fonts:
            selected = DEFAULT_OUTPUT_FONT
        for widg in (self.output_sample, self.label_sample):
            widg.config(font=(selected, self.font_size))
        self.entry_sample.config(font=("dejavu sans mono", self.font_size))

    def show_font_size(self, evt):
        self.font_size = self.fontSizeVar.get()

# from redraw.py

def redraw_person_tab(
        evt=None, main_window=None, current_person=None, current_name=None):        
    formats = make_formats_dict()
    current_file, current_dir = get_current_file()
    findings_table = main_window.findings_table
    main_window.update_idletasks()
    if current_person:
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_person, (current_person,))
        conn.commit()
        cur.close()
        conn.close()
    unbind_widgets(findings_table)
    redraw_current_person_area(
        current_person, main_window, current_name, current_file, current_dir)
    redraw_events_table(findings_table)
    if current_person:
        redraw_families_table(evt, current_person, main_window)

    configall(main_window.root, formats)
    resize_scrollbar(main_window.root, main_window.master)

def unbind_widgets(findings_table):
    for k,v in findings_table.kintip_bindings.items():
        if k == "on_enter":
            for lst in v:
                lst[0].unbind("<Enter>", lst[1])                    
        elif k == "on_leave":
            for lst in v:
                lst[0].unbind("<Leave>", lst[1])
        findings_table.kintip_bindings = {"on_enter": [], "on_leave": []}

    for k,v in findings_table.main_window.nukefam_table.idtip_bindings.items():
        if k == "on_enter":
            for lst in v:
                lst[0].unbind("<Enter>", lst[1])                    
        elif k == "on_leave":
            for lst in v:
                lst[0].unbind("<Leave>", lst[1])
        findings_table.main_window.nukefam_table.idtip_bindings = {
            "on_enter": [], "on_leave": []}

def redraw_current_person_area(
        current_person, main_window, current_name, current_file, current_dir):
    main_window.person_entry.delete(0, 'end')
    main_window.show_top_pic(current_file, current_dir, current_person)
    main_window.person_entry.current_id = None
    print("line", looky(seeline()).lineno, "current_file:", current_file)
    print("line", looky(seeline()).lineno, "current_name:", current_name)
    main_window.current_person_name = current_name
    main_window.current_person_label.config(
        text="Current Person (ID): {} ({})".format(current_name, current_person))

def redraw_families_table(evt, current_person, main_window):
    main_window.findings_table.kin_widths = [0, 0, 0, 0, 0, 0]
    for ent in main_window.nukefam_table.nukefam_inputs:
        ent.delete(0, "end")
    main_window.nukefam_table.ma_input.delete(0, "end")
    main_window.nukefam_table.pa_input.delete(0, "end")
    main_window.nukefam_table.new_kid_input.delete(0, "end")
    main_window.nukefam_table.new_kid_frame.grid_forget()
    main_window.nukefam_table.current_person_alt_parents = []
    main_window.nukefam_table.compound_parent_type = "Children's"        
    for widg in main_window.nukefam_table.nukefam_containers: 
        widg.destroy() 
    main_window.nukefam_table.parent_types = []
    main_window.nukefam_table.nukefam_containers = []

    main_window.nukefam_table.family_data = initialize_family_data_dict()

    if evt: # user pressed CTRL+S for example
        main_window.nukefam_table.make_nukefam_inputs(
            current_person=main_window.findings_table.current_person)
    else: # user pressed OK to change current person for example  
        main_window.nukefam_table.make_nukefam_inputs()

def redraw_events_table(findings_table):
    for lst in findings_table.cell_pool:
        for widg in lst[1]:
            if widg.winfo_subclass() == 'EntryAuto':
                widg.delete(0, 'end')
                # pass
            elif widg.winfo_subclass() == 'LabelButtonText':
                widg.config(text='')
            widg.grid_forget()
    findings_table.event_input.grid_forget()
    findings_table.add_event_button.grid_forget()

    findings_table.new_row = 0 
    findings_table.widths = [0, 0, 0, 0, 0]
    findings_table.kin_widths = [0, 0, 0, 0, 0, 0]
    findings_table.set_cell_content()
    findings_table.show_table_cells()

def resize_scrollbar(root, canvas):
    root.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

def fix_tab_traversal(families_table, findings_table):
    """ Create a tab traversal since the nukefam_table 
        can't be made first, but should be traversed first.
    """
    for table in (families_table, findings_table):
        table.lift()

def initialize_family_data_dict():
    """ This is mainly used in families.py but also used here in redraw.py
        for redrawing the person tab when changes are made by the user. Imports
        go from here to families.py.
    """
    family_data = [
        [
            [
                {'finding': None, 'sorter': [0, 0, 0]}, 
                {'id': None, 'name': '', 'kin_type_id': 2, 
                    'kin_type': 'father', 'labwidg': None, 'inwidg': None}, 
                {'id': None, 'name': '', 'kin_type_id': 1, 
                    'kin_type': 'mother', 'labwidg': None, 'inwidg': None}
            ],
        ],
        {},
    ]
    return family_data

# from utes.py

#   -   -   -   see toykinter_widgets.py for statusbar tooltips   -   -   -   #
#       which by now are built into the Border class in window_border.py

class ToolTip(object):
    '''
        TOOLTIPS BY MICHAEL FOORD 
        (used for ribbon menu icons and widgets dynamically gridded). 
        Don't use for anything that'll be destroyed by clicking because
        tooltips are displayed by pointing w/ mouse and thus a tooltip 
        will be displaying when destroy takes place thus leaving the 
        tooltip on the screen since the FocusOut that is supposed to 
        destroy the tooltip can't take place.
    '''

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        ''' Display text in tooltip window '''

        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        # self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = LabelStay(
            tw, 
            text=self.text, 
            justify='left',
            relief='solid', 
            bd=1,
            bg=NEUTRAL_COLOR, fg="white")
        # label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      # background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      # font=("tahoma", 10, "normal"),
                      # fg='black')
        label.pack(ipadx=6)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()    

def create_tooltip(widget, text):
    ''' Call w/ arguments to use M. Foord's ToolTip class. '''
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()

    toolTip = ToolTip(widget)
    widget.bind('<Enter>', enter, add="+")
    widget.bind('<Leave>', leave, add="+")

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

# from styles.py

""" Some special case widgets exist which require special attention to get them
    to change colors immediately upon changing the color scheme. These widgets
    include those which respond to hover events by changing color, those which
    have dropdown elements, and those 
    which have color schemes of their own. The technique for making this happen
    is simple and involves giving these widget classes a class-level variable
    for each of its changable colors.
"""
ALL_WIDGET_CLASSES = (
    Label, Button, LabelHilited3, LabelMovable, LabelStay,
    ButtonBigPic, Entry, Frame, Border, EntryAutoPersonHilited,
    Separator, ComboArrow, Scrollbar, FontPicker,
    LabelStatusbar, TabBook, DropdownMenu, ToplevelHilited)

activeBgFg_activeFgBg = ("ButtonFlatHilited",)
activeBgHead = ("ButtonQuiet", "ButtonPlain", "Button", "Scale")
activeBgHilite = ("Checkbutton", "Radiobutton", "RadiobuttonBig", )
activeFg = ("Checkbutton", "Radiobutton", "RadiobuttonBig", "Button")
bg_fg = (
    "LabelFrame", "Sizer", "Checkbutton", "Radiobutton", "ButtonQuiet", 
    "LabelH2", "LabelH3", "LabelEntry", "ButtonPlain", "Label", 
    "MessageCopiable", "Button", "Scale", "RadiobuttonBig", "LabelStatusbar", 
    "LabelSearch")
bg_fgHilite = ("ButtonBigPic",)
bgFg_fgBg = ("LabelNegative", )
bgHead = ("FrameHilited2", "LabelHilited", "LabelTip2")
bgHilite = (
    "FrameHilited", "FrameHilited3", "FrameHilited4","CanvasHilited", 
    "TitleBarButtonSolidBG", "Entry", "Text", "ComboArrow",  
    "ButtonFlatHilited", "LabelHeader", "LabelHilited3", "EntryAutoHilited", 
    "EntryAutoPersonHilited", ) 
fG = (
    "LabelTip2", "ButtonFlatHilited", "LabelHeader", "Entry",
    "ComboArrow", "EntryAutoPersonHilited", "EntryAutoHilited")
fontH2 = ("LabelH2", )
fontH3 = ("LabelH3", "LabelHeader", )
fontBoilerplate = ("ButtonQuiet", )
fontIn = (
    "LabelEntry", "ButtonPlain", "Entry", "Text", "EntryAutoHilited", 
    "EntryAutoPersonHilited")
fontOut = (
    "Label", "MessageCopiable", "Button", "Scale", "RadiobuttonBig", 
    "LabelNegative", "ComboArrow")
fontStatus = ("LabelStatusbar", "LabelTip2")
highlightbackground = ("Scale", )
highlightcolorHead = ("Scale", )
insertBgFg = (
    "Entry", "Text", "EntryAutoHilited", "EntryAutoPersonHilited")
selectBgHead = (
    "Entry", "Text", "EntryAutoHilited", "EntryAutoPersonHilited")
selectColorBg = ("Checkbutton", )
selectColorHilite = ("Radiobutton", "RadiobuttonBig")
selectFg = (
    "Entry", "Text", "EntryAutoHilited", "EntryAutoPersonHilited")
troughColorHilite = ("Scale", )
bgOnly = (
    "Frame", "Canvas", "FrameHilited6", "FontPicker",
    "Dialogue", "TabBook", "PersonSearch", "EditRow",
    "Gallery", "StatusbarTooltips", "EventsTable",
    "Main", "DatePreferences", "GedcomExceptions", "ScrolledText")

if __name__ == "__main__":

    from toykinter_widgets import run_statusbar_tooltips

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

    root = tk.Tk()

    canvas = Border(root, root)
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

    button = Button(window, text="RECOLORIZE", command=recolorize)
    ent2 = EntryAutoPerson(window, width=60)
    ent2.insert(0, "It's important to not be blinded by your computer screen.")

    ent3 = EntryAutoPerson(window, width=60)
    ent3.insert(0, "It's convenient to be able to read the words on the screen.")

    lh3_1 = LabelHilited3(window, text="These two labels are used in dropdown menu...")
    lh3_2 = LabelHilited3(window, text="...so they have to respond to events.")
    values = ["red", "green", "yellow", "blue"]
    combo1 = Combobox(window, root, values=values)
    combo2 = Combobox(window, root, values=values)
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

    l1.grid(column=0, row=0, pady=6)
    ent_colors.grid(column=1, row=0, pady=6)
    sep0.grid(column=0, row=1, pady=6, columnspan=2, sticky="ew")
    l5.grid(column=0, row=2, pady=6)
    l6.grid(column=0, row=3, pady=6)
    ent_font.grid(column=1, row=2, pady=6)
    ent_font_size.grid(column=1, row=3, pady=6)
    sep1.grid(pady=6, columnspan=2, sticky="ew")
    button.grid(pady=6)
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

    configall(root, formats)
    resize_scrolled_content(root, canvas, window)

    visited = (
        (ent_colors,
            "Color Scheme Input",
            "Input an official Treebard color_scheme_id."),
        (ent_font,
            "Font Family Input",
            "Input a font family that's on your computer."),
        (ent_font_size,
            "Font Size Input",
            "Input your preferred font size."))
    run_statusbar_tooltips(
        visited, 
        canvas.statusbar.status_label, 
        canvas.statusbar.tooltip_label)

    root.mainloop()

