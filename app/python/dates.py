# dates

import tkinter as tk
import sqlite3
from files import current_file
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from styles import make_formats_dict
from messages import open_error_message, dates_msg, open_input_message
# from query_strings import (
    
# )

import dev_tools as dt
from dev_tools import looky, seeline




'''
    There are places where this code appears redundant, for example while 
    initially weeding out bad user input, some facts have to be found (e.g. 
    which number represents the year); facts which will 
    be needed later. Instead of passing these findings along, sometimes they're 
    rediscovered later when they're needed, in order to 
    keep the various procedures better separated 
    from each other. If we were dealing with big data here, this would be 
    inefficient, but in this case, where all this code exists for the purpose of
    validating one single string, I think it's better to keep the code easy to 
    read than to try and kill two birds with one stone and end up with complex,
    confusing procedures that are not strictly separated from each other. I'd rather do something easy twice than confuse two processes out of
    sheer neatnickism and end up with tangled procedures.

    However there is not total separation of concerns because for example,
    you gotta know what the year is or what the month is when you gotta know, 
    so finding bad dates relies on finding out some other things too.

    Also I assume that everything this module does could be imported from any
    number of libraries but I enjoyed writing this module three times and I
    like having easy access to the procedures I'm using and knowing that the
    code was custom-written for my needs and doesn't contain a bunch of extra
    stuff that I don't need. "DATES" is a huge topic and no doubt the available
    libraries for dealing with them are way over my head.

    I've tried making this a class, but a big class to validate one string? The
    result is a bunch of instance variables that can be changed all over a big
    class, which can have the same confusing effect as global variables, all to validate one single string. I like
    classes but in this case, working the code out procedurally seemed like a
    better approach, after trying it both ways.

    Treebard GPS has to remain accessible to neophyte coders such as genealogists
    who want to customize their own applications.
'''

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

DAYS_30 = ('ap', 'jun', 's', 'no')

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

# ABB_PAIRS: [['bef/aft', 'bef./aft.', 'prior to/later than', 'before/after'], ['BCE/CE', 'BC/AD', 'B.C.E./C.E.', 'B.C./A.D.'], ['OS/NS', 'O.S./N.S.', 'old style/new style', 'Old Style/New Style']]

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

root = None

def validate_date(
    parent,
    inwidg,
    initial,
    final,
    finding):

    global root

    print("line", looky(seeline()).lineno, "inwidg, initial, final, finding:", inwidg, initial, final, finding)

    root = parent

    final = find_bad_dates(final)
    print("line", looky(seeline()).lineno, "final:", final)
    if final is None: return

    final, order = make_date_dict(list(final))
    print("line", looky(seeline()).lineno, "final:", final)
    if final is None: return

    final = order_compound_dates(final, order)
    print("line", looky(seeline()).lineno, "final:", final)
    if final is None: return

    print("line", looky(seeline()).lineno, "final:", final)    
    return final

def find_bad_dates(final):

    for sep in SEPTORS:
        final = final.replace(sep, " ")
    terms = final.split()

    for term in terms:
        term = term.strip()

    compounds = find_word_errors(terms)
    if not compounds:
        return
    
    final = find_number_errors(compounds)

    return final

def find_word_errors(terms):

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
    compound_date_link = None
    for term in terms:
        if term.lower() in ("and", "to"):
            if compound_date_link is not None:
                print("repeated word 'and' or 'to' error")
                return               
            compound_date_link = term
        elif compound_date_link is None:
            comp1.append(term)
        elif compound_date_link is not None:
            comp2.append(term)
        else:
            print("line", looky(seeline()).lineno, "case not handled:")

    if len(month_words) > 1 and compound_date_link is None:
        print("two dates no connector error")
        return

    return comp1, comp2, compound_date_link

def find_number_errors(compounds):

    def standardize_month(term):
        if term.startswith(OK_MONTHS):
            for mo in OK_MONTHS:
                if term.startswith(mo):
                    term = mo
                    break
        return term

    for lst in (compounds[0:2]):
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
            j = 0
            for term in lst:
                if term.lower() in ALL_MONTHS:
                    if abc > 1:
                        print("too many months input error")
                        return
                    else:
                        lst[j] = standardize_month(term)                        
                    abc += 1
                j += 1                    
            if abc == 0:
                print("no month error")
                return
    return compounds

def clarify_year(numbers, lst):
    copy = lst
    numbers, year = open_input_message(root, "Type the year as a four-digit "
        "number. For example, the year 33 should be typed as 0033.", 
        "Clarify Year", "OK", "CANCEL", numbers)
    a = 0
    for num in numbers:
        if int(num) == int(year):
            if a == 1:
                day = numbers[0]
            elif a == 0:
                day = numbers[1]
            x = 0
            for item in copy:
                if item.isalpha() is False and item != day:
                    lst[x] = year
                x += 1
            break
        a += 1
    
    return year, day, lst   

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
        
        under_two = 0
        nums = []
        for item in lst:
            if item.isdigit():
                nums.append(item)
                if len(item) < 3:
                    if under_two > 0:
                        year, day, lst = clarify_year(nums, lst)
                        date_dict[b]["year"] = year
                    else:
                        under_two += 1
                elif len(item) > 2:                       
                    date_dict[b]["year"] = item
                    break                
        return lst

    def find_day(lst, b):
        i = 0
        for item in lst:
            if item.isdigit():
                if len(item) > 2:
                    i += 1
                    continue
                elif len(item) <= 2:
                    date_dict[b]["day"] = item
                    break
            i += 1

        return lst

    date_dict = [{}, {}]
    if len(final) == 1: # REMEMBER TO FIX THIS, UNTIL IT'S FIXED I HAVE TO INPUT COMPOUND DATES ONLY
        pass
    elif len(final) > 1:
        comps = [final[0], final[1]]
        b = 0
        for lst in comps:
            lst = find_month(lst, b)
            lst = find_year(lst, b)
            lst = find_day(lst, b)
            comps[b] = lst
            b += 1

        # date_dict.insert(1, final[1])
    # print("line", looky(seeline()).lineno, "date_dict:", date_dict)
    # print("line", looky(seeline()).lineno, "final:", final)

    check_days_in_months(date_dict)

    order = ["ad", "ad"]        
    e = 0
    for lst in final[0:2]:
        for item in lst:
            if item.upper() in BC:
                order[e] = "bc"
            elif item.upper() in AD:
                order[e] = "ad"
        e += 1  

    f = 0
    for lst in final[0:2]:
        for item in lst:
            if not item.isdigit() and not item.lower().startswith(OK_MONTHS):
                term = assign_prefixes_suffixes(date_dict, lst, item)
                print("line", looky(seeline()).lineno, "term:", term)
        f += 1

    return date_dict, order

# line 173 final: (['10', 'June', '1884', 'bc', 'est'], ['1', 'oc', 'abt', 'ad', '18'], 'to')
# line 177 final: [{'month': 'jun', 'year': '1884', 'day': '10'}, {'month': 'oc', 'year': '0018', 'day': '1'}]

def assign_prefixes_suffixes(date_dict, lst, item):
    print("line", looky(seeline()).lineno, "date_dict, lst, item:", date_dict, lst, item)
# line 431 date_dict, lst, item: [{'month': 'jun', 'year': '1884', 'day': '10'}, {'month': 'ap', 'year': '1492', 'day': '1'}] ['10', 'June', '1884', 'est', 'bc'] June
    term = item # delete this
    return term

def check_days_in_months(date_dict):
    for dkt in date_dict:
        if len(dkt) != 0:
            leap_year = False
            maxdays = 31
            if dkt["month"] == "f":
                maxdays = 28
                if int(dkt["year"]) % 4 == 0:
                    maxdays = 29
            elif dkt["month"] in DAYS_30:
                maxdays = 30
            if int(dkt["day"]) > maxdays:
                print("too many days for that month error")
                return

def order_compound_dates(final, order):
    if len(final) < 2:
        return final
    sort1 = []
    sort2 = [[], []]    
    u = 0
    for dkt in final:
        sort1.append(int(dkt["year"]))
        w = 1
        for mo in OK_MONTHS:
            if dkt["month"] == mo:
                sort2[u].append(w)
                continue
            w += 1
        sort2[u].append(int(dkt["day"]))
        dkt["sort1"] = sort1[u]
        dkt["sort2"] = sort2[u]
        u += 1
   
    if order == ["ad", "ad"]:
        fwd = sorted(final, key=lambda i: i["sort1"])
        sort_again = fwd
        if sort1[0] == sort1[1]:
            sort_again = sorted(fwd, key=lambda i: i["sort2"])
        return sort_again
    elif order == ["bc", "bc"]:
        rev = sorted(final, key=lambda i: i["sort1"], reverse=True) 
        sort_again = rev
        if sort1[0] == sort1[1]:
            sort_again = sorted(rev, key=lambda i: i["sort2"])
        return sort_again
    elif order == ["ad", "bc"]:
        right = [final[1], final[0]]
        return right
    elif order == ["bc", "ad"]:
        return final

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
# add link, prefixes & suffixes to date_dict
# fix `if len(final) == 1:` line 391
# update db
# get formatting & display right 1) when editing in table & 2) on load