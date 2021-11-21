# error_messages.py

from tkinter import StringVar, IntVar
from window_border import Dialogue
from scrolling import Scrollbar, resize_scrolled_content
from widgets import Label, Button, Frame, LabelHeader, Entry, Radiobutton
from styles import config_generic
import dev_tools as dt
from dev_tools import looky, seeline





def open_message(master, message, title, buttlab, inwidg=None):

    def close():
        '''
            See events_table `err_done` for examples of how to override
            this if more needs to be done on closing the error message.
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

    msg.resize_window(lab)

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

    msg.resize_window(lab)

    return msg, lab, ok_butt, cancel_butt, buttonbox

class InputMessage(Dialogue):
    def __init__(
            self, master, return_focus_to=None, root=None, title="", ok_txt="", 
            cancel_txt="", head1="", head2="", wraplength=450, radtext=[], 
            radfocal=0, entry=False, radio=False, scrolled=False, 
            grab=False, treebard=None, *args, **kwargs):
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
        self.grab = grab
        self.treebard = treebard

        self.canvas.title_1.config(text=title)
        self.canvas.title_2.config(text="")

        self.got = StringVar()
        self.radvar = IntVar(None, 0)
        if scrolled is True:
            self.make_scrollbars()
        self.make_containers()
        self.make_widgets()
        self.make_inputs()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        if scrolled is True:
            resize_scrolled_content(self, self.canvas, self.window)
        else:
            self.resize_window(self.head)

        if self.grab is True: self.grab_set()
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
            column=1, row=3, sticky="e", padx=12, pady=(18,12), columnspan=2)

    def make_widgets(self):
        self.head = LabelHeader(
            self.header, text=self.head1, justify='left', 
            wraplength=self.wraplength)
        self.head.grid(
            column=0, row=0, sticky='news', padx=12, pady=12, 
            columnspan=2, ipadx=6, ipady=3)
        head2 = Label(
            self.header, text=self.head2)
        head2.grid(column=0, row=1)        
        maxx = max(len(self.ok_txt), len(self.cancel_txt))
        self.b1 = Button(
            self.buttons, text=self.ok_txt, command=self.ok, width=maxx)
        self.b1.grid(column=0, row=0, sticky='e', ipadx=3)
        b2 = Button(
            self.buttons, text=self.cancel_txt, command=self.cancel, width=maxx)
        b2.grid(column=1, row=0, padx=(6,0), sticky='e', ipadx=3)

    def make_inputs(self):

        if self.entry is True:
            self.inPut = Entry(self.inputs, textvariable=self.got)
            self.inPut.grid(column=1, row=1, padx=12)
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

    def ok(self, evt=None):
        self.cancel()

    def cancel(self, evt=None):
        self.destroy()

    def show(self):
        if self.entry:
            gotten = self.got.get()
            return gotten
        elif self.radio:
            chosen = self.radvar.get()
            return chosen







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
    lab2 = Label(msg.window, text="{} or {}?".format(user_input[0], user_input[1]))
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

    msg.resize_window(lab)

    master.wait_window(msg)
    got = show()
    return user_input, got

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

    got = StringVar()

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

    msg.resize_window(lab)
    master.wait_window(msg)
    gotten = show()
    return gotten


def open_option_message(
        master, message, title, ok_lab, cancel_lab, radvar, radtext):
    '''
        Like open_input_message but gets input from Radiobuttons. Made this to
        use in `ask_if_after_death()` and `id_couple_event` in events_table.py 
        but because of complexity, I ended up copying most of this to the 
        module instead of trying to import and adapt it. So this function as a 
        whole is actually untested.
    '''
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
        msg.window, text=message, justify='left', wraplength=450)
    lab.grid(
        column=0, row=0, sticky='news', padx=12, pady=12, 
        columnspan=2, ipadx=6, ipady=3)    
    for i in range(2):
        rad = Radiobutton(
            msg.window,  
            text=radtext[i],
            value=i,
            variable=radvar,
            anchor='w')
        rad.grid(column=0, row=i+1, sticky='ew')
        if i == 0:
            rad.focus_set()
    buttonbox = Frame(msg.window)
    buttonbox.grid(
        column=0, row=3, sticky='e', padx=(0,12), pady=12, columnspan=2)
    ok_butt = Button(buttonbox, text=ok_lab, command=ok, width=6)
    ok_butt.grid(column=0, row=0, sticky='e')
    cancel_butt = Button(buttonbox, text=cancel_lab, command=cancel, width=6)
    cancel_butt.grid(column=1, row=0, padx=(6,0), sticky='e')
    msg.grab_set()
    msg.resize_window(lab)
    master.wait_window(msg)
    got = show()
    return msg, got

places_err = (
    "A place cannot contain itself.\n\nSelect a "
    "chain of places that are nested inside each other.",
)

events_msg = (
    "The same person was used twice.",
    "Please enter a kin type for each person.",
    "A second person must be entered for a couple event.",
    "Offspring events can't be changed to other event types. You "
    "can delete the event and make a new event.",
    "A couple event can't be changed to a non-couple event, or "
        "vice-versa. For example, a marriage can be changed to "
        "a wedding but a death can't be changed to a divorce. "
        "Delete unwanted events and create new ones to "
        "replace them if they're incompatible in this way. To "
        "delete an event, delete the event type in the first column.",
    "An event is about to be deleted. This can't be undone. For "
        "couple events, the event will be deleted for both "
        "partners. For offspring events, the child's birth event "
        "will be deleted, but not the child.",
    "Each person has one birth and one death event. To add more "
        "hypothetical birth or death events, add them as assertions "
        "instead of conclusions. The events table is for conclusions, "
        "but assertions can be added freely by clicking the SOURCES "
        "button at the end of the birth or death event row or by "
        "going directly to the assertions tab if you prefer to make "
        "no conclusions at this time.",
    "A non-offspring event can't be changed to an offspring event. "
        "You can delete the event and make a new event.",
    "Offspring events can't be created directly. Create a new person "
        "and give them parents, and the parents' offspring events "
        "will be created automatically.",
    "Does the new event type occur after death?",
)

names_msg = (
    "This birth name already exists. To create a "
        "new person by the same name, click OK. The "
        "two persons can be merged later if desired.",
    "That name type doesn't exist yet. Create it?",
)

notes_msg = (
    "Any note can be linked to any number of entities.",
    "The current note can be linked to any number of elements "
        "such as persons, places, assertions, conclusions, or sources.",
    "Type a unique subtopic name for the new note.",
    "Each subtopic can be used once in a tree.",
    "Blank notes are OK but not blank note titles.",
)

dates_msg = (
    "One of the words 'and' or 'to' can be used once in a compound date. "
        "Input should be like 'feb 27 1885 to 1886' for 'from 27 Feb 1885 to 1886' "
        "or '1884 and mar 1885' for 'between 1884 and March 1885'.",
    "One month is allowed per date. For compound dates, the two dates have to be "
        "separated by 'and' or 'to'.",
    "For compound dates connected by 'and' or 'to', two months are possible. For "
        "single dates there can only be one month.",
    "If no month is input, no day can be input",
    "Each part of a compound date can have one prefix and one suffix. Each single "
        "date can have one prefix and one suffix. Prefixes include est, abt, bef, aft, "
        "and cal. Suffixes include AD, BC, CE, BCE, NS and OS.",
    "One date includes only one year.",
    "Date input included too many numerical terms. Input months as text, for "
        "example: feb for February, jul for July, may for May, etc.",
    "Each single date can include a maximum of five terms. Each compound date can "
        "include five terms in each part plus a link ('and' or 'to) between the two "
        "parts. The parts within a date can be in any order, for example 'nov 1885 14 "
        "est bc' for 'estimated 14 Nov 1885 BC'.",
    "Day and year are input as numbers. Months are input as abbreviated text "
        "such as mar, sep, dec. The date input seems to be lacking numerical input.",
    "A compound date should include two distinct and complete single dates "
        "separated by 'and' or 'to'. Treebard translates input separated by 'and' into "
        "a range such as 'between 1885 and 1886'. Compound dates separated by 'to' are "
        "translated into a span such as 'from 1912 to Feb 1915'. The input was for two "
        "identical dates. ",
    "That month doesn't have that many days. In leap years, February has 29 days. "
        "Leap years are evenly divisible by 4.",
    "Type the year as a four-digit number. For example, the year 33 should be "
        "typed as 0033.",
    "A 4-digit year must be entered. For years prior to the year 1000, add "
        "leading zeroes. For example, for the year 12 AD or the year 12 BC, "
        "type '0012' without the quotation marks. Or for the year 108, type "
        "'0108'.",
)

fonts_msg = (
    "Press ALT+P then CTRL+S to resize the scrollbar after changing fonts.",
)

opening_msg = ("The requested file has been moved, deleted or renamed outside "
        "of Treebard's controls. To use the file, restore it to its original folder "
        "and name. Any file changes should be made from within Treebard using "
        "Treebard's tools.",
    "Treebard will use your title as the tree's display title. "
        "Treebard will save 'Smith Family Tree' as a database file at `{current "
        "drive}/treebard_gps/data/smith_family_tree/smith_family_tree.tbd`",
    "This feature is not complete. Please visit https://treebard.proboards.com if "
        "you would like to assist or advise regarding this feature.",
)


