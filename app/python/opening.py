# opening.py

import tkinter as tk
from widgets import Toplevel, Canvas, Button
from PIL import Image, ImageTk
from files import (
    open_tree, make_tree, save_as, save_copy_as, rename_tree, project_path)
from styles import make_formats_dict, config_generic 
from utes import center_dialog
import dev_tools as dt
from dev_tools import looky, seeline   






formats = make_formats_dict()

class SplashScreen(Toplevel):
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        master = self.master

        self.master.iconify()
        self.master.overrideredirect(1)
        self.overrideredirect(1)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        splash_file = "{}/images/splash_small.gif".format(project_path)
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
            str(int(width*0.33)), 
            str(int(height*0.33)), 
            dlg_pos[0], 
            dlg_pos[1]))

        self.after(500, self.destroy)
        self.master.wait_window(self)
        self.master.overrideredirect(0)
        self.master.deiconify()
        self.master.overrideredirect(1)

    def open_treebard(self):

        ''' This opening window is important because you never want to open 
            a tree automatically. If the user has two trees that are similar,
            he might start working on the wrong tree without realizing it. Or
            if the wrong tree opens automatically and it's really huge, he
            might have to wait for it to open just so he can close it. So 
            this opening dialog might be a bit of a nuisance to deal 
            with on each loading of the app, but it's not optional. '''

        self.open_tbard = Toplevel(self.master)
        self.open_tbard.title('Open, Create, or Copy a Tree')
        self.open_tbard.grab_set()

        opener = Button(
            self.open_tbard, 
            text='OPEN TREE', 
            command=lambda: open_tree(self.master, dialog=self.open_tbard))
        opener.grid(column=0, row=0, padx=24, pady=24)
        opener.focus_set()

        new = Button(
            self.open_tbard, 
            text='NEW TREE',
            command=lambda: make_tree(self.master, dialog=self.open_tbard))
        new.grid(column=1, row=0, padx=24, pady=24)

        saveas = Button(
            self.open_tbard, 
            text='SAVE AS',
            command=lambda: save_as(self.master))
        saveas.grid(column=2, row=0, padx=24, pady=24)

        savecopyas = Button(
            self.open_tbard, 
            text='SAVE COPY AS', 
            command=lambda: save_copy_as())
        savecopyas.grid(column=3, row=0, padx=24, pady=24)

        rename = Button(
            self.open_tbard, 
            text='RENAME TREE', 
            command=lambda: rename_tree(self.master))
        rename.grid(column=4, row=0, padx=24, pady=24)

        config_generic(self.open_tbard)

        dlg_pos = center_dialog(self.open_tbard)
        self.open_tbard.geometry("+{}+{}".format(dlg_pos[0], dlg_pos[1])) 

# def open_treebard():

    # ''' This opening window is important because you never want to open 
        # a tree automatically. If the user has two trees that are similar,
        # he might start working on the wrong tree without realizing it. Or
        # if the wrong tree opens automatically and it's really huge, he
        # might have to wait for it to open just so he can close it. So 
        # this opening dialog might be a bit of a nuisance to deal 
        # with on each loading of the app, but it's not optional. '''

    # open_tbard = Toplevel()
    # open_tbard.title('Open, Create, or Copy a Tree')

    # opener = Button(
        # open_tbard, 
        # text='OPEN TREE', 
        # command=lambda: open_tree(root, dialog=open_tbard))
    # opener.grid(column=0, row=0, padx=24, pady=24)
    # opener.focus_set()

    # new = Button(
        # open_tbard, 
        # text='NEW TREE',
        # command=lambda: make_tree(root, dialog=open_tbard))
    # new.grid(column=1, row=0, padx=24, pady=24)

    # saveas = Button(
        # open_tbard, 
        # text='SAVE AS',
        # command=lambda: save_as(root))
    # saveas.grid(column=2, row=0, padx=24, pady=24)

    # savecopyas = Button(
        # open_tbard, 
        # text='SAVE COPY AS', 
        # command=lambda: save_copy_as())
    # savecopyas.grid(column=3, row=0, padx=24, pady=24)

    # rename = Button(
        # open_tbard, 
        # text='RENAME TREE', 
        # command=lambda: rename_tree(root))
    # rename.grid(column=4, row=0, padx=24, pady=24)

    # config_generic(open_tbard)

    # dlg_pos = utes.center_dialog(open_tbard)
    # open_tbard.geometry("+{}+{}".format(dlg_pos[0], dlg_pos[1])) 




# def open_treebard(self):

    # ''' This opening window is important because you never want to open 
        # a tree automatically. If the user has two trees that are similar,
        # he might start working on the wrong tree without realizing it. Or
        # if the wrong tree opens automatically and it's really huge, he
        # might have to wait for it to open just so he can close it. So 
        # this opening dialog might be a bit of a nuisance to deal 
        # with on each loading of the app, but it's not optional. '''

    # self.open_tbard = Toplevel()
    # self.open_tbard.title('Open, Create, or Copy a Tree')

    # open = Button(
        # self.open_tbard, 
        # text='OPEN TREE', 
        # command=lambda: self.files.open_tree(root, dialog=self.open_tbard))
    # open.grid(column=0, row=0, padx=24, pady=24)
    # open.focus_set()

    # new = Button(
        # self.open_tbard, 
        # text='NEW TREE',
        # command=lambda: self.files.make_tree(root, dialog=self.open_tbard))
    # new.grid(column=1, row=0, padx=24, pady=24)

    # saveas = Button(
        # self.open_tbard, 
        # text='SAVE AS',
        # command=lambda: self.files.save_as(root))
    # saveas.grid(column=2, row=0, padx=24, pady=24)

    # savecopyas = Button(
        # self.open_tbard, 
        # text='SAVE COPY AS', 
        # command=lambda: self.files.save_copy_as())
    # savecopyas.grid(column=3, row=0, padx=24, pady=24)

    # rename = Button(
        # self.open_tbard, 
        # text='RENAME TREE', 
        # command=lambda: self.files.rename_tree(root))
    # rename.grid(column=4, row=0, padx=24, pady=24)

    # ST.config_generic(self.open_tbard)

    # dlg_pos = utes.center_dialog(self.open_tbard)
    # self.open_tbard.geometry("+{}+{}".format(dlg_pos[0], dlg_pos[1])) 