# combobox

'''
    Replaces ttk.Combobox with an easily configurable widget.

    Configuration is done tkinter style, instead of pitting ttk.Style
    and Windows themes against each other to see which one wins, as is
    the norm when trying to configure ttk widgets.

    Unlike ttk.Combobox...
        ...dropdown items are selected with mouse, Return key, or spacebar
        ...colors including Entry background are easily configured
        ...clicking either Entry or Arrow opens then closes dropdown on 
            alternate clicks
        ...FocusOut event can be bound to the dropdown items (still to test)
        ...arrow traversal thru dropdown loops to top or bottom when bottom 
            or top is reached
        ...dropdown opens with either Up or Down arrow key, with either top 
            or bottom item highlighted
        ...a long dropdown auto-scrolls while traversing with arrow keys
        ...a dropdown item with text longer than the window displays a tooltip 
            that shows the whole text
        ...the arrow button changes color when the Entry is in focus.
'''

import tkinter as tk
from widgets import (FrameHilited3, Entry, ToplevelHilited, 
    LabelHilited, ButtonFlatHilited, LabelTip2)
from scrolling import CanvasScrolledBG2
from styles import config_generic, make_formats_dict
import dev_tools as dt



formats = make_formats_dict()

class Combobox(FrameHilited3):
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

        self.make_widgets()
        master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')
        self.root.bind('<Configure>', self.hide_all_drops)

    def close_dropdown(self, evt):
        '''
            Runs only on ButtonRelease-1.
        '''
        widg = evt.widget
        if widg == self.canvas.vert:
            self.scrollbar_clicked = True
        if widg in (self, self.arrow, self.entry, self.canvas.vert):
            return
        self.drop.withdraw()

    def make_widgets(self):

        self.entry = Entry(self, textvariable=self.var)
        self.arrow = LabelHilited(self, text='\u25BC', width=2)

        self.entry.grid(column=0, row=0)
        self.arrow.grid(column=1, row=0, padx=0, pady=0)

        self.next_on_tab = self.tk_focusNext()
        self.prev_on_tab = self.tk_focusPrev()

        self.update_idletasks()
        self.width = self.winfo_reqwidth()

        self.drop = ToplevelHilited(
            self,
            bd=0)
        self.drop.withdraw()
        Combobox.hive.append(self.drop)
        self.master.bind('<Escape>', self.hide_all_drops)

        self.drop.grid_columnconfigure(0, weight=1)
        self.drop.grid_rowconfigure(0, weight=1)

        self.canvas = CanvasScrolledBG2(
            self.drop,
            fixed_width=True,
            scrollregion_width=self.width,
            scrollbar='vert')
        self.canvas.grid(column=0, row=0, sticky='news')

        self.canvas.content.grid_columnconfigure(0, weight=1)
        self.canvas.content.grid_rowconfigure('all', weight=1)

        self.canvas.vert.grid(column=1, row=0, sticky='ns') 

        self.entry.bind('<KeyPress>', self.open_or_close_dropdown)

        for widg in (self.entry, self.arrow):
            widg.bind('<Button-1>', self.open_or_close_dropdown)
    
        self.arrow.bind('<Button-1>', self.focus_entry_on_arrow_click, add='+')        

        for frm in (self, self.canvas.content):
            frm.bind('<FocusIn>', self.highlight_arrow)
            frm.bind('<FocusOut>', self.unhighlight_arrow)

        self.drop.bind('<FocusIn>', self.focus_dropdown)

        self.config_values(self.values)
        config_generic(self.drop)

    def config_values(self, values):
        b = ButtonFlatHilited(self.canvas.content, text='Sample')
        one_height = b.winfo_reqheight()
        b.destroy()
        self.fit_height = one_height * len(values)

        self.values = values
        self.lenval = len(self.values)

        for button in self.buttons:
            button.destroy()
        self.buttons = []

        CanvasScrolledBG2.config_fixed_width_canvas(self)

        c = 0
        for item in values:
            bt = ButtonFlatHilited(self.canvas.content, text=item, anchor='w')
            bt.grid(column=0, row=c, sticky='ew') 
            # for event in ('<Return>', '<space>'): 
            for event in ('<Button-1>', '<Return>', '<space>'):
                bt.bind(event, self.get_clicked)
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
            on highlight. Some of this code is borrowed from Michael Foord.
        '''

        text=widg.cget('text')

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

    def hide_all_drops(self, evt):
        for dropdown in Combobox.hive:
            dropdown.withdraw()

    def open_or_close_dropdown(self, evt=None):
        if evt is None: # dropdown item clicked--no evt bec. of Button command option
            if self.callback:
                self.callback(self.selected)
            self.drop.withdraw()
            return
        evt_type = evt.type
        evt_sym = evt.keysym
        first = self.buttons[0]
        print('245 self.lenval is', self.lenval)
        last = self.buttons[self.lenval - 1]
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
        y_off = self.winfo_reqheight()

        self.fit_height = self.canvas.content.winfo_reqheight()
        self.drop.wm_overrideredirect(1)
        fly_up = self.get_vertical_pos()
        if fly_up[0] is False:
            y = y + y_off
        else:
            y = fly_up[1]
       
        self.drop.geometry('{}x{}+{}+{}'.format(
            self.width, self.height, x, y)) 
        self.drop.deiconify() 
        self.hide_other_drops()

    def get_vertical_pos(self):

        fly_up = False
        self.update_idletasks()
        vertical_pos = self.winfo_rooty()
        vertical_rel = self.winfo_y()
        combo_height = self.winfo_reqheight()
        top_o_drop = vertical_pos + vertical_rel + combo_height
        clearance = self.screen_height - top_o_drop

        if clearance < self.height:
            fly_up = True

        return (fly_up, vertical_pos - self.height)

    def highlight(self, evt):
        widg = evt.widget
        self.update_idletasks()
        widg.config(bg=formats['bg'])

    def unhighlight(self, evt):
        widg = evt.widget
        widg.config(bg=formats['highlight_bg'])

    def focus_dropdown(self, evt):
        for widg in self.buttons:
            widg.config(takefocus=1)

    def tab_out_of_dropdown_fwd(self, evt):

        for widg in self.buttons:
            widg.config(takefocus=0)

        self.selected = evt.widget
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.selected.cget('text'))
        next_on_tab = self.tk_focusNext()
        next_on_tab = next_on_tab.tk_focusNext()
        next_on_tab.focus_set()

    def tab_out_of_dropdown_back(self, evt):

        for widg in self.buttons:
            widg.config(takefocus=0)

        self.selected = evt.widget
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.selected.cget('text'))
        prev_on_tab = self.tk_focusPrev()
        prev_on_tab.focus_set()

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
        print('this will not print if overridden (callback)')

    def combobox_selected(self):
        '''
            A function specified on instantiation will run when
            the selection is made. Similar to ttk's <<ComboboxSelected>>
            but instead of binding to a virtual event, just pass the
            name of the function in the constructor.
        '''
        print('this will not print if overridden (combobox_selected)')

if __name__ == '__main__':

    from widgets import FrameStay, Label
    from scrolling import CanvasScrolledBG1, CanvasScrolled

    color_strings = [
        'AliceBlue',
        'AntiqueWhite',
        'Aqua',
        'Aquamarine',
        'Azure',
        'Beige',
        'Bisque',
        'Black',
        'BlanchedAlmond',
        'Blue',
        'BlueViolet',
        'Brown',
        'BurlyWood',
        'CadetBlue',
        'Chartreuse',
        'Chocolate',
        'Coral',
        'CornflowerBlue',
        'Cornsilk',
        'Crimson',
        'Cyan',
        'DarkBlue',
        'DarkCyan',
        'DarkGoldenRod',
        'DarkGray',
        'DarkGrey',
        'DarkGreen',
        'DarkKhaki',
        'DarkMagenta',
        'DarkOliveGreen',
        'DarkOrange',
        'DarkOrchid',
        'DarkRed',
        'DarkSalmon',
        'DarkSeaGreen',
        'DarkSlateBlue',
        'DarkSlateGray',
        'DarkSlateGrey',
        'DarkTurquoise',
        'DarkViolet',
        'DeepPink',
        'DeepSkyBlue',
        'DimGray',
        'DimGrey',
        'DodgerBlue',
        'FireBrick',
        'FloralWhite',
        'ForestGreen',
        'Fuchsia',
        'Gainsboro',
        'GhostWhite',
        'Gold',
        'GoldenRod',
        'Gray',
        'Grey',
        'Green',
        'GreenYellow',
        'HoneyDew',
        'HotPink',
        'IndianRed',
        'Indigo',
        'Ivory',
        'Khaki',
        'Lavender',
        'LavenderBlush',
        'LawnGreen',
        'LemonChiffon',
        'LightBlue',
        'LightCoral',
        'LightCyan',
        'LightGoldenRodYellow',
        'LightGray',
        'LightGrey',
        'LightGreen',
        'LightPink',
        'LightSalmon',
        'LightSeaGreen',
        'LightSkyBlue',
        'LightSlateGray',
        'LightSlateGrey',
        'LightSteelBlue',
        'LightYellow',
        'Lime',
        'LimeGreen',
        'Linen',
        'Magenta',
        'Maroon',
        'MediumAquaMarine',
        'MediumBlue',
        'MediumOrchid',
        'MediumPurple',
        'MediumSeaGreen',
        'MediumSlateBlue',
        'MediumSpringGreen',
        'MediumTurquoise',
        'MediumVioletRed',
        'MidnightBlue',
        'MintCream',
        'MistyRose',
        'Moccasin',
        'NavajoWhite',
        'Navy',
        'OldLace',
        'Olive',
        'OliveDrab',
        'Orange',
        'OrangeRed',
        'Orchid',
        'PaleGoldenRod',
        'PaleGreen',
        'PaleTurquoise',
        'PaleVioletRed',
        'PapayaWhip',
        'PeachPuff',
        'Peru',
        'Pink',
        'Plum',
        'PowderBlue',
        'Purple',
        'Red',
        'RosyBrown',
        'RoyalBlue',
        'SaddleBrown',
        'Salmon',
        'SandyBrown',
        'SeaGreen',
        'SeaShell',
        'Sienna',
        'Silver',
        'SkyBlue',
        'SlateBlue',
        'SlateGray',
        'SlateGrey',
        'Snow',
        'SpringGreen',
        'SteelBlue',
        'Tan',
        'Teal',
        'Thistle',
        'Tomato',
        'Turquoise',
        'Violet',
        'Wheat',
        'White',
        'WhiteSmokewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
        'Yellow']

    caseless_colors = []
    for color in color_strings:
        color = color.lower()
        caseless_colors.append(color)

    short_list = ('yellow', 'red', 'blue')

    def colorize(button=None, combo=None):
        '''
            Selects the right widget because only one at a time is not None.
        '''
        def do_it():
            frm.config(bg=color)
            combo.selected = None
            combo.typed = None
        combo = None
        if button == flat:
            combo = b
        elif button is flat2:
            combo = bb
        if combo == None:
            return
        combo.get_typed()
        if combo.selected:
            color = combo.selected.cget('text')
            do_it()
        elif combo.typed:
            color = combo.typed
            do_it()

    def combobox_selected(cbo):
        string_input = cbo.var.get()
        if string_input in caseless_colors:
            color = string_input
            ok = '{}\nis a\nvalid\ncolor.'.format(color.title())
            cbox_select.config(text=ok)
        else:
            cbox_select.config(text=msg)  

    def test_bind_to_dropdown_items(evt):
        print("evt.widget.cget('text'):", evt.widget.cget('text'))

    root = tk.Tk()
    root.focus_set()
    root.grid_columnconfigure(0, weight=1)
    root.geometry('+500+200')

    # main canvas
    canvas_0 = CanvasScrolledBG1(root, resizable=True, scrollbar='both')
    CanvasScrolledBG1.config_resizable_canvas(canvas_0) # *****
    canvas_0.grid(column=0, row=0, sticky='news')
    canvas_0.vert.grid(column=1, row=0, sticky='ns')
    canvas_0.horiz.grid(column=0, row=1, sticky='ew') 
    canvas_0.content.grid_columnconfigure(0, weight=1)
    canvas_0.content.grid_rowconfigure(1, weight=1)

    b = Combobox(
        canvas_0.content,
        root,
        callback=colorize,
        height=75, 
        values=caseless_colors,
        scrollbar_size=16)
    flat = ButtonFlatHilited(canvas_0.content, text='Apply Combo 1')
    flat.config(command=lambda button=flat: colorize(button))
    b.config_values(short_list)
    # You can't do this in ttk.Combobox:
    for widg in b.buttons:
        widg.bind('<FocusOut>', test_bind_to_dropdown_items)

    bb = Combobox(
        canvas_0.content,
        root,
        callback=colorize,
        height=450, 
        values=caseless_colors,
        scrollbar_size=16)

    Combobox.combobox_selected = combobox_selected

    flat2 = ButtonFlatHilited(canvas_0.content, text='Apply Combo 2')
    flat2.config(command=lambda button=flat2: colorize(button))

    b.grid(column=0, row=0, padx=6, pady=6)
    flat.grid(column=1, row=0, padx=6, pady=6)
    bb.grid(column=2, row=0, padx=6, pady=6)
    flat2.grid(column=3, row=0, padx=6, pady=6)
        
    frm = FrameStay(canvas_0.content)
    for i in range(10):
        lab = Label(frm, text=i)
        lab.grid(column=0, row=i+1, sticky='ew')

    msg = 'No valid\ncolor\nhas been\nchosen'
    cbox_select = Label(canvas_0.content, text=msg)

    frm.grid(column=0, row=1, sticky='news', columnspan=3)
    cbox_select.grid(column=3, row=1, sticky='news')

    CanvasScrolled.config_scrolled_canvases(main_app=root)

    root.mainloop()


