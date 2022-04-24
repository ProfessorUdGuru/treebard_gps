# error_messages.py

from tkinter import StringVar, IntVar
from scrolling import resize_scrolled_content
from widgets import (
    Label, Button, Frame, LabelHeader, Entry, Radiobutton, Checkbutton,
    configall, make_formats_dict, Dialogue, Scrollbar)
import dev_tools as dt
from dev_tools import looky, seeline






class InputMessage(Dialogue):
    def __init__(
            self, master, return_focus_to=None, root=None, title="", 
            ok_txt="", cancel_txt="", head1="", head2="", wraplength=450, 
            radtext=[], radfocal=0, entry=False, radio=False, 
            check=False, chktext=[], chkfocal=0,
            scrolled=False, grab=False, treebard=None, ok_button=True, *args, **kwargs):
        Dialogue.__init__(self, master, *args, **kwargs)

        self.master = master
        self.return_focus_to = return_focus_to
        self.root = root
        self.title = title
        self.head1 = head1
        self.head2 = head2
        self.ok_txt = ok_txt
        self.cancel_txt = cancel_txt
        self.wraplength = wraplength
        self.radtext = radtext
        self.radfocal = radfocal
        self.entry = entry
        self.radio = radio
        self.check = check
        self.chktext = chktext
        self.chkfocal = chkfocal
        self.scrolled = scrolled
        self.grab = grab
        self.treebard = treebard
        self.ok_button = ok_button

        self.canvas.title_1.config(text=title)
        self.canvas.title_2.config(text="")

        self.got = StringVar()
        self.radvar = IntVar(None, 0)
        self.chkvar = IntVar(None, 0)
        if scrolled is True:
            self.make_scrollbars()
        self.make_containers()
        self.make_widgets()
        self.make_inputs()
        self.formats = make_formats_dict()
        configall(self, self.formats)

        self.ok_was_pressed = False

        self.bind("<Return>", self.input_message_ok)
        self.bind("<Escape>", self.cancel)

        if scrolled is True:
            good_height = int(self.winfo_screenheight() * 0.9)
            self.maxsize(800, good_height)        
            resize_scrolled_content(self, self.canvas, self.window)
            self.center_dialog(self, win_height=good_height)
        else:
            self.resize_window()

        if self.grab is True: 
            self.grab_set()            

        self.deiconify()
        self.master.wait_window(self)
        self.run_post_op()

    def center_dialog(self, frame=None, win_height=None):
        '''
            If frame is True, it works but not if the window has more content
            that what will fit in the screen vertically. In this case I had
            to use win_height which is a minimum height based on the screen
            height. This is based on center_dialog() function in utes.py
            which didn't work here. Possibly the `frame` parameter should be 
            removed.
        '''
        if win_height:
            self.update_idletasks()
            win_width = frame.winfo_reqwidth()
            win_height = win_height
            right_pos = int(self.winfo_screenwidth()/2 - win_width/2)
            down_pos = int(self.winfo_screenheight()/2 - win_height/2)
        elif frame:
            self.update_idletasks()
            win_width = frame.winfo_reqwidth()
            win_height = frame.winfo_reqheight()
            right_pos = int(self.winfo_screenwidth()/2 - win_width/2)
            down_pos = int(self.winfo_screenheight()/2 - win_height/2)
        else:
            self.update_idletasks()
            win_width = self.winfo_reqwidth()
            win_height = self.winfo_reqheight()
            right_pos = int(self.winfo_screenwidth()/2 - win_width/2)
            down_pos = int(self.winfo_screenheight()/2 - win_height/2)
        self.geometry("+{}+{}".format(right_pos, down_pos))

    def make_scrollbars(self):

        scridth = 16
        scridth_n = Frame(self.window, height=scridth)
        scridth_w = Frame(self.window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

        if self.treebard:
            self.treebard.scroll_mouse.append_to_list([self.canvas, self.window])
            self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.window.vsb = Scrollbar(
            self, 
            hideable=True, 
            command=self.canvas.yview,
            width=scridth)
        self.window.hsb = Scrollbar(
            self, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=self.window.hsb.set, 
            yscrollcommand=self.window.vsb.set)
        self.window.vsb.grid(column=2, row=4, sticky='ns')
        self.window.hsb.grid(column=1, row=5, sticky='ew')

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

    def make_containers(self):

        self.header = Frame(self.window)
        self.inputs = Frame(self.window)
        self.buttons = Frame(self.window)

        self.header.grid(column=1, row=1, sticky="news", pady=(12,0))
        self.inputs.grid(column=1, row=2, sticky="news")
        self.buttons.grid(
            column=1, row=3, sticky="e", padx=12, pady=12, columnspan=2)

    def make_widgets(self):
        self.head = LabelHeader(
            self.header, text=self.head1, justify='left', 
            wraplength=self.wraplength)
        self.head.grid(
            column=0, row=0, sticky='news', padx=12,  
            columnspan=2, ipadx=6, ipady=3)
        self.info = Label(self.header, text=self.head2)
        self.info.grid(column=0, row=1, padx=12, pady=12)        
        maxx = max(len(self.ok_txt), len(self.cancel_txt))
        if self.ok_button is True:
            self.b1 = Button(
                self.buttons, text=self.ok_txt, command=self.input_message_ok, width=maxx)
            self.b1.grid(column=0, row=0, sticky='e', ipadx=3)
        self.b2 = Button(
            self.buttons, text=self.cancel_txt, command=self.cancel, width=maxx)
        self.b2.grid(column=1, row=0, padx=(6,0), sticky='e', ipadx=3)

    def make_inputs(self):

        if self.entry is True:
            self.inPut = Entry(self.inputs, textvariable=self.got)
            self.inPut.grid(column=1, row=1, padx=12)
            self.inPut.focus_set()
        elif self.radio is True:
            self.radframe = Frame(self.inputs)
            self.radframe.grid()
            radios = []
            for i in range(len(self.radtext)):
                rad = Radiobutton(
                    self.radframe,  
                    text=self.radtext[i],
                    value=i,
                    variable=self.radvar,
                    anchor='w')
                rad.grid(column=0, row=i, sticky='ew')
                radios.append(rad)    
            radios[self.radfocal].focus_set()
        elif self.check is True:
            self.chkframe = Frame(self.inputs)
            self.chkframe.grid()
            checks = []
            a = 0
            for i in self.chktext:
                chk = Checkbutton(
                    self.chkframe,  
                    text=self.chktext[a],
                    variable=self.chkvar,
                    anchor='w')
                chk.grid(column=0, row=a, sticky='ew')
                checks.append(chk) 
                a += 1
            checks[self.chkfocal].focus_set()
        if self.ok_button is False:
            self.b2.focus_set()
        
    def run_post_op(self):
        if self.grab is True: 
            self.grab_release()

        if self.return_focus_to:
            self.return_focus_to.focus_set()

        if self.root:
            self.root.lift()

    def input_message_ok(self, evt=None):
        self.ok_was_pressed = True
        self.cancel()

    def cancel(self, evt=None):
        print("line", looky(seeline()).lineno, "self.ok_was_pressed:", self.ok_was_pressed)
        self.ok_was_pressed = False
        self.destroy()

    def show(self):
        if self.entry:
            gotten = self.got.get()
            return gotten
        elif self.radio:
            chosen = self.radvar.get()
            return chosen
        elif self.check:
            chosen = self.chkvar.get()
            return chosen

def open_yes_no_message(master, message, title, ok_lab, cancel_lab):
    def ok():
        cancel()

    def cancel():
        msg.destroy()

    formats = make_formats_dict()
    msg = Dialogue(master)
    msg.canvas.title_1.config(text=title)
    msg.canvas.title_2.config(text="")
    lab = LabelHeader(
        msg.window, text=message, justify='left', wraplength=600)
    lab.grid(
        column=0, row=0, sticky='news', padx=12, pady=12, 
        columnspan=2, ipadx=6, ipady=3)
    buttonbox = Frame(msg.window)
    buttonbox.grid(column=0, row=1, sticky='e', padx=(0,12), pady=12)
    ok_butt = Button(buttonbox, text=ok_lab, command=cancel, width=6)
    ok_butt.grid(column=0, row=0, padx=6)
    cancel_butt = Button(buttonbox, text=cancel_lab, command=cancel, width=6)
    cancel_butt.grid(column=1, row=0, padx=6)
    ok_butt.focus_set()

    configall(msg, formats)
    msg.resize_window()

    return msg, lab, ok_butt, cancel_butt, buttonbox

def open_input_message(master, message, title, ok_lab, cancel_lab, user_input):

    def ok():
        cancel()

    def cancel():
        msg.destroy()

    def show():
        gotten = got.get()
        return gotten

    got = StringVar()

    msg = Dialogue(master)
    msg.canvas.title_1.config(text=title)
    msg.canvas.title_2.config(text="")
    lab = LabelHeader(
        msg.window, text=message, justify='left', wraplength=300)
    lab.grid(
        column=0, row=0, sticky='news', padx=12, pady=12, 
        columnspan=2, ipadx=6, ipady=3)
    lab2 = Label(msg.window, text="{} or {}?".format(
        user_input[0], user_input[1]))
    lab2.grid(column=0, row=1)
    inPut = Entry(msg.window, textvariable=got)
    inPut.grid(column=1, row=1, padx=(0,12))
    buttonbox = Frame(msg.window)

    buttonbox.grid(
        column=0, row=2, sticky='e', padx=(0,12), pady=12, columnspan=2)
    ok_butt = Button(buttonbox, text=ok_lab, command=ok, width=6)
    ok_butt.grid(column=0, row=0, sticky='e')
    cancel_butt = Button(buttonbox, text=cancel_lab, command=cancel, width=6)
    cancel_butt.grid(column=1, row=0, padx=(6,0), sticky='e')
    inPut.focus_set()
    
    config_generic(msg)
    msg.resize_window()

    master.wait_window(msg)
    got = show()
    return user_input, got

