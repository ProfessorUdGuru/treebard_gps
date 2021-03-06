# dev_tools

from inspect import stack
from datetime import datetime
from shutil import copy2
import inspect as iii
import tkinter as tk

def get_screensize():
    r = tk.Tk()
    x = r.winfo_screenwidth()
    y = r.winfo_screenheight()
    return x, y
    

looky = iii.getframeinfo
seeline = iii.currentframe
# to use:
# print(looky(seeline()).lineno)
# to get the real line no. do this:
#     x = 66
#     print("line", looky(seeline()).lineno, "x:", x)
# so I made a macro in Notepad++ that I ran after typing the value I want to print
# the macro is called print_a_line and its keyboard shortcut is CTRL+SHIFT+F5


# ****************************************************************


'''
	Made this module for the rollback tool since the tool didn't
	work when trying to import it by itself. This will also keep
    this sort of thing separate from the app itself.
'''

def make_rollback_copy():
    ''' 
        Call this from any .py file in the working folder to create a rollback
        for that file in the rollbacks directory with a timestamp appended to 
        the file name. 
    '''

    file_to_save = stack()[1][1]
    now = datetime.now()

    stamp = now.strftime("%Y%m%d%H%M")

    barename = file_to_save.split('.')
    barename = barename[0]
    barename = barename.split('\\')
    barename = barename[len(barename)-1]

    newname = barename + stamp + '.py'
    copy2(file_to_save, 'D:/treebard_2021/rollbacks/' + newname)