# files

from sys import argv
from os import path, rename, mkdir
from shutil import copy2
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import sqlite3
from query_strings import (
    select_closing_state_prior_tree, update_closing_state_tree)
import dev_tools as dt
from dev_tools import looky, seeline

current_path = argv[0].replace("\\", "/")
split_path = current_path.split("/")
current_drive = "{}/".format(split_path[0])
app_path = "{}treebard_gps/app/python/".format(current_drive)
app_name = split_path[4]
new_file_path = "{}treebard_gps/data/".format(current_drive)
global_db_path = "{}treebard_gps/data/settings/treebard.db".format(
    current_drive)
default_new_tree = "{}treebard_gps/data/settings/default_new_tree.db".format(
    current_drive)
untouched_copy_default_new_tree = "treebard_gps/app/default/default_new_tree.db"

print("current_path:", current_path)
print("split_path:", split_path)
print("current_drive:", current_drive)
print("app_name:", app_name)
print("global_db_path:", global_db_path)

# current_path: D:/treebard_gps/app/python/treebard_root_023.py
# split_path: ['D:', 'treebard_gps', 'app', 'python', 'treebard_root_023.py']
# current_drive: D:/
# app_name: treebard_root_023.py

# REPLACE OBSOLETE HODGE-PODGE-STYLE STRINGS:

# # split_path = path.splitdrive(current_path)
# # current_drive = '{}/'.format(split_path[0])
# # app_path = '{}treebard_gps/app/python/'.format(current_drive)
# # # db_path
# # global_db_path = "{}treebard_gps/data/settings/treebard.db".format(current_drive)

# print("argv", argv)
# print("current_path", current_path)
# print("split_path", split_path)
# print("current_drive", current_drive)
# print("app_path", app_path)
# print("global_db_path", global_db_path)
# # argv ['D:\\treebard_gps\\app\\python\\treebard_root_023.py']
# # current_path D:/treebard_gps/app/python/treebard_root_023.py
# # split_path ('D:', '\\treebard_gps\\app\\python\\treebard_root_023.py')
# # current_drive D:\
# # app_path D:\treebard_gps/app/python/
# # global_db_path D:\treebard_gps/data/settings/treebard.db


prior_file = ""
current_file = ""
# current_dir = ""

def get_prior_tree():
    conn = sqlite3.connect(global_db_path)
    cur = conn.cursor()
    cur.execute(select_closing_state_prior_tree)
    prior_file = cur.fetchone()
    cur.close()
    conn.close()
    if prior_file:
        prior_file = prior_file[0]
    else:
        prior_file = ''

    return prior_file

def get_current_file(): # change to get_prior_file and write another funx to get current file from user/open dlg etc.; THIS FUNX BASES current_file ON prior_file SO THIS IS USED ON PIC CLICK, NOT RUN AUTOMATICALLY
    global prior_file, current_file # prior_file not a global bec this code doesn't change it?
    prior_file = get_prior_tree()
    if prior_file is None:
        return

    if prior_file == 'default_new_tree.db': # is this still needed? Seems like I did this as part of a procedure that would open and/or copy the default tree if it were needed, but the details escape me now. Probably part of make_new_tree() since it would be using the default tree as a template.
        current_file = prior_file
        current_dir = '{}treebard_gps/data/settings'.format(
            current_drive)

    elif len(prior_file) > 0:
        current_dir = prior_file.rstrip('.tbd')
        current_file = '{}treebard_gps/data/{}/{}'.format(
            current_drive, current_dir, prior_file)
    else:
        current_file = ''
    file_ok = path.exists(current_file)
    if file_ok is False:
        valid_dummy = 'default_new_tree.db'
        # last-used tree was moved/deleted outside of Treebard controls,
        #    so don't let SQLite make a blank db by that name
        set_current_file(valid_dummy)
        current_file = '{}treebard_gps/data/settings/{}'.format(
            current_drive, valid_dummy)
        current_dir = '{}treebard_gps/data/settings'.format(
            current_drive)
    return current_file, current_dir

def set_current_file(current_file):
    if len(current_file.strip()) == 0:
        return
    # current_dir = current_file.rstrip(".tbd")
    # if isnewfile is False:
        # db_path = "{}treebard_gps/data/{}/{}".format(
            # current_drive, current_dir, current_file) 
    # else:
    # print("line", looky(seeline()).lineno, "current_file:", current_file)
    # current_file = current_file.split("/")[3]
    # if isnewfile is True:
        # print("line", looky(seeline()).lineno, "current_file:", current_file)
        # print("line", looky(seeline()).lineno, "current_dir:", current_dir)
        # print("line", looky(seeline()).lineno, "current_drive:", current_drive)
# line 111 current_file: D:/treebard_gps/data/sample_tree_copy1.tbd
# line 112 current_dir: D:/treebard_gps/data/sample_tree_copy1
# line 113 current_drive: D:/
# line 118 db_path: D:/treebard_gps/data/sample_tree_copy1/sample_tree_copy1.tbd
        
        # mkdir(current_file.rstrip(".tbd"))
        # db_path = "{}/{}".format(current_dir, current_file.split("/")[3])
    # print("line", looky(seeline()).lineno, "db_path:", db_path)
    conn = sqlite3.connect(global_db_path)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    cur.execute(update_closing_state_tree, (current_file,))
    conn.commit()
    cur.close()
    conn.close()

def open_tree(root, funx, dialog=None):
    ''' 
        Re: what shows up pre-loaded into the dialog's 
            directory input: tkinter's default behavior is 
        1) last directory opened from is loaded by default;
        2) if nothing has been opened from before, 
            current working directory is default;
        3) but if initialdir is provided below, 
            dialog opens with that instead;
        4) and if that doesn't work, dialog opens with 
            My Documents the pre-loaded directory
    '''

    init_dir = get_opening_dir()
    current_file = get_current_file()[0]

    open_dialog = filedialog.askopenfilename(
        initialdir=init_dir,
        title = 'Select Tree to Open', 
        defaultextension = ".tbd", 
        filetypes=(
            ('Treebard family trees','*.tbd'),
            ('all files','*.*')))
    if len(current_file) == 0:
        return
    # if len(current_file) != 0:
    current_path = open_dialog.split('/')
    current_file = current_path[len(current_path)-1]
    set_current_file(current_file)
    change_tree_title(root)
    funx()
    if dialog:
        dialog.destroy() 

def get_new_tree_title(current_file):
    ext_idx = current_file.rfind('.')
    slash_idx = current_file.rfind('/')+1
    file_only = current_file[slash_idx:ext_idx]
    return file_only

def change_tree_title(parent):
    # current_file = get_current_file()[0]
    file_only = get_new_tree_title(current_file) 
    # fix this for Border class
    # parent.title('{}            Treebard Genieware Pattern Simulation'.format(
        # file_only))

def get_opening_dir():
    '''detects root drive of current working directory, 
        e.g. if running from flash drive or hard drive
        then detects user's save directory'''
    init_dir = current_drive + 'treebard_gps/data' # later
    # init_dir = current_drive + 'treebard_gps/data/sample_tree' # during dev
    return init_dir

def make_tree(root):
    '''
        I'm using Tkinter's simpledialog instead of its file dialog because
        user is not currently a big part of the filename and directory process
        when creating a new tree, and this way I can keep it simple for now.
        Since Treebard is portable I don't think it's a good idea to let the
        user store files just anywhere but I haven't thought it through yet.
    '''

    new_tree_name = askstring("Input", "New Tree Name")
    print("line", looky(seeline()).lineno, "new_tree_name:", new_tree_name)
    current_dir = new_tree_name.lower().replace(" ", "_").strip()
    print("line", looky(seeline()).lineno, "current_dir:", current_dir)
    if len(current_dir) == 0:
        return
# new_file_path = "{}treebard_gps/data/".format(current_drive)
    new_path = new_file_path
    current_file = "{}.tbd".format(current_dir)
    full_path = "{}{}".format(new_path, current_dir)
    print("line", looky(seeline()).lineno, "new_path:", new_path)
    print("line", looky(seeline()).lineno, "full_path:", full_path)
    mkdir(full_path)
    copy2(default_new_tree, full_path)
    set_current_file(current_file)
    change_tree_title(root);print("new_tree_name:", new_tree_name)
    # open new tree


# def make_tree(root, dialog=None, isnewfile=True):
    # this version gives user choice of folder which is wrong
    # def get_default_db():
        # '''detects root drive of current working directory, 
           # e.g. if running from partitioned hd or USB'''
        # root_drive_local = current_drive.replace('\\', '/')
        # init_file = '{}treebard_gps/data/settings/default_new_tree.db'.format(
            # root_drive_local)
        # return init_file

    # init_dir = get_opening_dir()
    # init_file = get_default_db()

    # current_file = filedialog.asksaveasfilename(
        # initialdir = init_dir,
        # title = 'Create a New Tree', 
        # defaultextension = '.tbd', 
        # filetypes = (
            # ('Treebard genealogy trees','*.tbd'),
            # ('all files','*.*')))
    # print("line", looky(seeline()).lineno, "current_file:", current_file)
    # if len(current_file) == 0:
        # return
    # copy2(init_file, current_file)
    # set_current_file(current_file, isnewfile)
    # change_tree_title(root)
    # if dialog:
        # dialog.destroy()
        
def save_as(root, evt=None):

    init_dir = get_opening_dir()
    current_file = get_current_file()[0]
    saveas_dialog = filedialog.asksaveasfilename(
        initialdir = init_dir,
        initialfile = current_file,
        title = 'Copy Current Tree to a New Tree and Make New Tree Current', 
        defaultextension = '.tbd', 
        filetypes = (
            ('Treebard family trees','*.tbd'),
            ('all files','*.*')))

    try:
        copy2(current_file, saveas_dialog)
    except FileNotFoundError:
        messagebox.showerror(
            'Tree Not Found', 
            'The file does not exist in the location given.')

    current_file = saveas_dialog
    if current_file != "":
        set_current_file(current_file)
        change_tree_title(root)
    else:
        pass

def save_copy_as(evt=None):
    ''' 
        Like save_as except new file is not made current; 
        old file remains current.
    '''

    init_dir = get_opening_dir()

    current_file = get_current_file()[0]

    # New name is chosen for old file.
    copy_dialog = filedialog.asksaveasfilename(
        initialdir = init_dir, 
        initialfile = current_file,
        title = 'Copy Current Tree as a New Tree but Don\'t Open the New Tree', 
        defaultextension = ".tbd", 
        filetypes = (('Treebard family trees','*.tbd'),('all files','*.*')))
    # Old file is copied to new name.
    if copy_dialog != "":
        copy2(current_file, copy_dialog)
    else:
        pass

def rename_tree(root, evt=None): 
    ''' 
        Like save_as, a new file becomes current but the other features 
        are different from save_as: old file is deleted; 
        if new filename already exists, it can't be overwritten 
        so rename will fail.
    '''

    init_dir = get_opening_dir()

    current_file = get_current_file()[0]

    rename_dialog = filedialog.asksaveasfilename(
        initialdir = init_dir, 
        initialfile = current_file,
        title = 'Copy Current Tree to a New Tree by a New Name and '
            'Delete the Old Tree', 
        defaultextension = ".tbd", 
        filetypes = (('Treebard family trees','*.tbd'),('all files','*.*')))

    if rename_dialog != '':
        try:
            rename(current_file, rename_dialog)
            current_file = rename_dialog

            set_current_file(current_file)
            change_tree_title(root)
        except FileExistsError:
            messagebox.showerror(
                'File name already exists.', 
                'Please give the file a unique name.')
    else: 
        pass

def close_tree(root):
    # disable tabs pertaining to indiv. tree (but not places)
    # disable all menu items and icon menu except Open & ?
    # update title
    pass

def exit_app(self):
    pass

def import_gedcom(root):
    # do the gedcom stuff
    # run make_new
    # update title
    pass

def export_gedcom(root):
    # do the gedcom stuff
    pass

def backup_tree(self):
    # make a zip file
    pass

def delete_tree(root):
    # open a dialog
    # remove tree from current_file column in db if current
    #    & put default tree there
    # remove from title
    pass

def open_sample(self):
    # open the sample tree that came with treebard
    pass



