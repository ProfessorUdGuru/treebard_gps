# treebard_root_021.py

# _20 replaced root with icon which was used only for a taskbar icon, and view which became the new root but was really an ordinary toplevel. It worked but it was too much trouble for too little wonderfulness so I will roll this back to the normal root way of doing things. Also planning to move all the Toykinter widgets out of widgets.py into another module toykinter_widgets.py and manually compare and synchronize them with the toykinter modules which are now ahead of these, having been just now used together in a demo app so there have been lots of changes to make them work. Also planning to get rid of all ttk widgets now, having proved it can be done.         # NESTED_PLACES HAS TO BE REFACTORED SO THAT ONLY THE PRIMARY NESTING
        #   IS STORED IN THE DATABASE AND THE OTHERS ARE COMPUTED BY PYTHON AS NEEDED.
        #   BETTER YET: STORE ONLY THE PAIRS AND ELIMINATE NESTED PLACES TABLE. SINCE
        #   THE NESTINGS ARE COMPUTED FROM THE PAIRS, STORING THEM AT ALL IS WRONG 
        #   BECAUSE THEY'RE ONLY NEEDED IN THE GUI AND NOT USED TO PERFORM ANY LOGIC,
        #   SO THEY SHOULD BE COMPUTED ON THE FLY FOR THE AUTOFILLS TO USE.

import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from files import project_path
from window_border import Border
from scrolling import MousewheelScrolling
from styles import config_generic, make_formats_dict
from main import Main
from widgets import Toplevel
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
               |         |                           
               treebard_root_020                                            
                                                       
                    
'''         

class Treebard():

    def __init__(self, root):
        self.root = root
        self.make_main_canvas_and_border()
        self.configure_mousewheel_scrolling()

    def make_main_canvas_and_border(self):
        self.canvas = Border(
            self.root, 
            size=4, # use 3, 4, 7, or 11
            menubar=True, 
            ribbon_menu=True)
        self.main = Main(self.canvas, self.root, self)
        self.canvas.create_window(0, 0, anchor='nw', window=self.main)

    def configure_mousewheel_scrolling(self):
        self.scroll_mouse = MousewheelScrolling(self.root, self.canvas)
        self.scroll_mouse.append_to_list([self.canvas, self.main])
        self.scroll_mouse.configure_mousewheel_scrolling(in_root=True)

def main():

    root = tk.Tk()

    root.geometry('+100+50')
    root.overrideredirect(1)
    root.iconbitmap(default='{}favicon.ico'.format(project_path)) 
    Treebard(root)

    config_generic(root)

    root.mainloop()


    # def __init__(self, view):
        # self.view = view
        # self.make_main_canvas_and_border()
        # self.configure_mousewheel_scrolling()

    # def make_main_canvas_and_border(self):
        # self.canvas = Border(
            # self.view, 
            # size=11, 
            # menubar=True, 
            # ribbon_menu=True)
        # self.main = Main(self.canvas, self.view, self)
        # self.canvas.create_window(0, 0, anchor='nw', window=self.main)

    # def configure_mousewheel_scrolling(self):
        # self.scroll_mouse = MousewheelScrolling(self.view, self.canvas)
        # self.scroll_mouse.append_to_list([self.canvas, self.main])
        # self.scroll_mouse.configure_mousewheel_scrolling(in_root=True)

# def main():

    # def withdraw_new_root(event): 
        # view.withdraw()

    # def show_new_root(event): 
        # view.deiconify()

    # def make_taskbar_flyout_image():
        # width = 600
        # height = 300
        # flyout_pic_file = '{}images/minstrels_o_beverley_16th_cent_england.gif'.format(
            # project_path)
        # # flyout_pic_file = 'images/minstrels_o_beverley_16th_cent_england.gif'
        # pil_img = Image.open(flyout_pic_file)
        # tk_img = ImageTk.PhotoImage(pil_img)
        # flyout_canvas = tk.Canvas(icon, height=height, width=width)
        # flyout_canvas.create_image(0, 0, anchor='nw', image=tk_img)
        # flyout_canvas.grid()
        # flyout_canvas.image = tk_img

    # def configure_root():
        # icon.title('Treebard GPS')
        # # set size to size of image and move off screen
        # icon.geometry('600x300+-2500+0')
        # icon.focus_set() # so one click on taskbar icon gets result
        # icon.attributes("-alpha", 0.0)
        # icon.iconbitmap(default='{}favicon.ico'.format(project_path)) 
        # icon.bind("<Unmap>", withdraw_new_root)
        # icon.bind("<Map>", show_new_root)

    # icon = tk.Tk()

    # view = tk.Toplevel(icon, name='view')
    # view.geometry('+0+0')
    # view.overrideredirect(1)

    # Treebard(view)

    # make_taskbar_flyout_image()
    # configure_root()

    # icon.mainloop()

if __name__ == '__main__':
    main()

