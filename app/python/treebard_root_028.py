# treebard_root_028.py

# retiring _027 to 1) consolidate various stray collections back into a single family_data dict (again) and 2) refactor the way name strings are displayed, stored and parsed.

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
    #   error was prevented everywhere else by placing these lines of code last.
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

# BRANCH: names_refactor
# export the dbs

# BRANCH: families_table
# Keep the UI and start the code from scratch. Here are the new goals.
    # 1) Parents and alt parents work the same, parameterized. Parents and partners and children work the same, parameterized. There is one method for all. 
    # 2) Since all the pertinent inputs are for names, they all work the same. An initial and final value are compared on FocusIn/FocusOut. Upon focus out, the final input is classified based on whether existing, dupe, new, or unlink is called for. All the if/else is done in one place, not inside the main procedure, then a single procedure is used for every name.
    # 3) The data dict works the same for parents, alt parents, partners, and children. For example, there can be more than one set of alt parents, but that doesn't mean the bio parents shd work differently just because there's only one pair of them. There shd not be all these differnt sections of the dict. They are all names, all people, all have a name and an ID, a name type, etc. So just add another key as to whether they are parents, foster parents, partners, or children of the current person. Put all the person dicts in the same list or dict and sort them by category, then within each category sort them by date. The 2 main categories are parents and families. Each person has a key for their relationship to the current person. Then the list is built in this order: Father, mother, alt parents in order of related event dates, partners, children.
    # 4) Each person will have an event date key which is a sorter for partners and children. For partners, it's a marital event. For children, it's a birth event.
    # 5) A null person id will be treated the same in all cases. 
    # 6) Create the table in a separate model space, leaving the families.py module intact till the code is ready to plug into it.
    # 7) Nametips will be created for use in family table since this is where most of the names are, and extended to other places that they're used such as roles dialog.
#                     PARENTS       ALT PARENTS    PARTNERS        CHILDREN
# NONE>EXISTING          X              X             X
# NONE>DUPE              X              X             X
# NONE>NEW               
# CHANGE>EXISTING        X              X             X
# CHANGE>DUPE            X              X
# CHANGE>NEW             X              X
# UNLINK                 X              X             X
# Keep the existing design (?) and get rid of the code. Start from scratch, use the table above to test each functionality. When one is fixed check all prior to make sure they have not been broken. Start with a complete dict of all needed data that will not have to be patched or appended to. Make every input work the same (just tab out; if ok no problem, if not ok or validation needed, open a dialog). Everything has to work the same. Keep the dupe dialog and unlink dialog, they work, keep the design of the table, but discard the code and start fresh. Try to make the queries as complex as the situation so nothing will have to be thought of and added later.
# get rid of dkt["order"] in the nukes table dict if it's not being used anywhere
# get rid of "nukes, nuke, nuclear" and replace with "nukefam"
# when add alt parent & tab out, focus goes not to next widg in tab order. What worked for parent fields didn't work here.
# after clicking one of the partner radios, the bottom radio at the input doesn't work anymore
# if no partners, both buttons are active and the single radio button is not selected, both of which are wrong
# consolidate various stray collections back into a single family_data dict (again) 
# adding an existing person as father works but adding an existing person as mother opens PersonAdd wrongly unless it's the first thing you do; vice versa (switch father and mother above)
# after checkbutton dlg works for deleting offspring, make sure it works for alt birth children
# see `# WHAT ABOUT ALSO GETTING OFFSPRING/ALT BIRTH EVENTS HERE?`  2) make the list checks a list of dicts with a dict for events and a dict for children; 3) when making the dlg, put events at top and children below, not mixed up POINT BEING IF YOU CAN UNLINK EVENTS INDIVIDUALLY YOU HAVE TO BE ABLE TO UNLINK CHILDREN TOO BECAUSE THESE ARE THE 2 THINGS THAT GET PARTNERS INTO THE FAMILY TABLE
# adding james to melodie's father input doesn't work; if you don't restart the app, the add father is then broken for all, ie it opens add person dialog when trying to add existing person as father; the latter problem will probably be fixed automatically when the former one is fixed.
# if you delete an existing parent of child, 1) unlink dlg opens w/out checks and 2) if you click cancel it unlinks but should not. It's expected that this should do something since it works for childless partners linked only by marital events. Solution is to deal with children unlinking same as event unlinking on same dlg see above.
# make a functionality for adding or changing one of the partners in a couple event; currently there's a way to delete a partner from an event, there's a way to delete an event, there's a way to create a new event, but no way to edit an existing event as to its partners; maybe just double click the event ie label that says 'wedding' to open a dialog (identical to the new event dialog?) wherein the partner can be edited. It has to do everything that could be done in the family table and more.
# "Children's None" should be "Children's Mother" or something, see Wesley Warren...'s partner/child
# still getting "name unknown" on some kintips?
# unlink child on delete
# make it possible to change gender, birth/death dates for children right there in the table
# double click any name in table to change curr per
# make it impossible for a person to be their own parent, partner or child, see Nettie Womble who is her own father
# add error messages for these cases: mother and father same person, mother & father same gender (msg: Anyone can marry anyone but biological parents are usually M or F, for exceptional cases use other or unknown instead of m or f); make it impossible to add a child who is already a child or a partner who is already a partner, but it is possible to add a partner who is already a child or to add a child who is already a partner.
# the left margin of the child table should not vary depending on row widths. Compare James with Fannie, Fannie looks terrible bec her child has a short name and no dates. Fix Fannie to start at a left margin and James should then start at the same left margin.
# add idtips to name inputs in the families table first, then other places except search which already has better name tips
# export dbs to .sql

# BRANCH: cleanup
# When a person is used they aren't being moved to the front of the list. Is this because the list is restarted after every time a new person is made? Don't worry about it if it's not easy to fix, as long as this feature works with places which are much more complicated strings to type out.
# pressing enter in person autofill on person tab after name fills in throws an error re: colors
# ADD/FIND button doesn't work
# move queries to module and delete import strings for unused queries
# rename queries not named acc to standard eg select_person_id_finding
# see `if length == 2` in get_any_name_with_id() in names.py: this was just added and before that a similar process was done repeatedly in various places such as current_person display, wherever a name might need to be shown. Everything still works but this procedure should be deleted from where it's no longer needed since it's been added to get_any_name_with_id()
# Did I forget to replace open_input_message and open_input_message2 with InputMessage? See opening.py, files.py, dropdown.py, I thought the new class was supposed to replace all these as was done apparently already in dates.py. I thought the new class was made so these three overlapping large functions could be deleted from messages.py as well as the radio input message which hasn't even been tested.
# colorizer: if click copy then immed click apply, error (pass? return?) Happens bec no scheme, so deal with if no scheme hilit, apply should do nothing
# find all the usages of queries that have to be run twice to deal with columns that can be used either of 2 ways such as parent_id1/parent_id2 and rewrite the code so that the whole record is gotten once with select * (or as much as will be needed) and parse the record with python, assign values according to obvious correspondences
# delete unused imports all modules
# statustips rcm also for unlinker
""" Redo all docstrings everywhere to look
    like this.
"""
# export dbs to .sql
# fix redraw() so top pic changes on ctrl-s if the main pic was changed w/ radio in gallery

# BRANCH: dates
# clarify_year might not working in dates.py, there is a chain of error messages, sometimes it has to be OK'd twice, and make sure it doesn't run on CANCEL and original value is returned to the input (InputMessage works now in notes.py and families.py for a model). Currently cancel seems to be deleting the date which moves the event to the attributes table. The second time it sort of works but deletes the number that's not a year. It also doesn't display AD on years less than 4 digits long.
# export dbs to .sql

# BRANCH: names_tab
# Redo names tab so it's about names, not making a new person. Two menus should be able to open the new person dialog to create a new person. The names tab should have the table of names but maybe not all the new person stuff.
# In save_new_person() in names.py, have to indicate whether the image is supposed to be main_image (1) vs (0). 1 is now the default in the insert query (insert_images_elements) to images_elements, which makes the new person's image display correctly for now; if it's made main and there's already a main_image the main has to be changed to 0 programmatically.
# Don't let a default image be entered (see new person dialog) if a non-default image already exists for that person. If the person already has a default image, it can be changed to a different default image, a real image, or to no image.
# If user selects his own photo as default, prepend "0_default_image_" to user's file name.
# If no main_image has been input to db, Treebard will use no image or default image selected by user. User can make settings in images/prefs tab so that one photo is used as default for all when no pic or can select one for F and one for M, one for places, one for sources. Treebard will provide defaults which user can change. There's no reason to input a default_image_ placeholder image as anything but a main_image so make it impossible.
# export dbs to .sql

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
# export dbs to .sql

# BRANCH: dialogs
# add another label in each row of roles dialog to show id of role person in case of dupe names
# put a separator btwn events and attributes
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
# notes dialog: can't create a first note when none exist yet for a conclusion because of division by zero error in size_toc(); 20220220 mini-effort to fix this had consequences undealt-with; also re: autocreated kin events like adoption, fosterage, offspring, guardianship: make it possible to add/access/edit roles & notes on offspring/alt_parentage event rows of the events table; SEE "non_empty_roles, non_empty_notes"
# get rid of checkbutton stuff in InputMessage and also radiobutton stuff if not used anywhere
# change default image system instead of prepending 0_ to image names, have a boolean col in image table for the 5 default image male, female, unisex, place, source, and prepend these to the list when sorting; also the hard-coded string `0_default_image_unisex.jpg` needs to be a variable defined by a query instead of being hard-coded in gallery.py and persons.py
# place new/dupes dlg, if CANCEL pressed the orig content is filled in but not if dlg closed with X button
# when autofilling a place in evts table, if the column is narrow due to lack of contents, it will change size every time you type a char which causes the whole table to flash while trying to type. Possibly while typing into the autofill, detect a max length as different places try to fill in, and keep that length until focus out, at which time that length can just be released so the col can resize to its final contents. However, the size will still change each time the max length increases, so better to start with a generous hard-coded max length so this will rarely happen.    
# in main do list change names.py to persons.py
# Can't open an empty notes dlg, division by zero error.
# person search table is messed up. Same person shows for both mother and father. Sorting only works right for ID. Clicking a name to make the person current works but the nukes table is not redrawn.
# export dbs to .sql

# BRANCH: conclusions
# change events_table column 1 to CONCLUSIONS instead of events and fix the code everywhere to make this work right. Should be easy, no restructuring involved. Events is wrong since it's now events & attributes and since there are also events & attributes in the assertions/sources dialog, it is now time to start sticking to Treebard's core philosophy and differentiate between conclusions and assertions at all times. Better to never use terms like events & attributes in a conspicuous place like the first row of the conclusions table. Also change everywhere including docs events table > conclusions table. And the first step is to change the name of the module from events_table.py to conclusions_table.py. Remember that conclusions are called findings in the code; "events" are cases where something like an event_type refers equally to assertions and conclusions (claims & findings) and never use "event" where "finding" should be used.
# export dbs to .sql

# BRANCH: sources
# IDEA for copy/pasting citations. This is still tedious and uncertain because you sometimes don't remember what's in a clipboard till you try pasting it. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, like a plus sign, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys. If this idea isn't practical, it still leads to the notion of a tabular display of citations which would make copy & paste very easy instead of showing individual citations on nearly empty dialogs that you have to sift through looking for the right one, and seeing them all together might be useful for the sake of comparison.
# Edit official do list and move to directory /etc/, edit ReadMe, re-dump 2 databases to .sql files.
# Website: change "units of genealogy" to "elements of genealogy", add FAQ to Treebard Topics.
# Get rid of the quote marks in the rcm messages, just use one long line per message.
# Post new screenshots and announce next phase (export GEDCOM?).
# export dbs to .sql

# BRANCH: after_refactor
# delete extraneous backups and rollbacks from hard drive, keep the backups only
# update the website, add topics eg parents (now including alt parents), change screenshots & code in the forum
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
# export dbs to .sql

# ADD TO MAIN DO LIST:
# nuke area on Person Tab: remove scrollbars & canvas & window if the hideable ones never appear, it seems they might not be necessary.
# colorizer: get Tab traversal to trigger autoscroll when going from a visible to a non-visible row. Already works for arrow traversal.
# colorizer: swatch_canvas: adding to mousewheel scrolling doesn't work
# website topics: add a button at bottom to view all topics on one page, then create the page and upload it, with all topics on one page, this is so search engines will find the text, otherwise it's buried in javascript and can't be searched
# NUKES TABLE on person tab: unhide kintype IDs 3, 26, 27, 28 and make them work same as 1 & 2

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

# USER DOCS: name autofill--using it to input new names
'''
Just type a plus sign in any person input, followed by the new name which can be typed or pasted. The Add Person dialog will open. When it closes, type the name normally and it will autofill.
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

# USER DOCS: names: REWRITE THIS, NO LONGER TRUE, EG CAN'T INPUT NAMES TO BLANK PARTNERS
'''
    In Treebard, a person's name is not treated casually. On the current person page,
    you can change the gender, birth date, or death date of the current person's child, but not the
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

# DEV DOC: GENDER
'''
    Wherever couples are shown together, if gender matters, the male should go on the left and 
    the female on the right. This will be what people expect. This translates to storing male-
    oriented kin types such as father and husband in kin_type_id1 and female kin types
    in kin_type_id2 (re: findings_persons table). The rest of the time, for example in the case of 
    unisex kin types such as "spouse" or "foster parent", or same-gender relationships, 
    Treebard will display each person on the left or right depending on where the user inputs them.
    So if the user wants to store Bob and Jim's relationship, and Jim is input to the left, 
    then his data will be stored as kin_type_id1 in findings_persons and as person_id1 in
    persons_persons. Bob will end up displaying on the right, stored in the _2 columns in the db.
    There is no other way to do this, without writing rules for fluctuating cultural trends
    which are basically none of Treebard's business such as whether or not "wife" and "husband" 
    can be used for same-gender couples. Treebard doesn't care about current or modern trends
    because we don't want to change our code every time a new terminology becomes trendy
    in reference to gender issues. Treebard plans to still be here when these issues are no
    longer issues, 10,000 years from now. So flexibility has to be built into our policies from 
    the start. Flexibility built into the code, not an attitude of waiting for the trends to
    dictate what our next refactoring will look like. The goal is for the code to not generally
    change with the times, because of flexibility being built into the original design. The point
    is that it's up to the coder to make sure that fathers & husbands, etc., go into the _1
    db columns, not by manipulating the user's input with code, but by providing inputs that
    will make it normal for the user to put them in this way. The drawback is that if user
    inputs Marci on the left and Jane on the right, then changes their mind and decides that
    Jane was supposed to occupy the husband role but Treebard is only so compliant, well sorry, 
    it's not my problem. The user will have to solve problems like that, probably by deleting 
    some data and re-entering it.

    Actually this probably doesn't apply to biological parents since fathers and mothers are 
    constrained by code manipulations to
    display on the left and right respectively, but this doesn't extend to adoptive parents,
    for example, so it's better to always put males in the _1 columns and females in the
    _2 columns so as to not be entertaining exceptions in the code design.

    Since there can be gender constraints only in regards to biological father and mother roles,
    the _1 & _2 columns in the db can't be changed to _m & _f. You still have to be able to put
    either gender in either column.
'''

# DEVDOCS: person autofill inputs: 
'''There's a quirk in the system for autofilling names that will rarely if ever show up, and seems to be harmless so far when it shows up in the Change Current Person field at the top of the app, above the tabs section. If you type a "z" and there are only two names--say "Zachary Dupree"--that start with a "z" and both names are exactly the same, the duplicate name chooser will open as soon as you type the "z", asking you to select which Zachary Dupree you wanted. This is fine if you wanted to use Zachary Dupree but not if you wanted to enter Zoe Blankenship for the first time. The glitch is harmless and the workaround is simple. Cancel out of the duplicates dialog, delete EVERTHING BUT THE Z that autofills, and finish typing Zoe's name. Everything will work as expected. This could be "fixed" with several lines of code but it will happen so rarely that Treebard prefers the workaround, which possibly anyone could figure out if they weren't reading this. As soon as there are two differently spelled names in the database--i.e. one other name that starts with a "z" besides the two "Zachary Duprees"--the problem will never occur again when typing a "z". To test this with the sample_tree.tbd file, delete any name starting with a "z" except for the two instances of Zachary somebody, and follow the instructions above. We are confident that this problem will seldom occur and will easily be worked around.
'''
'''
Treebard uses an original-vs.-final-content test to eliminate validating and responding to inputs that haven't changed as the user tabs through them. It also eliminates superfluous dialogs. This works fine in the case where the input empties after use, and in the case where content is programatically inserted and not always changed. But in the case where there's always content inserted programatically and content is generally always going to change, an extra test is needed to detect duplicate names. For example, in the roles dialog, role names can be changed, but if John Smith is changed to a different John Smith, the usual test isn't enough. So in edit autofills, we have to test not only for whether the content has changed, but also if the content hasn't changed, we have to test for whether the final content has duplicates. A change might have been intended. That way, tabbing out of John Smith's edit input will always open a dupe checking dialog. There is a simple workaround, but the user would have to know the ID of the new John Smith and input it like "#5927" instead of inputting "John Smith". Users who happen to remember IDs for duplicate names might be able to use this sometimes, and looking up an ID is easy, but generally the inconvenience of having to look at a simple dialog to clarify which John Smith was meant, each time a role person named John Smith is edited, would be no big deal and would happen rarely.
'''




 
