# files.py

from sys import argv
from os import path, rename, mkdir, listdir
from shutil import copy2
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
from query_strings import (
    select_closing_state_prior_tree, update_closing_state_tree,
    update_closing_state_tree_is_closed, update_closing_state_recent_files, 
    select_closing_state_recent_files)
from utes import titlize
import dev_tools as dt
from dev_tools import looky, seeline




current_path = argv[0].replace("\\", "/")
split_path = current_path.split("/")
current_drive = "{}/".format(split_path[0])
app_path = "{}treebard_gps/app/python/".format(current_drive)
app_name = split_path[4]
init_dir = "{}treebard_gps/data".format(current_drive)
new_file_path = "{}treebard_gps/data/".format(current_drive)
global_db_path = "{}treebard_gps/data/settings/treebard.db".format(
    current_drive)
default_new_tree = "{}treebard_gps/data/settings/default_new_tree.db".format(
    current_drive)
default_new_tree_images = "{}treebard_gps/data/settings/images".format(current_drive)
print("line", looky(seeline()).lineno, "default_new_tree_images:", default_new_tree_images)
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

def get_prior_file():
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

def get_current_file():
    '''
        As soon as a file opens, it should be set as the prior file. I.E. the 
        prior file IS the current file.
    '''
    prior_file = get_prior_file()
    if prior_file is None:
        return
    if prior_file == 'default_new_tree.db':
        current_file = prior_file
        current_dir = '{}treebard_gps/data/settings'.format(current_drive)
    elif len(prior_file) > 0:
        current_dir = prior_file.rstrip('.tbd')
        current_file = '{}treebard_gps/data/{}/{}'.format(
            current_drive, current_dir, prior_file)
    else:
        current_file = ''
    return current_file, current_dir    

def set_current_file(current_file):
    if len(current_file.strip()) == 0:
        return
    conn = sqlite3.connect(global_db_path)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    cur.execute(update_closing_state_tree, (current_file,))
    conn.commit()
    cur.close()
    conn.close()

def handle_open_event(evt, treebard):
    '''
        This `handle...` callback, like others in this module with a similar 
        name, takes `evt` as its obligatory first parameter while getting its 
        extra parameters from a lambda that's used to call it. This callback 
        then runs the main function, passing along the extra parameters.
    '''
    open_tree(treebard)

def open_tree(treebard, dialog=None):
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

    open_dialog = filedialog.askopenfilename(
        initialdir = init_dir,
        title = 'Select Tree to Open', 
        defaultextension = ".tbd", 
        filetypes=(
            ('Treebard family trees','*.tbd'),
            ('all files','*.*')))
    if len(open_dialog) == 0:
        return
    current_path = open_dialog.split('/')
    current_file = current_path[len(current_path) - 1]
    set_current_file(current_file)
    tree_title = current_file.replace("_", " ").rstrip(".tbd")
    tree_title = titlize(tree_title)
    filter_tree_title(tree_title) 
    change_tree_title(treebard)
    treebard.make_main_window()
    if dialog:
        dialog.destroy() 

def filter_tree_title(tree_title):

    stored_string = ""
    recent_files = get_recent_files()
    if len(tree_title) == 0: return
    if recent_files is None: return
    save_recent_tree(tree_title, recent_files)

def save_recent_tree(tree_title, recent_files):
    if tree_title not in recent_files:
        recent_files.insert(0, tree_title)
    else:
        recent_files.insert(0, recent_files.pop(recent_files.index(tree_title)))
    if len(recent_files) > 20:
        recent_files = recent_files[0:20]

    stored_string = "_+_".join(recent_files)
    conn = sqlite3.connect(global_db_path)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    cur.execute(update_closing_state_recent_files, (stored_string,))
    conn.commit()
    cur.close()
    conn.close()

def get_recent_files():
    conn = sqlite3.connect(global_db_path)
    cur = conn.cursor()
    cur.execute(select_closing_state_recent_files)
    stored_string = cur.fetchone()[0]
    cur.close()
    conn.close()
    if len(stored_string) == 0:
        return []
    recent_files = stored_string.split("_+_")
    return recent_files

def get_tree_title(current_file):
    file_only = current_file.split("/")[4].rstrip(".tbd").replace("_", " ")
    tree_title = titlize(file_only)
    return tree_title

def change_tree_title(treebard):
    current_file = get_current_file()[0]
    file_only = get_tree_title(current_file) 
    treebard.canvas.title_2.config(text=file_only)

def handle_new_tree_event(evt, root, treebard, open_input_message, opening_msg):
    make_tree(root, treebard, open_input_message, opening_msg)

def make_tree(
    root, treebard, open_input_message, opening_msg, opening_dialog=None):
    '''
        The user can still keep copies of his files anywhere but I think to be 
        portable, everything the program needs has to be kept in one folder.
        So at this time, Treebard creates the program files and folder based on
        a title suggested by the user when he makes a new tree.

    '''

    new_tree_name = open_input_message(
        root, opening_msg[1], "Give the Tree a Unique Title", "OK", "CANCEL")
    current_dir = new_tree_name.lower().replace(" ", "_").strip()
    if len(current_dir) == 0:
        return
    new_path = new_file_path
    current_file = "{}.tbd".format(current_dir)
    dir_path = "{}{}".format(new_path, current_dir)
    mkdir(dir_path)
    mkdir("{}/images".format(dir_path))
    file_path = "{}/{}".format(dir_path, current_file)
    copy2(default_new_tree, file_path)
    for img in listdir(default_new_tree_images):
        src_dir = "{}/{}".format(default_new_tree_images, img)
        dest_dir = "{}/images/{}".format(dir_path, img)
        copy2(src_dir, dest_dir)
    set_current_file(current_file)
    change_tree_title(treebard)
    if opening_dialog:
        opening_dialog.destroy()
    root.focus_set()
    treebard.make_main_window()
    tree_title = current_file.replace("_", " ").rstrip(".tbd")
    tree_title = titlize(tree_title)
    filter_tree_title(tree_title) 

def save_as(root, evt=None):

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

def set_closing(evt=None):

    conn = sqlite3.connect(global_db_path)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(update_closing_state_tree_is_closed)
    conn.commit()
    cur.close()
    conn.close()

def close_tree(evt=None, treebard=None):
    # disable tabs pertaining to indiv. tree (but not places)
    # disable all menu items and icon menu except Open & ?
    treebard.canvas.delete(treebard.main_window)
    treebard.canvas.title_2.config(text="For All Ages")
    set_closing()

def exit_app(evt, root):
    def close_app():
        root.after(1500, root.quit)
    set_closing()
    close_app()

def import_gedcom(root, open_message, msg):
    # do the gedcom stuff
    # run make_new
    # update title
    msg = open_message(root, msg, "Feature Doesn't Exist", "OK")
    msg[0].grab_set()
    msg[1].config(aspect=400)
    return
    
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