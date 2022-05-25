# numerology_001

# add notes thru person_id = 20
# readme "copy to something like celebrities.db and in that copy, delete rows where private=1 before making .sql flat file; don't share the version with your family's names in it, especially living people."
# make flat file for git; create the local and github repos


import tkinter as tk
import sqlite3
import dev_tools as dt
from dev_tools import looky, seeline





file = "d:/treebard_gps/etc_not_in_repo/numerology.db"

select_matching_names = '''
    SELECT person_id, names, note
    FROM person 
    WHERE numstrings = ?
'''

select_note = '''
    SELECT note
    FROM person
    WHERE person_id = ?
'''

ONES = ('a', 'j', 's') 
TWOS = ('b', 'k', 't')
THREES = ('c', 'l', 'u') 
FOURS = ('d', 'm', 'v') 
FIVES = ('e', 'n', 'w') 
SIXES = ('f', 'o', 'x')
SEVENS = ('g', 'p', 'y')
EIGHTS = ('h', 'q', 'z')
NINES = ('i',  'r')

CHAR_DICT = {
	ONES : 1,
	TWOS : 2,
	THREES : 3,
	FOURS : 4,
	FIVES : 5,
	SIXES : 6,
	SEVENS : 7,
	EIGHTS : 8,
	NINES : 9}

VOWELS = ('a', 'e', 'i', 'o', 'u')
CONSONANTS = (
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 
    's', 't', 'v', 'w', 'x', 'y', 'z')

FG = "bisque"
BG = "teal"
BG2 = "steelblue"
BG3 = "gray"
FONT1 = ("courier", 16)
FONT2 = ("arial", 16)
FONT3 = ("arial black", 18)

class NumerologyCalculator():
    def __init__(self, root):

        self.root = root

        self.matches = []
        self.person_id = None
        self.clicked_person_id = None

        self.make_widgets()

    def make_widgets(self):
        self.privvy = tk.IntVar()

        lab1 = tk.Label(self.root, bg=BG, fg=FG, text="Full Name at Birth:")
        lab1.grid(column=0, row=1, pady=(6,0), sticky="e", padx=(6,0))

        self.ent1 = tk.Entry(self.root, bg=BG3, width=40, font=FONT2)
        self.ent1.grid(column=1, row=1, pady=(6,0), padx=6)

        button = tk.Button(self.root, text="CALCULATE", command=self.calculate, width=12, bg=BG2, fg=FG)
        button.grid(column=1, row=2, sticky="e", padx=(0,6), pady=(6,0))

        self.frm = tk.Frame(self.root, bg=BG, width=400, height=200)
        self.frm.grid(column=0, row=3, columnspan=2, pady=(6,0), padx=6, sticky="news")

        self.result = tk.Label(self.root, bg=BG, fg=FG, text="result", font=FONT3)
        self.result.grid(column=0, row=4, columnspan=2, pady=(6,0))

        self.private = tk.Checkbutton(
            self.root, text="Private", command=self.set_privvy, 
            bg="#121212", fg=FG, activebackground="green", 
            highlightbackground=FG, highlightcolor="magenta", 
            selectcolor=BG2, activeforeground="orange")
        self.private.grid(column=0, row=5, sticky="w", pady=(6,0), padx=(6,0))

        store_button = tk.Button(self.root, text="STORE RESULT", command=self.store, width=12, bg=BG2, fg=FG)
        store_button.grid(column=1, row=5, sticky="e", padx=(0,6), pady=(6,0))

        self.match_frame = tk.Frame(self.root, bg=BG, width=400, height=200)
        self.match_frame.grid(column=0, row=6, sticky="news", columnspan=2, pady=(6,0), padx=6)

        lab = tk.Label(self.root, bg=BG, fg=FG, text="Show all of:")
        lab.grid(column=0, row=7, pady=(6,0), sticky="ew", padx=(6,0))

        self.show_all = tk.Entry(self.root, bg=BG3, width=6, font=FONT2)
        self.show_all.grid(column=1, row=7, pady=(6,0), sticky="w", padx=(6,0))

        show_button = tk.Button(
            self.root, text="SHOW ALL", 
            command=self.display_stored, 
            width=12, bg=BG2, fg=FG)
        show_button.grid(column=1, row=8, sticky="e", padx=(0,6), pady=6)

        self.lab2 = tk.Label(self.root, bg=BG, fg=FG, text="Notes", anchor="w")
        self.lab2.grid(column=2, row=0, sticky='we', padx=(0,6), pady=(6,0))

        self.notes = Text(
            self.root, bg=BG3, fg=FG, font=FONT1, 
            width=30, wrap='word', cursor='center_ptr')
        self.notes.grid(column=2, row=1, rowspan=7, padx=(0,6), pady=6)
        self.notes.focus_set() 

    def run_stage_2(self, stg):
        if len(str(stg)) > 1:
            sumall = str(stg)
            x = 0
            for char in sumall:
                x += int(char)
        else:
            x = stg
        return x

    def recalculate(self, evt):

        new_vowels = []
        new_consonants = []

        for child in self.frm.winfo_children():
            text = child.cget("text")
            row = child.grid_info()["row"]
            if row == 0:
                new_vowels.append(text)
            elif row == 1:
                new_consonants.append(text)

        u = 0
        for lst in (new_vowels, new_consonants):
            x = 0
            for ltr in lst:
                for k,v in CHAR_DICT.items():
                    if ltr.lower() in k:
                        lst[x] = v
                x += 1            
            u += 1

        final = self.add_values(new_vowels, new_consonants)

        self.result.config(text=final)

    def calculate(self, evt=None):
        name = self.ent1.get()

        name = name.split()
        lowered = [i.lower() for i in name]
        name = "".join(lowered)

        nums_vowel = []
        nums_consonant = []

        for char in name:
            if char == "": 
                continue
            for k,v in CHAR_DICT.items():
                if char in k and char in VOWELS:
                    nums_vowel.append(v)
                elif char in k and char in CONSONANTS:
                    nums_consonant.append(v)

        final = self.add_values(nums_vowel, nums_consonant)
        self.result.config(text=final)
        self.display(name)

    def add_values(self, v, c):
        sum_vowels = sum(v)
        sum_consonants = sum(c)
        sum_all = sum_vowels + sum_consonants
        sum_vowels = str(sum_vowels)
        sum_consonants = str(sum_consonants)
        sum_all = str(sum_all)

        sumv = 0
        for char in sum_vowels:
            sumv += int(char)

        sumc = 0
        for char in sum_consonants:
            sumc += int(char)

        suma = 0
        for char in sum_all:
            suma += int(char)

        final = ''
        for stg in (sumv, sumc, suma):
            stg = self.run_stage_2(stg)
            final = final + str(stg)
        return final

    def display(self, name):
        for child in self.frm.winfo_children():
            child.destroy()
        if len(name) == 0:
            return
        col = 0
        for letter in name:
            ltr = LabelMovable(self.frm, bg=BG, text=letter.upper(), font=FONT3)
            if letter in VOWELS:
                row = 0
            elif letter in CONSONANTS:
                row = 1
            ltr.grid(column=col, row=row, padx=3, pady=3)
            ltr.bind('<KeyRelease-Up>', self.recalculate)
            ltr.bind('<KeyRelease-Down>', self.recalculate)
            col += 1
        self.lab2.config(text="Notes For {}".format(self.ent1.get()))

    def store(self):
        name = self.ent1.get()
        value = self.result.cget("text")
        private_or_not = self.privvy.get()
        note = self.notes.get(1.0, 'end-1c')
        conn = sqlite3.connect(file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        cur.execute(
            '''
                INSERT INTO person 
                VALUES (null, ?, ?, ?, ?)
            ''',
            (name, value, private_or_not, note))
        conn.commit()
        self.display_stored(value=value)
        cur.close()
        conn.close()

        self.clear_inputs()

    def clear_inputs(self):
        self.private.deselect()

        self.ent1.delete(0, 'end')

        for child in self.frm.winfo_children():
            child.destroy()

        self.result.config(text="result")

        self.notes.focus_set() 

        for child in self.match_frame.winfo_children():
            child.destroy()

        self.show_all.delete(0, 'end')

        self.lab2.config(text="Notes")

        self.notes.delete(1.0, 'end')

    def set_privvy(self):
        private = self.privvy.get()
        if private == 0:
            self.privvy.set(1)
        elif private == 1:
            self.privvy.set(0)

    def display_stored(self, value=None):
        if value is None:
            value=self.show_all.get()
        conn = sqlite3.connect(file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        cur.execute(select_matching_names, (value,))
        self.matches = [list(i) for i in cur.fetchall()]
        for child in self.match_frame.winfo_children():
            child.destroy()
        w = 0
        for match in self.matches:
            mt = tk.Label(self.match_frame, text=match[1], bg=BG, fg=FG)
            mt.grid(column=0, row=w, sticky="w")
            mt.bind("<Button-1>", self.show_note)
            match.append(mt)
            w += 1
        cur.close()
        conn.close()

        self.lab2.config(text="Notes")
        self.notes.delete(1.0, 'end')

    def show_note(self, evt):
        self.notes.delete(1.0, 'end')
        self.lab2.config(text="")
        widg = evt.widget
        conn = sqlite3.connect(file)
        cur = conn.cursor()
        for lst in self.matches:
            if widg == lst[3]:
                self.clicked_person_id = lst[0]
        cur.execute(select_note, (self.clicked_person_id,))
        note = cur.fetchone()
        if note:
            if note[0]:
                self.notes.insert(1.0, note[0])
                self.lab2.config(text="Notes For {}".format(widg.cget("text")))
        cur.close()
        conn.close()

class LabelMovable(tk.Label):
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

    def __init__(self, master, first_column=0, first_row=0, *args, **kwargs):
        tk.Label.__init__(self, master, *args, **kwargs)

        self.master = master
        self.first_column = first_column
        self.first_row = first_row

        self.config(
            takefocus=1, 
            bg=BG3, 
            fg=FG, 
            font=FONT1)
        self.bind('<FocusIn>', self.highlight_on_focus)
        self.bind('<FocusOut>', self.unhighlight_on_unfocus)
        self.bind('<Key>', self.locate)
        self.bind('<Key>', self.move)

    def highlight(self, evt):
        self.config(bg=BG2)

    def unhighlight(self, evt):
        self.config(bg=BG3)

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
        evt.widget.config(bg=BG2)

    def unhighlight_on_unfocus(self, evt):        
        evt.widget.config(bg=BG3)

class Text(tk.Text):
    """ Make the Text widget use Tab key for traversal as do other widgets.
        `return('break')` prevents the built-in binding to Tab. """
    def __init__(self, master, *args, **kwargs): 
        tk.Text.__init__(self, master, *args, **kwargs)

        self.bind("<Tab>", self.focus_next_window)
        self.bind("<Shift-Tab>", self.focus_prev_window)

    def focus_next_window(self, evt):
        evt.widget.tk_focusNext().focus()
        return('break')

    def focus_prev_window(self, evt):
        evt.widget.tk_focusPrev().focus()
        return('break')

if __name__ == '__main__':

    root = tk.Tk()
    root.columnconfigure(0, weight=1)

    root.config(bg="#121212")
    root.title("Numerology 101 by Professor U. d'Guru")
    NumerologyCalculator(root)

    root.mainloop()

# TO DO: Make a delete button, there are some mistakes and duplicates in db










