# files (import as files)

from os import path, rename
from shutil import copy2
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
from query_strings import (select_current_tree, update_current_tree)
import dev_tools as dt

root_drive = '{}{}'.format(path.abspath('.').split(path.sep)[0], path.sep)
conn_fig = '{}treebard_gps/data/sample_tree/sample_tree.tbd'.format(root_drive)

def get_current_file():
    conn = sqlite3.connect(conn_fig)
    cur = conn.cursor()
    cur.execute(select_current_tree)
    cur_tup = cur.fetchone()

    if cur_tup:
        cur_tup = cur_tup[0]
    else:
        cur_tup = ''

    if cur_tup == 'default_new_tree.db':
        current_file = cur_tup
        current_dir = '{}treebard_gps/data/settings'.format(
            root_drive)

    elif len(cur_tup) > 0:
        current_dir = cur_tup.rstrip('.tbd')
        current_file = '{}treebard_gps/data/{}/{}'.format(
            root_drive, current_dir, cur_tup)
    else:
        current_file = ''
    cur.close()
    conn.close()
    file_ok = path.exists(current_file)
    if file_ok is False:
        valid_dummy = 'default_new_tree.db'
        # last-used tree was moved/deleted outside of Treebard controls,
        #    so don't let sqlite make a blank db by that name
        set_current_file(valid_dummy)
        current_file = '{}treebard_gps/data/settings/{}'.format(
            root_drive, valid_dummy)
        current_dir = '{}treebard_gps/data/settings'.format(
            root_drive)
    return current_file, current_dir

def set_current_file(new_current_file):
    if new_current_file.strip() != '':
        current_file = new_current_file
        conn = sqlite3.connect(conn_fig)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_tree, (current_file,))
        conn.commit()
        cur.close()
        conn.close()

def open_tree(root, dialog=None):
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
    if len(current_file) != 0:
        current_path = open_dialog.split('/')
        current_file = current_path[len(current_path)-1]
        set_current_file(current_file)
        change_tree_title(root)
    else:
        pass                                                                        
    # self.parent.main.canvas.grid() # DO NOT DELETE

    # # ************* DO NOT DELETE yet
    # # This block of code has to be repeated in each method 
    # #    that opens a tree so try to make a resuable method 
    # #    instead of repeating.
    # events = self.parent.main.persons.findings_table
    # attributes = self.parent.main.persons.attributes_table
    # # Runs once to get a master list of findings that includes
    # #   both events and attributes.
    # events.distinguish_evt_att()
    # # Save the second value so it will still exist when 
    # #   FindingsTable class is instantiated as attributes table.         
    # attributes.current_person_attributes = events.current_person_attributes
    # # runs once for each FindingsTable instance
    # events.make_findings_table(events.current_person_events)
    # attributes.make_findings_table(attributes.current_person_attributes)
    # # *************

    if dialog:
        dialog.destroy() 

def get_new_tree_title(current_file):
    ext_idx = current_file.rfind('.')
    slash_idx = current_file.rfind('/')+1
    file_only = current_file[slash_idx:ext_idx]
    return file_only

def change_tree_title(parent):
    current_file = get_current_file()[0]
    file_only = get_new_tree_title(current_file) 
    parent.title('{}            Treebard Genieware Pattern Simulation'.format(
        file_only))

def get_opening_dir():
    '''detects root drive of current working directory, 
        e.g. if running from flash drive or hard drive
        then detects user's save directory'''
    # init_dir = root_drive + 'treebard_gps/data' # later
    init_dir = root_drive + 'treebard_gps/data/sample_tree' # during dev
    return init_dir

def make_tree(parent, dialog=None):

    def get_default_db():
        '''detects root drive of current working directory, 
           e.g. if running from partitioned hd or USB'''
        root_drive_local = root_drive.replace('\\', '/')
        init_file = '{}treebard_permanent/default_new_tree.db'.format(
            root_drive_local)
        return init_file

    init_dir = get_opening_dir()
    init_file = get_default_db()

    createnew_dialog = filedialog.asksaveasfilename(
        initialdir = init_dir,
        title = 'Create a New Tree', 
        defaultextension = '.tbd', 
        filetypes = (
            ('Treebard genealogy trees','*.tbd'),
            ('all files','*.*')))
    if createnew_dialog != '':
        copy2(init_file, createnew_dialog)

        current_file = createnew_dialog
        set_current_file(current_file)
        change_tree_title(root)
    else: 
        pass

    # # self.parent.main.canvas.grid()# see lines 81 & 217 root_017 MIGHT NEED TO DO THIS

    # # *************
    # # This block of code has to be repeated in each method 
    # #    that opens a tree so try to make a resuable method 
    # #    instead of repeating. It's only been tested in open_tree().
    # events = self.parent.main.persons.findings_table
    # attributes = self.parent.main.persons.attributes_table
    # # Runs once to get a master list of findings that includes
    # #   both events and attributes.
    # events.distinguish_evt_att()
    # # Save the second value so it will still exist when 
    # #   FindingsTable class is instantiated as attributes table.         
    # attributes.current_person_attributes = events.current_person_attributes
    # # runs once for each FindingsTable instance
    # events.make_findings_table(events.current_person_events)
    # attributes.make_findings_table(attributes.current_person_attributes)
    # # *************

    if dialog:
        dialog.destroy()
        
def save_as(root):

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

def save_copy_as(self):
    ''' Like save_as except new file is not made current; 
        old file remains current.'''

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

def rename_tree(root): 
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



