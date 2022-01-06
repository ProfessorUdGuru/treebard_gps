# treebard_root_024.py

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

        self.formats = make_formats_dict(tree_is_open=False)
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
            self.formats,
            menubar=True, 
            ribbon_menu=True,
            # tree_is_open=0
)
        self.canvas.title_1.config(text="Treebard GPS")

    def make_main_window(self):
        '''
            This is delayed till when the current file is known, so it's called 
            in opening.py. So for example, passing a reference to the Treebard
            instance via Main might not work before Treebard has been
            instantiated, e.g. see `treebard.scroll_mouse...` below which had
            to be called last.
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
        self.formats = make_formats_dict()

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
    splash = SplashScreen(root, treebard)
    splash.open_treebard(treebard.make_main_window)
    # Manually closing the opening dialog throws an error re: scroll_mouse. This     
    #   error was solved everywhere else by placing these lines of code last.
    try:
        treebard.scroll_mouse.append_to_list(
            treebard.main.nuke_table.nuke_canvas, resizable=False)
        treebard.scroll_mouse.configure_mousewheel_scrolling(in_root=True)
    except AttributeError:
        pass
 
    config_generic(root)
    root.mainloop()

if __name__ == '__main__':
    start()


# DO LIST

# BRANCH: kin

# The new color entries shd use input font not output font. The explainers font shd change size when everything else does.
# There shd be spacer rows (frames w/columnspan=2) above and below the new color inputs and explainers and only the spacers shd expand in case of big font. 
# edit rcm & statustips
# APPLY and test all
# copy color_scheme table to default .db X2
# center content in prefs tabs
# get rid of tree_is_open and the relevant column in treebard.db, see get_opening_settings() in styles.py
# retest edit/delete mother/father
# update partner: when edited/deleted, the marital events all have to reflect the change
# update_child on edit/delete, make sure offspring events reflect the change
# ADD PARTNER/ADD CHILD buttons & entry
# move queries to module and delete import strings for unused queries
# rename queries not named acc to standard eg select_person_id_finding
# add error messages for these cases: mother and father same person, mother & father same gender (msg: Anyone can marry anyone but biological parents are usually M or F, for exceptional cases use other or unknown instead of m or f)
# if the nuke_table is small, there's too much space above & below the top_pic. What if top_pic had rowspan=2?
# new kin person Input will be parsed to use existing person if # and create new person if not. make it impossible to add a child who is already a child or a partner who is already a partner, but it is possible to add a partner who is already a child or to add a child who is already a partner. It is also possible to add someone with a name that already exists in the table, just not an id
# make it possible to change name, gender or date here & save in db; make it possible to unlink a person from the family by deleting their name from the table
# Add to after death event types in default, default_untouched, and sample db's: autopsy, inquest.
# see `if length == 2` in get_any_name_with_id() in names.py: this was just added and before that a similar process was done repeatedly in various places such as current_person display, wherever a name might need to be shown. Everything still works but this procedure should be deleted from where it's no longer needed since it's been added to get_any_name_with_id()
# Did I forget to replace open_input_message and open_input_message2 with InputMessage? See opening.py, files.py, dropdown.py, I thought the new class was supposed to replace all these as was done apparently already in dates.py. I thought the new class was made so these three overlapping large functions could be deleted from messages.py as well as the radio input message which hasn't even been tested.
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
# make a custom tab traversal list so order is current person area, gallery, new event area, nukes table, events table
# statustips rcm

# BRANCH: names_images
# Redo names tab so it's about names, not making a new person. Two menus should be able to open the new person dialog to create a new person. The names tab should have the table of names but maybe not all the new person stuff.
# In save_new_name() in names.py, have to indicate whether the image is supposed to be main_image (1) vs (0). 1 is now the default in the insert query (insert_images_elements) to images_elements, which makes the new person's image display correctly for now; if it's made main and there's already a main_image the main has to be changed to 0 programmatically.
# Don't let a default image be entered (see new person dialog) if a non-default image already exists for that person. If the person already has a default image, it can be changed to a different default image, a real image, or to no image.
# If user selects his own photo as default, prepend "default_image_" to user's file name.
# If no main_image has been input to db, Treebard will use no image or default image selected by user. User can make settings in images/prefs tab so that one photo is used as default for all when no pic or can select one for F and one for M, one for places, one for sources. Treebard will provide defaults which user can change. There's no reason to input a default_image_ placeholder image as anything but a main_image so make it impossible.

# BRANCH: dialogs
# in each tab of each tabbook, use Map event to focus one of the widgets on that tab when that tab is switched to, see colorizer arrow_in_first() as an example
# Refactor gallery so all work the same in a dialog opened by clicking a main image in a tab. Also I found out when I deleted all the padding that there's no scridth. There should be nothing in any tab that's ever bigger than the persons tab events table. Then the tabs could be used for what they're needed for, like searching and getting details about links and stuff, instead of looking at pictures that don't fit in the tab anyway.
# In main.py make_widgets() should be broken up into smaller funx eg make_family_table() etc. after restructing gallery into 3 dialogs.
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
# colorizer: get Tab traversal to trigger autoscroll when going from a visible to a non-visible row. Already works for arrow traversal.
# colorizer: swatch_canvas: adding to mousewheel scrolling doesn't work

# DEV DOCS:
# Files: remember to close the root with the X on the title bar or the close button. If you close the app by closing the X on the terminal, set_closing() will not run.
# Colorizer: 
'''
    Re: `yview_moveto` using only two settings (0.0 or 1.0) for
    "auto-scrolled all the way up" or all the way down. The user
    can scroll manually to any increment, but when traversing
    the schemes with the arrow keys, the scrolling is automatic
    so the user doesn't have to grab the mouse. This feature is
    currently limited to either all up or all down.

    To accomodate a lot more color schemes than the 60-plus that
    I've already tested with the auto-scrolling feature, it
    would be necessary to use positions between the 0.0 and 1.0
    currently being used. As it is now, the user is limited to 
    two pages of swatches, three rows each. Unless the size of the
    canvas is increased to four rows of swatches per page; then it 
    would be two pages of swatches, four rows each. 

    See the scrollbar in the custom_combobox_widget.py for an 
    example of proportional autoscrolling being done
    with the Toykinter scrollbar, but who needs that many color
    schemes anyway? Especially since any and all of the built-in
    color schemes could be hidden, then the user could make his
    own dozens of schemes. And actually, there's no real limit to
    how many schemes there can be, if the user doesn't mind
    manually scrolling when there are more than six rows of
    swatches. Seems like this is already overkill, who needs
    more than 84 color schemes (6 rows of 14 each)? 

    Anyway, the `get()` method for the scrollbar should work for
    doing something with intermediate scrollbar positions. The method
    has been started in the Colorizer class but should be moved to the
    Scrollbar class in scrolling.py.
'''

# USER DOCS: policies:
'''
    We can use gender only to define whether a parent of a child is a 
    mother or a father since we are referring to biological roles.
    Treebard doesn't care about sexual preferences or whether a mother
    and father of children are married or not. Unlike other programs,
    Treebard doesn't automatically use words like 'spouse' when two
    people have children together. The user has a choice of kin_types
    and we refer to members of a couple according to the user's wishes.
'''





 
