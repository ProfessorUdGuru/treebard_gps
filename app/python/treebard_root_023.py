# treebard_root_023.py

import tkinter as tk
import sqlite3    
from PIL import Image, ImageTk
from files import app_path, global_db_path, current_drive, open_tree
from dropdown import DropdownMenu, placeholder
from window_border import Border
from opening import SplashScreen
from scrolling import MousewheelScrolling
from styles import config_generic, make_formats_dict
from main import Main
from widgets import Button, Frame, ButtonPlain
from dates import get_date_formats   
from utes import create_tooltip
from query_strings import (
    update_closing_state_tree_is_open, select_date_format)
import dev_tools as dt
from dev_tools import looky, seeline



'''
IMPORTS STRUCTURE:

               window_border 
               |  |    |   |
               |  |    |   places
               |  |    |       |
               |  |  events_table                              
               |  |  |   |         
               |  main   |                                  
               |    |    |                           
               treebard_root_020                  
                                                        
                    
'''




# setting to less than 1.0 below prevents maximize from working
# setting to more than 1.0 prevents scrollbar from appearing since everything fits in the window but the window is big so you have to drag it by the title bar since it won't scroll unless you manually resize it. Conclusion: keep it 1.0.
MAX_WINDOW_HEIGHT = 1.0 # if 1.0, scrollbar is available immediately
MAX_WINDOW_WIDTH = 1.0 # if > 1.0, no sb because window is big enough to show all
ICONS = (
    'open', 'cut', 'copy', 'paste', 'print', 'home', 'first', 
    'previous', 'next', 'last', 'search', 'add', 'settings', 
    'note', 'back', 'forward') 

class Treebard():

    def __init__(self, root):
        self.root = root
        self.make_main_canvas()
        self.make_menus()
        self.menus_show = True
        self.root.bind("<KeyPress-F10>", self.make_menus_disappear)

    def make_menus(self):
        self.make_top_menu()
        self.make_icon_menu()

    def make_top_menu(self):
        top_menu = DropdownMenu(self.canvas.menu_frame, self.root, self) 
        top_menu.grid(column=0, row=0)

    def make_icon_menu(self):
        ribbon = {}        
        r = 0
        for name in ICONS:
            file = '{}/images/{}.gif'.format(app_path, name)
            pil_img = Image.open(file)
            tk_img = ImageTk.PhotoImage(pil_img, master=self.canvas)
            icon = ButtonPlain(
                self.canvas.ribbon_frame,
                image=tk_img,
                command=lambda name=name: placeholder(name),
                takefocus=0)
            icon.image = tk_img
            icon.grid(column=r, row=0)
            create_tooltip(icon, name.title())
            ribbon[name] = icon
            r += 1
        
        ribbon['open'].config(command=lambda: open_tree(self))
        ribbon['home'].config(command=self.root.quit)

    def make_menus_disappear(self, evt):
        if self.menus_show is True:
            self.canvas.menu_frame.grid_remove()
            self.canvas.ribbon_frame.grid_remove()
            self.menus_show = False
        else:
            self.canvas.menu_frame.grid()
            self.canvas.ribbon_frame.grid()
            self.menus_show = True

    def make_main_canvas(self):
        self.canvas = Border(
            self.root,
            self.root,
            menubar=True, 
            ribbon_menu=True,
            tree_is_open=0)
        self.canvas.title_1.config(text="Treebard GPS")

    def make_main_window(self):
        '''
            This is delayed till when the current file is known, so it's called 
            in opening.py.
        '''
        self.main = Main(self.canvas, self.root, self)        
        self.main_window = self.canvas.create_window(
            0, 0, anchor='nw', window=self.main)
        self.configure_mousewheel_scrolling()
        conn = sqlite3.connect(global_db_path)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        cur.execute(update_closing_state_tree_is_open)
        conn.commit()
        cur.close()
        conn.close()
        date_prefs = get_date_formats(tree_is_open=1)
        self.canvas.colorize_border()

    def configure_mousewheel_scrolling(self):
        self.scroll_mouse = MousewheelScrolling(self.root, self.canvas)
        self.scroll_mouse.append_to_list([self.canvas, self.main])
        self.scroll_mouse.configure_mousewheel_scrolling(in_root=True)

def start():

    root = tk.Tk()
    root.geometry('+75+10')
    root.iconbitmap(default='{}favicon.ico'.format(app_path))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.maxsize(
        width=int(MAX_WINDOW_WIDTH * screen_width), 
        height=int(MAX_WINDOW_HEIGHT * screen_height))
    treebard = Treebard(root)
    config_generic(root)
    splash = SplashScreen(root, treebard)
    splash.open_treebard(treebard.make_main_window)  
    root.mainloop()

if __name__ == '__main__':
    start()


# DO LIST

# BRANCH: kin

# FIRST STEP IS TO REMOVE THE NUKES AREA CODE TO ITS OWN MODULE
# Then put all spouses in nukes dict

# add all marital events to partner dict
# Add partners to table who have no children with current_person (based on marital events); if partner has children ignore the marriage except to use the date (or even divorce date) in ordering broods in the nuke table; instead of labeling "mother of children" use kin_type eg "spouse"
# update partner: when edited/deleted, the marital events all have to reflect the change
# give james a 3rd brood to see if the vert sb appears
# update_child
# ADD PARTNER/ADD CHILD buttons & entry
# move queries to module and delete import strings for unused queries
# rename queries not named acc to standard eg select_person_id_finding
# add error messages for these cases: mother and father same person, mother & father same gender (msg: Anyone can marry anyone but biological parents are usually M or F, for exceptional cases use other or unknown instead of m or f)
# if the nuke_table is small, there's too much space above & below the top_pic. What if top_pic had rowspan=2? 
# something keeps setting current person in db to null, maybe when starting to open app but cancel w/out going past opening dialog THIS IS CAUSED BY CLICKING CTRL+S
# opening default color on alternate openings when using File > Close > Exit menu commands
# when clicking into an autofill and tabbing on from there, it highlights as expected, but when tabbing into an autofill from the picture, none of them highlight so you can't tell what's in focus. More importantly than highlighting, the insert cursor isn't visible either unless you click into the entry. UPDATE: ACTUALLY THE PROBLEM ISN'T AS STATED ABOVE. The problem is that you tab through the widgets once and they register everything but don't show that they're focused. Then you tab through them all again and they work right. Both times they get their events so it's not a matter of a double set of widgets with one on top of the other, because the widget count is 28 which is one set and if they were gridded atop each other, only the top widgets would get events. The problem is solved by commenting `self.findings_table.redraw()` line 300 main.py which brings back the problem described in the comment there. Using CTRL+S to redraw manually does not cause the problem described there so will do that for now.
# new kin person Input will be parsed to use existing person if # and create new person if not. make it impossible to add a child who is already a child or a partner who is already a partner, but it is possible to add a partner who is already a child or to add a child who is already a partner. It is also possible to add someone with a name that already exists in the table, just not an id
# make it possible to change name, gender or date here & save in db; make it possible to unlink a person from the family by deleting their name from the table
# Add to after death event types in default, default_untouched, and sample db's: autopsy, inquest.
# see `if length == 2` in get_any_name_with_id() in names.py: this was just added and before that a similar process was done repeatedly in various places such as current_person display, wherever a name might need to be shown. Everything still works but this procedure should be deleted from where it's no longer needed since it's been added to get_any_name_with_id()
# getting this error sometimes when changing current person eg input `#1`:
# Exception in Tkinter callback
# Traceback (most recent call last):
  # File "C:\Users\Lutherman\AppData\Local\Programs\Python\Python39\lib\tkinter\__init__.py", line 1884, in __call__
    # return self.func(*args)
  # File "D:\treebard_gps\app\python\autofill.py", line 73, in get_typed
    # do_it()
  # File "D:\treebard_gps\app\python\autofill.py", line 66, in do_it
    # self.show_hits(hits, self.pos)
# AttributeError: 'EntryAutoHilited' object has no attribute 'pos'
# find all the usages of queries that have to be run twice to deal with columns that can be used either of 2 ways such as parent_id1/parent_id2 and rewrite the code so that the whole record is gotten once with select * (or as much as will be needed) and parse the record with python, assign values according to obvious correspondences
# dump the sample db so repo will get the right stuff
# put padding around attributes table
# delete unused imports main.py
# statustips rcm

# BRANCH: names_images
# Redo names tab so it's about names, not making a new person. Two menus should be able to open the new person dialog to create a new person. The names tab should have the table of names but maybe not all the new person stuff.
# In save_new_name() in names.py, have to indicate whether the image is supposed to be main_image (1) vs (0). 1 is now the default in the insert query (insert_images_elements) to images_elements, which makes the new person's image display correctly for now; if it's made main and there's already a main_image the main has to be changed to 0 programmatically.
# Don't let a default image be entered (see new person dialog) if a non-default image already exists for that person. If the person already has a default image, it can be changed to a different default image, a real image, or to no image.
# If user selects his own photo as default, prepend "default_image_" to user's file name.
# If no main_image has been input to db, Treebard will use no image or default image selected by user. User can make settings in images/prefs tab so that one photo is used as default for all when no pic or can select one for F and one for M, one for places, one for sources. Treebard will provide defaults which user can change. There's no reason to input a default_image_ placeholder image as anything but a main_image so make it impossible.

# BRANCH: dialogs
# Refactor gallery so all work the same in a dialog opened by clicking a main image in a tab. Also I found out when I deleted all the padding that there's no scridth. There should be nothing in any tab that's ever bigger than the persons tab events table. Then the tabs could be used for what they're needed for, like searching and getting details about links and stuff, instead of looking at pictures that don't fit in the tab anyway.
# In main.py make_widgets() should be broken up into smaller funx eg make_family_table() etc. after restructing gallery into 3 dialogs.
# Did I forget to replace open_input_message and open_input_message2 with InputMessage? See opening.py, files.py, dropdown.py, I thought the new class was supposed to replace all these as was done apparently already in dates.py. I thought the new class was made so these three overlapping large functions could be deleted from messages.py as well as the radio input message which hasn't even been tested.
# Get rid of all calls to title() in dropdown.py and just give the values with caps as they should be shown, for example title() is changing GEDCOM to Gedcom in File menu.
# In the File menu items add an item "Restore Sample Tree to Original State" and have it grayed out if the sample tree is not actually open.
# Add to Search dlg: checkbox "Speed Up Search" with tooltip "Search will begin after three characters are typed. Don't select this for number searches." Select it by default.
# All dialogs: run the custom dialog closing code when clicking X on title bar.
# Add to do list for new_event dialog: add person search button.
# In notes dialog, if a non-unique topic is entered, there should be an error message, currently there's a SQLite error which locks the database.

# BRANCH: sources
# IDEA for copy/pasting citations. This is still tedious and uncertain because you sometimes don't remember what's in a clipboard till you try pasting it. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, like a plus sign, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys. If this idea isn't practical, it still leads to the notion of a tabular display of citations which would make copy & paste very easy instead of showing individual citations on nearly empty dialogs that you have to sift through looking for the right one, and seeing them all together might be useful for the sake of comparison.
# Edit official do list and move to directory /etc/, edit ReadMe, re-dump 2 databases to .sql files.
# Website: change "units of genealogy" to "elements of genealogy", add FAQ to Treebard Topics.
# Get rid of the quote marks in the rcm messages, just use one long line per message.
# Post new screenshots and announce next phase (export GEDCOM?).

# BRANCH: after_refactor
# install virtual machine and linux
# Export GEDCOM.
# Make sure there's a way to make new person, new name, new place, new source, citation, etc. for all elements and types.
# Add functionality to places, sources, names tabs for alias and edit/delete. 
# Refactor date calculator, give it a menu command to open it. Other tools eg: old census tool like my spreadsheet with templates of all the pre-1850 US census and a way to make your own templates for other census such as state census where household members are listed roughly by age/gender but without names.
# Add widgets and storage for all the tabs.
# Add a menu item to open treebard.com.
# Menu: add functionality to menu choices.
# Combobox: when scrolling if the mouse strays off the scrollbar the dropdown undrops, I've seen a way to fix that but what was it?
# Links tab: start with making a way to link any note to any element.
# Files: when new empty tree is made, "name unknown" is a person in the db autofill list should not include this, search should not include this.

# ADD TO MAIN DO LIST:
# nuke area on Person Tab: remove scrollbars & canvas & window if the hideable ones never appear, it seems they might not be necessary.

# DEV DOCS:
# Files: remember to close the root with the X on the title bar or the close button. If you close the app by closing the X on the terminal, set_closing() will not run.

# USER DOCS:
'''
    We can use gender only to define whether a parent of a child is a 
    mother or a father since we are referring to biological roles.
    Treebard doesn't care about sexual preferences or whether a mother
    and father of children are married or not. Unlike other programs,
    Treebard doesn't automatically use words like 'spouse' when two
    people have children together. The user has a choice of kin_types
    and we refer to members of a couple according to the user's wishes.
'''


 
