# treebard_root_020.py

# _19 was doing well but then I realized that because of not using the Windows border, the app doesn't get an icon on the taskbar. So restructuring again. Keep it the same (Treebard class is not a widget) but add a new pseudo-root, a Toplevel widget called view which is what's actually seen. The flyout image for the Windows taskbar on hover is an image on the real root. The root has the windows taskbar and that flyout image, nothing else. The pseudo-root has all the capabilities of root and follows the root when withdrawn or deiconified.

# Also in this restructuring I want to pay more attention to providing easy reference to base classes such as root, treebard, view, main, etc as the various parts are added. I want to pass basic references and never go master.master.master to get what I want.

# To avoid confusion I will change "root" to "icon" and use "view" for the new root, the visible app. So the Tk instance will now be called "icon" because that's what it's being used for.

import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from files import project_path
from window_border import Border
from scrolling import MousewheelScrolling
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
    def __init__(self, view):
        self.view = view
        self.make_main_canvas_and_border()
        self.configure_mousewheel_scrolling()

    def make_main_canvas_and_border(self):
        self.canvas = Border(
            self.view, 
            size=11, 
            menubar=True, 
            ribbon_menu=True)
        self.main = Main(self.canvas, self.view, self)
        self.canvas.create_window(0, 0, anchor='nw', window=self.main)

    def configure_mousewheel_scrolling(self):
        self.scroll_mouse = MousewheelScrolling(self.view, self.canvas)
        self.scroll_mouse.append_to_list([self.canvas, self.main])
        self.scroll_mouse.configure_mousewheel_scrolling(in_root=True)

def main():

    def withdraw_new_root(event): 
        view.withdraw()

    def show_new_root(event): 
        view.deiconify()

    def make_taskbar_flyout_image():
        width = 600
        height = 300
        flyout_pic_file = '{}images/minstrels_o_beverley_16th_cent_england.gif'.format(
            project_path)
        # flyout_pic_file = 'images/minstrels_o_beverley_16th_cent_england.gif'
        pil_img = Image.open(flyout_pic_file)
        tk_img = ImageTk.PhotoImage(pil_img)
        flyout_canvas = tk.Canvas(icon, height=height, width=width)
        flyout_canvas.create_image(0, 0, anchor='nw', image=tk_img)
        flyout_canvas.grid()
        flyout_canvas.image = tk_img

    def configure_root():
        icon.title('Treebard GPS')
        # set size to size of image and move off screen
        icon.geometry('600x300+-2500+0')
        icon.focus_set() # so one click on taskbar icon gets result
        icon.attributes("-alpha", 0.0)
        icon.iconbitmap(default='{}favicon.ico'.format(project_path)) 
        icon.bind("<Unmap>", withdraw_new_root)
        icon.bind("<Map>", show_new_root)

    icon = tk.Tk()

    view = tk.Toplevel(icon, name='view')
    view.geometry('+0+0')
    view.overrideredirect(1)

    Treebard(view)

    make_taskbar_flyout_image()
    configure_root()

    icon.mainloop()

if __name__ == '__main__':
    main()

