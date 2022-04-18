# toykinter_widgets.py

from widgets import Framex, FrameStay, Labelx, Frame, Label, make_formats_dict
from files import app_path
from PIL import Image, ImageTk
import dev_tools as dt
from dev_tools import looky, seeline




formats = make_formats_dict()

# ************** statusbar tooltips sizegrip **************

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

def run_statusbar_tooltips(visited, status_label, tooltip_label):
    '''
        Uses lambda to add args to event
        since tkinter expects only one arg in a callback.
    '''

    def handle_statusbar_tooltips(event):
        for tup in visited:
            if tup[0] is event.widget:
                if event.type == '9': # FocusIn
                    status_label.config(text=tup[1])
                elif event.type == '10': # FocusOut
                    status_label.config(text='')
                elif event.type == '7': # Enter
                    tooltip_label.grid(
                        column=1, row=0, 
                        sticky='e', padx=(6,24))
                    tooltip_label.config(
                        text=tup[2],
                        bg='black',
                        fg='white',
                        font=LabelStatusbar.formats["status"])
                elif event.type == '8': # Leave
                    tooltip_label.grid_remove()
                    tooltip_label.config(
                        bg=formats['bg'], text='', fg=formats['bg'])

    statusbar_events = ['<FocusIn>', '<FocusOut>', '<Enter>', '<Leave>']

    for tup in visited:
        widg = tup[0]
        status = tup[1]
        tooltip = tup[2]
        for event_pattern in statusbar_events:
            # error if tup[0] has been destroyed 
            #   so don't use these with destroyable widgets
            # different tooltips are available in utes.py
            widg.bind(event_pattern, handle_statusbar_tooltips, add='+')

        status_label.config(font=formats['status'])

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






