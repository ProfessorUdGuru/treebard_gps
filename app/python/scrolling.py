# mousewheel_scrolling_without_permanent_dialogs

import tkinter as tk
from widgets import (Canvas, FrameHilited3, Entry, ToplevelHilited, Text,
    LabelHilited, ButtonFlatHilited, LabelTip2, CanvasHilited, Framex, Frame)
from styles import make_formats_dict, config_generic
import dev_tools as dt



'''
	One purpose of this module is to summarize how to make a canvas and 
    scrollbar do different things under a variety of circumstances.

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

    The class is a custom "Toykinter" widget based on the Tkinter API so using 
    it is almost identical to using the Tkinter scrollbar except that it can be 
    easily configured like any Tkinter widget instead of using Windows system 
    colors. Also it is optionally hideable; default for that option is False. 
    The complication with the hideable scrollbar is that it needs a place to be
    when it appears, so an offset--a blank space the same size as the hidden 
    scrollbar--had to be added to the required size of the window. Then a spacer 
    had to be added to the north and west edges of the window to balance this out. 
    These procedures increase the size of the window to prevent the scrollbar 
    from appearing before it's needed.

    II. CANVAS, SCROLLBAR AND WINDOW SIZING:

    There are several things that can have dimensions so think of them as a stack
    with the toplevel (root or dialog) on bottom:

        toplevel
        scrollregion
        canvas
        window (content frame)

    The canvas is a widget, gridded, packed or placed like any other widget.

    The "content frame" is a single frame covering the whole canvas, so that
    when the canvas is scrolled, the effect is that the content and all its 
    widgets are being scrolled. Since this frame is not gridded but created 
    by canvas.create_window(), in the code where it says 'window' this should be
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
    it could contain a smaller scrolled area of a fixed size. In this case, the 
    scrollregion doesn't get set to bbox('all') but to a fized size at least 
    the size of the canvas. The resizing methods are not needed here.

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
    ScrollApp, and Combobox classes below are the bee's knees, as well as the 
    Border class which is in window_border.py.

'''

formats = make_formats_dict()

def resize_scrolled_content(toplevel, canvas, window): 
    '''
        Besides configuring the scrollbar when the content changes, this 
        gives a hideable scrollbar a place to grid (scridth) so the 
        scrollbar doesn't appear before it's needed due to its own
        width. Extra space or "scridth" is added where the hidden scrollbars
        will appear. Extra spacer frames (such as scridth_n and scridth_w in
        main.py) are added to balance this out (don't do any of this with
        padding). The end result is a hideable scrollbar without a lop-sided 
        border around the canvas.
    '''

    def resize_scrollbar():
        toplevel.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    def resize_window():
        '''
            Don't try to detect scrollbar width (scridth) in this function.
            For some reason it causes certain combinations of values
            below to freeze the app. Hard-coded is good enough since there
            are only a few sizes of scrollbar. Add 10 to the scrollbar width 
            and that gives it wiggle room (makes it work right--not sure why).
        '''

        toplevel.update_idletasks()
        if toplevel.winfo_name() == 'view':
            bar_height = 96 # menubar + ribbon + statusbar
            scridth = 30
        else:
            bar_height = 27 # statusbar
            scridth = 26
        page_x = window.winfo_reqwidth() + scridth
        page_y = window.winfo_reqheight() + scridth + bar_height
        toplevel.geometry('{}x{}'.format(page_x, page_y))

    resize_scrollbar()
    resize_window()

class MousewheelScrolling():
    def __init__(self, root, main_canvas):

        self.root = root
        self.scroll_this = self.main_canvas = main_canvas

        # self.resizable_canvases = [None, None]
        # self.nested_canvases = [None]
        self.resizable_canvases = []
        self.nested_canvases = []
# WHENEVER A WIDGET is added to these lists (except root), bind them to destroy evt so if they are destroyed they are autoremoved from the list. Best if I can autodetect when a list is changed so the new members can autobind to destroy. Do this by making a method that appends things to the list. When the method runs, the things get bound.
    def scroller(self, event):
        '''
            The error is when the mousewheel is used over a toplevel 
            with no canvas, which happens because there are Comboboxes 
            in dialogs that have a fixed size and don't need to scroll.
            Saving this for later when mousewheel functionality is 
            added to the Combobox dropdown.
        '''
        
        # self.scroll_this.yview_scroll(
            # int(-1*(event.delta/120)), 'units')
        # DO NOT DELETE
        try:
            self.scroll_this.yview_scroll(
                int(-1*(event.delta/120)), 'units')
        except AttributeError:
            pass
        
    def look_under_mouse(self, evt):
        self.root.bind_all('<MouseWheel>', self.scroller)
        evt.widget.bind('<Enter>', self.look_under_mouse)
        self.scroll_this = evt.widget
        evt.widget.bind('<Leave>', self.forget_canvas) 

    def forget_canvas(self, evt):
        canvas_left = evt.widget
        if canvas_left is self.main_canvas:
            canvas_left.unbind_all('<MouseWheel>') 
        elif canvas_left in self.nested_canvases:
            self.scroll_this = self.main_canvas 
        else:
            canvas_left.unbind_all('<MouseWheel>') 

    def remove_from_list(self, evt):
        canvas = evt.widget
        resizers = [i[0] for i in self.resizable_canvases]
        nesteds = self.nested_canvases
        if canvas in resizers:
            idx = resizers.index(canvas)
            del self.resizable_canvases[idx]
        elif canvas in nesteds:
            idx = nesteds.index(canvas)
            del self.nested_canvases[idx]

    def append_to_list(self, appendee, resizable=True):
        if resizable is True:
            self.resizable_canvases.append(appendee)
            appendee = appendee[0]
        else:
            self.nested_canvases.append(appendee)
        appendee.bind('<Destroy>', self.remove_from_list)

    def configure_mousewheel_scrolling(
            self,
            in_root=False):

        if in_root is True:
            self.root.bind_all('<MouseWheel>', self.scroller)
        self.root.update_idletasks()

        for canvas in self.resizable_canvases:
            canvas[0].bind('<Enter>', self.look_under_mouse)
        for canvas in self.nested_canvases:
            canvas.bind('<Enter>', self.look_under_mouse)
        for canvas in self.resizable_canvases:
            canvas, window = canvas[0], canvas[1]
            resize_scrolled_content(canvas.master, canvas, window)

class Scrollbar(Canvas):
    '''
        A scrollbar is gridded as a sibling of what it's scrolling. Set the 
        command attribute during construction; it's a python keyword argument 
        but not a Tkinter option so vscroll.config(command=self.yview) won't 
        work. This scrollbar works well and can be made any size or color. It's
        lacking the little arrows at the ends of the trough, which aren't 
        needed, in my opinion, except when scrolling technical stuff line by 
        line. But the little arrows can be added sometime.
    '''

    def __init__(
        self, master, width=16, orient='vertical', hideable=False, **kwargs):

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

        self.slidercolor = formats['bg']
        self.troughcolor = formats['head_bg']

        if orient == 'vertical':
            self.config(width=width)
        elif orient == 'horizontal':
            self.config(height=width)

        self.config(bg=self.troughcolor, bd=0, highlightthickness=0)

        self.create_rectangle(
            0, 0, 1, 1, 
            fill=self.slidercolor, 
            width=1,    # this is border width
            outline=formats['highlight_bg'], 
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

        height = self.winfo_height()
        width = self.winfo_width()

        if self.orient == 'vertical':
            x0 = 0
            y0 = max(int(height * lo), 0)
            x1 = width - 1
            y1 = min(int(height * hi), height)
        elif self.orient == 'horizontal':
            x0 = max(int(width * lo), 0)
            y0 = 0
            x1 = min(int(width * hi), width)
            y1 = height -1

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

    def colorize(self):
        formats = make_formats_dict()
        self.slidercolor = formats['bg']
        self.troughcolor = formats['head_bg']
        self.config(bg=self.troughcolor)

class Combobox(FrameHilited3):

    '''
        This is in the scrolling module to remind me to add mousewheel
        scrolling to the combobox dropdown sometime, but it's not critical.
    '''

    hive = []

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
            "Toykinter" widgets are just Tkinter widgets cobbled together with
            Tkinter (not ttk) building blocks and Python code. They exist so
            that purely Tkinter methods can be used to configure them. They were
            created because their author--a coding novice--wants his app to be
            easily configurable with one set of procedures instead of using
            ttk.Style in addition to the classic Tkinter configuration methods.
            This Toykinter combobox replaces the ttk.Combobox. It works best 
            if the Border class is used to replace the Windows title bar and
            resizing grips/borders etc. The main problem with this combobox
            if the Windows border is used is that clicking the Windows
            border doesn't close a combobox dropdown. This is mostly a
            cosmetic problem; the combobox still works. A dropdown can still
            be closed by clicking any Tkinter widget; the Windows title bar
            is not a Tkinter widget. The Combobox dropdown has a vertical
            scrollbar (also a Toykinter widget; see this module) which is hidden
            until needed. Currently the dropdown doesn't scroll with the
            mousewheel but that can be fixed by extending the method 
            configure_mousewheel_scrolling() in the MousewheelScrolling class (this module).
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

        self.make_widgets()
        self.master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')

        # expose only unique methods of Entry e.g. not self.config (self is a Frame and
        #    the Entry, Toplevel, Canvas, and window have to be configured together) so
        #    to size the entry use instance.config_drop_width(72)
        self.insert = self.entry.insert
        self.delete = self.entry.delete
        self.get = self.entry.get

    def make_widgets(self):
        self.entry = Entry(self, textvariable=self.var)
        self.arrow = LabelHilited(self, text='\u25BC', width=2)

        self.entry.grid(column=0, row=0)
        self.arrow.grid(column=1, row=0)

        self.update_idletasks()
        self.width = self.winfo_reqwidth()

        self.drop = ToplevelHilited(
            self,
            bd=0)
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
            self.drop, hideable=True, command=self.canvas.yview)
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
            frm.bind('<FocusIn>', self.highlight_arrow)
            frm.bind('<FocusOut>', self.unhighlight_arrow)

        self.drop.bind('<FocusIn>', self.focus_dropdown)
        self.drop.bind('<Unmap>', self.unhighlight_all_drop_items)

        self.current_combo_parts = [self, self.entry, self.arrow, self.scrollv_combo]
        for part in self.current_combo_parts:
            part.bind('<Enter>', self.unbind_combo_parts)
            part.bind('<Leave>', self.rebind_combo_parts)

        self.config_values(self.values)
        
        config_generic(self.drop)

    def unbind_combo_parts(self, evt):
        self.master.unbind_all('<ButtonRelease-1>')

    def rebind_combo_parts(self, evt):
        self.master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')

    def unhighlight_all_drop_items(self, evt):
        for child in self.content.winfo_children():
            child.config(bg=formats['highlight_bg'])

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

        b = ButtonFlatHilited(self.content, text='Sample')
        one_height = b.winfo_reqheight()
        b.destroy()
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
            bt.bind('<Enter>', self.highlight)
            bt.bind('<Leave>', self.unhighlight)
            bt.bind('<Tab>', self.tab_out_of_dropdown_fwd)
            bt.bind('<Shift-Tab>', self.tab_out_of_dropdown_back)
            bt.bind('<KeyPress>', self.traverse_on_arrow)
            bt.bind('<FocusOut>', self.unhighlight)
            bt.bind('<FocusOut>', self.get_tip_widg, add='+')
            bt.bind('<FocusIn>', self.get_tip_widg)
            bt.bind('<Enter>', self.get_tip_widg, add='+')
            bt.bind('<Leave>', self.get_tip_widg, add='+')
            self.buttons.append(bt)
            c += 1
        for b in self.buttons:
            b.config(command=self.callback)

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

    def highlight_arrow(self, evt):
        self.arrow.config(bg=formats['head_bg'])

    def unhighlight_arrow(self, evt):
        self.arrow.config(bg=formats['highlight_bg'])

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
            added the try/except to pass on it instead of figuring out a
            proper solution.
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
        if evt is None: # dropdown item clicked--no evt bec. of Button command option
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
                first.config(bg=formats['bg'])
                first.focus_set()
                self.canvas.yview_moveto(0.0)
            elif evt_sym == 'Up':
                last.config(bg=formats['bg'])
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

    def highlight(self, evt):
        for widg in self.buttons:
            widg.config(bg=formats['highlight_bg'])
        widg = evt.widget
        self.update_idletasks()
        widg.config(bg=formats['bg'])
        self.selected = widg
        widg.focus_set()

    def unhighlight(self, evt):
        widg = evt.widget
        x, y = self.winfo_pointerxy()
        hovered = self.winfo_containing(x,y)
        if hovered in self.buttons:
            widg.config(bg=formats['highlight_bg'])

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
            widg.config(bg=formats['highlight_bg'])
        if evt_type == '4':
            self.selected = evt.widget
        elif evt_type == '2' and evt_sym == 'Down':
            self.selected = next_item
        elif evt_type == '2' and evt_sym == 'Up':
            self.selected = prev_item

        self.selected.config(bg=formats['bg'])
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
        self.trigger_down = self.height - self.widg_height * 3
        self.trigger_up = self.height - self.widg_height * 2
        self.update_idletasks()
        next_item = widg.tk_focusNext()
        prev_item = widg.tk_focusPrev()
        rel_ht = widg.winfo_y()

        if sym == 'Down':
            if next_item in self.buttons:
                self.highlight_on_traverse(evt, next_item=next_item)
            else:
                next_item = self.buttons[0]
                next_item.focus_set()
                next_item.config(bg=formats['bg'])
                self.canvas.yview_moveto(0.0)

        elif sym == 'Up':
            if prev_item in self.buttons:
                self.highlight_on_traverse(evt, prev_item=prev_item)
            else:
                prev_item = self.buttons[self.lenval-1]
                prev_item.focus_set()
                prev_item.config(bg=formats['bg'])
                self.canvas.yview_moveto(1.0)

    def callback(self):
        '''
            A function specified on instantiation.
        '''
        print('scr 927 this will not print if overridden (callback)')

    def combobox_selected(self):
        '''
            A function specified on instantiation will run when
            the selection is made. Similar to ttk's <<ComboboxSelected>>
            but instead of binding to a virtual event, just pass the
            name of the function in the constructor.
        '''
        print('scr 936 this will not print if overridden (combobox_selected)')

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
        self.text.configure(yscrollcommand=self.ysb.set)
        self.ysb.grid(column=1, row=0, sticky='ns')

        self.bind_class('Text', '<Tab>', self.focus_next_window)
        self.bind_class('Text', '<Shift-Tab>', self.focus_prev_window)

    # make the Text widget use tab key for traversal like other widgets
    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return('break')

    def focus_prev_window(self, event):
        event.widget.tk_focusPrev().focus()
        return('break')

class ScrolledTextSaver(Framex):
    def __init__(self, master, use_input, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.text = TextSaver(self, use_input)
        self.text.grid(column=0, row=0)
        self.ysb = Scrollbar(
            self, 
            width=16,
            orient='vertical', 
            hideable=True,
            command=self.text.yview)
        self.text.configure(yscrollcommand=self.ysb.set)
        self.ysb.grid(column=1, row=0, sticky='ns')

        # expose methods of the Text widget
        self.config = self.text.config
        self.bind = self.text.bind 

if __name__ == '__main__':

    from widgets import (Frame, Toplevel, LabelStay, Button)

    root = tk.Tk()
    root.title('ROOT WINDOW')
    root.geometry('500x400+800+200')

    def open_top2():

        def close_top2():
            top2.destroy()

        top2 = Toplevel(root)
        top2.title('SCROLLED WINDOW')
        canvas2 = Canvas(top2)
        canvas2.content = Frame(canvas2)
        canvas2.content.columnconfigure(0, weight=1)
        canvas2.content.rowconfigure(0, weight=1)
        canvas2.vsb = Scrollbar(
            top2, hideable=True, width=20, command=canvas2.yview)
        canvas2.hsb = Scrollbar(
            top2, orient='horizontal', hideable=True, 
            width=20, command=canvas2.xview)
        canvas2.config(
            xscrollcommand=canvas2.hsb.set, 
            yscrollcommand=canvas2.vsb.set)
        canvas2.create_window(0, 0, anchor='nw', window=canvas2.content)
        close2 = Button(canvas2.content, text='CLOSE', command=close_top2)
        top2.columnconfigure(0, weight=1)
        top2.rowconfigure(0, weight=1)
        canvas2.grid(column=0, row=0, sticky='news')
        canvas2.hsb.grid(column=0, row=1, sticky='ew')
        canvas2.vsb.grid(column=1, row=0, sticky='ns')
        cbo2 = Combobox(
            canvas2.content, root, values=values, height=200, scrollbar_size=12)
        cbo2.grid(column=0, row=0)
        close2.grid(column=0, row=1)

        lab2 = LabelStay(
            canvas2.content, 
            text='This is a scrolled toplevel\nThis is a scrolled toplevel\n'
                'This is a scrolled toplevel\nThis is a scrolled toplevel\n'
                'This is a scrolled toplevel', 
            font=('courier', 45))
        lab2.grid()

        # mousewheel scrolling part 3 of 3
        scroll_mouse.append_to_list([canvas2, canvas2.content])
        scroll_mouse.configure_mousewheel_scrolling()

    def make_widgets_unscrolled_dialog():
        lab1 = LabelStay(
            top1, 
            text='This is an unscrolled toplevel\nThis is an unscrolled toplevel\n'
                'This is an unscrolled toplevel\nThis is an unscrolled toplevel\n'
                'This is an unscrolled toplevel', 
            font=('courier', 24))
        lab1.grid()

    def make_content_fixed_size_canvas():

        lab3 = LabelStay(
            canvas3.content, 
            text='This is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size\nThis is a nested scrolled canvas with a fixed size', 
            font=('courier', 18))   
     
        lab3.grid(column=0, row=0)

        cbo3 = Combobox(canvas3.content, root, values=values, height=200, scrollbar_size=12)
        cbo3.grid(column=0, row=1)

        root.update_idletasks()
        width = canvas3.content.winfo_reqwidth()
        height = canvas3.content.winfo_reqheight()

        return width, height, cbo3

    values = ('red', 'white', 'blue', 'yellow', 'greennnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn', 'pink', 'orange')

    treebard=None

    # main canvas
    canvas = Canvas(root)
    scroll_this = canvas
    canvas.content = Frame(canvas)
    canvas.content.rowconfigure(0, weight=1)
    vsb = Scrollbar(root, hideable=True, width=24, command=canvas.yview)
    hsb = Scrollbar(
        root, orient='horizontal', hideable=True, width=24, command=canvas.xview)
    canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
    canvas.create_window(0, 0, anchor='nw', window=canvas.content)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    canvas.grid(column=0, row=0, sticky='news')
    hsb.grid(column=0, row=2, sticky='ew')
    vsb.grid(column=1, row=0, sticky='ns')

    f1 = Frame(canvas.content)
    f2 = Frame(canvas.content)
    f3 = Frame(canvas.content)
    f1.pack(side='top', fill='x')
    f2.pack(side='top', fill='x')
    f3.pack(side='top', fill='x')

    top1 = Toplevel(root)
    top1.title('UNSCROLLED WINDOW') 

    lab = LabelStay(
        f1,
        text='This is the root window\nThis is the root window\n'
            'This is the root window\nThis is the root window\n'
            'This is the root window', 
        font=('courier', 48))
    lab.grid(column=0, row=0)

    # mousewhele scrolling part 1 of 3
    #   Instantiate mousewheel scrolling once for the whole app
    #   and do it before any command that opens a participating dialog.
    scroll_mouse = MousewheelScrolling(root, canvas)
    open0 = Button(
        f1, 
        text='OPEN DIALOG', 
        command=lambda scr=scroll_mouse: open_top2())
    open0.grid(column=0, row=1)
    make_widgets_unscrolled_dialog()

    # nested canvas fixed size
    canvas3 = Canvas(f2, width=500, height=300)
    canvas3.content = Frame(canvas3)
    vsb3 = Scrollbar(f2, width=16, command=canvas3.yview)
    hsb3 = Scrollbar(
        f2, width=16, orient='horizontal', 
        command=canvas3.xview)
    canvas3.config(xscrollcommand=hsb3.set, yscrollcommand=vsb3.set)
    canvas3.create_window(0, 0, anchor='nw', window=canvas3.content)
    width, height, cbo3 = make_content_fixed_size_canvas()
    canvas3.config(scrollregion=(0, 0, width, height))
    canvas3.grid(column=0, row=1, sticky='news')
    hsb3.grid(column=0, row=2, sticky='ew')
    vsb3.grid(column=1, row=1, sticky='ns')

    cbo = Combobox(f3, root, values=values, height=200, scrollbar_size=12)
    cbo.grid(column=0, row=0)

    # mousewheel scrolling part 2 of 3
    scroll_mouse.append_to_list([canvas, canvas.content])
    scroll_mouse.append_to_list(canvas3, resizable=False)
    scroll_mouse.configure_mousewheel_scrolling(in_root=True)
    
    config_generic(root)
    root.mainloop()

