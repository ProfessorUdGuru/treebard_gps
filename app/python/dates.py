# dates

import os
import files
import tkinter as tk
from tkinter import ttk
import sqlite3
import styles as st
import widgets as wdg
import right_click_menu as rcm
import files

'''
    Validate dates so bad dates can't be entered. Provides very 
    flexible input formats and user-selected output formats.
    Only non-ambiguous output formats are available.
'''
 
current_file = files.get_current_file()[0]

date_pref_combos = {}

ST = st.ThemeStyles()

OK_SEPTORS = (' ', '-', '/', '*', '.')

OK_MONTHS = (
    'ja', 'f', 'mar', 'ap', 'may', 'jun', 
    'jul', 'au', 's', 'oc', 'no', 'd')

MONTH_ABBS = (
    'ja.', 'jan.', 'f.', 'fe.', 'feb.', 'mar.', 'ap.', 'apr.', 
    'jun.', 'jul.', 'au.', 'aug.', 's.', 'se.', 'sep.', 'sept.', 
    'oc.', 'oct.', 'no.', 'nov.', 'd.', 'de.', 'dec.')

INPUT_PFX = ['est', 'cal', 'abt', 'bef', 'aft']

INPUT_SFX = ['ad', 'bc', 'os', 'ns', 'ce', 'bce']

OK_ABBS = INPUT_PFX + INPUT_SFX

MONTH_CONVERSIONS = {
    '01': ['01', 'Jan',  'Jan.', 'January'],
    '02': ['02', 'Feb',  'Feb.', 'February'],
    '03': ['03', 'Mar',  'Mar.', 'March'],
    '04': ['04', 'Apr',  'Apr.', 'April'],
    '05': ['05', 'May',  'May',  'May'],
    '06': ['06', 'June', 'June', 'June'],
    '07': ['07', 'July', 'July', 'July'],
    '08': ['08', 'Aug',  'Aug.', 'August'],
    '09': ['09', 'Sep',  'Sep.', 'September'],
    '10': ['10', 'Oct',  'Oct.', 'October'],
    '11': ['11', 'Nov',  'Nov.', 'November'],
    '12': ['12', 'Dec',  'Dec.', 'December']}

# date output options
EST = ("est", "est.", "estimated", "est'd")
ABT = ("abt", "about", "circa", "ca", "ca.", "approximately", "approx.")
CAL = ("cal", "calc", "calc.", "cal.", "calculated", "calc'd")
BEF = ("bef", "bef.", "prior to", "before")
AFT = ("aft", "aft.", "later than", "after")
BC = ("BCE", "BC", "B.C.E.", "B.C.")
AD = ("CE", "AD", "C.E.", "A.D.")
JULIAN = ("OS", "O.S.", "old style", "Old Style")
GREGORIAN = ("NS", "N.S.", "new style", "New Style")

PAIRS = ((BEF, AFT), (BC, AD), (JULIAN, GREGORIAN))
ABB_PAIRS = []

q = 0
for pair in PAIRS:
    paired = []
    for r, s in zip(pair[0], pair[1]):
        stg = '{}/{}'.format(r, s)
        paired.append(stg)
    ABB_PAIRS.append(paired) 
    q += 1

DATE_PREF_COMBOS = (
    ("18 April 1906", "18 Apr 1906", "18 Apr. 1906", "April 18, 1906", 
        "Apr 18, 1906", "Apr. 18, 1906", "1906-04-18", "1906/04/18", 
        "1906.04.18"),
    EST, ABT, CAL,
    ABB_PAIRS[0], ABB_PAIRS[1], ABB_PAIRS[2],
    ("from [date 1] to [date 2]", "fr. [date 1] to [date 2]", 
        "frm [date 1] to [date 2]", "fr [date 1] to [date 2]"),
    ("btwn [date 1] & [date 2]", "btwn [date 1] and [date 2]",  
        "bet [date 1] & [date 2]", "bet [date 1] and [date 2]", 
        "bet. [date 1] & [date 2]" , "bet. [date 1] and [date 2]",
        "between [date 1] & [date 2]", "between [date 1] and [date 2]"))

DATE_FORMATS = (
    'alpha_dmy', 'alpha_dmy_abb', 'alpha_dmy_dot', 'alpha_mdy', 
    'alpha_mdy_abb', 'alpha_mdy_dot', 'iso_dash', 'iso_slash', 'iso_dot')

SPAN_FORMATS = ("from_to", "fr._to", "frm_to", "fr_to")

RANGE_FORMATS = (
    "btwn_&", "btwn_and", "bet_&", "bet_and", "bet._&", 
        "bet._and", "between_&", "between_and")

DATE_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[0], DATE_FORMATS))

SPAN_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[7], SPAN_FORMATS))

RANGE_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[8], RANGE_FORMATS))

OK_PREFIXES = ABT+EST+CAL+BEF+AFT
OK_SUFFIXES = BC+AD+JULIAN+GREGORIAN

class ValidDate():
    '''
        All dates are single dates till combined for storage or display. 
        The 7 categories of date are:
        simple (18 April 1856)
        span1_known (1855 in '1855 to 1859')
        span1_unknown (? in '? to 1859')
        span2_known (1859 in '1855 to 1859')
        span2_unknown  (? in '1855 to ?')
        range1 (1900 in 'btwn 1900 and 1910')
        range2 (1910 in 'btwn 1900 and 1910')
    '''

    def __init__(self):

        self.widg = ''
        self.year = ''
        self.month = ''
        self.day = ''
        self.pref = ''
        self.suff = ''
        self.prefix = ''
        self.suffix = ''
        self.code = ''
        self.small = []
        self.med = []
        self.big = []
        self.numbers = []
        self.output_1 = '' # formatted date
        self.output_2 = '' # formatted date
        self.date_1 = '' # iso date saved for end of 2-date process
        self.link = []
        self.date_to_store = '' # single final iso or first iso for later

        self.date_format = ''
        self.est_format = ''
        self.abt_format = ''
        self.cal_format = ''
        self.befaft_format = ''
        self.epoch_format = ''
        self.julegreg_format = ''

        self.input_type = ''
        self.and_to = None
        self.input_1 = [] # raw input
        self.input_2 = [] # raw input
        self.iso_date = '' # standardized single iso date

        self.valid = True
        self.ents = []
        self.cols = []
        self.valids = []
        self.clarifier_is_running = False
        self.unknowns = []
        self.ok = None
        self.frm = None

        self.finding_id = None

# UTILITIES

    def reset_all_vars(self):
        self.reset_one_use_vars()
        self.and_to = None
        self.output_1 = ''
        self.output_2 = ''
        self.date_1 = ''
        self.link = []
        self.input_1 = []
        self.input_2 = []
        self.widg = ''
        self.date_to_store = ''
        self.finding_id = None
        self.clarifier_is_running = False

    def reset_one_use_vars(self):
        
        self.year = ''
        self.month = ''
        self.day = ''
        self.pref = ''
        self.suff = ''
        self.prefix = ''
        self.suffix = ''
      
        self.code = ''
        self.small = []
        self.med = []
        self.big = []
        self.numbers = []
        self.iso_date = ''

        self.valid = True
        self.ents = []
        self.cols = []
        self.valids = []
        self.unknowns = []
        self.ok = None
        self.frm = None

    def store_valid_date(self):
        ''' 
            finding_id is sent over from FindingsTable class where 
            it's used to identify a row in the findings table. Gets validated
            date from edited findings table date fields on FocusOut,
            and stores it in ISO format in the right row of the finding table 
            in database.
        '''
        
        current_file = files.get_current_file()[0]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        cur.execute('''
            UPDATE finding 
            SET date = ? 
            WHERE finding_id = ?''', 
            (self.date_to_store, self.finding_id))
        conn.commit()
        cur.close()
        conn.close()

    def strip_lead_trail(self, stg, sym):
        stg = stg.strip(sym)
        return stg

    def fix_double_spaces(self, stg, delim):
        ''' e.g. "   1985    05   12-*   " becomes "1985 05 12" '''

        # run loop more than once in case user inputs various septors
        for sym in delim:
            stg = self.strip_lead_trail(stg, sym)
        for sym in delim:
            stg = self.strip_lead_trail(stg, sym)
        for sym in delim:
            stg = self.strip_lead_trail(stg, sym)
        for sym in delim:
            if sym*2 in stg:
                stg = stg.replace(sym*2, sym)
                stg = self.fix_double_spaces(stg, delim)
        return stg

    def minimize_mo_stg(self, mo_stg):
        if mo_stg.startswith(('j', 'm')):
            month = mo_stg[0:3]
        elif mo_stg.startswith(('a', 'o', 'n')):
            month = mo_stg[0:2]
        else:
            month = mo_stg[0]
        if month == 'jan':
            month = 'ja'
        return month

    def change_month_to_num(self, mo_stg):
        ISO_MONTHS = {
            'ja': '01', 'f': '02', 'mar': '03', 'ap': '04', 'may': '05', 
            'jun': '06', 'jul': '07', 'au': '08', 's': '09', 'oc': '10', 
            'no': '11', 'd': '12'}
        for k,v in ISO_MONTHS.items():
            if mo_stg.lower().startswith(k) is True:
                month = v
        return month

    def validate_month_by_length(self):
        if self.month is None:
            self.day = '00'
            return '00'
        elif int(self.month) in (4, 6, 9, 11):
            if len(self.day) == 0:
                self.day = '00'
            if int(self.day) > 30:
                self.widg.clear_bad_data(
                    'int(self.day) > 30', 'That month has only 30 days.')
                self.reset_all_vars()
                return

        elif int(self.month) == 2:
            leap = False
            if int(self.year)%4 == 0:
                if int(self.year)%100 == 0:
                    if int(self.year)%400 == 0:
                        leap = True
                elif int(self.year)%100 != 0:
                    leap = True
            if len(self.day) == 0:
                self.month = '2'
            elif leap is False:
                if int(self.day) > 28:
                    self.widg.clear_bad_data(
                    'int(self.day) > 28', 'February in a non-leap-year '
                        'has only 28 days.')
                    self.reset_all_vars()
                    return
                else:
                    self.month = '2'
            elif leap is True:
                if int(self.day) > 29:
                    self.widg.clear_bad_data(
                    'int(self.day) > 29', 'February in a leap year '
                        'has only 29 days.')
                    self.reset_all_vars()
                    return
                else:
                    self.month = '2'
        return self.month

    def standardize_for_iso(self):
        if len(self.year) < 4:
            zeroes = 4 - len(self.year)
            self.year = '0' * zeroes + self.year
        if self.month is not None and len(self.month) < 2:
            zeroes = 2 - len(self.month)
            self.month = '0' * zeroes + self.month
        if self.day is not None and len(self.day) < 2:
            zeroes = 2 - len(self.day)
            self.day = '0' * zeroes + self.day
        if len(self.suff) > 0:
            self.suff = self.suff
        date = '{}-{}-{}-{}-{}'.format(
            self.pref, self.year, self.month, self.day, self.suff)
        if self.input_type in ('range1', 'span1'):
            self.date_1 = date
        return date

    def handle_commas(self, input, day, septor, comma_count):
        if comma_count == 1:
            idx_comma = input.find(',')
            idx_septor = input.find(septor)
            idx_last = len(input) - 1
            idx_septor_rt = input.rfind(septor)
            if idx_septor < idx_comma and idx_comma != idx_last:
                day = input[idx_septor+1:idx_comma]
            elif idx_septor < idx_comma and idx_comma == idx_last:
                day = input[idx_septor_rt + 1:idx_last]
                if len(day) > 2 or int(day) > 31:
                    self.widg.clear_bad_data(
                        'len(day) > 2 or int(day) > 31',
                        'Day over 31 or too many digits.')
                    self.reset_all_vars()
                    return
            elif idx_septor > idx_comma:
                day = input[0:idx_comma]

        input = input.replace(',', '')
        return input

# HANDLE RAW INPUT
    # the variable input seems to be unused here
    def validate_date_or_not(self, input, widg, finding_id=None):
        ''' 
            When clarifier dialog opens, it sets a variable to True
            so that the FocusOut of the events table cell will
            not trigger another validation process.  
        '''

        if self.clarifier_is_running is True:
            self.clarifier_is_running = False
            return
        elif self.clarifier_is_running is False:
            self.classify_one_date(widg, finding_id=finding_id)

    def classify_one_date(self, widg, finding_id=None):
        ''' 
            Gets raw input, figures out what kind of input 
            it contains, and runs the right function for 
            that type of input. If two dates are in the input, 
            the first date in the compound date is run first 
            but both dates are classfied immediately upon 
            FocusOut. The input_type value refers to the first 
            date till its validation process is complete, then 
            it is set to the value and input_type of the second 
            date in the compound input. 
            Runs on FocusOut of any date input widget
            if widget contents have changed or when constructing 
            findings table from stored data. If date comes from db it's 
            already validated and no validation is done. finding_id 
            is not used in this function but is set here because it's 
            passed in from self.validate_date_or_not() being called 
            in the FindingsTable class where it says v(input, widg,
            finding_id=self.finding_id) in use_input(). self.finding_id 
            is set by FocusIn or Button-1 click in EntryLabel using
            get_cell_ref(). If input 
            is typed into findings table cell by user, input has to be 
            validated and finding_id is needed. If user input is 
            typed into a tester field in the date prefs tab, validation 
            is done but no finding_id is needed. If user clicks in a 
            field that displays an existing date, 
            but tabs out w/out making changes, 
            no validation is done. self.finding_id is not None when 
            input is from user editing date on findings table; 
            self.finding_id is not None when input is making table 
            from values stored in db; self.finding_id is None when 
            input is from tester date fields in prefs. ''' 

        self.widg = widg
        self.finding_id = finding_id
        # EntryLabel or Entry? (Entry inherits from Frame)
        if self.widg.winfo_class() == 'Label':
            input = self.widg.cget('text')
        elif self.widg.winfo_class() == 'Frame':
            input = self.ent.widg.get()

        if len(input) == 0:
            self.date_to_store = '-0000-00-00-'
            self.store_valid_date()
            return

        if input.count('?') > 1:
            self.widg.clear_bad_data(
                "input.count('?') > 1", 
                "Only one unknown date allowed in span.")
            self.reset_all_vars()
            return

        if ' to ' in input:
            self.and_to = ' to '
        elif ' and ' in input:
            self.and_to = ' and '
        else:
            self.input_type = 'single'
            self.input_1 = input

        if self.and_to:
            lst = input.split(self.and_to)
            self.input_1 = [lst[0]]
            self.input_2 = [lst[1]]

        if self.and_to == ' to ' and '?' in input:
            d = 0
            for lst in [self.input_1, self.input_2]:

                if lst[0].strip() == '?' and d == 0:
                    self.input_type = 'span1_unknown'
                    self.input_2.append('span2')
                elif lst[0].strip() == '?' and d == 1:
                    self.input_type = 'span1'
                    self.input_1 = self.input_1[0]
                    lst.append('span2_unknown')
                d += 1
        elif self.and_to == ' to ':
            self.input_type = 'span1'
            self.input_1 = self.input_1[0]
            self.input_2.append('span2')
        elif self.and_to == ' and ':
            self.input_type = 'range1'
            self.input_1 = self.input_1[0]
            self.input_2.append('range2')

        if self.input_type in ('single', 'span1', 'range1'):
            self.prepare_date(self.input_1)
        elif self.input_type == 'span1_unknown':
            self.output_unknown_span1()

# METHODS FOR DATES TREATED IN ISOLATION FROM OTHER DATES 

    def prepare_date(self, input):
        input = self.fix_double_spaces(input, OK_SEPTORS)

        for abbrev in MONTH_ABBS:
            if input.find(abbrev.lower()) != -1:
                new_abbrev = abbrev.strip('.')
                input = input.replace(abbrev, new_abbrev)

        septors = []
        for char in input:
            if char in OK_SEPTORS and char not in septors:
                septors.append(char)
        day = '00'

        comma_count = input.count(',')
        if comma_count > 1:
            self.widg.clear_bad_data(
                "comma_count > 1",
                "Too many commas in date input.")
            self.reset_all_vars()
            return

        if len(septors) == 0:
            input = [input]
        elif len(septors) == 1:
            septor = septors[0]
            if ',' in input:

                input = self.handle_commas(input, day, septor, comma_count)
            if input:
                input = input.split(septor)
            elif input is None:
                return
        else:
            self.widg.clear_bad_data(
                "len(septors) != 1 or 0",
                "No more than one character out of [space, dot, "
                    "forward slash, dot, or star] can be used as a "
                    "separator between date parts. Exception: "
                    "only a space can be used as a spacer around "
                    "'and' or 'to'. HINT: Just separate all date "
                    "parts with a space.")
            self.reset_all_vars()
            return

        for char in input:            
            if char.isalnum() is False and char not in OK_SEPTORS:
                self.widg.clear_bad_data(
                    'non-alphanum char not in OK_SEPTORS',
                    'That character is not allowed in a date input.')
                self.reset_all_vars()
                return

        self.sift_input(input, day=day)

    def sift_input(self, input, day='00'):

        words = []
        prefixes = []
        suffixes = []
        months = []
        mo_stg = ''
        a = '00'
        c = None
        d = None
        if len(input) > 5:
            self.widg.clear_bad_data(
                'len(input) > 5', 
                'A date can have only five parts including '
                    'prefix and suffix.')
            self.reset_all_vars()
            return

        for part in input:
            if part.isalpha() is True:
                words.append(part)

        for word in words:
            if words.count(word) > 1:
                self.widg.clear_bad_data(
                    'words.count(word) > 1', 
                    'A word can\'t be repeated within a single date.')
                self.reset_all_vars()
                return
            word = word.lower()
            if word in OK_ABBS and word in OK_PREFIXES:
                prefixes.append(word)
            elif word in OK_ABBS and word.upper() in OK_SUFFIXES:
                suffixes.append(word)
            elif word.startswith(OK_MONTHS) is True:
                months.append(word)
            else:
                month = ''
                self.widg.clear_bad_data(
                    'bad month string', 
                    'Misc. date input error, error type unknown.')
                self.reset_all_vars()
                return 

        if len(prefixes) > 1 or len(suffixes) > 1 or len(months) > 1:
            self.widg.clear_bad_data(
                'len(prefixes) > 1 or len(suffixes) > 1 or '
                    'len(months) > 1', 
                'More than one prefix, suffix, or month was input.')
            self.reset_all_vars()
            return
        else:
            if len(prefixes) == 1:
                self.pref = prefixes[0]
            if len(suffixes) == 1:
                self.suff = suffixes[0].upper()

            if len(months) == 1:
                mo_stg = months[0]
                mo_stg = self.minimize_mo_stg(mo_stg)
                a = self.change_month_to_num(mo_stg)
            else:
                month = '00'
        for part in input:
            if part.isnumeric() is True:
                if len(part) == 1:
                    part = '0{}'.format(part)
                self.numbers.append(part)
        if len(self.numbers) > 3:
            self.widg.clear_bad_data(
                'len(self.numbers) > 3', 
                'More than three numbers were input.')
            self.reset_all_vars()
            return

        if len(day) == 1:
            day = '0{}'.format(day)

        same = False
        for num in self.numbers:
            if int(num) > 9999 or len(num) > 5:
                self.widg.clear_bad_data(
                    'int(num) > 9999 or len(num) > 5',
                    'Maximum year is 9999.')
                self.reset_all_vars()
                return
            if (5 > len(num) > 2) or (31 < int(num) < 10000):
                self.big.append(num)
            elif 0 < len(num) < 3:
                # code c is btwn 1 & 12 known to be a day 
                #    because it follows a comma
                # code d ditto btwn 13 & 31
                if 0 < int(num) < 13:
                    if num != day:
                        self.small.append(num)
                    elif num == day and same is False:
                        c = day
                        same = True
                    elif num == day and same is True:                        
                        self.small.append(num)
                elif 12 < int(num) < 32:
                    if num != day:
                        self.med.append(num)
                    elif num == day:
                        d = day
                elif int(num) == 0:
                    pass          
                else:
                    self.widg.clear_bad_data(
                        'bad number input', 
                        'Misc. date input error of unknown type.')
                    self.reset_all_vars()
                    return             

        sm = len(self.small)
        self.code = self.code + 's' * sm
        md = len(self.med)
        self.code = self.code + 'm' * md
        bg = len(self.big)
        self.code = self.code + 'b' * bg
        if a != '00':
            self.code = self.code + 'a'

        if day != '00':
            if c is not None:           
                self.code = self.code + 'c'
                self.grok_codes(month=a, day=c)
            elif d is not None:           
                self.code = self.code + 'd'
                self.grok_codes(month=a, day=d)
        else:
            self.grok_codes(month=a)

    def grok_codes(self, month='00', day='00'):
        indented_bullet = '\n   \u2022 '.format()
        if ('bb' in self.code or 'cc' in self.code or
                'aa' in self.code or 'dd' in self.code or
                self.code in (
            'mmm', 'mmb', 'mmc', 'mbc', 'a', 
            'c', 'd', 'mm', 'mb', '')):
                self.widg.clear_bad_data(
                    'disallowed date code',
                    'Not a valid date for one of these reasons:'
                        '{}no input for month;{}no input for year;'
                        '{}too many numbers over 31;{}more than one month '
                        'given;{}more than one day given.'.format(
                            indented_bullet, indented_bullet, indented_bullet,
                            indented_bullet, indented_bullet))
                self.reset_all_vars()
                return

        if self.code in ('smm',):
            self.month = self.small[0]
            self.numbers = sorted(self.numbers)
            x = self.numbers[1]
            if self.numbers[2] == x:
                self.year = x
                self.day = x            
            else:
                self.make_iso()
                return

        elif self.code in ('smd', 'smc'):
            self.month = self.small[0]
            self.year = self.med[0]
            self.day = day

        elif self.code in ('ssb',):
            self.numbers = sorted(self.numbers, reverse=True)
            x = self.numbers[1]
            if self.numbers[2] == x:
                self.year = self.numbers[0]
                self.month = x
                self.day = x
            else:
                self.year = self.big[0]
                self.make_iso()
                return

        elif self.code in ('sbc', 'sbd'):
            self.month = self.small[0]
            self.year = self.big[0]
            self.day = day

        elif self.code in ('sba',):
            self.year = self.big[0]
            self.month = month
            self.day = self.small[0]

        elif self.code in ('bac', 'bad'):
            self.year = self.big[0]
            self.month = month
            self.day = day

        elif self.code in ('smb', 'mba'):
            self.year = self.big[0]
            self.day = self.med[0]
            if 's' in self.code:
                self.month = self.small[0]
            else:
                self.month = month

        elif self.code in ('sss',):
            x = self.numbers[0]
            if self.numbers[1] == x and self.numbers[2] == x:
                self.year = x
                self.month = x
                self.day = x
            else:
                self.make_iso()
                return

        elif self.code in ('ssc',):
            self.day = day
            x = self.numbers[0]
            if self.numbers[1] == x and self.numbers[2] == x:
                self.year = x
                self.month = x
            else:
                self.make_iso()
                return

        elif self.code in ('ssm',):
            self.numbers = sorted(self.numbers)
            month = self.numbers[0]
            if self.numbers[1] == month:
                self.month = month
                self.make_iso()
                return
            else: 
                self.make_iso()
                return

        elif self.code in ('ssd',):
            self.day = day
            self.numbers = sorted(self.numbers)
            x = self.numbers[0]
            if self.numbers[1] == x:
                self.year = x
                self.month = x
            else:
                self.make_iso()
                return

        elif self.code in ('ssa',):
            self.month = month

            x = int(month)
            if int(self.numbers[0]) == x and int(self.numbers[1]) == x:
                yr = str(x)
                mo = str(x)
                dy = str(x)
                self.add_zeroes(yr, mo, dy)

            elif (int(self.numbers[0]) != x and 
                    int(self.numbers[0]) == int(self.numbers[1])):
                yr = str(self.numbers[0])
                mo = str(x)
                dy = yr
                self.add_zeroes(yr, mo, dy)

            else:
                self.month = month
                self.make_iso()
                return

        elif self.code in ('sac', 'sad'):
            self.year = self.small[0]
            self.month = month
            self.day = day

        elif self.code in ('sma', 'mma'):
            self.month = month
            self.make_iso()
            return

        elif self.code in ('mac', 'mad'):
            self.year = self.med[0]
            self.month = month
            self.day = day

        elif len(self.code) < 3:
            if 'c' in self.code or 'd' in self.code:
                self.widg.clear_bad_data(
                    "len(self.code) < 3 and 'c' or 'd' in self.code",
                    "If date has only two parts, one of them can't "
                        "be a day. (Treebard interprets any number "
                        "following a comma to be a day.)")
                self.reset_all_vars()
                return
            day = '00'
            if self.code in ('sa', 'ma'):
                self.month = month
                if self.code[0] == 's':
                    self.year = self.small[0]
                elif self.code [0] == 'm':
                    self.year = self.med[0]
            elif self.code in ('ba',):
                self.year = self.big[0]
                self.month = month
            elif self.code in ('ss',):
                x = self.numbers[0]
                if self.numbers[1] == x:
                    self.year = x
                    self.month = x
                else:
                    self.day = day
                    self.make_iso()       
                    return
            elif self.code in ('sm',):
                self.year = self.med[0]
                self.month = self.small[0]
            elif self.code in ('sb',):
                self.year = self.big[0]
                self.month = self.small[0]
            elif self.code in ('s', 'm', 'b'):
                self.month = None
                self.day = None
                if self.code in ('s',):
                    self.year = self.small[0]            
                elif self.code in ('m',):
                    self.year = self.med[0]
                elif self.code in ('b',):
                    self.year = self.big[0]
        self.month = self.validate_month_by_length()
        if self.month:
            self.iso_date = self.standardize_for_iso()
            if self.input_type in ('single', 'range1', 'span1'):
                self.output_first_date()
            elif self.input_type in ('range2', 'span2'):
                self.output_second_date()
            elif self.input_type == 'span2_unknown':
                self.output_unknown_span2()

    def format_one_date(self):
        self.update_display_prefs()
        date = self.apply_display_prefs()
        print('dates 859 self.widg is', self.widg)
        if self.widg.winfo_class() == 'Label':
            self.widg.config(text=date)
        elif self.widg.winfo_class() == 'Frame':
            pass
        self.reset_all_vars()

# METHODS FOR MEMBERS OF A PAIR OF DATES COMPRISING A COMPOUND DATE

    def output_unknown_span1(self):

        self.output_1 = '?'
        self.input_type = self.input_2[1]
        self.input_2 = self.input_2[0]
        self.reset_one_use_vars()

        self.prepare_date(self.input_2)

    def output_unknown_span2(self):

        span_format = self.link[0].split('_')

        ordered_compound_date = '{} {} {} ?'.format(
            span_format[0], self.output_1, span_format[1])

        if self.widg.winfo_class() == 'Label':
            self.widg.config(text=ordered_compound_date)
            # self.widg.config(state='normal')
            # self.widg.config(text=ordered_compound_date)
            # self.widg.config(state='readonly', width=len(self.widg.get()))
        elif self.widg.winfo_class() == 'Frame':
            pass
     
        self.date_to_store = '{}-to-?'.format(self.date_1)
        if self.finding_id:
            self.store_valid_date()
        self.reset_all_vars()
        return ordered_compound_date

    def output_first_date(self):

        date = self.iso_date.split('-')
        self.prefix = date[0]
        self.year = date[1]
        self.month = date[2]
        self.day = date[3] 
        self.suffix = date[4]
        self.date_to_store = '{}-{}-{}-{}-{}'.format(
            self.prefix, self.year, self.month, 
            self.day, self.suffix)
        if self.input_type == 'single':
            if self.finding_id:
                self.store_valid_date()
            self.format_one_date()

        elif self.input_type in ('span1', 'range1'):
            self.format_first_date()

    def format_first_date(self):

        self.update_display_prefs()

        date = self.apply_display_prefs()

        self.output_1 = date
        self.input_type = self.input_2[1]
        self.input_2 = self.input_2[0]

        self.reset_one_use_vars()
        if self.input_type in ('span2', 'range2'):
            self.prepare_date(self.input_2)
        elif self.input_type == 'span2_unknown':
            self.output_unknown_span2()

    def output_second_date(self):

        if self.output_1 == '?':
            self.date_1 == '?'

        date = self.iso_date.split('-')
        self.prefix = date[0]
        self.year = date[1]
        self.month = date[2]
        self.day = date[3] 
        self.suffix = date[4]
        self.date_to_store = '{}-{}-{}-{}-{}-{}-{}'.format(
            self.date_1, self.and_to.strip(), 
            self.prefix, self.year, self.month, 
            self.day, self.suffix)
        self.format_second_date()

    def format_second_date(self):

        self.update_display_prefs()

        date = self.apply_display_prefs()
        self.output_2 = date

        if self.output_1 == '?':

            span_format = self.link[0].split('_')  
            
            link = self.and_to.replace(' ', '-')

            self.date_to_store = '?-to-{}'.format(self.iso_date)

            if self.finding_id:
                self.store_valid_date()

            ordered_compound_date = '{} ? {} {}'.format(
                span_format[0], span_format[1], self.output_2)  

        else:
            both_ymd = []
            for stg in (self.date_1, self.iso_date):
                stg = stg.strip('-')
                both_ymd.append(stg.split('-'))
            ordered_compound_date = self.sort_by_era(both_ymd)

        self.widg.config(text=ordered_compound_date)

        self.reset_all_vars()

    def sort_by_era(self, both_ymd):
        sorter_by_epoch = []

        e = 0            
        for lst in both_ymd:
            last_stg = len(lst) - 1
            sfix = ''
            if (lst[last_stg].isalpha() is True and 
                    lst[last_stg] not in ('ns', 'os')):                
                sfix = lst[last_stg]
            mo = 0
            dy = 0
            if lst[0].isalpha() is True:
                f = 1
            elif lst[0].isalpha() is False:
                f = 0
            yr = int(lst[f]) 
            if lst[f+1] != '00':
                mo = int(lst[f+1])
                if lst[f+2] != '00':
                    dy = int(lst[f+2])
            int_date = (yr, mo, dy)
            if e == 0:
                sorter_by_epoch.append(
                    [int_date, self.output_1, sfix, self.date_1])
            elif e == 1:
                sorter_by_epoch.append(
                    [int_date, self.output_2, sfix, self.iso_date])
            e += 1
        one_suffix = sorter_by_epoch[0][2]
        other_suffix = sorter_by_epoch[1][2]
        if one_suffix in ('', 'ad') and other_suffix in ('', 'ad'):
            dates = sorted(sorter_by_epoch)
        elif one_suffix == 'bc' and other_suffix == one_suffix:
            dates = sorted(sorter_by_epoch, reverse=True)
        elif other_suffix == 'bc' and one_suffix in ('', 'ad'):
            dates = [sorter_by_epoch[1], sorter_by_epoch[0]]
        elif other_suffix in ('', 'ad') and one_suffix == 'bc':
            dates = [sorter_by_epoch[0], sorter_by_epoch[1]]
        first_date = dates[0][1]
        second_date = dates[1][1]
        span_format = self.link[0].split('_')
        range_format = self.link[1].split('_')
     
        if self.and_to == ' to ':
            ordered_compound_date = '{} {} {} {}'.format(
                span_format[0], first_date, span_format[1], second_date)
        elif self.and_to == ' and ':
            ordered_compound_date = '{} {} {} {}'.format(
                range_format[0], 
                first_date, 
                range_format[1], 
                second_date)

        iso_1 = dates[0][3]        
        iso_2 = dates[1][3]
        link = self.and_to.replace(' ', '-')

        self.date_to_store = '{}{}{}'.format(
            iso_1, link, iso_2)

        if self.finding_id:
            self.store_valid_date()
        return ordered_compound_date

# APPLY USER FORMAT DISPLAY PREFERENCES

    def format_unknown_date_for_table(self, parts):
        self.update_display_prefs()
        if parts[6] == '?':
            self.prefix = parts[0]
            self.year = parts[1]
            self.month = parts[2]
            self.day = parts[3]
            self.suffix = parts[4]
            date1 = self.apply_display_prefs()

            span_format = self.link[0].split('_')

            ordered_compound_date = '{} {} {} ?'.format(
                span_format[0], date1, span_format[1])
            self.reset_all_vars()
       
        elif parts[0] == '?':
            self.prefix = parts[2]
            self.year = parts[3]
            self.month = parts[4]
            self.day = parts[5]
            self.suffix = parts[6]
            date2 = self.apply_display_prefs()

            span_format = self.link[0].split('_')

            ordered_compound_date = '{} ? {} {}'.format(
                span_format[0], span_format[1], date2)
            self.reset_all_vars()

        return ordered_compound_date

    def select_function(self, value, widg=None):

        self.widg = widg
        parts = value.split('-')
        if parts[6] == '?' or parts[0] == '?':
            return self.format_unknown_date_for_table(parts)
        else:
            return self.format_compound_date_for_table(value)        

    def format_compound_date_for_table(self, value):
        parts = value.split('-')
        self.update_display_prefs()

        self.prefix = parts[0]
        self.year = parts[1]
        self.month = parts[2]
        self.day = parts[3]
        self.suffix = parts[4]
        date1 = self.apply_display_prefs()

        self.and_to = ' {} '.format(parts[5])
        self.prefix = parts[6]
        self.year = parts[7]
        self.month = parts[8]
        self.day = parts[9]
        self.suffix = parts[10]
        date2 = self.apply_display_prefs()

        self.output_1 = date1
        self.output_2 = date2

        two_iso = value.split(self.and_to.strip())

        both_ymd = []
        for stg in two_iso:
            stg = stg.strip('-')
            both_ymd.append(stg.split('-'))
        ordered_compound_date = self.sort_by_era(both_ymd)

        self.reset_all_vars()
        return ordered_compound_date

    def format_date_for_table(self, value, widg=None):
        ''' Formats single dates. '''

        self.update_display_prefs()
        self.widg = widg
        parts = value.split('-')
        self.prefix = parts[0]
        self.year = parts[1]
        self.month = parts[2]
        self.day = parts[3]
        self.suffix = parts[4]
        date = self.apply_display_prefs()

        self.reset_all_vars()
        return date

    def update_display_prefs(self):

        date_formats_all = self.get_date_output_prefs()
        self.date_format = date_formats_all[0]
        self.est_format = date_formats_all[1]
        self.abt_format = date_formats_all[2]
        self.cal_format = date_formats_all[3]
        self.befaft_format = date_formats_all[4]
        self.epoch_format = date_formats_all[5]
        self.julegreg_format = date_formats_all[6]
        span_format = date_formats_all[7]
        range_format = date_formats_all[8]
        if self.and_to:
            self.link = self.pass_compound_format(
                span_format, range_format)

    def add_zeroes(self, yr, mo, dy):

        if len(yr) < 4:
            self.year = yr.zfill(4)
        if mo is not None and len(mo) < 2:
            self.month = mo.zfill(2)
        if dy is not None and len(dy) < 2:
            self.day = dy.zfill(2)
        elif dy is not None and len(dy) == 2:
            self.day = dy

    def apply_display_prefs(self):

        if self.prefix in EST:
            self.prefix = self.est_format
        elif self.prefix in ABT:
            self.prefix = self.abt_format
        elif self.prefix in CAL:
            self.prefix = self.cal_format
        elif self.prefix in BEF+AFT:
            choices = self.befaft_format.split('/')
            if self.prefix == 'bef':
                self.prefix = choices[0]
            elif self.prefix == 'aft':
                self.prefix = choices[1]
        if self.suffix.upper() in BC+AD:
            choices = self.epoch_format.split('/')
            if self.suffix in ('bc', 'bce', 'BC', 'BCE'):
                self.suffix = choices[0]
            elif self.suffix in ('ad', 'ce', 'AD', 'CE'):
                self.suffix = choices[1]
        elif len(self.suffix) == 0 and (0 < int(self.year) < 1000):
            choices = self.epoch_format.split('/')
            self.suffix = choices[1]

        elif self.suffix.upper() in JULIAN+GREGORIAN:
            choices = self.julegreg_format.split('/')
            if self.suffix == 'os':
                self.suffix = choices[0]
            elif self.suffix == 'ns':
                self.suffix = choices[1]

        if self.date_format.startswith('alpha') is True:
            abc_form = True
            iso_form = False
        elif self.date_format.startswith('iso') is True:
            iso_form = True
            abc_form = False

        if abc_form is True:
            if self.date_format.endswith('abb'):
                for k,v in MONTH_CONVERSIONS.items():
                    if self.month == k:
                        self.month = v[1]
            elif self.date_format.endswith('dot'):
                for k,v in MONTH_CONVERSIONS.items():
                    if self.month == k:
                        self.month = v[2]
            else:
                for k,v in MONTH_CONVERSIONS.items():
                    if self.month == k:
                        self.month = v[3]

            if self.day == ('00'):
                self.day = ''

            self.year = self.year.lstrip('0')

            if self.month == '00':
                self.month = ''

            if 'dmy' in self.date_format:
                date = '{} {} {} {} {}'.format(
                    self.prefix, self.day, self.month, 
                    self.year, self.suffix)
                date = date.replace('  ', ' ').replace('  ', ' ')

            elif 'mdy' in self.date_format:
                if len(self.month) > 0:
                    if len(self.day) > 0:
                        date = '{} {} {}, {} {}'.format(
                            self.prefix, self.month, self.day, 
                            self.year, self.suffix)
                    elif len(self.day) == 0:
                        date = '{} {} {} {}'.format(
                            self.prefix, self.month, self.year, 
                            self.suffix)
                elif len(self.month) == 0 and len(self.day) == 0:
                    date = '{} {} {}'.format(self.prefix, self.year, 
                        self.suffix)

        elif iso_form is True:
                
            if self.date_format.endswith('dash') is True:
                septor = '-'
            elif self.date_format.endswith('slash') is True:
                septor = '/'
            elif self.date_format.endswith('dot') is True:
                septor = '.'
            date = '{} {}{}{}{}{} {}'.format(
                self.prefix, self.year, septor, self.month, 
                septor, self.day, self.suffix)

        date = date.strip()
        
        return date 

    def pass_compound_format(self, h, r):
        lst = [h, r]
        return lst

    def get_date_output_prefs(self):

        current_file = files.get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute('''
            SELECT date_format, est, abt, cal, bef_aft, 
                bc_ad, os_ns, span, range 
            FROM date_per_tree 
            WHERE date_per_tree_id = 1''')
        tree_date_format = cur.fetchall()[0]
        cur.close()
        conn.close()

        # conn = sqlite3.connect(st.conn_fig)
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        cur.execute('''
            SELECT date_format, est, abt, cal, bef_aft, 
                bc_ad, os_ns, span, range
            FROM date_per_user 
            WHERE date_per_user_id = 1''')
        user_date_format = cur.fetchall()[0]

        cur.execute('''
            SELECT date_format, est, abt, cal, bef_aft, 
               bc_ad, os_ns, span, range
            FROM date_global 
            WHERE date_global_id = 1''')
        global_date_format = cur.fetchall()[0]

        cur.close()
        conn.close()

        composite_date_prefs = list(global_date_format)

        y = 0
        for b, c in zip(user_date_format, tree_date_format):
            if c is not None:
                composite_date_prefs[y] = c
            elif b is not None:
                composite_date_prefs[y] = b
            y += 1  

        return composite_date_prefs

# DATES CLARIFIER DIALOG

    def validate_iso(self):
        ymd = []

        if len(self.month) == 1:
            self.month = '0{}'.format(self.month)

        if len(self.day) == 1:
            self.day = '0{}'.format(self.day)

        if len(self.year) == 1:
            self.year = '0{}'.format(self.year)

        ymd.append(self.year)
        ymd.append(self.month)
        ymd.append(self.day)
        for num in ymd:
            if num not in self.valids:
                for child in self.clarifier.winfo_children():
                    if (child.winfo_class() == 'Frame' and 
                            child.winfo_subclass() == 'Entry'):
                        child.delete(0, 'end')
                self.valid = False
                break

        return self.valid

    def format_for_tester(self):
        ''' Can this be deleted? '''

        print('format_for_tester executed')

    def close_iso(self, evt=None):
        self.clarifier.destroy()
        self.clarifier_is_running = False

    def send_date(self, evt=None):
        self.valid = True

        for tup in self.cols:
            input = tup[1].get().strip()
            if len(input) == 0 or input.isnumeric() is False:
                tup[1].delete(0, 'end')
                tup[1].focus_set()
                return
            if tup[0] == 0:
                self.year = input
            elif tup[0] == 1:
                if 0 < int(input) < 13:
                    self.month = input
                else:
                    for ent in self.ents:
                        ent.delete(0, 'end')
                    tup[1].focus_set()
                    return
            elif tup[0] == 2:
                self.day = input

        self.month = self.validate_month_by_length()
        if self.month:
            self.valid = self.validate_iso()
            if self.valid is True:
                self.iso_date = self.standardize_for_iso()
                if self.input_type in ('single', 'range1', 'span1'):
                    self.output_first_date()
                elif self.input_type in ('range2', 'span2'):
                    self.output_second_date()
                self.close_iso()

    def clear_typed(self, evt):
        ''' Runs on every FocusOut from a clarifier entry. '''

        used = []
        empty_entries = []
        last_unused = ''
        for child in self.frm.mainframe.winfo_children():
            if (child.winfo_class() == 'Frame' and 
                    child.winfo_subclass() == 'Entry'):
                content = child.get()
                if len(content) == 0: 
                    empty_entries.append(child)
                else:
                    used.append(content)
        vestige = list(self.unknowns)
        for content in used:
            if content in vestige:
                vestige.remove(content)

        if len(vestige) == 1:
            last_unused = vestige[0]

        if len(empty_entries) == 1:
            empty_entries[0].insert(0, last_unused) 

            self.ok.focus_set()

    def make_header_row(self, heads):

        n = 0
        for head in heads:
            lab = wdg.LabelColumn(
                self.frm.mainframe, text=heads[n])
            lab.grid(column=n, row=0, sticky='ew', pady=(12,0), padx=12)
            n += 1 

    def make_iso_frame(self):

        heads = ('Year', 'Month', 'Day')

        self.frm = wdg.Table(self.clarifier, heads)
        self.frm.grid(column=0, row=1, columnspan=3)
        self.frm.grid_columnconfigure(0, weight=1)
        self.frm.grid_columnconfigure(1, weight=1)
        self.frm.grid_columnconfigure(2, weight=1)

        instrux = wdg.LabelH3(self.clarifier, text='')
        instrux.grid(column=0, row=0, columnspan=3, pady=(0,12))

        self.valids = list(self.numbers)
        if len(self.valids) == 2 and len(self.month) == 0:
            self.valids.append('00')
        elif len(self.valids) == 2:
            self.valids.append(self.month)

        self.make_header_row(heads)

        knowns = []
        h = 0
        for name in (self.year, self.month, self.day):
            if name is None:
                name = 'nothing'
            elif len(name) == 0:
                name = 'zip'
            if name:
                if name == 'zip':
                    ent = wdg.Entry( 
                       self.frm.mainframe, 
                       # width=5, 
                       # font=formats['input_font']
)
                    ent.grid(column=h, row=2, padx=12, pady=12)
                    self.ents.append(ent)
                    self.cols.append((ent.grid_info()['column'], ent))
                    ent.bind('<FocusOut>', self.clear_typed)
                    ent.config(width=5)
                  
                else:
                    lab = wdg.Label(self.frm.mainframe, text=name)
                    lab.grid(column=h, row=2, padx=(3,0), pady=12, sticky='we')
                    knowns.append(name)
            h += 1

        self.ents[0].focus_set()

        self.unknowns = list(self.valids)
        for num in knowns:
            if num in self.unknowns:
                self.unknowns.remove(num)

        for num in self.unknowns:
            idx = self.unknowns.index(num)
            num = num.lstrip('0')
            self.unknowns[idx] = num

        definables = ', '.join(self.unknowns)
        instrux.config(text='Define {}:'.format(definables))        

    def make_iso(self):
        ''' 
            Open a clarifier dialog so user can input ISO
            format of intended date. Only opens for ambiguous date
            input such as "10 9 1717" which could be Oct 9 or Sept 10.
            Autofills as much as possible so it barely slows the user
            down. But inputting dates like "mar 10" instead of
            "3 10" keeps it from ever opening. And other tricks 
            like putting a comma after the day, like "3 10, 1876". 
            Even "10, 3 1876" needs no clarification. 
        '''

        self.clarifier_is_running = True
        self.clarifier = tk.Toplevel(padx=24, pady=24)
        self.clarifier.grab_set()
        self.clarifier.title('Clarify Date Parts')
        self.clarifier.geometry('+800+300') # center this in screen

        self.make_iso_frame()

        self.ok = wdg.Button(
            self.clarifier, 
            text='OK', 
            width=6, 
            command=self.send_date)
        self.ok.grid(column=0, row=2, sticky='w', padx=12, pady=(12,0), ipadx=3)

        x = wdg.Button(
            self.clarifier, 
            text='CANCEL', 
            command=self.close_iso, 
            width=6)
        x.grid(column=2, row=2, sticky='e', padx=12, pady=(12,0), ipadx=3)
        self.clarifier.bind('<Return>', self.send_date)
        ST.config_generic(self.clarifier)

# DATE PREFERENCES TAB IN PREFERENCES TAB

def revert_to_default(this_tree_or_all):

    conn = sqlite3.connect(current_file)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()

    cur.execute('DELETE FROM date_per_tree')
    conn.commit()

    cur.execute('''
        INSERT INTO date_per_tree 
        VALUES (1, null, null, null, null, null, null, null, null, null)''')
    conn.commit()

    cur.close()
    conn.close()

    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    cur.execute('DELETE FROM date_per_user')
    conn.commit()

    cur.execute('''
        INSERT INTO date_per_user 
        VALUES (1, null, null, null, null, null, null, null, null, null)''')
    conn.commit()

    cur.close()
    conn.close()

    this_tree_or_all.set('local')

    for combo in date_pref_combos.values():
        if len(combo.get()) != 0:
            combo.delete_content()

def get_rad_val(this_tree_or_all):
    val = this_tree_or_all.get()
    return val

def submit_date_prefs(this_tree_or_all):               

    for combo in date_pref_combos.values():
        if len(combo.get()) != 0:
            var_form = combo.get()
            if combo == date_pref_combos['General']:
                date_form = var_form
                for k,v in DATE_FORMAT_LOOKUP.items():
                    if date_form == k:
                        date_form = v
            elif combo == date_pref_combos['Estimated']:
                est_form = var_form
            elif combo == date_pref_combos['Approximate']:
                abt_form = var_form
            elif combo == date_pref_combos['Calculated']:
                cal_form = var_form
            elif combo == date_pref_combos['Before/After']:
                befaft_form = var_form
            elif combo == date_pref_combos['Epoch']:
                epoch_form = var_form
            elif combo == date_pref_combos['Julian/Gregorian']:
                julegreg_form = var_form
            elif combo == date_pref_combos['From...To...']:
                span_form = var_form
                for k,v in SPAN_FORMAT_LOOKUP.items():
                    if span_form == k:
                        span_form = v
            elif combo == date_pref_combos['Between...And...']:
                range_form = var_form
                for k,v in RANGE_FORMAT_LOOKUP.items():
                    if range_form == k:
                        range_form = v

        val = get_rad_val(this_tree_or_all)

        if val == 'local' and len(combo.get()) != 0:

            current_file = files.get_current_file()[0]
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            if combo is date_pref_combos['General']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET date_format = ? 
                    WHERE date_per_tree_id = 1''', 
                    (date_form,))
            elif combo is date_pref_combos['Estimated']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET est = ? 
                    WHERE date_per_tree_id = 1''', 
                    (est_form,))
            elif combo is date_pref_combos['Approximate']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET abt = ? 
                    WHERE date_per_tree_id = 1''', 
                    (abt_form,))
            elif combo is date_pref_combos['Calculated']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET cal = ? 
                    WHERE date_per_tree_id = 1''', 
                    (cal_form,))
            elif combo is date_pref_combos['Before/After']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET bef_aft = ? 
                    WHERE date_per_tree_id = 1''', 
                    (befaft_form,))
            elif combo is date_pref_combos['Epoch']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET bc_ad = ? 
                    WHERE date_per_tree_id = 1''', 
                    (epoch_form,))
            elif combo is date_pref_combos['Julian/Gregorian']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET os_ns = ? 
                    WHERE date_per_tree_id = 1''', 
                    (julegreg_form,))
            elif combo is date_pref_combos['From...To...']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET span = ? 
                    WHERE date_per_tree_id = 1''', 
                    (span_form,))
            elif combo is date_pref_combos['Between...And...']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET range = ? 
                    WHERE date_per_tree_id = 1''', 
                    (range_form,))

            conn.commit()
            cur.close()
            conn.close() 

        elif val == 'global' and len(combo.get()) != 0:
            
            # conn = sqlite3.connect(st.conn_fig)
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()

            if combo is date_pref_combos['General']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET date_format = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (date_form,))
            elif combo is date_pref_combos['Estimated']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET est = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (est_form,))
            elif combo is date_pref_combos['Approximate']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET abt = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (abt_form,))
            elif combo is date_pref_combos['Calculated']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET cal = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (cal_form,))
            elif combo is date_pref_combos['Before/After']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET bef_aft = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (befaft_form,))
            elif combo is date_pref_combos['Epoch']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET bc_ad = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (epoch_form,))
            elif combo is date_pref_combos['Julian/Gregorian']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET os_ns = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (julegreg_form,))
            elif combo is date_pref_combos['From...To...']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET span = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (span_form,))
            elif combo is date_pref_combos['Between...And...']:
                cur.execute(''' 
                    UPDATE date_per_user 
                    SET range = ? 
                    WHERE date_per_user_id = 1 ''', 
                    (range_form,))

            conn.commit()            

            cur.close()
            conn.close()
            # why is connection being closed and reopened here?
            current_file = files.get_current_file()[0]
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            if combo is date_pref_combos['General']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET date_format = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Estimated']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET est = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Approximate']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET abt = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Calculated']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET cal = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Before/After']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET bef_aft = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Epoch']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET bc_ad = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Julian/Gregorian']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET os_ns = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['From...To...']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET span = NULL 
                    WHERE date_per_tree_id = 1''')
            elif combo is date_pref_combos['Between...And...']:
                cur.execute('''
                    UPDATE date_per_tree 
                    SET range = NULL 
                    WHERE date_per_tree_id = 1''')
            conn.commit()
            cur.close()
            conn.close()

        combo.delete_content()

    this_tree_or_all.set('local')

def format_misc_date(iso_date):
    date_show = ValidDate()
    if '-and-' not in iso_date and '-to-' not in iso_date:
        formatted_date = date_show.format_date_for_table(iso_date)

    elif '-and-' in iso_date:
        date_show.and_to = ' and '
    elif '-to-' in iso_date:
        date_show.and_to = ' to '
    if date_show.and_to:
        formatted_date = date_show.select_function(iso_date)
    return formatted_date

formats = st.make_formats_dict()















