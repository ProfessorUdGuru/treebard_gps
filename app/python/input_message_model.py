# input_message_model

import tkinter as tk
from window_border import Dialogue
from scrolling import Scrollbar, resize_scrolled_content
from widgets import Label, Button, Frame, LabelHeader, Entry, Radiobutton
from styles import config_generic
import dev_tools as dt
from dev_tools import looky, seeline




class InputMessage(Dialogue):
    def __init__(
            self, master, return_focus_to=None, root=None, title="", ok_txt="", 
            cancel_txt="", head1="", head2="", wraplength=450, radtext=[], 
            radfocal=0, entry=False, radio=False, scrolled=False, 
            user_input=None, grab=False, treebard=None, *args, **kwargs):
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
        self.scrolled = scrolled
        self.user_input = user_input
        self.grab = grab
        self.treebard = treebard

        self.canvas.title_1.config(text=title)
        self.canvas.title_2.config(text="")

        self.got = tk.StringVar()
        self.radvar = tk.IntVar(None, 0)
        if scrolled is True:
            self.make_scrollbars()
        self.make_containers()
        self.make_widgets()
        self.make_inputs()

        if self.grab is True: self.grab_set()

        resize_scrolled_content(self, self.canvas, self.window)
        self.deiconify()
        self.master.wait_window(self)
        self.run_post_op()

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

        self.header.grid(column=1, row=1, sticky="news")
        self.inputs.grid(column=1, row=2, sticky="news")
        self.buttons.grid(
            column=1, row=3, sticky="e", padx=(0,12), pady=(18,12), columnspan=2)

    def make_widgets(self):
        head = LabelHeader(
            self.header, text=self.head1, justify='left', wraplength=300)
        head.grid(
            column=0, row=0, sticky='news', padx=12, pady=12, 
            columnspan=2, ipadx=6, ipady=3)
        head2 = Label(
            self.header, text=self.head2)
        head2.grid(column=0, row=1)        

        b1 = Button(self.buttons, text=self.ok_txt, command=self.ok, width=6)
        b1.grid(column=0, row=0, sticky='e')
        b2 = Button(self.buttons, text=self.cancel_txt, command=self.cancel, width=6)
        b2.grid(column=1, row=0, padx=(6,0), sticky='e')

    def make_inputs(self):
        '''
            To make this class flexible to different designs, the inputs are 
            not gridded here, but in the instance i.e. self.radframe and 
            self.inPut.
        '''

        if self.entry is True:
            self.inPut = Entry(self.inputs, textvariable=self.got)
            self.inPut.grid(column=1, row=1, padx=(0,12))
            self.inPut.focus_set()
        if self.radio is True:
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
        
    def run_post_op(self):

        if self.grab is True: self.grab_release()
        if self.return_focus_to:
            self.return_focus_to.focus_set()
        self.root.lift()

    def ok(self):
        self.cancel()

    def cancel(self):
        self.destroy()

    def show(self):
        if self.entry:
            gotten = self.got.get()
            return gotten
        elif self.radio:
            chosen = self.radvar.get()
            return chosen

if __name__ == "__main__":

    def open_ent():
        ent = InputMessage(
            root, root=root, title="Input Message", 
            head1="These are your instructions.", head2="further instructions...", ok_txt="OK", cancel_txt="CANCEL", entry=True, 
            user_input="what user thought", scrolled=True)    
        display1.config(text=ent.show())

    def open_rad():
        rad = InputMessage(
            root, root=root, title="Radio Message", 
            head1="These are your options.", head2="it's like this...", 
            ok_txt="OK", cancel_txt="CANCEL", radio=True, 
            user_input="what user thought", scrolled=True,
            radtext=("horse", "goat", "monkey")) 
        display2.config(text=rad.show())

    root = tk.Tk()
    root.title("root window")
    root.geometry("500x400+900+300")
    root.columnconfigure(0, weight=1)

    b1 = Button(root, command=open_ent, text="OPEN INPUT DIALOG", width=24)
    b1.grid()

    b2 = Button(root, command=open_rad, text="OPEN RADIO DIALOG", width=24)
    b2.grid()

    display1 = Label(root)
    display1.grid()

    display2 = Label(root)
    display2.grid()

    config_generic(root)

    root.mainloop()



