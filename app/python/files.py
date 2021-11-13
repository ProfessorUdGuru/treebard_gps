# files

from sys import argv
from os import path, rename, mkdir, listdir
from shutil import copy2
from tkinter import (
    messagebox, filedialog, Label, Entry, Toplevel, StringVar, Frame, Button)
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
default_new_tree_images = "{}treebard_gps/data/settings/images".format(current_drive)
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
TBARD_NEUTRAL = "#878787"
TBARD_NEUTRAL2 = "#999999"

current_file = ""

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

def get_current_file():

    global current_file

    prior_file = get_prior_tree()
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
    print("line", looky(seeline()).lineno, "current_file:", current_file)
    file_ok = path.exists(current_file)
    print("line", looky(seeline()).lineno, "file_ok:", file_ok)

    if file_ok is False:
        # last-used tree was moved/deleted outside of Treebard controls,
        #    so don't let SQLite make a blank db by that name
        set_current_file("sample_tree.tbd")
        current_file = "{}treebard_gps/data/sample_tree/sample_tree.tbd".format(
            current_drive)
        current_dir = "{}treebard_gps/data/sample_tree".format(
            current_drive)
    # if file_ok is False:
        # valid_dummy = 'default_new_tree.db'
        # # last-used tree was moved/deleted outside of Treebard controls,
        # #    so don't let SQLite make a blank db by that name
        # set_current_file(valid_dummy)
        # current_file = '{}treebard_gps/data/settings/{}'.format(
            # current_drive, valid_dummy)
        # current_dir = '{}treebard_gps/data/settings'.format(
            # current_drive)
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

def open_tree(treebard, funx, dialog=None):
# def open_tree(root, funx, dialog=None):
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
    print("line", looky(seeline()).lineno, "running:")
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
    current_path = open_dialog.split('/')
    current_file = current_path[len(current_path)-1]
    set_current_file(current_file)
    change_tree_title(treebard)
    # change_tree_title(root)
    funx()
    if dialog:
        dialog.destroy() 

def get_new_tree_title(current_file):
    print("line", looky(seeline()).lineno, "current_file:", current_file)
# line 148 current_file: D:/treebard_gps/data/sprunk_tree/sprunk_tree.tbd
    file_only = current_file.split("/")[4].rstrip(".tbd").replace("_", " ").title()
    print("line", looky(seeline()).lineno, "file_only:", file_only)
    # ext_idx = current_file.rfind('.')
    # slash_idx = current_file.rfind('/')+1
    # file_only = current_file[slash_idx:ext_idx]
    return file_only

def change_tree_title(treebard):
    current_file = get_current_file()[0]
    file_only = get_new_tree_title(current_file) 
    print("line", looky(seeline()).lineno, "file_only:", file_only)
    treebard.canvas.title_2.config(text=file_only)

def get_opening_dir():
    '''detects root drive of current working directory, 
        e.g. if running from flash drive or hard drive
        then detects user's save directory'''
    init_dir = current_drive + 'treebard_gps/data' # later
    # init_dir = current_drive + 'treebard_gps/data/sample_tree' # during dev
    return init_dir

def make_tree(root, treebard, make_main_window, opening_dialog):
    '''
        I'm using a more palatable custom replacement for Tkinter's simpledialog instead of Tkinter's built-in file dialog because currently the user doesn't get to decide both project folders and project names, right now they both have to be the same, and this way I can keep it simple for now.
        Since Treebard is portable I don't think it's a good idea to let the
        user store files just anywhere but there might be a reason I haven't
        thought of. To keep Treebard simple and portable, the user can put
        Treebard on any drive and then Treebard makes decisions from there as
        to where files are saved and what to call project directories, based on the
        user's initial input of a tree title. The user can still keep copies 
        of his files anywhere but I think to be portable, everything the
        program needs has to be kept in one folder. Anyway, 
        simpledialog wasn't configurable, but my reason for using it was that it's
        needed here in files.py and I don't want to restructure my imports so
        that Treebard's messages can be imported from widgets.py. However I guess a custom dialog
        could be imported from an impartial module where it could be created
        by inheriting directly from tkinter Toplevel and then I would be able
        to include it in Treebard's colorizer scheme.

    '''

    new_tree_name = open_input_message(
        root, files_msg[0], "Give the Tree a Unique Title", "OK", "CANCEL")
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
    opening_dialog.destroy()
    root.focus_set()
    make_main_window()

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

class Dialogue(Toplevel):
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.config(bg=TBARD_NEUTRAL)

files_msg = ("Treebard will use your title as the tree's display title.\n"
    "Treebard will save 'Smith Family Tree' as a database file at\n`{current "
    "drive}/treebard_gps/data/smith_family_tree/smith_family_tree.tbd`",)

def open_input_message(root, message, title, ok_lab, cancel_lab):
    '''
        To avoid a circular import, this couldn't be imported in the usual way.
        There aren't supposed to be any widgets made in this general namespace
        since it would auto-create another instance of Tk(), so this is a 
        custom dialog used only here. Tkinter's simpledialog worked here but 
        it's stark white and apparently that can't be changed. 

        After creating this, I realized that the same-named function could be 
        passed here as a parameter of make_tree(), but I don't know if it could 
        be formatted with config_generic which can't be imported here. I didn't 
        try it yet. If it can be done it should be, but the code below should
        in that case be renamed in messages.py so as to not disturb
        current callings of messages.open_input_message()
    '''
    def ok():
        cancel()

    def cancel():
        msg.destroy()
        root.grab_set()

    def show():
        gotten = got.get()
        return gotten

    got = StringVar()

    msg = Dialogue(root)
    msg.grab_set()
    msg.title(title)
    msg.columnconfigure(0, weight=1)
    msg.rowconfigure(0, weight=1)
    lab = Label(
        msg, text=message, justify='left', bg=TBARD_NEUTRAL2, 
        font=("courier", 14, "bold"))
    lab.grid(column=0, row=0, sticky='news', padx=12, pady=12, columnspan=2)
    inPut = Entry(
        msg, textvariable=got, bg=TBARD_NEUTRAL2, width=48, 
        font=("dejavu sans mono", 14))
    inPut.grid(column=0, row=1, padx=12)
    buttonbox = Frame(msg, bg=TBARD_NEUTRAL)
    buttonbox.grid(column=0, row=2, sticky='e', padx=(0,12), pady=12)
    ok_butt = Button(
        buttonbox, text=ok_lab, command=cancel, width=7, bg=TBARD_NEUTRAL2)
    ok_butt.grid(column=0, row=0, padx=6, sticky='e')
    cancel_butt = Button(
        buttonbox, text=cancel_lab, command=cancel, width=7, bg=TBARD_NEUTRAL2)
    cancel_butt.grid(column=1, row=0, padx=6, sticky='e')
    inPut.focus_set()
    root.wait_window(msg)
    gotten = show()
    return gotten