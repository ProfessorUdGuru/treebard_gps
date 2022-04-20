# error_messages.py

from tkinter import StringVar
from scrolling import resize_scrolled_content
from widgets import (
    Label, Button, Frame, LabelHeader, Entry, Radiobutton, Checkbutton,
    configall, make_formats_dict, Dialogue, Scrollbar)
import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

def open_message(master, message, title, buttlab, inwidg=None):

    def close():
        '''
            Override this is more needs to be done on close.
        '''
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
    configall(msg, formats)
    msg.resize_window()

    return msg, lab, button

def open_yes_no_message(master, message, title, ok_lab, cancel_lab):

    def ok():
        cancel()

    def cancel():
        msg.destroy()

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

    # config_generic(msg)
    configall(msg, facebook)
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

# def open_input_message2(master, message, title, ok_lab, cancel_lab):
    # '''
        # For more primary-level input vs. error-level input.
    # '''

    # def ok():
        # cancel()

    # def cancel():
        # msg.destroy()
        # master.grab_set()

    # def show():
        # gotten = got.get()
        # return gotten

    # got = StringVar()

    # msg = Dialogue(master)
    # msg.grab_set()
    # msg.canvas.title_1.config(text=title)
    # msg.canvas.title_2.config(text="")
    # lab = LabelHeader(
        # msg.window, text=message, justify='left', 
        # font=("courier", 14, "bold"), wraplength=450)
    # lab.grid(
        # column=0, row=0, sticky='news', padx=12, pady=12, 
        # columnspan=2, ipadx=6, ipady=3)
    # inPut = Entry(
        # msg.window, textvariable=got, width=48, 
        # font=("dejavu sans mono", 14))
    # inPut.grid(column=0, row=1, padx=12)
    # buttonbox = Frame(msg.window)
    # buttonbox.grid(column=0, row=2, sticky='e', padx=(0,12), pady=12)
    # ok_butt = Button(
        # buttonbox, text=ok_lab, command=cancel, width=7)
    # ok_butt.grid(column=0, row=0, padx=6, sticky='e')
    # cancel_butt = Button(
        # buttonbox, text=cancel_lab, command=cancel, width=7)
    # cancel_butt.grid(column=1, row=0, padx=6, sticky='e')
    # inPut.focus_set()

    # config_generic(msg)
    # msg.resize_window()
    # master.wait_window(msg)
    # gotten = show()
    # return gotten

