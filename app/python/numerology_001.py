# numerology_001

# add notes thru person_id = 20
# readme "copy to something like celebrities.db and in that copy, delete rows where private=1 before making .sql flat file; don't share the version with your family's names in it, especially living people."
# make flat file for git; create the local and github repos


import tkinter as tk
import sqlite3
import dev_tools as dt
from dev_tools import looky, seeline





file = "d:/treebard_gps/etc/numerology.db"

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


# 922
# Edward Ernest Reinhold Junior (actor Judge Reinhold) May 21, 1957 Wilmington, Delaware
# David Robert Magin the Third (pat's brother)

# 191
# reece joseph jones 191
# Henry Mancini b. Enrico Nicola Mancini; April 16, 1924 – June 14, 1994

# 854
# Billie Jean Moffit (Billie Jean King--tennis player) born: November 22, 1943, Long Beach, California, U.S
# donald lee morey 854

# 584
# Robert Larimore Riggs (Bobby Riggs--tennis player) Born: February 25, 1918, Lincoln Heights CA
# Donald Ray Robertson
# actor Brad Pitt: William Bradley Pitt Born: 18 December 1963, Shawnee, Oklahoma, United States
# Ricky Dene Gervais, comedian, Born: June 25, 1961, Whitley, Reading, United Kingdom

# 483
# Alison Maria Krauss Born: 23 July 1971 Decatur, Illinois

# 145
# Rose Marie Fromherz

# 685
# william henry gates the third    born october 28 1955 - scorpio
# Antoinette Grace Gerber
# Mark Robert Michael Wahlberg Born: 5 June 1971, Dorchester, Boston, Massachusetts

# 628
# robert charles brozman

# 268
# Chester Burton Atkins
# Mark Alan Robertson
# John Fitzgerald Kennedy born 29 May 1917, Brookline, Massachusetts, 35th President of the United States, died November 22, 1963, at 12:30 p.m. Central Standard Time in Dallas, Texas, Dealey Plaza.

# 786
# Herbert Buckingham Khaury --Tiny Tim-- (April 12, 1932 – November 30, 1996) b. Manhattan NY
# Russell Asa Neal (inventor Bob Neal)
# David Bruce Rhaesa

# 865
# Terence Kemp McKenna  Nov 16, 1946 - Apr 3, 2000
# David Alan Richter b. Salina KS nov 5 1955
# stevenpauljobs born February 24, 1955 San Francisco, California, created Apple Computer in mid-1976 (birth name abdul lateef jandali)

# 281
# william burgess powell (amnesia victim "Benjaman Kyle") born August 29, 1948, in Lafayette, Indiana; disappeared in 1976.

# 821
# Francis Augustus Hamer (tracked down & killed Bonnie & Clyde) d. 7/10/1955
# Laura Phillips Anderson (musician Laurie Anderson)

# 246
# Pink (singer, aka Alecia Beth Moore) (born September 8, 1979)
# Roseann O'Donnell March 21, 1962
# Ferdinand Joseph LaMothe (Jelly Roll Morton)

# 426
# Geethali Norah Jones Shankar; March 30, 1979 USA
# robert eugene murray
# Taran Gostavo Braga Maquiran
# David Robert Magin Junior (pat's father)
# Henry St. Claire Fredericks Junior (musician Taj Mahal) born May 17, 1942 Harlem, New York

# 461
# David Andrew Sinclair Born: 26 June 1969, Sydney, Australia (biology of aging)

# 415
# David Byrne (songwriter, artist) 14 May 1952 (age 68) Dumbarton, Dunbartonshire, Scotland

# 235
# Zachary Monroe Bush MD, biology/environment/farming/health/teacher

# 123
# Diane Barbara Kapp

# 213
# charles hardin holly (singer Buddy Holly)  
# Nicholas Kim Coppola, (actor Nicholas Cage, born January 7, 1964, Long Beach, California)
# Elon Reeve Musk June 28, 1971 Pretoria, South Africa
# Kaspar Hauser (mystery boy)

# 112
# Aldous Leonard Huxley born July 26, 1894, Godalming, Surrey, England—died November 22, 1963, Los Angeles, California

# 764
# Clive Staples Lewis (C.S. Lewis, born November 29, 1898, Belfast, Ireland [now in Northern Ireland]—died November 22, 1963, Oxford, Oxfordshire, England)
# Harry Edward Nilsson the third (June 15, 1941 Brooklyn NY – January 15, 1994)

# 674
# Fred McFeely Rogers, TV show Mister Rogers Neighborhood, March 20, 1928 – February 27, 2003
# Matthew Paige Damon, actor (October 8, 1970 Cambridge, Massachusetts)
# Henry Saint Clair Fredericks (blues musician Taj Mahal) Born	May 17, 1942 Harlem, New York

# 617
# Michael Francis Moore April 23, 1954 Davison, Michigan
# jovilla ortega maquiran born little panay 22 Nov 1962 3:00 a.m.
# Herman Webster Mudgett aka "H H Holmes" America's first serial killer born 1861 Gilmanton, New Hampshire

# 178
# Terry Robert Miller born feb 9 1934 Neosho, Newton Co MO
# Bessie Louise Rathbun
# Mateo Gustavo Wilson born Nov 22 2020
# Hilary Ann Swank (actress), born July 30, 1974, Lincoln, Nebraska

# 371
# Donald Scott Robertson
# Opo of Opononi
# laura jeanne reese witherspoon actress born march 22 1976 - aries/taurus
# Owen Cunningham Wilson, actor born November 18, 1968 Dallas, Texas
# tammy wynette = virginia wynette pugh 371-8 May 5, 1942 – April 6, 1998
# patrick hubert kelly 371
# melissa marion ridgway 371 computer programmer/dog fanatic/hypochondriac
# the plumber who didn't wash his hands 371
# the trailer dweller who ran for pres every 4 years Jerry ? Carroll


# 731
# "Freddie Mercury"
# Bernard John Taupin 22 May 1950 (age 69) Sleaford, Lincolnshire, England (elton john's lyricist)
# Edward Harrison Norton; actor August 18, 1969, Boston, Massachusetts
# Jeffrey David McDonald

# 527
# Leonard Dietrich Orr Birth 15 Nov 1937 Walton, Delaware County, NY Death 	5 Sep 2019 Asheville, Buncombe County, NC

# 573
# Karen Anne Carpenter Mar 2, 1950, Feb 4, 1983
# William Jefferson Clinton, (pres bill clinton)

# 437
# ann marie zimmerman Capricorn
# Todd Harry Rundgren Born	June 22, 1948 Philadelphia, Pennsylvania

# 753
# John Anthony Burgess Wilson - Anthony Burgess, also called Joseph Kell, (born February 25, 1917, Manchester, England—died November 22, 1993, London)

# 718
# Joseph Levitch (comedian Jerry Lewis) March 16, 1926 - August 20, 2017 Newark, New Jersey, U.S.

# 663
# Stephen Edwin King, born September 21, 1947 Portland, Maine
# Hoyt Wayne Axton

# 933
# Jeffrey Bryne Griffy
# John David McAfee, founder of McAfee antivirus software, born 18 September 1945, Cinderford, Gloucestershire, England
# Robert Anthony De Niro Junior born August 17, 1943 New York City, U.S


# 393
# Rowan Sebastian Atkinson, Born 6 January 1955, Consett, County Durham, England

# 336
# patricia lee smith 336 (singer Patti Smith)

# 999
# Patricia Lee Huyett
# Steven Demetre Georgiou (Cat Stevens); 21 July 1948: London

# 595
# Barbara Ann Meier
# 2 1 9 2 1 9 1 1 5 5 4 5 9 5 9
#  3 1 2 3 1 1 2 6 1 9 9 5 5 5
#   4 3 5 4 2 3 8 7 1 9 5 1 1
#    7 8 9 6 5 2 6 8 1 5 6 2
#     6 8 6 2 7 8 5 9 6 2 8
#      5 5 8 9 6 4 5 6 8 1
#       1 4 8 5 1 9 2 5 9
#        5 3 4 6 1 2 7 5
#         8 7 1 7 3 9 3
#          6 8 8 1 3 3
#           5 7 9 4 6
#            3 7 4 1
#             1 2 5
#              3 7
#               1

# 955

# Alan Wilson Watts born 6 January 1915 Chislehurst, England Died	16 November 1973

# 549
# William Claude Dukenfield (W C Fields) born January 29, 1880 Darby, Pennsylvania, Died December 25, 1946

# 966
# Rodney Thomas Lunde
# Donovan Philips Leitch
# Orren Ray Robertson

# 696
# Marilyn Kay Moore

# 911
# Christine Ellen Hynde (Chrissie Hynde, The Pretenders)

# 819
# Richard Buckminster Fuller born July 12, 1895 Milton, Massachusetts
# "Luther Limbolust"
# Liv Rundgren (actress Liv Tyler) July 1, 1977, New York City, New York, U.S.
# Charlize Theron Born 7 August 1975 Benoni, South Africa
# Richard John Harris actor Born: 1 October 1930, Limerick, Ireland

# 279
# Cynthia Ann Stephanie Lauper Born: 22 June 1953 Astoria, NY
# Ann Elizabeth McCarthy (leo)

# 729
# Theodore Robert Bundy (Ted Bundy serial killer)
# Richard Milhous Nixon, Born: January 9, 1913, Yorba Linda, California 
# Thomas Earl Petty, singer
# Demi Gene Guynes, actress Demi Moore, born November 11, 1962 (quadruple Scorpio) Roswell, New Mexico, U.S.

# 742
# Eldon Russell Carter Junior
# Matthew David McConaughey, actor born November 4, 1969, Uvalde, Texas
# Reginald Kenneth Dwight 25 March 1947 Pinner, Middlesex, England (singer Elton John)

# 472
# Alicia Christian Foster  "Jodie Foster" Born: 19 November 1962, Los Angeles

# 257
# Minnie Julia Riperton was born in Chicago, Illinois on November 8, 1947
# Thomas Alva Edison Born: 11 February 1847, Milan, Ohio Died: 18 October 1931, West Orange, New Jersey
# David Vaughan Icke, conspiracy teacher, 29 April 1952 in Leicester, England

# 797
# Mark Elliot Zuckerberg

# 887
# "Limberluck"

# 538
# George Lafayette Heaton Junior
# Edward Estlin Cummings, (poet e e cummings)
# Dorthea Lauren Allegra Lapkus, comedian, born September 6, 1985, Evanston, Illinois

# 358
# Phoebe Ann Laub (Phoebe Snow) July 17, 1950 -  April 26, 2011 b. New York City

# 832
# Paul Rubenfeld, August 27, 1952, Peekskill, New York
# aka Paul Rubens aka PeeWee Herman

# 224
# John Joseph Nicholson, actor Jack Nicholson, Born: April 22, 1937, Neptune City, New Jersey
# Robin McLaurin Williams, actor and comedian, Born: July 21, 1951, St. Luke's Hospital, Chicago IL, Died: August 11, 2014, Paradise Cay, California 

# 167
# Mervyn Laurence Peake (9 July 1911 – 17 November 1968)
# James Michael Rhaesa (10 April 1957)
# James Edward Franco born April 19, 1978 Palo Alto, California
# Eunice Amelia Devenny born jun 5 1918 raton nm

# 551
# David Robert Jones (singer David Bowie)








