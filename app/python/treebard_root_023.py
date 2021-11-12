# treebard_root_023.py

# This version is needed because in _022 and preceding, I'd gotten into the habit of opening a hard-coded tree selection. So I wrote a lot of procedures in an order that didn't take into account that this was not how it was going to be done. I have to start over somewhat on the structure, not the structure but when things happen during the opening process, so the user can open the app without opening a tree, and thus still have access to file menu, help menu, tools menu, etc. User format preferences will not go into effect till he opens a specific tree, since user prefs are stored per tree and there will be only one set of formats (the defaults) stored in a separate global database. This version is broken from the start but for a whole version that works, it is stored in treebard_gps_backups/treebard_gps_20211110x. The best way will probably be to start a new model for the restructuring with only a Border, Dropdown, and Icon Menu. Anything else would be haphazard patchwork.

import tkinter as tk
from PIL import Image, ImageTk
from files import app_path, current_file
from dropdown import DropdownMenu, placeholder
from window_border import Border
from opening import SplashScreen
from scrolling import MousewheelScrolling
from styles import config_generic, make_formats_dict
from main import Main
from widgets import Toplevel, Button, Frame, ButtonPlain
from utes import create_tooltip
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
MAX_WINDOW_HEIGHT = 1.0 # if 1.0, sb is available immed
MAX_WINDOW_WIDTH = 1.0 # if > 1.0, no sb bec window is big enuf to show all
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
        top_menu = DropdownMenu(self.canvas.menu_frame, self.root) 
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
        
        ribbon['open'].config(command=lambda: open_tree(self.root))
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
            menubar=True, 
            ribbon_menu=True)
        self.canvas.title_1.config(text="Treebard GPS")
        # self.canvas.title_2.config(text=current_file)

    def make_main_window(self):
        '''
            This is delayed till when the current file is known.
            Currently it's called in opening.py to open the file that was last
            opened.
        '''
        self.main = Main(self.canvas, self.root, self)
        
        self.canvas.create_window(0, 0, anchor='nw', window=self.main)
        self.configure_mousewheel_scrolling()

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
    config_generic(root)
    splash = SplashScreen(root)
    # root.withdraw()# DO NOT DELETE
    treebard = Treebard(root)
    splash.open_treebard(treebard.make_main_window)    

    root.mainloop()

if __name__ == '__main__':
    start()

