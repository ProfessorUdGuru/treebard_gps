# opening.py

import tkinter as tk
import sqlite3
from os import listdir, path
from os.path import isfile, join
from window_border import Border
from widgets import Toplevel, Canvas, Button, Frame, ButtonPlain
from toykinter_widgets import run_statusbar_tooltips
from PIL import Image, ImageTk
from files import (
    open_tree, make_tree, import_gedcom, open_sample, app_path, global_db_path, get_current_file, set_closing)
from styles import make_formats_dict, config_generic
from messages import open_error_message, opening_msg, open_input_message2
from utes import center_dialog
from query_strings import (
    select_app_setting_openpic_dir, select_closing_state_openpic,
    update_closing_state_openpic
)
import dev_tools as dt
from dev_tools import looky, seeline   






formats = make_formats_dict()

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
            bg=formats['bg'])
        splash_canvas.create_image(width*0.33/2, height*0.33/2, image=tk_img)
        splash_canvas.pack()

        dlg_pos = center_dialog(self)
        self.geometry('{}x{}+{}+{}'.format(
            str(int(width * 0.33)), 
            str(int(height * 0.33)), 
            dlg_pos[0], 
            dlg_pos[1]))

        self.after(1000, self.destroy)
        self.master.wait_window(self)
        self.master.overrideredirect(0)
        self.master.deiconify()
        self.master.overrideredirect(1)

    def close_dialog(self, evt=None):
        print("line", looky(seeline()).lineno, "running:")
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
        self.opening_dialog.grab_set()
        # gridded in Border class:
        self.canvas = Border(self.opening_dialog, tree_is_open=0)
        self.canvas.title_1.config(text='Open, Create, or Copy a Tree')
        self.canvas.title_2.config(text="")
        self.canvas.quitt.bind("<Button-1>", self.close_dialog)

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor="nw", window=self.window)

        self.measure = Frame(self.window)
        self.measure.grid(column=0, row=0, sticky="ew")

        buttonbox = Frame(self.measure)
        buttonbox.grid(column=0, row=0, sticky="ew")

        self.picbutton = ButtonPlain(
            self.window,  
            command=lambda funx=self.treebard.make_main_window: self.open_prior_file(funx))
        self.picbutton.grid(column=0, row=1, sticky='news')

        opener = Button(
            buttonbox, 
            text='OPEN TREE', 
            command=lambda tbard=self.treebard, 
                # funx=make_main_window, 
                dlg=self.opening_dialog: open_tree(tbard, dlg))
                # dlg=self.opening_dialog: open_tree(treebard, funx, dlg))
        opener.grid(column=0, row=0, padx=24, pady=24)
        opener.focus_set()

        new = Button(
            buttonbox, 
            text='NEW TREE', 
            command=lambda root=self.master,
                treebard=self.treebard, 
                dlg=self.opening_dialog,
                errfunx=open_input_message2: make_tree(
                    root, self.treebard, dlg, errfunx))
                # dlg=self.opening_dialog: make_tree(root, self.treebard, dlg))
        new.grid(column=1, row=0, padx=24, pady=24)

        importgedcom = Button(
            buttonbox, 
            text='IMPORT',
            command=lambda: import_gedcom(self.master))
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

        config_generic(self.opening_dialog)
        self.master.wait_window(self.opening_dialog)
        self.store_last_openpic()

    def open_prior_file(self, make_main_window):
        self.opening_dialog.grab_release()
        self.opening_dialog.destroy()
        current_file = get_current_file()
        if path.exists(current_file[0]) is False:
            msg = open_error_message(self.master, opening_msg[0], "Missing File Error", "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            set_closing()
            return
        make_main_window()        

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
        '''
            It seems like extra steps are needed to make `center_dialog()` take
            the picture size into account. Getting the picture to be the same
            width as the buttonbox was easy, but getting Tkinter to include the
            height of the picture when centering the dialog vertically... 
            it took hours.
        '''

        self.select_opening_image()
        self.current_image = self.get_pic_dimensions()

        img1 = ImageTk.PhotoImage(self.current_image, master=self.master)
        self.picbutton.config(image=img1)
        self.picbutton.image = img1
        self.canvas.config(width=self.picwidth + 2, height=self.picheight + 80)
        self.picbutton.config(width=self.picwidth)
        dlg_pos = center_dialog(self.opening_dialog, frame=self.measure)
        self.opening_dialog.geometry(
            "+{}+{}".format(dlg_pos[0], int(dlg_pos[1] - (self.picheight / 2))))

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

