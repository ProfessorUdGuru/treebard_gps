# dates

import tkinter as tk
import sqlite3
from files import current_file
# from widgets import (
# )
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from styles import make_formats_dict
from messages import open_error_message, dates_msg
# from query_strings import (
    
# )

import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

# "." can't be used as a separator or it would prevent the user
#   from using a dot to denote an abbreviation e.g. "A.D."
SEPTORS = (" ", "/", "-", "*", "_")

OK_MONTHS = (
    'ja', 'f', 'mar', 'ap', 'may', 'jun', 
    'jul', 'au', 's', 'oc', 'no', 'd')

MONTH_ABBS = (
    'ja.', 'jan.', 'f.', 'fe.', 'feb.', 'mar.', 'ap.', 'apr.', 
    'jun.', 'jul.', 'au.', 'aug.', 's.', 'se.', 'sep.', 'sept.', 
    'oc.', 'oct.', 'no.', 'nov.', 'd.', 'de.', 'dec.',
    'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'sept', 
    'oct', 'nov', 'dec', 'fe', 'se', 'de')

FULL_MONTHS = (
    "january", "february", "march", "april", "may", "june", 
    "july", "august", "september", "october", "november", "december")

ALL_MONTHS = [i for i in OK_MONTHS] + [i for i in MONTH_ABBS] + [i for i in FULL_MONTHS]
# print("line", looky(seeline()).lineno, "ALL_MONTHS:", ALL_MONTHS)

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
print("line", looky(seeline()).lineno, "ABB_PAIRS:", ABB_PAIRS)
# line 85 ABB_PAIRS: [['bef/aft', 'bef./aft.', 'prior to/later than', 'before/after'], ['BCE/CE', 'BC/AD', 'B.C.E./C.E.', 'B.C./A.D.'], ['OS/NS', 'O.S./N.S.', 'old style/new style', 'Old Style/New Style']]

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

def validate_date(
    inwidg,
    initial,
    final,
    finding):

    print("line", looky(seeline()).lineno, "inwidg, initial, final, finding:", inwidg, initial, final, finding)

    final = find_bad_dates(final)
    if not final: return

    final = make_date_dict(list(final))
    if not final: return

    final = order_compound_dates(final)
    if not final: return


    



    print("line", looky(seeline()).lineno, "final:", final)    
    return final

def find_bad_dates(final):

    for sep in SEPTORS:
        final = final.replace(sep, " ")
    terms = final.split()

    for term in terms:
        term = term.strip()

    words = []
    month_words = []
    for term in terms:
        if term.lower() in ALL_MONTHS:
            month_words.append(term)
        elif term.lower() in ("to", "and"):
            pass
        elif term.isalpha() is True:
            words.append(term)
        else:
            "case not handled"

    if len(month_words) > 2:
        print("too many months error")

    for word in words:
        if word in ("and", "to") and words.count(word) > 1:
            print("repeated word error")
            return

    comp1 = []
    comp2 = []
    compsep = None
    for term in terms:
        print("line", looky(seeline()).lineno, "term:", term)
        if term in ("and", "to"):
            if compsep is not None:
                print("repeated word 'and' or 'to' error")
                return               
            compsep = term
        elif compsep is None:
            comp1.append(term)
        elif compsep is not None:
            comp2.append(term)
        else:
            print("line", looky(seeline()).lineno, "case not handled:")

    if len(month_words) > 1 and compsep is None:
        print("two dates no connector error")
        return

    for lst in (comp1, comp2):
        print("line", looky(seeline()).lineno, "lst:", lst)
        nums = 0
        over_two_digits = 0
        lenlist = len(lst)
        for item in lst:
            if item.isdigit() is True:
                if len(item) > 2: 
                    if over_two_digits > 0:
                        print("too many years input error")
                        return
                    else:
                        over_two_digits += 1
                nums += 1

        if nums >= 3:
            print("too many numerical terms error")
            return
        elif lenlist > 5:
            print("too many terms error")
            return

        prefixes = 0
        suffixes = 0
        for elem in lst:
            if elem.lower() in OK_PREFIXES:
                prefixes += 1
            elif elem.upper() in OK_SUFFIXES:
                suffixes += 1
        if prefixes > 1 or suffixes > 1:
            print("too many prefixes or suffixes error")
            return

        if lenlist == 1 and lst[0].isalpha() is True:
            print("lack of numerical items")
            return
        elif lenlist > 1:
            numbers = []
            for elem in lst:
                if elem.isdigit() is True:
                    numbers.append(int(elem))
            lennums = len(numbers)
            if lenlist == lennums:
                print("no month error")
                return
            abc = 0
            for i in lst:
                if i.lower() in ALL_MONTHS:
                    abc += 1
            if abc == 0:
                print("no month error")
                return
            if lennums == 2:
                over_31 = 0
                for number in numbers:
                    if number > 31:
                        if over_31 > 0:
                            print("too many years error")
                            return
                        over_31 += 1



    return (comp1, compsep, comp2)

def make_date_dict(final):

    def find_month(lst, b):
        g = 0
        for item in lst:
            if item.isalpha():
                if item.lower().startswith(OK_MONTHS):
                    for mo in OK_MONTHS:
                        if item.lower().startswith(mo):
                            month_key = mo
                            break
                    date_dict[b]["month"] = month_key
                    break
            g += 1
        return lst

    def find_year(lst, b):
        h = 0
        under_two = 0
        for item in lst:
            if item.isdigit():
                if len(item) < 3:
                    if under_two > 0:
                        lst = clarify_year(lst)
                    else:
                        under_two += 1
                elif len(item) > 2:                       
                    date_dict[b]["year"] = item
                    break
            h += 1    
        return lst

    def find_day(lst, b):
        i = 0
        for item in lst:
            if type(item) is not dict:
                if item.isdigit():  
                    date_dict[b]["day"] = item
                    break
            i += 1

        return lst

    def clarify_year(lst):
        print("line", looky(seeline()).lineno, "lst:", lst)
        return lst

    date_dict = [{}, {}]
                    
    if len(final) == 1:
        pass
    elif len(final) > 1:
        comps = [final[0], final[2]]
        b = 0
        for lst in comps:
            lst = find_month(lst, b)
            lst = find_year(lst, b)
            lst = find_day(lst, b)
            comps[b] = lst
            b += 1
        date_dict.insert(1, final[1])
    print("line", looky(seeline()).lineno, "date_dict:", date_dict)
    print("line", looky(seeline()).lineno, "final:", final)

                        




def order_compound_dates(final):
    print("line", looky(seeline()).lineno, "final:", final)
# line 259 final: (['10', 'June', '1884'], 'to', ['14', 'f', '1888'])


    order = ["ad", "ad"]        
    e = 0
    for lst in (final[0], final[2]):
        for item in lst:
            if item.upper() in BC:
                order[e] = "bc"
                continue
            elif item.upper() in AD:
                order[e] = "ad"
                continue
        e += 1
    print("line", looky(seeline()).lineno, "order:", order)
    if order == ("ad", "ad"):
        pass
    elif order == ("bc", "bc"):
        pass
    elif order == ("ad", "bc"):
        pass
    elif order == ("bc", "ad"):
        pass





if __name__ == "__main__":

    from autofill import EntryAuto
    from widgets import Entry

    root = tk.Tk()

    inwidg = EntryAuto(root)
    inwidg.grid()
    inwidg.focus_set()

    traverse = Entry(root)
    traverse.grid()


    root.mainloop()
    
# DO LIST
# clarify_year() eg 12 10 feb
# match allowable num of days in mo to month see over_31
# add prefixes & suffixes to date_dict