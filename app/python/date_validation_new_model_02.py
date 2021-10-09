# date_validation_new_model_02
# change to dates.py when finished

# CHANGE TO VERSION _02 202102081608
# Use dict until sorting has been done, then use list. Unnecessarily hard to detect many date elements by index when order doesn't even matter yet.

# CHANGE TO VERSION _03 202102101828
# 1) Storing date as iso no longer serves a purpose. I've eliminated most of the problems that EntryLabel had with inflexible data input, eg you can now leave "btwn" etc and the only problem left like that is having to retype the year 12 as 0012... can deal with that later (add a year column to db and only put something in it if the year is < len=4?... To get stored, a date has already been formatted. Then it has to be reformatted as iso and stored that way (for no reason) and then to display after being gotten out of db it has to be reformatted. When it could have been stored as a formatted date string and never mind iso.
# 2) If it becomes more convenient to make this a class then I will. Still undecided.

# GOALS
# Treat every input as if it were a compound date instead of planning to validate a single date and then having to treat compound dates as exceptional cases.
# Get ad/bc and prefixes/suffixes out of the way first and set them aside till the end
# Don't make it a class, a process is a verb not an object
# Make it take input from any widget that will hold a string
# Pass the raw string as a parameter to the first process.
# Each process will be called by the previous process so the many changes made to the evolving date string can easily be tracked. The prior version was a class so anything could be changed from anywhere and this was not appropriate for a single string with many changes being made to it.
# EntryLabel validates on focus out. Entries, Combobox, Text can validate on button or focus out.
# Don't validate possible good/bad strings one at a time. Make a superlist of possible good strings from smaller lists. Make sure no string occurs twice. Make sure two strings from the same list don't occur twice except for certain strings that can occur once for each half of a compound date. (Didn't try this.)
# don't allow any separator except a space
# the validator should not interact with the widgets in any way. EG clearing bad data from an input widget is not the validator's business, it will just cause problems because different input widgets work differently. Compromise was to make a DateError class and only this class interacts with the widgets. And only because of this class did I have to pass a widg parameter to the functions in this module.

import widgets as wdg
import styles as st
import sqlite3
from files import current_file

ST = st.ThemeStyles()
# current_file = files.get_current_file()[0]

mock_date_from_db = 'est-1846-oc-14-ad-to-abt-1855-no-12-ad'

class DateError(wdg.Toplevel):
    def __init__(self, message, widg, *args, **kwargs):
        wdg.Toplevel.__init__(self, *args, **kwargs)

        self.widg = widg
        self.title('Date Error')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frm = wdg.FrameHilited(self)
        lab = wdg.LabelHilited(frm, text=message)
        close = wdg.Button(self, text='OK', command=self.close)       

        frm.grid(column=0, row=0, padx=24, pady=(24,0), sticky='news')
        lab.grid(column=0, row=0, padx=24, pady=24)
        close.grid(column=0, row=1, pady=12)
        close.focus_set()
        self.grab_set()

        ST.config_generic(self)

    def highlight_error(self):
        '''
            Detect whether input is from wdg.EntryLabel, tk.Entry,
            ttk.Combobox, wdg.Entry, or tk.Text.
        '''

        kind = self.widg.winfo_class()
        if kind == 'Label':
            # uncomment when entrylabel fixed to unplace 
            #    instead of destroy the placed Entry:
            # self.widg.ent.select_range(0, 'end') # DO NOT DELETE
            pass
        elif kind in ('Entry', 'Combobox'):
            self.widg.select_range(0, 'end')
        elif kind == 'Text':
            pass
        elif kind == 'Frame':
            self.widg.ent.select_range(0, 'end')
        self.widg.focus_set()

    def close(self):
        self.grab_release()
        self.highlight_error()
        self.destroy()

def get_format_prefs():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(
        '''
            SELECT date_formats, abt, est, cal, bef_aft, 
                bc_ad, os_ns, span, range 
            FROM date_format 
            WHERE date_format_id = 1
        ''')
    prefs = cur.fetchall()
    prefs = [i for i in prefs[0]]
    cur.close()
    conn.close()
    return prefs

prefs = get_format_prefs()
date_format = prefs[0]
abt = prefs[1]
est = prefs[2]
cal = prefs[3]
bef_aft = prefs[4]
bc_ad = prefs[5]
os_ns = prefs[6]
from_to = prefs[7]
btwn_and = prefs[8]

simple_prefixes = {
    'est' : est,
    'abt' : abt,
    'cal' : cal}

AND_TO = ('and', 'to')

OK_MONTHS = (
    'ja', 'fe', 'mar', 'ap', 'may', 'jun', 
    'jul', 'au', 's', 'oc', 'no', 'd')

# MONTH_ABBS = (
    # 'ja.', 'jan.', 'fe.', 'feb.', 'mar.', 'ap.', 'apr.', 
    # 'jun.', 'jul.', 'au.', 'aug.', 's.', 'se.', 'sep.', 'sept.', 
    # 'oc.', 'oct.', 'no.', 'nov.', 'd.', 'de.', 'dec.')

INPUT_PFX = ['est', 'cal', 'abt', 'bef', 'aft']

INPUT_SFX = ['ad', 'bc', 'os', 'ns', 'ce', 'bce']

# OK_ABBS = INPUT_PFX + INPUT_SFX

MONTH_CONVERSIONS = {
    'ja': ['Jan',  'Jan.', 'January'],
    'fe': ['Feb',  'Feb.', 'February'],
    'mar': ['Mar',  'Mar.', 'March'],
    'ap': ['Apr',  'Apr.', 'April'],
    'may': ['May',  'May',  'May'],
    'jun': ['June', 'June', 'June'],
    'jul': ['July', 'July', 'July'],
    'au': ['Aug',  'Aug.', 'August'],
    's': ['Sep',  'Sep.', 'September'],
    'oc': ['Oct',  'Oct.', 'October'],
    'no': ['Nov',  'Nov.', 'November'],
    'd': ['Dec',  'Dec.', 'December']}

# date output options
EST = ("est", "est.", "estimated", "est'd")
ABT = ("abt", "about", "circa", "ca", "ca.", "approx.")
CAL = ("cal", "calc", "calc.", "cal.", "calc'd")
BEF = ("bef", "bef.", "prior to", "before")
AFT = ("aft", "aft.", "later than", "after")
BC = ("BCE", "BC", "B.C.E.", "B.C.")
AD = ("CE", "AD", "C.E.", "A.D.")
JUL = JULIAN = ("OS", "O.S.")
GREG = GREGORIAN = ("NS", "N.S.")

# PAIRS = ((BEF, AFT), (BC, AD), (JULIAN, GREGORIAN))
PAIRS = ((BEF, AFT), (BC, AD), (JUL, GREG))
ABB_PAIRS = []

q = 0
for pair in PAIRS:
    paired = []
    for r, s in zip(pair[0], pair[1]):
        stg = '{}/{}'.format(r, s)
        paired.append(stg)
    ABB_PAIRS.append(paired) 
    q += 1

COMPLEMENTS = (
    ('bef', 'aft'), ('bc', 'ad'), ('bc', 'ce'), 
    ('bce', 'ad'), ('bce', 'ce'), ('ns', 'os'))

DATE_PREF_COMBOS = (
    ("18 April 1906", "18 Apr 1906", "18 Apr. 1906", "April 18, 1906", 
        "Apr 18, 1906", "Apr. 18, 1906", "1906-04-18", 
        # "1906/04/18", "1906.04.18"
),
    EST, ABT, CAL,
    ABB_PAIRS[0], ABB_PAIRS[1], ABB_PAIRS[2],
    ("from [date 1] to [date 2]", "fr. [date 1] to [date 2]", 
        "frm [date 1] to [date 2]", "fr [date 1] to [date 2]"),
    ("btwn [date 1] & [date 2]", "btwn [date 1] and [date 2]",  
        "bet [date 1] & [date 2]", "bet [date 1] and [date 2]", 
        "bet. [date 1] & [date 2]" , "bet. [date 1] and [date 2]"))
        # "between [date 1] & [date 2]", "between [date 1] and [date 2]"))

DATE_FORMATS = (
    'dmy', 'dmy_abb', 'dmy_dot', 
    'mdy', 'mdy_abb', 'mdy_dot')

SPAN_FORMATS = ("from_to", "fr._to", "frm_to", "fr_to")

RANGE_FORMATS = (
    "btwn_&", "btwn_and", "bet_&", "bet_and", "bet._&", 
        "bet._and")
        # "bet._and", "between_&", "between_and")

DATE_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[0], DATE_FORMATS))

SPAN_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[7], SPAN_FORMATS))

RANGE_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[8], RANGE_FORMATS))

# OK_PREFIXES = ABT+EST+CAL+BEF+AFT
# OK_SUFFIXES = BC+AD+JULIAN+GREGORIAN

# MONTH_DICT = {
    # 'ja':'01', 'fe':'02', 'mar':'03', 'ap':'04', 'may':'05', 'jun':'06', 
    # 'jul':'07', 'au':'08', 's':'09', 'oc':'10', 'no':'11', 'd':'12'}

blank_date = {
    'link' : '',
    'date1' : {'year' : '', 'month' : '', 'day' : '', 'prefix' : '', 'suffix' : ''},
    'date2' : {'year' : '', 'month' : '', 'day' : '', 'prefix' : '', 'suffix' : ''}}

ERRORS = (
    "Date has too many terms.",
    "Repeated word in date.",
    "Year must be between 1 and 9999.",
    "Date contains conflicting information.",
    "Date is incomplete.",
    "Date is blank.",
    "Undatelike word.",
    "Too many numerical terms.",
    "Too many years input.",
    "'?' is used wrong.",
    "4-digit year required e.g. input '12 AD' as '0012'",
    "One suffix and one prefix maximum.",
    "Years have 4 digits ('1884', '0912'),\n"
        "days have 1 or 2 ('12', '02', '2'),\n"
        "and months have none ('ja', 'fe', 'mar', 'ap', 'may', etc.).",
    "The date doesn't exist."
)

ok_misc = [
    "est", "abt", "cal", "bef", "aft", ">", 
    "<", "bc", "ad", "bce", "ce", "os", "ns",
    "and", "to"]

def validate_date(date_in, widg):
    '''
        The validate_date.date_string variable is like a global
        so don't change it from more than one place. This code 
        can be made into a class if necessary but if so, don't
        change the nice way that values are passed right where
        they're needed. A lot of instance variables shouldn't be
        floating around changing each other, just to validate one string.
    '''
    process_user_input(date_in, widg)
    return validate_date.date_string

validate_date.date_string = ''

def process_user_input(date_in, widg):

    print('date_in is', date_in)

    date_dict = {
        'link' : '',
        'date1' : {'prefix' : '', 'year' : '', 'month' : '', 'day' : '', 'suffix' : ''},
        'date2' : {'prefix' : '', 'year' : '', 'month' : '', 'day' : '', 'suffix' : ''}}
    
    ok_words = list(ok_misc + list(OK_MONTHS))
    andex = None
    todex = None
    filtered = []
    spanrange = ('from', 'between', 'fr', 'frm', 'fr.', 'bet', 'bet.', 'btwn')
    ok = []
    lst = date_in.split()
    w = 0
    for word in lst:
        word = word.rstrip(',')
        if word.upper() in BC:
            ok.append('bc')
        elif word.upper() in AD:
            ok.append('ad')
        elif word.lower() in EST:
            ok.append('est')
        elif word.lower() in ABT:
            ok.append('abt')
        elif word.lower() in CAL:
            ok.append('cal')
        elif word.lower() in BEF:
            ok.append('bef')
        elif word.lower() in AFT:
            ok.append('aft')
        elif word.upper() in JUL:
            ok.append('os')
        elif word.upper() in GREG:
            ok.append('ns')
        elif word == '&':
            ok.append('and')
        elif word.lower() in spanrange:
            pass
        else:
            ok.append(word)
        w += 1   
    lst = ok
 
    length = len(lst)
    if length > 11:
        DateError(ERRORS[0], widg)
        return
    elif length == 0:
        DateError(ERRORS[5], widg)
        return
    p = 0
    copy_list = []
    for word in lst:
        low = word.lower()
        copy_list.append(low)
        p += 1
    lst = copy_list
    print("line", looky(seeline()).lineno, "lst:", lst)
    for word in lst:
        for abb in OK_MONTHS:
            if word.startswith(abb):
                word = abb
        terms_count = lst.count(word)
        if word.isalpha() is True:
            if terms_count > 2:
                DateError(ERRORS[1], widg)
                return
            elif word in ('and', 'to') and terms_count > 1:
                DateError(ERRORS[1], widg)
                return
            if word not in ok_words:
                DateError(ERRORS[6], widg)
                return

        if word.isdigit() is True:
            number = int(word)
            if number > 9999 or number < 1:
                DateError(ERRORS[2], widg)
                return

        if word == '?':
            idx = lst.index(word)
            other = list(lst)
            del other[idx]
            if '?' in other:
                DateError(ERRORS[9], widg)
                return

        filtered.append(word)
    print("line", looky(seeline()).lineno, "filtered:", filtered)
    if 'and' in filtered:
        if 'to' in filtered:
            DateError(ERRORS[3])
            return

    if 'and' in filtered:
        andex = filtered.index('and')
    elif 'to' in filtered:
        todex = filtered.index('to')
    else:
        date1 = filtered

    if andex is not None or todex is not None:
        if length < 3:
            DateError(ERRORS[4], widg)
            return
        elif todex is None:
            if '?' in filtered:
                DateError(ERRORS[9])
                return
    else:
        if length > 5:
            DateError(ERRORS[0], widg)
            return
    if andex:
        date1 = filtered[0:andex]
        date2 = filtered[andex+1:]
        date_dict['link'] = 'and'
    elif todex:
        date1 = filtered[0:todex]
        date2 = filtered[todex+1:]
        date_dict['link'] = 'to'
    else:
        date2 = ['', '', '', '', '']
        date_dict['link'] = ''
    if len(date1) > 5 or len(date2) > 5:
        DateError(ERRORS[0], widg)
        return
    print("line", looky(seeline()).lineno, "date_dict:", date_dict)
    process_date_parts(date_dict, date1, date2, widg)

def process_date_parts(date_dict, date1, date2, widg, unknown=None): 

    for date in (date1, date2):
        for pair in COMPLEMENTS:
            if pair[0] in date:
                if pair[1] in date:
                    DateError(ERRORS[3], widg)
                    return
    era_order = []
    n = 1
    for date in (date1, date2):
        if len(date) == 0:
            break
        no_suffix = True
        for suffix in ('ad', 'bc', 'ce', 'bce', 'os', 'ns'):
            if suffix in date:
                no_suffix = False
                break
        if no_suffix is True:
            date.append('ad')
        else:
            no_suffix = True            
            
        qty_terms = len(date)
        nums = 0
        for term in date:
            if term.isdigit() is True:
                nums += 1
            elif term == '?':
                if qty_terms > 2:
                    DateError(ERRORS[9], widg)
                    return
                else:
                    if n == 1:
                        unknown = 1
                    if n == 2:
                        unknown = 2                    
        if qty_terms >= 3:
            if nums > 2:
                DateError(ERRORS[7], widg)
                nums = 0
                return
            else:
                nums = 0
        elif qty_terms == 2:
            if nums > 1:
                DateError(ERRORS[7], widg)
                nums = 0
                return
            else:
                nums = 0        
        nums = 0
        for term in date:
            if term.isdigit() is True:
                nums += 1
        if nums > 2:
            nums = 0
            DateError(ERRORS[7], widg)
            return 
        else:
            nums = 0

        is_4_digits = 0
        over_2_digits = 0
        for term in date:
            if term.isdigit() is True:
                long = len(term)
                if long > 2:
                    over_2_digits += 1
                    if long == 4:
                        is_4_digits += 1
        if over_2_digits > 1:
            over_2_digits = 0
            DateError(ERRORS[8], widg)
            return
        else:
            over_2_digits = 0
        if is_4_digits < 1:
            if date[0] != '?' and len(date[1]) != 0:
                DateError(ERRORS[10], widg)
                is_4_digits = 0
                return
        else:
            is_4_digits = 0
        for affix_list in (INPUT_PFX, INPUT_SFX):
            is_affix = 0
            for term in date:
                if term in affix_list:
                    is_affix += 1
                    if is_affix > 1:
                        DateError(ERRORS[11], widg)
                        is_affix = 0
                        return
                    else:
                        is_affix += 1
                else:
                    is_affix = 0
        year = ''
        month = ''
        day = ''
        prefix = ''
        suffix = ''
        for term in date:
            if term.isdigit() is True:
                term_size = len(term)
                if term_size == 4:
                    year = term
                elif term_size == 3:
                    DateError(ERRORS[12], widg)
                    return
                elif term_size > 0 < 3:
                    day = term
            elif term.isalpha() is True:
                print('492 date.count(term) is', date.count(term))
                qty = date.count(term)
                if qty > 1:
                    DateError(ERRORS[1], widg)
                    return
                if term.startswith(OK_MONTHS) is True: 
                    month = term
                elif term in INPUT_PFX:
                    prefix = term
                elif term in INPUT_SFX:
                    suffix = term
                else:
                    print('term', term, 'not covered')
        if n == 1:
            date_dict['date1']['prefix'] = prefix
            date_dict['date1']['year'] = year
            date_dict['date1']['month'] = month
            date_dict['date1']['day'] = day
            date_dict['date1']['suffix'] = suffix
        elif n == 2:
            date_dict['date2']['prefix'] = prefix
            date_dict['date2']['year'] = year
            date_dict['date2']['month'] = month
            date_dict['date2']['day'] = day
            date_dict['date2']['suffix'] = suffix
        n += 1 
    print("line", looky(seeline()).lineno, "date_dict:", date_dict)
    apply_date_format(date_dict, widg, unknown=unknown)

def format_year_month_day(date_dict, idx):

    date1 = date_dict['date1']
    date2 = date_dict['date2']
    n = 0

    for month in (date1['month'], date2['month']):
        print("line", looky(seeline()).lineno, "month, n:", month, n)
        if len(month) == 0:
            n += 1
            continue

        for k,v in MONTH_CONVERSIONS.items():
            if month == k:
                month = v[idx]

        if n == 0:
            date_dict['date1']['month'] = month
        elif n == 1:
            date_dict['date2']['month'] = month
        n += 1

    h = 0
    for day in (date1['day'], date2['day']):

        if len(day) == 0:
            h += 1
            continue

        if 'mdy' in date_format:
            day = '{},'.format(day)
        if h == 0:
            date_dict['date1']['day'] = day
        elif h == 1:
            date_dict['date2']['day'] = day
        h += 1

    r = 0
    for year in (date1['year'], date2['year']):
        year = year.lstrip('0')
        if r == 0:
            date_dict['date1']['year'] = year
        elif r == 1:
            date_dict['date2']['year'] = year
        r += 1

def apply_date_format(date_dict, widg, unknown=None):
    print("line", looky(seeline()).lineno, "date_dict:", date_dict)
    print("line", looky(seeline()).lineno, "unknown:", unknown)
    date_string = ''
    link = None
    date1 = ''
    date2 = ''    

    if 'abb' in date_format:
        format_year_month_day(date_dict, 0)
    elif 'dot' in date_format:
        format_year_month_day(date_dict, 1)
    else:
        format_year_month_day(date_dict, 2)

    date1 = date_dict['date1']
    date2 = date_dict['date2']

    for t in range(2):   
        if t == 0:
            if unknown == 1:
                date1['year'] = ' ?'
            elif date1['suffix'] == 'ad':
                if int(date1['year']) > 999:
                    date1['suffix'] = ''
        elif t == 1:
            if len(date_dict['link']) != 0:
                if unknown == 2:
                    date2['year'] = '?'
                elif date2['suffix'] == 'ad':
                    if int(date2['year']) > 999:
                        date2['suffix'] = ''
    format_prefixes(date_dict)
    format_suffixes(date_dict)
    sort_dates(date_dict, widg, unknown=unknown)

def format_prefixes(date_dict):
    date1 = date_dict['date1']
    date2 = date_dict['date2']
    for date in (date1, date2):
            prefix = ''
            if date['prefix'] in ('abt', 'est', 'cal'):
                prefix_type = date['prefix']
                for k,v in simple_prefixes.items():
                    if prefix_type == k:
                        prefix = v
                        break
            elif date['prefix'] in ('bef', 'aft'):
                before_after = bef_aft.split('/')
                bef = before_after[0]
                aft = before_after[1]
                prefix = bef if date['prefix'] == 'bef' else aft
            if len(prefix) != 0:
                date['prefix'] = prefix

def format_suffixes(date_dict):
    date1 = date_dict['date1']
    date2 = date_dict['date2']
    for date in (date1, date2):
        suffix = ''
        if date['suffix'] in ('bc', 'ad', 'bce', 'ce'):
            era = bc_ad.split('/')
            b_c = era[0]
            a_d = era[1]
            suffix = b_c if date['suffix'] == 'bc' else a_d
        elif date['suffix'] in ('ns', 'os'):
            style = os_ns.split('/')
            o_s = style[0]
            n_s = style[1]
            suffix = o_s if date['suffix'] == 'os' else n_s
        if len(suffix) != 0:
            date['suffix'] = suffix    

def sort_dates(date_dict, widg, unknown=None):
    
    date1 = date_dict['date1']
    date2 = date_dict['date2']
    link = date_dict['link']
    date_list = [link, [date1], [date2]]

    j = 1
    for date in (date1, date2):
        sorter = []
        if len(date['month']) != 0:
            month = date['month'] # 'Oct.'
            for k,v in MONTH_CONVERSIONS.items():
                for abb in v:
                    if month == abb:
                        month = k
                        break
            d = 1
            for abb in OK_MONTHS:
                if abb == month:
                    mo = d
                    continue 
                d += 1
        else:
            mo = 0
        if date['suffix'] in BC:
            sfx = 'bc'
        elif date['suffix'] in AD or len(date['suffix']) == 0:
            sfx = 'ad'
        else:
            sfx = ''
        y = 0
        for num in (date['year'], date['day']):
            if len(num) != 0:
                if y == 0 and unknown is None:
                    yr = int(num)
                elif y == 0 and unknown is not None:
                    yr = ' ?'
                elif y == 1:
                    day = int(num.rstrip(','))
            else:
                if y == 0:
                    yr = 0
                elif y == 1:
                    day = 0
            y += 1
        sorter.extend([yr, mo, day, sfx])
        date_list[j].extend(sorter)    
        j += 1 

    era1 = date_list[1][4]
    era2 = date_list[2][4]
    era_order = (era1, era2)
    sort_this = date_list[1:]

    if len(link) != 0 and unknown is None:
        if era_order == ('ad', 'bc'):
            sort_this = sorted(
                sort_this, 
                key=lambda i: i[1:4])
            sort_this = sorted(
                sort_this, 
                key=lambda i: i[len(i)-1], 
                reverse=True)
        elif era_order == ('bc', 'bc'):
            sort_this = sorted(
                sort_this, 
                key=lambda i: i[1:4],
                reverse=True)
        elif era_order == ('ad', 'ad'):
            sort_this = sorted(
                sort_this, 
                key=lambda i: i[1:4])
        elif era_order == ('bc', 'ad'):
            sort_this = sorted(
                sort_this, 
                key=lambda i: i[len(i)-1], 
                reverse=True)

    date1 = sort_this[0][0]
    date2 = sort_this[1][0]
    link = date_dict['link']
    if link == 'and':
        link = btwn_and
    elif link == 'to':
        link = from_to
    link = link.split('_')
    if len(link[0]) != 0:
        pre = link[0]
        mid = link[1]
        begin1 = date1['prefix'] 
        begin2 = date2['prefix']
        final1 = '{} {}'.format(pre, begin1)
        final2 = '{} {}'.format(mid, begin2) 
        date1['prefix'] = final1
        date2['prefix'] = final2

    date_list[1:] = sort_this
    date1 = date_list[1]
    date2 = date_list[2]
    for date in (date1, date2):
        maxday = 31
        year = date[0]
        month = date[1] 
        day = date[2]
        if month in (4, 6, 9, 11):
            maxday = 30
        elif month == 2:
            if year % 4 == 0:
                maxday = 29
            else:
                maxday = 28
        if day > maxday:
            DateError(ERRORS[13], widg)
            return
    d1 = date_list[1][0]
    d2 = date_list[2][0]
    b = 1
    for term in (d1, d2):        
        new_list = list((
            term['prefix'], term['year'], term['month'], 
            term['day'], term['suffix']))
        date_list[b] = new_list
        b += 1
    make_date_string(date_list, unknown=unknown)

def make_date_string(date_list, unknown=None):
    date1 = date_list[1]
    date2 = date_list[2]

    if 'dmy' in date_format:
        d = 1
        for date in (date1, date2):
            reverse_dm = date[1:4]
            reverse_dm.reverse()
            date_list[d][1:4] = reverse_dm
            d += 1
    elif 'mdy' in date_format:
        e = 1
        for date in (date1, date2):
            date = date_list[e]
            date.insert(3, date.pop(1))
            e += 1
    link = ''
    t = 0
    for item in date_list:
        if t == 0:
            if len(item) != 0:
                link = ' {} '.format(item)
        if t == 1:
            if unknown == 1:
                date1 = '{}{}'.format(date1[0], date1[3])
            elif item[4] in AD or item[4] == '':
                if int(item[3]) > 999:
                    item[4] = ''
                date1 = ' '.join(item)
            elif item[4] in BC or item[4] in JUL or item[4] in GREG:
                date1 = ' '.join(item)
            else:
                print("line", looky(seeline()).lineno, "item:", item)
        elif t == 2:
            if len(link) != 0:
                if unknown == 2:
                    date2 = '{}{}'.format(date2[0], date2[3])
                elif item[4] in AD or item[4] == '':
                    if int(item[3]) > 999:
                        item[4] = ''
                    date2 = ' '.join(item)
                elif item[4] in BC or item[4] in JUL or item[4] in GREG:
                    date2 = ' '.join(item)
                else:
                    print("line", looky(seeline()).lineno, "item:", item)
        t += 1

    date_string = '{} {}'.format(date1, date2)
    if len(link) == 0:
        date_string = date1

    a = date_string.replace('    ', ' ')
    b = a.replace('   ', ' ')
    c = b.replace('  ', ' ')
    date_string = c.strip()
    print("line", looky(seeline()).lineno, "date_string:", date_string)
    validate_date.date_string = date_string
    

def get_date_from_db(widg):

    conn = sqlite3.connect('c:/treebard_gps/app/python/test_date_in_out.db')
    cur = conn.cursor()
    cur.execute(
        '''
            SELECT dates 
            FROM date_test 
            WHERE date_test_id = 1
        ''')
    stored_date = cur.fetchone()[0]
    cur.close()
    conn.close()
    print("line", looky(seeline()).lineno, "stored_date:", stored_date)
    stored_date = format_valid_iso(stored_date, widg)

    return stored_date

def format_valid_iso(stored_date, widg):
    '''
        Change the stored string to a dict of values.
        Skip validation, go straight to formatting.
    '''
    unknown = None
    stored_date
    ifdb = stored_date.split('-')
    print("line", looky(seeline()).lineno, "ifdb:", ifdb)
    date_dict = {
        'link' : ifdb[5],
        'date1' : {
            'prefix' : ifdb[0],
            'year' : ifdb[1],
            'month' : ifdb[2],
            'day' : ifdb[3],
            'suffix' : ifdb[4]},
        'date2' : {
            'prefix' : ifdb[6],
            'year' : ifdb[7],
            'month' : ifdb[8],
            'day' : ifdb[9],
            'suffix' : ifdb[10]}}

    link = date_dict['link']
    print('876 link is', link)
    if link == 'to':
        print("864 date_dict['date1']['year'], date_dict['date2']['year'] is", date_dict['date1']['year'], date_dict['date2']['year'])

    apply_date_format(date_dict, widg, unknown=unknown)
    return date_dict

# to run formatting code, start with a date in this form:
# 570 date_dict is {'link': '', 'date1': {'prefix': '', 'year': '1499', 'month': '', 'day': '', 'suffix': 'ad'}, 'date2': {'prefix': '', 'year': '', 'month': '', 'day': '', 'suffix': 'ad'}}

# DO LIST
# make iso version of good date to store in db
# get out of db make dict, test both from_db True or False, Dates from_db don't have to be validated, just formatted for display.
# show error dlg in center of screen
# move this code to dates.py and refactor as needed till it works in findings table, search table? and date prefs tab
# fix db and delete extra db tables. 



# DO LIST from _03
# MOVE THIS DO LIST TO VERSION _2 AND ROLL BACK TO _2 SINCE THE PURPOSE OF _3 WAS TO STORE FORMATTED DATES, THEN DEAL WITH EVERYTHING ON THIS DO LIST BEFORE PROCEEDING, ESPECIALLY DON'T CONCAT BETWN+EST etc. AND MAKE IT A CLASS
# year is being put in the wrong place
# Replace tuples like not in ('bet', 'bet.'...) with variables for the tuple
# Try to replace function variables (hidden globals) with return values starting with encode-date
# MAKE date code string, start with ad for suffix by default so it's never blank, and for code use 'from' 'to' 'and' 'bet'
# test with all the prefixes and suffixes
# Add 9 cols to date_format db table for default_date_formats, default_abt, etc. and query them to get vals instead of hard-coding vals
# format misc date 1663 not needed? Search class--get rid of formatting of dates and fix sorter hopefully using code already in new dates module
# Try fixing all the old dates that still display as iso, using the gui only
# hard-coded spots have to be replaced with code:
    # DatePrefsWidgets 
# make date inputs work on date prefs tab, replace this line:
    # self.date_test.validate_date_or_not(input, widg)
# make date input work in new event maker where it says this:         date_test.classify_one_date(
# move this code to dates.py and refactor as needed till it works in findings table, search table? and date prefs tab, if necessary make the validator a class 
# delete extra db tables re date settings. 
# Rewrite right click menu topics and statustips for date settings


# Put in main do list under dates: Not retyping a year less than 4 digits is not currently allowed, which is an exception to the policy that "if it can be displayed in a formatted date, then it can be left there after some edit is made." But from 1884 B.C.E. to Oct 11, 12 C.E. for example gets an error bec. 12 is not four digits. I don't want to change this now because it's an edge case. It will only happen if 1) the person is actually inputting years < 999 and 2) the user wants to edit such a date. It stores fine if input as a 4-digit year eg 0012 and the error message that comes up is correct. I'm leaving it for now.



       

    