# opening.py

import tkinter as tk
import sqlite3
from os import listdir, path
from os.path import isfile, join
from window_border import Border
from widgets import Toplevel, Canvas, Button, Frame, ButtonBigPic
from toykinter_widgets import run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from messages_context_help import opening_dlg_help_msg
from PIL import Image, ImageTk
from files import (
    open_tree, make_tree, import_gedcom, open_sample, app_path, global_db_path,
    get_current_file, set_closing, change_tree_title, filter_tree_title)
from styles import config_generic
from messages import open_message, opening_msg, open_input_message2
from utes import center_dialog, titlize
from query_strings import (
    select_app_setting_openpic_dir, select_closing_state_openpic,
    update_closing_state_openpic, select_closing_state_recent_files
)
import dev_tools as dt
from dev_tools import looky, seeline   




class SplashScreen(Toplevel):
    def __init__(self, master, treebard, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.treebard = treebard
        self.master.iconify()
        self.master.overrideredirect(1)
        self.overrideredirect(1)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        splash_file = "{}/images/splash.gif".format(app_path)
        pil_img = Image.open(splash_file)
        tk_img = ImageTk.PhotoImage(pil_img)
        splash_canvas = Canvas(
            self, 
            height=height*0.33, 
            width=width*0.33,
            bg=self.treebard.formats['bg'])
        splash_canvas.create_image(width*0.33/2, height*0.33/2, image=tk_img)
        splash_canvas.pack()

        center_dialog(self)

        self.after(1000, self.destroy)
        self.master.wait_window(self)
        self.master.overrideredirect(0)
        self.master.deiconify()
        self.master.overrideredirect(1)

    def close_dialog(self, evt=None):
        self.opening_dialog.destroy()

    def open_treebard(self, make_main_window):

        ''' The opening dialog is important because you never want to open 
            a tree automatically. If the user has two trees that are similar,
            he might start working on the wrong tree without realizing it. Or
            if the wrong tree opens automatically and it's really huge, he
            might have to wait for it to open just so he can close it. So the 
            user has to select a tree to open every time the app loads. 
        '''

        self.opening_dialog = Toplevel(self.master)
        self.opening_dialog.rc_menu = RightClickMenu(self.master)
        self.opening_dialog.grab_set()
        self.canvas = Border(self.opening_dialog, self.master, self.treebard.formats)
        self.canvas.title_1.config(text='Open, Create, or Copy a Tree')
        self.canvas.title_2.config(text="")

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor="nw", window=self.window)

        self.measure = Frame(self.window)
        self.measure.grid(column=0, row=0, sticky="ew")

        buttonbox = Frame(self.measure)
        buttonbox.grid(column=0, row=0, sticky="ew")

        self.picbutton = ButtonBigPic(
            self.window,  
            command=lambda funx=self.treebard.make_main_window: self.open_prior_file(funx))
        self.picbutton.grid(column=0, row=1, sticky='news')
        self.picbutton.focus_set()

        opener = Button(
            buttonbox, 
            text='OPEN TREE', 
            command=lambda tbard=self.treebard, 
                dlg=self.opening_dialog: open_tree(tbard, dlg))
        opener.grid(column=0, row=0, padx=24, pady=24)

        new = Button(
            buttonbox, 
            text='NEW TREE', 
            command=lambda root=self.master,
                treebard=self.treebard,
                errfunx=open_input_message2,
                errmsg=opening_msg, 
                opening_dialog=self.opening_dialog: make_tree(
                    root, self.treebard, errfunx, errmsg, opening_dialog))
        new.grid(column=1, row=0, padx=24, pady=24)

        importgedcom = Button(
            buttonbox, 
            text='IMPORT',
            command=lambda: import_gedcom(
                self.master, open_message, opening_msg[2]))
        importgedcom.grid(column=2, row=0, padx=24, pady=24)

        opensample = Button(
            buttonbox, 
            text='SAMPLE TREE', 
            command= open_sample)
        opensample.grid(column=3, row=0, padx=24, pady=24)

        cancel = Button(
            buttonbox, 
            text='CANCEL', 
            command=self.close_dialog)
        cancel.grid(column=4, row=0, padx=24, pady=24)
 
        self.update_idletasks()
        self.picwidth = buttonbox.winfo_reqwidth() 
        self.show_openpic() 

        visited = (
            (opener, 
                "Open Tree...", 
                "Open an existing tree."),
            (new, 
                "New Tree...", 
                "Create a new tree."),
            (importgedcom, 
                "Import GEDCOM...", 
                "Create a new tree from an existing GEDCOM file."),
            (opensample, 
                "Open Sample Tree...", 
                "Open the tree that comes with Treebard."),
            (cancel, 
                "Close Dialog", 
                "Close this dialog leaving Treebard open."),
            (self.picbutton, 
                "Open Prior Tree", 
                "Re-open the last tree that was used.")
)        
        run_statusbar_tooltips(
            visited, 
            self.canvas.statusbar.status_label, 
            self.canvas.statusbar.tooltip_label)

        rcm_widgets = (
            opener, new, importgedcom, opensample, cancel, self.picbutton)
        make_rc_menus(
            rcm_widgets, 
            self.opening_dialog.rc_menu,
            opening_dlg_help_msg)

        config_generic(self.opening_dialog)
        self.master.wait_window(self.opening_dialog)
        self.store_last_openpic()

    def open_prior_file(self, make_main_window):
        self.opening_dialog.grab_release()
        self.opening_dialog.destroy()
        current_file = get_current_file()
        if path.exists(current_file[0]) is False:
            msg = open_message(self.master, opening_msg[0], "Missing File Error", "OK")
            msg[0].grab_set()
            set_closing()
            return
        make_main_window() 
        tree_title = current_file[1].replace("_", " ")
        tree_title = titlize(tree_title)
        filter_tree_title(tree_title)
        change_tree_title(self.treebard)

    def store_last_openpic(self):
        conn = sqlite3.connect(global_db_path)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_closing_state_openpic, (self.openpic,))
        conn.commit()
        cur.close()
        conn.close()

    def get_pic_dimensions(self):

        img_stg = ''.join(self.openpic)
        new_stg = '{}/{}/{}'.format(app_path, self.openpic_dir, img_stg)
        self.current_image = Image.open(new_stg)
        resize_factor = self.picwidth / self.current_image.width
        self.picwidth = int(resize_factor * self.current_image.width)
        self.picheight = int(resize_factor * self.current_image.height)
        self.current_image = self.current_image.resize(
            (self.picwidth, self.picheight), 
            Image.ANTIALIAS)
        return self.current_image

    def show_openpic(self):

        self.select_opening_image()
        self.current_image = self.get_pic_dimensions()

        img1 = ImageTk.PhotoImage(self.current_image, master=self.master)
        self.picbutton.config(image=img1)
        self.picbutton.image = img1
        bd_ht = 2
        frm_ht = 80
        self.canvas.config(
            width=self.picwidth + 2, height=self.picheight + bd_ht + frm_ht)
        self.picbutton.config(width=self.picwidth)
        center_dialog(self.opening_dialog, frame=self.window)

    def select_opening_image(self):
        conn = sqlite3.connect(global_db_path)
        cur = conn.cursor()
        cur.execute(select_app_setting_openpic_dir)
        openpic_dir = cur.fetchone()
        userpath = False
        if openpic_dir[0] is None:
            self.openpic_dir = openpic_dir[1]
        else:
            self.openpic_dir = openpic_dir[0]
            userpath = True

        # user can input any desired path to pictures in a settings tab
        # if user's path is no good, use openpic_dir[1] after all
        if userpath:
            print("line", looky(seeline()).lineno, "provide full path including drive:")
        else:
            tbardpath = "{}/images/openpic/".format(app_path)
            all_openpics = [f for f in listdir(tbardpath) if isfile(
                join(tbardpath, f))]

        cur.execute(select_closing_state_openpic)
        last_openpic = cur.fetchone()[0]
        cur.close()
        conn.close()
        last_in_list = len(all_openpics) - 1
        p = 0
        for pic in all_openpics:
            if p + 1 > last_in_list:
                self.openpic = all_openpics[0]
                break
            elif pic == last_openpic:
                self.openpic = all_openpics[p + 1]
                break
            else:
                p += 1

