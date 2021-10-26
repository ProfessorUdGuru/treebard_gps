# dropdown.py

import tkinter as tk
from widgets import Label, Frame
from scrolling import Scrollbar
import dev_tools as dt
from dev_tools import looky, seeline








class DropdownMenu(Frame):
    def __init__(self, master, drop0=[], drop1=[], drop2=[], *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master 
        self.drop0 = drop0
        self.drop1 = drop1
        self.drop2 = drop2
        self.make_widgets()

    def make_widgets(self):

        for i in range(20):
            lab = Label(self, text="help", bg="teal", fg="orange")
            lab.grid(column=i, row=0) 



if __name__ == "__main__":

    from window_border import Border
    from widgets import Button

    def make_widgets():
        root.columnconfigure(1, weight=1)
        canvas = Border(root, size=3, menubar=True)
        canvas.title_1.config(text="Person Search Dialog")
        canvas.title_2.config(text="")

        window = Frame(canvas)
        canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

        window.vsb = Scrollbar(
            root, 
            hideable=True, 
            command=canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            root, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        dropdown = DropdownMenu(canvas.menu)
        dropdown.grid(column=0, row=0, sticky='ew')

        buttonbox = Frame(window)
        b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        window.columnconfigure(2, weight=1)
        window.rowconfigure(1, weight=1)
        buttonbox.grid(column=0, row=3, sticky='e', pady=6)

        b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        make_inputs(window)

    def make_inputs(window):

        root.columnconfigure(1, weight=1)

        header = Frame(window)
        header.grid(column=0, row=0, sticky='ew')

        search_dlg_heading = Label(
            header, 
            text='Person Search')
        search_dlg_heading.grid(column=0, row=0, pady=(24,0))

        instrux = Label(
            header, text='Search for person by name(s) or id number:')
        instrux.grid(column=0, row=1, sticky='e', padx=24, pady=12)

    def cancel():
        root.quit()

    root = tk.Tk()
    root.geometry("1600x400+200+200")
    root.config(bg="black")

    make_widgets()





    root.mainloop()