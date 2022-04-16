# widgets.py

import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from styles import make_formats_dict, NEUTRAL_COLOR
from utes import create_tooltip  
import dev_tools as dt
from dev_tools import looky, seeline



formats = make_formats_dict()

# print('formats is', formats)
# formats is {'bg': '#34615f', 'highlight_bg': '#4a8a87', 'head_bg': '#486a8c', 'fg': '#b9ddd9', 'output_font': ('courier', 16), 'input_font': ('tahoma', 16), 'heading1': ('courier', 32, 'bold'), 'heading2': ('courier', 24, 'bold'), 'heading3': ('courier', 17, 'bold'), 'heading4': ('courier', 13, 'bold'), 'status': ('tahoma', 13), 'boilerplate': ('tahoma', 10), 'show_font': ('tahoma', 16, 'italic'), 'titlebar_0': ('tahoma', 10, 'bold'), 'titlebar_1': ('tahoma', 14, 'bold'), 'titlebar_2': ('tahoma', 16, 'bold'), 'titlebar_3': ('tahoma', 20, 'bold'), 'titlebar_hilited_0': ('tahoma', 10), 'titlebar_hilited_1': ('tahoma', 14), 'titlebar_hilited_2': ('tahoma', 16), 'titlebar_hilited_3': ('tahoma', 20), 'unshow_font': ('tahoma', 14, 'italic')}

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

class LabelHilited(Labelx):
    """ Used in Combobox for arrow. """
    formats = formats
    head_bg = formats["head_bg"]
    fg = formats["fg"]
    output_font = formats["output_font"]
    highlight_bg = formats["highlight_bg"]

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs) 
        self.config(
            bg=LabelHilited.highlight_bg, 
            fg=LabelHilited.fg,
            font=LabelHilited.output_font)

    def highlight(self, evt):
        self.config(bg=LabelHilited.head_bg)

    def unhighlight(self, evt):
        self.config(bg=LabelHilited.highlight_bg)

class LabelHilited3(Labelx):
    ''' 
        Like Label with a different background and a monospaced sans-serif font. 
        Because it's monospaced, this font is ideal for places such as dropdown
        menus where a single label needs to have both flush left and flush right
        text with variable space in the middle keeping both strings flush. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()

        self.config(
            bg=self.formats['highlight_bg'], 
            fg=self.formats['fg'],
            font=self.formats['input_font'])

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

class LabelButtonImage(Labelx):
    """ A label that looks and works like a button. Good for
        images since it sizes itself to its contents, so don't
        add width and height to this class or change its color.
        The class-level variables are used by the child class that
        inherits from it.
    """
    formats = formats
    bg = formats["bg"]
    head_bg = formats["head_bg"]
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

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
        formats = make_formats_dict()
        self.config(relief='sunken', bg=LabelButtonImage.head_bg)
        # self.config(relief='sunken', bg=formats['head_bg'])

    def on_release(self, evt):
        formats = make_formats_dict()
        self.config(relief='raised', bg=LabelButtonImage.bg)
        # self.config(relief='raised', bg=formats['bg'])

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

class LabelButtonText(LabelButtonImage):
    """ A label that looks and works like a button. Displays text. See its
        parent class for class variables used by colorizer.
    """
    def __init__(self, master, width=8, *args, **kwargs):
        LabelButtonImage.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()

        self.config(
            anchor='center',
            borderwidth=1, 
            relief='raised', 
            takefocus=1,
            bg=self.formats['bg'],
            width=width,
            font=self.formats['input_font'],
            fg=self.formats['fg'])

class LabelDots(LabelButtonText):
    ''' 
        Display clickable dots if more info, no dots 
        if no more info. 
    '''
    def __init__(
            self, 
            master,
            dialog_class,
            treebard,
            formats,
            person_autofill_values=None,
            *args, **kwargs):
        LabelButtonText.__init__(self, master, *args, **kwargs)

        self.master = master
        self.dialog_class = dialog_class
        self.treebard = treebard
        self.formats = formats
        self.person_autofill_values = person_autofill_values

        self.current_person = None
        
        self.root = master.master

        self.finding_id = None
        self.header = []
        self.config(width=5, font=self.formats['heading3'])
        self.bind('<Button-1>', self.open_dialog)
        self.bind('<Return>', self.open_dialog)
        self.bind('<space>', self.open_dialog)

    def open_dialog(self, evt):
        dlg = self.dialog_class(
            self.master, 
            self.finding_id, 
            self.header, 
            self.current_person,
            self.treebard,
            self.formats,
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

class LabelButtonImage(Labelx):
    ''' 
        A label that looks and works like a button. Good for
        images since it sizes itself to its contents, so don't
        add width and height to this class or change its color.
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

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
        formats = make_formats_dict()
        self.config(relief='sunken', bg=formats['head_bg'])

    def on_release(self, evt):
        formats = make_formats_dict()
        self.config(relief='raised', bg=formats['bg'])

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

class LabelButtonText(LabelButtonImage):
    ''' 
        A label that looks and works like a button. Displays Text.
    '''

    def __init__(self, master, width=8, *args, **kwargs):
        LabelButtonImage.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['input_font'],
            anchor='center',
            borderwidth=1, 
            relief='raised', 
            takefocus=1,
            width=width)

class LabelMovable(LabelHilited):
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
    head_bg = formats["head_bg"]
    highlight_bg = formats["highlight_bg"]

    def __init__(self, master, first_column=0, first_row=0, *args, **kwargs):
        LabelHilited.__init__(self, master, *args, **kwargs)

        self.master = master
        self.first_column = first_column
        self.first_row = first_row

        self.config(
            takefocus=1, 
            bg=LabelMovable.highlight_bg, 
            fg=LabelMovable.fg, 
            font=formats['output_font'])
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

    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()
        self.config(
            bd=0, 
            relief="flat",
            bg=self.formats['bg'],  
            fg=self.formats['highlight_bg'],
            cursor='hand2')
        self.bind('<FocusIn>', self.highlight)
        self.bind('<FocusOut>', self.unhighlight)

    def highlight(self, evt):
        self.config(bg=self.formats['fg'])

    def unhighlight(self, evt):
        self.config(bg=self.formats['bg'])

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
            insertbackground=formats['fg']) 

class EntryUnhilited(Entryx):
    '''
        Looks like a Label.
    '''
    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        
        self.config(
            bd=0,
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'])

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
        All my toplevels have to declare a parent whether they need one or not.
        This keeps the code consistent and symmetrical across all widgets,
        even though Tkinter doesn't require a parent for its Toplevel.
    '''

    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Toplevel(Toplevelx):
    def __init__(self, master, *args, **kwargs):
        Toplevelx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'])

class ToplevelHilited(Toplevelx):
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
            highlightthickness=0) 

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



