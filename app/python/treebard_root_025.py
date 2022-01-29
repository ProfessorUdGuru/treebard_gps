# treebard_root_025.py

# Up till now I didn't realize I had no way to differentiate, in findings_persons, one couple from another, if one of the partners was unknown. Say for example James has two records of an offspring event with null partners in each. We don't know if the two children are siblings but Treebard will assume they are since the 2 partners are both null. The reason I changed from having a person_id column in findings_persons, and a separate record for each of the partners in a couple, was that I needed a single row for both persons. But it has been a real pain to write the logic, since I have to check both partners and parse order 1_2 or 2_1 etc. Now I find it isn't even capable of doing what needs to be done, so have to change the structure again. Instead of a person_id1 and person_id2 column in findings_persons, there has to be a single FK for a person_person table wherein each couple will have a single row and single ID. This will solve all my problems except now I have to rewrite all the code that tried to deal with findings_persons, so have saved a copy of the existing files up to now and will rewrite all that code now after creating the new table and fixing findings_persons table.

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



"""
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
                                                        
                    
"""




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

        self.formats = make_formats_dict()
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
 
# NEXT STEP IS TO WRITE CODE FOR THE ADD PARTNER/ADD CHILD BUTTONS.
# double click to change curr per
# if gender is "other" don't display it in child table
# make it possible to change gender, birth/death dates for children right there in the table
# ADD PARTNER/ADD CHILD buttons & entry
# pressing enter in person autofill on person tab after name fills in throws an error re: colors
# ADD/FIND button doesn't work
# move queries to module and delete import strings for unused queries
# rename queries not named acc to standard eg select_person_id_finding
# add error messages for these cases: mother and father same person, mother & father same gender (msg: Anyone can marry anyone but biological parents are usually M or F, for exceptional cases use other or unknown instead of m or f)
# if the nuke_table is small, there's too much space above & below the top_pic. What if top_pic had rowspan=2?
# new kin person Input will be parsed to use existing person if # and create new person if not. make it impossible to add a child who is already a child or a partner who is already a partner, but it is possible to add a partner who is already a child or to add a child who is already a partner. It is also possible to add someone with a name that already exists in the table, just not an id
# make it possible to change name, gender or date here & save in db; make it possible to unlink a person from the family by deleting their name from the table
# the left margin of the child table should not vary depending on row widths. Compare James with Fannie, Fannie looks terrible bec her child has a short name and no dates. Fix Fannie to start at a left margin and James should then start at the same left margin.
# Add to after death event types in default, default_untouched, and sample db's: autopsy, inquest.
# see `if length == 2` in get_any_name_with_id() in names.py: this was just added and before that a similar process was done repeatedly in various places such as current_person display, wherever a name might need to be shown. Everything still works but this procedure should be deleted from where it's no longer needed since it's been added to get_any_name_with_id()
# Did I forget to replace open_input_message and open_input_message2 with InputMessage? See opening.py, files.py, dropdown.py, I thought the new class was supposed to replace all these as was done apparently already in dates.py. I thought the new class was made so these three overlapping large functions could be deleted from messages.py as well as the radio input message which hasn't even been tested.
# getting this error sometimes when changing current person w/ id, as soon as # is typed:
# Exception in Tkinter callback
# Traceback (most recent call last):
  # File "C:\Users\Lutherman\AppData\Local\Programs\Python\Python39\lib\tkinter\__init__.py", line 1884, in __call__
    # return self.func(*args)
  # File "D:\treebard_gps\app\python\autofill.py", line 73, in get_typed
    # do_it()
  # File "D:\treebard_gps\app\python\autofill.py", line 66, in do_it
    # self.show_hits(hits, self.pos)
# AttributeError: 'EntryAutoHilited' object has no attribute 'pos'
# colorizer: if click copy then immed click apply, error (pass? return?) Happens bec no scheme, so deal with if no scheme hilit, apply shd do nothing
# find all the usages of queries that have to be run twice to deal with columns that can be used either of 2 ways such as parent_id1/parent_id2 and rewrite the code so that the whole record is gotten once with select * (or as much as will be needed) and parse the record with python, assign values according to obvious correspondences
# dump the sample db so repo will get the right stuff
# put padding around attributes table
# delete unused imports main.py
# make a custom tab traversal list so order is current person area, gallery, new event area, nukes table, events table
# statustips rcm also for unlinker
# RCM: Current Person Tab: Nuclear Family Table: This table shows the current person's parents, spouses and other marital partners, and biological children. The partners are all shown at the same time, along with any children that they had with the current person, so there's a scrollbar in case there are a lot of spouses and/or children. To change an existing partner who is a parent of some of the current person's children, just change what's in the table by typing a different name. The name you're looking for will fill in, along with the person's ID number, if the person is already in the tree. If not, a dialog will open so you can add the person to the tree and to the family. In either case, the previous parent/partner will now have his/her own row in the family table, if any marital events such as wedding, marriage, divorce, etc. were shared by the current person and his/her partner, to indicate that they were partners. The terminology used to input the partner, such as "spouse", "wife", "partner", etc. will be used instead of "mother/father of children". The various partners will be sorted in the family table by approximate date, using dates of marital events and dates of children's births to arrange the table chronologically as closely as possible.\n\nTo delete a partner, just delete them. If they have children with the current person, the children's names will remain, and the input for the missing parent will be blank. The deleted parent will not be deleted from the tree, but will be unlinked from the children. If the person has one or more marital events with the current person, he/she will have his own row in the family table.
""" Redo all docstrings everywhere to look
    like this.
"""

# BRANCH: dates

# clarify_year might not working in dates.py, there is a chain of error messages, sometimes it has to be OK'd twice, and make sure it doesn't run on CANCEL and original value is returned to the input (InputMessage works now in notes.py and families.py for a model). Currently cancel seems to be deleting the date which moves the event to the attributes table. The second time it sort of works but deletes the number that's not a year. It also doesn't display AD on years less than 4 digits long.

# BRANCH: types

# This started when I found I'd failed to stop using the formats table for default_formats, led to the realization that the formats table needs to go away, led to a grand new structure using the fact that I now have a global db again so might as well use it. Below it says to store an fk for color scheme but to do that right, color scheme table needs to be moved to treebard.db. So will keep using formats for fonts and current color scheme only till I get to this branch, since I have no other place to put them.
# get rid of get_current_formats() in styles.py
# get rid of tree_is_open column in treebard.db, see get_opening_settings() in styles.py which now has a get_opening_settings_default() which is not being used instead of the boolean which was not being used anymore. It should be used to open the bare app w/out a tree but apparently this is already being done somehow, not shure why it's working, whether I planned it that way or it just happened by accident. Look in opening.py and trace the code flow to see what's going on. Right now it's opening in the sample_tree current color scheme but not sure why.
# What about putting color_schemes in treebard.db where it belongs? As well as all the other types? And places? How about making all these changes into a new branch to be started when kin is finished?
# first get rid of all refs to the format table ie: 
#   (update_format_color_scheme has to be changed to current see lines 17 & 583 colorizer.py); 
#   (select_default_format_font_size in window_border.py lines 13, 112 has to be changed to the table in treebard.db); 
#   (update_format_font has to be changed to current see font_picker.py lines 7 & 102) 
#   (select_opening_settings has to be changed to treebard.db see styles.py lines 5 & 608);
# Failed to consider that font is also stored in format currently so a current_font_id needs to be stored in current as an fk but there is no table for font_schemes as there is for color schemes, nor should there be. A font scheme is a size and a family. Defaults for both exist in treebard.db already, re: output font. Defaults for input font aren't user changable. So a place is needed for 2 font columns and we don't want a bunch of saved schemes. The solution is to put the 2 columns in current. This leads to another question: what's the difference between current and closing_state? They both have one record. They're both used to open things the same way they were closed. Answer: they're both needed. Closing state is global stuff that applies no matter what tree is open or closed. Current needs a row for each tree. Make a new table in treebard.db called trees and one called current. Each tree will get a pk in trees. Then in closing state, there will be a prior_tree_id fk instead of a text field for prior_tree. Delete the column tree_is_open. In current there will be a record for each tree. So things can open the same way they were closed, without first opening the tree to read its prefs. So when a tree is created or destroyed, its name is added to or deleted from the trees table. Make a new table in treebard.db called current with this schema: current_id PK, tree_id refs tree.tree_id, cols for font size & family, fk col for color_scheme_id
# types tab: have a combobox to change content from one type to another. Start with color schemes. Have a button to delete all hidden schemes (if not built-in).
# drop table format from default.db, etc., copy to untouched.db, make a treebard_untouched.db to keep in app/default also

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
# center content in prefs tabs

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

# USER DOCS: names:
'''
    In Treebard, a person's name is not treated casually. On the current person page,
    you can change the gender, birth date, or death date of a child, but not the
    child's name. You can create a child by adding any name to a blank field, and 
    the same goes for partners and parents of the current person in the immediate
    family table. Once a name has been added to the field, in order to change
    the name, you can make that person the current person by double-clicking the
    name or by using the top field labeled "Change Current Person".

    Names input are assigned the "birth name" type by default, but you can change
    this while adding the person or at any later time, in the names tab for the
    current person. If you don't know the person's birth name but have another 
    name such as an alias, pseudonym, nickname, married name, etc., you can enter
    this name and register it properly as a name type other than "birth name". So
    if you change the current person to this person, the name will be followed by
    the name type in parentheses. For example, if you know Jo Jones' married name
    but not her maiden name, you can enter the married name and it will be displayed
    as "Jo Jones (married name)". As soon as you find her birth name, it will change
    to "Josephine Hendrickson".

    This helps in the case where you might be tempted to name someone "unknown" so
    you can keep track of known information about the person when you have no inkling
    of a name. You know she was born in Iceland but what do you call her, so you can
    create a person and note her birth place? The problem with calling her "unknown"
    is that someone who doesn't know much English might think that's her actual name.
    But Treebard has name types and displays them when there's no birth name. So in a
    case like this, you can add the person, add some obviously non-name characters
    such as "_____ _____", or "???", or "-----", or "xxxxxxxxx", and the Treebard will
    display the name type along with the non-name as such: "_____ _____ (unknown name)".

    Characters not allowed in a person's name: parentheses, pound sign (#).
'''





 
