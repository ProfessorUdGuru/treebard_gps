# dates

import tkinter as tk
import sqlite3
from files import get_current_file
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from styles import make_formats_dict
from messages import open_error_message, dates_msg, open_input_message
# from query_strings import select_date_format, select_default_date_format
from query_strings import select_date_format
import dev_tools as dt
from dev_tools import looky, seeline






'''
    Treebard's policy is to let the user input dates with extreme freedom while
    displaying dates without regard for how the date was input, but rather
    in reference to stored user preferences. So this module is kinda complex
    but since it's written strictly in accordance with the needs of Treebard,
    there's nothing here that doesn't need to be here.

    Another policy is to have no pop-up calendars and the like when the user
    tries to input a date. These encumbrances only slow down input which is more easily typed, and while coders might like them because they're cute or 
    convenient, users find them annoying if trying to do any significant amount 
    of data input. In Treebard, a date is input as a typed string, with several
    choices of delimiter between date elements, and with the elements typed in 
    almost any order. 

    The policy of not allowing numerical month input makes it easy for Treebard
    to tell which number is the year and which number is the day, except for years
    less than 100. In this case a simple dialog coaches the user to input short
    years with leading zeroes. So the only time a user has to worry about inputting
    date elements in a fixed order is when typing "and" or "to" between two
    compound dates. For example, the user can type "1852 ja 3 est and bc 14 f 1901 
    abt" and Treebard will know that this means "between about 14 Feb 1901 BC 
    and estimated 3 Jan 1852 AD". This allows the user to just start typing, 
    and as long as the "and" or "to" is in the right place, the input will be 
    correctly interpreted.

    Another policy is to allow no bad date input and no ambiguous date input. 
    Treebard is meant to be easily sharable. Allowing numerical month input 
    would be good for some parts of our program by increasing flexibility of input
    to infinity and beyond, but would bloat the code and open up the possibility 
    of easily misinterpreted dates when trees are shared from one country to 
    another.

    Another policy is to ignore that period of time when the Gregorian Calendar was 
    being adopted in lieu of the ancient Julian Calendar. Some genieware uglifies 
    these dates according to when western cultures were supposedly making this 
    transition. Treebard uglifies no date. The transition took place at different 
    times in different countries, in fact it has only recently taken place in some 
    countries. The user can mark his dates "old style" or "new style" in whatever 
    formatting he prefers, but dates like "14 Oct 1752/1753" cannot exist in 
    Treebard.

    Globals are used for `root` and `widg` because we are validating a single
    string found in a single Entry in a single app and none of that will ever
    change. These values are set once per use and don't change during the 
    procedure.

    There are places where this code appears redundant, for example while 
    initially weeding out bad user input, some facts have to be found (e.g. 
    which number represents the year); facts which will 
    be needed later. Instead of passing these findings along, sometimes they're 
    rediscovered later when they're needed, in order to 
    keep the various procedures better separated 
    from each other. If we were dealing with big data here, this might be 
    inexcusable, but in this case, where all this code exists for the purpose of
    validating one single string, I think it's better to keep the code easy to 
    read than to try and kill two birds with one stone and end up with complex,
    confusing procedures that are not strictly separated from each other. I'd rather do something easy twice than confuse two processes out of
    sheer neatnickism and end up with tangled procedures.

    But there can't be total separation of concerns because for example,
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

    As for the history of this module's development, big trouble was had at first
    due to trying to have the code care whether the date input was supposed to 
    be a compound date or not (like "from 1845 to 1872"). Finally it was revealed
    to me that all date inputs should be treated as compound, and if the second
    term in the list was empty, then it could just be ignored. Another early 
    problem was caused by letting the user input months as numbers. Disallowing
    this simplified the programmer's task big-time. Treebard policy is to
    disallow numerical month DISPLAY because of cultural differences in the 
    ordering of numerical date values which would make for ambiguity from one 
    country to another. This would make sharing trees a big hassle in some cases.
    Extending this policy to date INPUT seemed only logical when considering how 
    much less code bloat would exist if it were done.

    Treebard GPS has to remain accessible to neophyte coders such as genealogists
    who want to customize their own applications.
'''

formats = make_formats_dict()
current_file = get_current_file()[0]


# def get_default_date_formats():
    # conn = sqlite3.connect(global_db_path)
    # cur = conn.cursor()
    # cur.execute(select_default_date_format)
    # default_date_prefs = cur.fetchone()
    # cur.close()
    # conn.close()
    # return default_date_prefs

def get_date_formats():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_date_format)
    date_prefs = cur.fetchone()
    cur.close()
    conn.close()
    return date_prefs

# date_prefs = get_default_date_formats()
date_prefs = get_date_formats()

# "." can't be used as a separator as it would prevent the user
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

STORE_PFX = ['est', 'cal', 'abt', 'bef', 'aft']

STORE_SFX = ['ad', 'bc', 'os', 'ns', 'ce', 'bce']

OK_ABBS = STORE_PFX + STORE_SFX

MONTH_CONVERSIONS = {
    'ja': ['January', 'Jan', 'Jan.'],
    'f': ['February', 'Feb', 'Feb.'],
    'mar': ['March', 'Mar', 'Mar.'],
    'ap': ['April', 'Apr', 'Apr.'],
    'may': ['May',  'May', 'May'],
    'jun': ['June', 'June', 'June'],
    'jul': ['July', 'July', 'July'],
    'au': ['August', 'Aug', 'Aug.'],
    's': ['September', 'Sep', 'Sep.'],
    'oc': ['October', 'Oct', 'Oct.'],
    'no': ['November', 'Nov', 'Nov.'],
    'd': ['December', 'Dec', 'Dec.']}

EST = ["est", "est.", "est'd"]
ABT = ["abt", "about", "circa", "ca", "ca.", "approx."]
CAL = ["cal", "calc", "calc.", "cal.", "calc'd"]
BEF = ["bef", "bef.", "before"]
AFT = ["aft", "aft.", "after"]
BC = ["BCE", "BC", "B.C.E.", "B.C."]
AD = ["CE", "AD", "C.E.", "A.D."]
JULIAN = ["OS", "O.S.", "old style", "Old Style"]
GREGORIAN = ["NS", "N.S.", "new style", "New Style"]

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
        "bet. [date 1] & [date 2]" , "bet. [date 1] and [date 2]"))

DATE_FORMATS = (
    'dmy', 'dmy_abb', 'dmy_dot', 'mdy', 'mdy_abb', 'mdy_dot')

SPAN_FORMATS = ("from_to", "fr._to", "frm_to", "fr_to")

RANGE_FORMATS = (
    "btwn_&", "btwn_and", "bet_&", "bet_and", "bet._&", "bet._and")

FORMAT_TO_STRIP = ("from", "fr.", "frm", "fr", "btwn", "bet", "bet.", ",", "between")

DATE_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[0], DATE_FORMATS))
# print("line", looky(seeline()).lineno, "DATE_FORMAT_LOOKUP:", DATE_FORMAT_LOOKUP)
# line 215 DATE_FORMAT_LOOKUP: {'18 April 1906': 'dmy', '18 Apr 1906': 'dmy_abb', '18 Apr. 1906': 'dmy_dot', 'April 18, 1906': 'mdy', 'Apr 18, 1906': 'mdy_abb', 'Apr. 18, 1906': 'mdy_dot'}

SPAN_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[7], SPAN_FORMATS))
# print("line", looky(seeline()).lineno, "SPAN_FORMAT_LOOKUP:", SPAN_FORMAT_LOOKUP)
# line 212 SPAN_FORMAT_LOOKUP: {'from [date 1] to [date 2]': 'from_to', 'fr. [date 1] to [date 2]': 'fr._to', 'frm [date 1] to [date 2]': 'frm_to', 'fr [date 1] to [date 2]': 'fr_to'}

RANGE_FORMAT_LOOKUP = dict(zip(DATE_PREF_COMBOS[8], RANGE_FORMATS))
# print("line", looky(seeline()).lineno, "RANGE_FORMAT_LOOKUP:", RANGE_FORMAT_LOOKUP)
# line 221 RANGE_FORMAT_LOOKUP: {'btwn [date 1] & [date 2]': 'btwn_&', 'btwn [date 1] and [date 2]': 'btwn_and', 'bet [date 1] & [date 2]': 'bet_&', 'bet [date 1] and [date 2]': 'bet_and', 'bet. [date 1] & [date 2]': 'bet._&', 'bet. [date 1] and [date 2]': 'bet._and'}

OK_PREFIXES = ABT+EST+CAL+BEF+AFT
OK_SUFFIXES = BC+AD+JULIAN+GREGORIAN

root = None
widg = None

def validate_date(
    parent,
    inwidg,
    # initial,
    final,
    # finding
):

    global root, widg

    root = parent
    widg = inwidg

    final = find_bad_dates(final)
    if final is None: return

    results = make_date_dict(list(final))
    if results:        
        final, order, compound_date_link = results
    else:
        return
    if final is None: return

    final = order_compound_dates(final, order, compound_date_link)
    if final is None: return

    final = make_date_string(final)

    return final

def find_bad_dates(final):

    final = final.replace("&", "and")
    for mark in FORMAT_TO_STRIP:
        final = final.replace(mark, "")

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

def count_month_words(info):
    compound = False
    month_words = []
    for term in info:
        if term.lower() in ALL_MONTHS:
            month_words.append(term)
        elif term.lower() in ("to", "and"):
            compound = True
        else:
            "case not handled"
    return month_words, compound

def err_done0(widg, dlg):
    widg.delete(0, 'end')
    dlg.destroy()
    widg.focus_set()

def find_word_errors(terms):

    month_words, compound = count_month_words(terms)
    compound_date_link = None
    comp1 = []
    comp2 = []
    for term in terms:
        if term.lower() in ("and", "to"):
            if compound_date_link is not None:
                msg = open_error_message(
                    root, 
                    dates_msg[0], 
                    "Repeated Compound Date Link", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(
                    command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
                return               
            compound_date_link = term
        elif compound_date_link is None:
            comp1.append(term)
        elif compound_date_link is not None:
            comp2.append(term)
        else:
            print("line", looky(seeline()).lineno, "case not handled:")

    months = len(month_words)

    if months > 1 and compound_date_link is None:
        msg = open_error_message(
            root, 
            dates_msg[1], 
            "Too Many Months Input", 
            "OK")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(
            command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
        return
    if months > 2:
        msg = open_error_message(
            root, 
            dates_msg[2], 
            "Too Many Months Input", 
            "OK")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(
            command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
        return
    elif months == 2:
        pass
    elif months <= 1:
        for lst in (comp1, comp2):
            n = 0
            for item in lst:
                if item.isdigit():
                    n += 1
            if months == 1 and n > 1:
                month_words2 = count_month_words(lst)[0]
                if len(month_words2) == months:
                    pass
                else: 
                    msg = open_error_message(
                        root, 
                        dates_msg[3], 
                        "Day Input Without Month", 
                        "OK")
                    msg[0].grab_set()
                    msg[1].config(aspect=400)
                    msg[2].config(
                        command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
                    return
            elif months == 0 and n == 1:
                pass
            elif months == 0 and n > 1:
                msg = open_error_message(
                    root, 
                    dates_msg[3], 
                    "Day Input Without Month", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(
                    command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
                return

    for lst in (comp1, comp2):
        prefixes = 0
        suffixes = 0
        for elem in lst:
            if elem.lower() in OK_PREFIXES:
                prefixes += 1
            elif elem.upper() in OK_SUFFIXES:
                suffixes += 1
        if prefixes > 1 or suffixes > 1:
            msg = open_error_message(
                root, 
                dates_msg[4], 
                "Too Many Prefixes or Suffixes", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(
                command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
            return

    return comp1, comp2, compound_date_link, compound

def standardize_month(term):
    if term.startswith(OK_MONTHS):
        for mo in OK_MONTHS:
            if term.startswith(mo):
                term = mo
                break
    return term

def find_number_errors(compounds):

    for lst in compounds[0:2]:
        nums = 0
        over_two_digits = 0
        lenlist = len(lst)
        for item in lst:
            if item.isdigit() is True:
                if len(item) > 2: 
                    if over_two_digits > 0:
                        msg = open_error_message(
                            root, 
                            dates_msg[5], 
                            "Too Many Years Input", 
                            "OK")
                        msg[0].grab_set()
                        msg[1].config(aspect=400)
                        msg[2].config(
                            command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
                        return
                    else:
                        over_two_digits += 1
                nums += 1

        if nums >= 3:
            msg = open_error_message(
                root, 
                dates_msg[6], 
                "Too Many Numerical Terms Input", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(
                command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
            return
        elif lenlist > 5:
            msg = open_error_message(
                root, 
                dates_msg[7], 
                "Too Many Terms Input", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(
                command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
            return

        if lenlist == 1 and lst[0].isalpha() is True:
            msg = open_error_message(
                root, 
                dates_msg[8], 
                "Numerical Terms Input Lacking", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(
                command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
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

        def add_zeros(lst, the_one):
            fixed = the_one[0]
            length = len(the_one[0])
            idx = the_one[1]
            if length == 2:
                fixed = "00" + the_one[0]
            elif length == 3:
                fixed = "0" + the_one[0]
            lst[idx] = fixed
            return lst 
        
        num_count = []
        u = 0
        for item in lst:
            if item.isdigit():
                num_count.append((item, u))
            u += 1
        if len(num_count) == 1:
            the_one = num_count[0]
            lst = add_zeros(lst, the_one)
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

    compound_date_link, compound = final[2:]
    date_dict = [{}, {}]
    if len(final) == 1:
        comps = [final[0]]
    elif len(final) > 1:
        comps = [final[0], final[1]]
        b = 0
    for lst in comps:
        lst = find_month(lst, b)
        lst = find_year(lst, b)
        lst = find_day(lst, b)
        comps[b] = lst
        b += 1
    check_days_in_months(date_dict)
    order = ["ad", "ad"]        
    e = 0
    for lst in comps:
        for item in lst:
            if item.upper() in BC:
                order[e] = "bc"
            elif item.upper() in AD:
                order[e] = "ad"
        e += 1 
    f = 0
    for lst in comps:
        for item in lst:
            if not item.isdigit() and not item.lower().startswith(OK_MONTHS):
                if item.lower() in OK_PREFIXES:
                    date_dict = assign_prefixes(date_dict, item, f)
                elif (item in OK_SUFFIXES or 
                        item.upper() in OK_SUFFIXES or item.title() in OK_SUFFIXES):
                    date_dict = assign_suffixes(date_dict, item, f)
        f += 1
    if compound is True:
        if date_dict[0] == date_dict[1]:
            msg = open_error_message(
                root, 
                dates_msg[9], 
                "Indistinct Compound Date", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(
                command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
            return

    return date_dict, order, compound_date_link

def assign_prefixes(date_dict, item, f):
    item = item.lower()
    if item in ABT:
        term = "abt"
    elif item in EST:
        term = "est"
    elif item in CAL:
        term = "cal"
    elif item in BEF:
        term = "bef"
    elif item in AFT:
        term = "aft"
    date_dict[f]["prefix"] = term

    return date_dict

def assign_suffixes(date_dict, item, f):
    for i in (item, item.upper(), item.title()):
        if i in BC:
            term = "bc"
            break
        elif i in AD:
            term = "ad"
            break
        elif i in JULIAN:
            term = "os"
            break
        elif i in GREGORIAN:
            term = "ns"
            break
    date_dict[f]["suffix"] = term

    return date_dict

def check_days_in_months(date_dict):
    for dkt in date_dict:
        if dkt.get("month") is None:
            continue
        if len(dkt) != 0:
            leap_year = False
            maxdays = 31
            if dkt["month"] == "f":
                maxdays = 28
                if int(dkt["year"]) % 4 == 0:
                    maxdays = 29
            elif dkt["month"] in DAYS_30:
                maxdays = 30 
            if dkt.get("day") and int(dkt["day"]) > maxdays:
                msg = open_error_message(
                    root, 
                    dates_msg[10], 
                    "Too Many Days for the Month", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(
                    command=lambda widg=widg, dlg=msg[0]: err_done0(widg, dlg))
                return

def order_compound_dates(final, order, compound_date_link):
    if len(final[1]) == 0:
        final.insert(1, "")
        return final
    sort1 = []
    sort2 = [[], []]    
    u = 0
    for dkt in final:
        sort1.append(int(dkt["year"]))
        w = 1
        for mo in OK_MONTHS:
            if dkt.get("month") and dkt["month"] == mo:
                sort2[u].append(w)
                continue
            w += 1
        if dkt.get("day"):
            sort2[u].append(int(dkt["day"]))
        dkt["sort1"] = sort1[u]
        dkt["sort2"] = sort2[u]
        u += 1
    if order == ["ad", "ad"]:
        fwd = sorted(final, key=lambda i: i["sort1"])
        sort_again = fwd
        if sort1[0] == sort1[1]:
            sort_again = sorted(fwd, key=lambda i: i["sort2"])
        sort_again.insert(1, compound_date_link)
        return sort_again
    elif order == ["bc", "bc"]:
        rev = sorted(final, key=lambda i: i["sort1"], reverse=True) 
        sort_again = rev
        if sort1[0] == sort1[1]:
            sort_again = sorted(rev, key=lambda i: i["sort2"])
        sort_again.insert(1, compound_date_link)
        return sort_again
    elif order == ["ad", "bc"]:
        right = [final[1], final[0]]
        right.insert(1, compound_date_link)
        return right
    elif order == ["bc", "ad"]:
        final.insert(1, compound_date_link)
        return final

def make_date_string(final):

    def concat_parts(
            prefix1="", year1="0000", month1="00", day1="00", suffix1="",
            link="", prefix2="", year2="", month2="", day2="", suffix2=""):
        date_string = "{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}".format(
            prefix1, year1, month1, day1, suffix1, 
            link, prefix2, year2, month2, day2, suffix2)
        return date_string

    comp1 = final[0]
    link = final[1]
    comp2 = final[2]

    prefix1 = comp1.get("prefix", "")
    year1 = comp1.get("year", "")
    month1 = comp1.get("month", "")
    day1 = comp1.get("day", "")
    suffix1 = comp1.get("suffix", "")
    if len(link) == 0:
        return concat_parts(prefix1, year1, month1, day1, suffix1)
    link = link
    prefix2 = comp2.get("prefix", "")
    year2 = comp2.get("year", "")
    month2 = comp2.get("month", "")
    day2 = comp2.get("day", "")
    suffix2 = comp2.get("suffix", "")
    return concat_parts(
        prefix1, year1, month1, day1, suffix1,
        link, prefix2, year2, month2, day2, suffix2)

def format_stored_date(stored_date):
    if stored_date == "-0000-00-00----0000-00-00-":
        return ""
    dateform = date_prefs[0]
    formatted_date = ""
    preprefix = ""
    prefix1 = ""
    year1 = ""
    month1 = ""
    day1 = ""
    suffix1 = ""
    link = ""
    prefix2 = ""
    year2 = ""
    month2 = ""
    day2 = ""
    suffix2 = ""
    span = False
    ranje = False
    compound = False
    parts = stored_date.split("-")

    if 'to' in parts:
        span = True
        compound = True
    elif 'and' in parts:
        ranje = True
        compound = True

    y = 0
    for part in parts:
        if len(part) == 0:
            pass
        elif y in (0, 6):
            part = find_prefix(part)
            if y == 0:
                prefix1 = part                
            elif y == 6:
                prefix2 = part
        elif y in (1, 7):
            part = part.lstrip("0")
            if y == 1:
                year1 = part
            elif y == 7:
                year2 = part
        elif y in (2, 8):
            part = convert_month(part, dateform)
            if y == 2:
                month1 = part
            elif y == 8:
                month2 = part
        elif y in (3, 9):
            part = part.lstrip("0")
            if y == 3:
                day1 = part
            elif y == 9:
                day2 = part
        elif y in (4, 10):
            part = find_suffix(part)
            if y == 4:
                suffix1 = part
            elif y == 10:
                suffix2 = part
        elif y == 5:
            if compound is False:
                break
            if span is True:
                part = date_prefs[7].split("_")
                preprefix = part[0]
                link = part[1]
            elif ranje is True:
                part = date_prefs[8].split("_")
                preprefix = part[0]
                link = part[1]
        y += 1

    t = 0
    for tup in ((suffix1, year1), (suffix2, year2)):        
        suffix = tup[0]
        year = tup[1]
        if suffix in AD:
            if int(year) > 99:
                suffix = ""
        if t == 0:
            suffix1 = suffix
        elif t == 1:
            suffix2 = suffix
        t += 1

    month_first_commas2 = (
        preprefix, prefix1, month1, day1 + ",", year1, suffix1, 
        link, prefix2, month2, day2 + ",", year2, suffix2)

    month_first_comma_a = (
        preprefix, prefix1, month1, day1 + ",", year1, suffix1, 
        link, prefix2, month2, day2, year2, suffix2)

    month_first_comma_b = (
        preprefix, prefix1, month1, day1, year1, suffix1, 
        link, prefix2, month2, day2 + ",", year2, suffix2)

    month_first_no_comma = (
        preprefix, prefix1, month1, day1, year1, suffix1, 
        link, prefix2, month2, day2, year2, suffix2)

    day_first = (
        preprefix, prefix1, day1, month1, year1, suffix1, 
        link, prefix2, day2, month2, year2, suffix2)

    len1 = len(day1)
    len2 = len(day2)

    if "dm" in dateform:
        order = day_first
    elif "md" in dateform:
        if compound is True:
            if len1 > 0 and len2 > 0:
                order = month_first_commas2
            elif len1 > 0 and len2 == 0:
                order = month_first_comma_a
            elif len1 == 0 and len2 > 0:
                order = month_first_comma_b
            else:
                order = month_first_no_comma
        else:
            if len1 > 0:
                order = month_first_comma_a
            else:
                order = month_first_no_comma

    formatted_date = "{} {} {} {} {} {} {} {} {} {} {} {}".format(*order)

    formatted_date = " ".join(formatted_date.split())

    return formatted_date

def find_prefix(part):
    if part == 'abt':
        prefix = date_prefs[1]
    elif part == 'est':
        prefix = date_prefs[2]
    elif part == 'cal':
        prefix = date_prefs[3]
    elif part in ('bef', 'aft'):
        bef_aft = date_prefs[4].split("/")
        if part == 'bef':
            prefix = bef_aft[0]
        elif part == 'aft':
            prefix = bef_aft[1]
    else:
        prefix = ""
    return prefix

def find_suffix(part):
    if part in ("bc, ad"):
        bc_ad = date_prefs[5].split("/")
        if part == "bc":
            suffix = bc_ad[0]
        elif part == "ad":
            suffix = bc_ad[1]
    elif part in ("os, ns"):
        os_ns = date_prefs[6].split("/")
        if part == "os":
            suffix = bc_ad[0]
        elif part == "ns":
            suffix = bc_ad[1]
    else:
        suffix = ""
    return suffix

def convert_month(part, dateform):
    month = ""
    idx = 0
    if 'abb' in dateform:
        idx = 1
    elif 'dot' in dateform:
        idx = 2
    for k,v in MONTH_CONVERSIONS.items():
        if k == part:
            month = v[idx] 
            break
    return month

        


if __name__ == "__main__":

    # this doesn't do anything yet

    from autofill import EntryAuto
    from widgets import Entry

    root = tk.Tk()

    inwidg = EntryAuto(root)
    inwidg.grid()
    inwidg.focus_set()

    traverse = Entry(root)
    traverse.grid()

    root.mainloop()


    

