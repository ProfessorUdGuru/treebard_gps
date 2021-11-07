# gallery.py (import as gl)

import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from files import current_file, current_dir, current_drive, project_path
from styles import make_formats_dict
from widgets import (
    Frame, Canvas, Button, Label, Radiobutton, 
    LabelH3, MessageCopiable, LabelStay)
from utes import create_tooltip
from names import get_current_person
from query_strings import (
    select_all_place_images, select_all_source_images, 
    select_all_person_images, select_current_person_id, 
    select_current_person_image, update_images_entities_zero,
    update_images_entities_one
)
import dev_tools as dt
from dev_tools import looky, seeline




formats = make_formats_dict()

class Gallery(Frame):

    def __init__(
            self, master, tabbook, 
            graphics_tab, 
            root, canvas,
            current_person_name=None, current_source_name=None, current_place_name=None,
            *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.tabbook = tabbook
        self.graphics_tab = graphics_tab
        self.root = root
        self.canvas = canvas
        if current_person_name:
            self.current_entity_name = current_person_name
        elif current_source_name:
            self.current_entity_name = current_source_name
        elif current_place_name:
            self.current_entity_name = current_place_name
        else:
            print("line", looky(seeline()).lineno, "case_not_handled:")

        # self.graphics_tab = self.tabbook.store['graphics']
        print("line", looky(seeline()).lineno, "self.graphics_tab:", self.graphics_tab)

        self.counter = 0
        self.thumb_labels = []
        self.width_strings = []
        self.height_strings = []

        self.current_person = get_current_person()[0]

        # set_window_max_size(self.master) # *********************************


        pix_data = self.get_current_pix_data()
        if len(pix_data) != 0:
            self.filter_pix_data(pix_data)
            self.make_widgets() 
        elif self.master.winfo_class() == "Toplevel":
            self.master.destroy()

    def make_widgets(self):

        if self.master.winfo_class() == 'Toplevel':
            gallery_canvas = Canvas(
                self.master,
                bd=0,
                highlightthickness=0)

            self.gallery_content = Frame(gallery_canvas)
            gallery_canvas.grid(row=0, column=0, sticky='nsew')

            self.master.grid_columnconfigure(0, weight=1)
            self.master.grid_rowconfigure(0, weight=1)
        else:
            self.gallery_content = Frame(self.master)
            self.gallery_content.grid(column=0, row=0)

        self.thumb_canvas = Canvas(
            self.gallery_content, 
            bd=0, 
            highlightthickness=0,
            bg=formats['bg'])
        self.thumb_canvas.pack(padx=12, pady=12)

        self.thumbstrip = Frame(self.thumb_canvas)
        self.thumbstrip.pack(side='top')

        self.previous_img = Button(self.gallery_content, text='<<', width=6)

        self.pic_canvas = Canvas(
            self.gallery_content, 
            highlightbackground=formats['bg'])
        self.pic_canvas.bind('<Button-1>', self.focus_clicked)
        self.pic_canvas.bind('<Button-1>', self.scroll_start, add='+')
        self.pic_canvas.bind('<B1-Motion>', self.scroll_move)     

        self.img_path = '{}treebard_gps\data\{}\images\{}'.format(
            current_drive, self.image_dir, self.main_pic)
        img_big = Image.open(self.img_path)
        self.tk_img = ImageTk.PhotoImage(img_big)
        self.pic_canvas.image = self.tk_img

        z = 0
        self.current_pictures = sorted(self.current_pictures)
        for img in self.current_pictures:
            pic_col = Frame(self.thumbstrip)
            pic_col.pack(side='left', expand=1, fill='y')

            pic_file = img
            self.img_path = '{}treebard_gps\data\{}\images\{}'.format(
                current_drive, self.image_dir, pic_file)
            idx = len(pic_file)
            bare = pic_file[0:idx-4]
            thumbsy = Image.open(self.img_path)
            self.width_strings.append(thumbsy.width)
            self.height_strings.append(thumbsy.height)
            thumbsy.thumbnail((185,85))
            thumb_path = '{}images/{}_tmb.png'.format(project_path, bare)
            # overwrites file by same name if it exists 
            thumbsy.save(thumb_path)
            small = ImageTk.PhotoImage(file=thumb_path, master=self.thumbstrip)

            thumb = Label(
                pic_col,
                image=small)
            thumb.pack(expand=1, fill='y')
            thumb.image = small

            self.thumb_labels.append(thumb)

            # lambda used to save value in loop
            if self.master.winfo_class() == 'Toplevel':
                rad = Radiobutton(
                    pic_col,
                    takefocus=0,
                    value=pic_file,
                    command=lambda pic_file=pic_file: self.set_main_pic(
                        pic_file))   
                rad.pack()

                if rad['value'] == self.main_pic:
                    rad.select()

            else:                
                rad = Frame(
                    pic_col,
                    height=24,
                    width=24)   
                rad.pack(expand=1, fill='both')
                if self.master.winfo_name() == 'source_tab':
                    pic_file = '{}, {}'.format(self.source, pic_file)
            
            create_tooltip(rad, pic_file)

            z += 1

        self.pil_img = img_big
        self.fit_canvas_to_pic()

        self.thumb_dict = dict(zip(self.thumb_labels, self.current_pictures))
        self.next_img = Button(self.gallery_content, text='>>', width=6)

        panel = Frame(self.gallery_content)

        subject = LabelH3(panel, text=self.current_entity_name)
        subject.grid(column=0, row=0, sticky='ew')

        # labels with selectable multiline text
        self.caption_lab = MessageCopiable(panel, width=36)
        self.picfile_lab = MessageCopiable(panel, width=36)
        self.picsize_lab = MessageCopiable(panel, width=36)
        edit = Button(
            panel, 
            text='EDIT', 
            width=8, 
            command=lambda graphics=self.graphics_tab: self.go_to_graphics(graphics))

        self.previous_img.config(command=self.back)
        self.next_img.config(command=self.forward)

        panel.grid_rowconfigure(0, weight=2)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_rowconfigure(4, weight=2)

        self.caption_lab.grid(column=0, row=1, pady=(12,12), sticky='ew')
        self.caption_lab.insert(1.0, self.caption_text)

        self.picfile_lab.grid(column=0, row=2, pady=(12,0), sticky='ew')
        self.picfile_lab.insert(1.0, self.img_path)

        self.picsize_lab.grid(column=0, row=3, pady=(0,24), sticky='ew')
        self.picsize_lab.insert(
            1.0, 
            'width: {}, height: {}'.format(
                self.pil_img.width, self.pil_img.height))

        edit.grid(column=0, row=4)

        self.caption_lab.set_height()
        self.picfile_lab.set_height()
        self.picsize_lab.set_height()

        self.previous_img.pack(side='left', padx=12)
        self.pic_canvas.pack(side='left', expand=1, fill='y')
        self.next_img.pack(side='left', padx=12)

        panel.pack(side='left', expand=1, fill='y')

        for thumb in self.thumb_labels:
            thumb.bind('<Button-1>', self.show_clicked)

        self.pic_canvas.bind('<Key-Left>', lambda evt: self.back())

        self.pic_canvas.bind('<Key-Right>', lambda evt: self.forward())

        # add statusbar-tooltips

        self.visited = (
            (self.thumbstrip, 
                "Thumbnail Views", 
                "Click thumbnail to display. Hover below to see "
                   "file name. If radio, click to make main image."),
            (self.pic_canvas, 
                "Image", 
                "Arrow keys change image when it's in focus."),
            (self.previous_img, 
                "Left Button", 
                "Click with mouse or when highlighted click with spacebar."),
            (self.next_img, 
                "Right Button", 
                "Click with mouse or when highlighted click with spacebar.")) 

        if self.master.winfo_class() == 'Toplevel':
     
            box = Frame(self.master)
            box.grid(column=0, row=1, pady=12)

            close = Button(
                box, 
                text='CLOSE', 
                width=8, 
                command=self.cancel_gallery)  
            close.grid()
            self.master.protocol('WM_DELETE_WINDOW', self.cancel_gallery)

        self.thumb_canvas.create_window(0, 0, anchor='nw', window=self.thumbstrip)
        self.thumb_canvas.config(
            scrollregion=(
                0, 0, 
                self.thumbstrip.winfo_reqwidth(), 
                self.thumbstrip.winfo_reqheight()))
        
        self.thumb_canvas.config(
            width=self.root.maxsize()[0], 
            height=self.thumbstrip.winfo_reqheight())
        
        scroll_width = int(self.thumb_canvas['scrollregion'].split(' ')[2])

        if scroll_width >= int(self.thumb_canvas['width']):
            for child in self.thumbstrip.winfo_children():
                for gchild in child.winfo_children():
                    gchild.bind("<Enter>", self.thumb_start)
                    gchild.bind("<Motion>", self.thumb_move)

        if self.master.winfo_class() == 'Toplevel':

            gallery_canvas.create_window(
                0, 0, anchor=tk.NW, window=self.gallery_content)
            self.resize_scrollbar()
            self.resize_window()

        self.config_labels()
            
    def resize_scrollbar(self):
        self.master.update_idletasks()                     
        self.pic_canvas.config(scrollregion=self.pic_canvas.bbox("all")) 

    def resize_window(self):
        self.master.update_idletasks()
        page_x = self.gallery_content.winfo_reqwidth()
        page_y = self.gallery_content.winfo_reqheight()+48
        self.master.geometry('{}x{}'.format(page_x, page_y))

    def cancel_gallery(self, event=None):
        self.root.focus_set()
        self.master.destroy() 

    def focus_clicked(self, evt):
        evt.widget.focus_set()

    def hilite(evt):
        evt.widget.config(bg=formats['highlight_bg'])

    def unhilite(evt):
        evt.widget.config(bg=formats['bg'])

    def show_clicked(self, evt):

        select_pic = self.current_pictures.index(self.thumb_dict[evt.widget])

        self.chosen_picfile = self.current_pictures[select_pic]
        # current_dir = get_current_file()[1]
        self.img_path = '{}treebard_gps\data\{}\images\{}'.format(current_drive, current_dir, self.chosen_picfile)

        # pix_data = self.get_current_pix_data()
        # for tup in pix_data:
            # if tup[1] == self.chosen_picfile:
                # self.caption_text = tup[2]

        pix_data = self.get_current_pix_data()
        for tup in pix_data:
            if tup[0] == self.chosen_picfile:
                self.caption_text = tup[1]

        new = Image.open(self.img_path)
        self.tk_img = ImageTk.PhotoImage(new)

        self.pil_img = new
        self.fit_canvas_to_pic()

        self.pic_canvas.image = self.tk_img

        self.pic_canvas.config(
            scrollregion=(0, 0, self.pil_img.width, self.pil_img.height))

        self.config_labels()

        self.counter = select_pic

    def scroll_start(self, event):
        self.pic_canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.pic_canvas.scan_dragto(event.x, event.y, gain=5)

    def thumb_start(self, event):
        self.thumb_canvas.scan_mark(event.x, event.y)

    def thumb_move(self, event):
        self.thumb_canvas.scan_dragto(event.x, event.y, gain=1)

    def go_to_graphics(self, graphics):

        # if frame with this name already exists it's replaced
        # https://stackoverflow.com/questions/59518905/naming-a-widget-to-auto-destroy-replace-it
        picwin = Frame(graphics, name='exists')
        picwin.pack()

        curr_pic = self.picfile_lab.get(1.0, 'end')
        curr_pic = curr_pic.strip('\n')

        img_path = curr_pic
        edit_pic = Image.open(img_path)
        edit_img = ImageTk.PhotoImage(edit_pic)
        editlab = LabelStay(
            picwin,
            image=edit_img)

        editlab.image = edit_img

        self.tabbook.active = self.tabbook.tabdict["graphics"][1]
        self.tabbook.make_active()

        # scroll to top so controls are seen when tab opens
        self.canvas.yview_moveto(0.0)
        
        if self.master.winfo_class() == 'Toplevel':
            self.master.lower(belowThis=self.tabbook)

        editlab.pack() # When this grids a big pic, the whole tabbook gets big
        
        # prevent large pics from blowing up size of the whole tabbook
        #    when placed here by edit button on a gallery
        #    Will need more attention when ready to make the graphics tab.
        editlab.config(width=700, height=700)

    def filter_pix_data(self, pix_data):

        def second_item(s):
            return s[1]

        pix_data = sorted(pix_data, key=second_item) 

        for lst in pix_data:
            if lst[2] == 1:
                self.main_pic = lst[0]
                self.caption_text = lst[1]
                if self.master.winfo_name() == 'source_tab':
                    self.source = lst[3]

        self.current_pictures = []
        for lst in pix_data:
            self.current_pictures.append(lst[0]) 
        self.caption_path = []
        for lst in pix_data:
            self.caption_path.append((lst[0], lst[1])) 

    def back(self, evt=None):

        if self.counter == 0:
            self.counter = len(self.caption_path)    
        self.counter -= 1 
        self.img_path = '{}treebard_gps\data\{}\images\{}'.format(
            current_drive, current_dir, self.caption_path[self.counter][0])
        self.caption_text = self.caption_path[self.counter][1]

        new = Image.open(self.img_path)
        self.tk_img = ImageTk.PhotoImage(new)
        self.pil_img = new
        self.fit_canvas_to_pic()
        self.pic_canvas.image = self.tk_img

        self.pic_canvas.config(
            scrollregion=(0, 0, self.pil_img.width, self.pil_img.height))

        self.config_labels()

    def forward(self, evt=None):

        self.counter += 1 
        if self.counter == len(self.caption_path):
            self.counter = 0
        self.img_path = '{}treebard_gps\\data\\{}\\images\\{}'.format(
            current_drive, current_dir, self.caption_path[self.counter][0])
        self.caption_text = self.caption_path[self.counter][1]

        new = Image.open(self.img_path)
        self.tk_img = ImageTk.PhotoImage(new)
        self.pil_img = new
        self.fit_canvas_to_pic()
        self.pic_canvas.image = self.tk_img

        self.pic_canvas.config(
            scrollregion=(0, 0, self.pil_img.width, self.pil_img.height))

        self.config_labels()

    def get_current_pix_data(self):
        self.image_dir = current_dir
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()

        if self.master.winfo_name() == 'place_tab':
            cur.execute(select_all_place_images)
        elif self.master.winfo_name() == 'source_tab':
            cur.execute(select_all_source_images)
        elif self.master.winfo_class() == 'Toplevel': # person images
            cur.execute(select_all_person_images, (self.current_person,))

        if self.master.winfo_class() != 'Toplevel':
            pix_data = cur.fetchall()
        else:
            pix_data = cur.fetchall()
            pix_data = [list(i) for i in pix_data]
        cur.close()
        conn.close() 

        copy = list(pix_data)
        pix_data = []
        for pic in copy:
            if not pic[0].startswith("default_image"):
                pic_name = pic[0]
                if not pic in pix_data:
                    pix_data.append(pic)        

        return pix_data

    def fit_canvas_to_pic(self):

        # make the buttons stay in one place as pics change
        max_wd = max(self.width_strings)
        max_ht = max(self.height_strings)
        scr_wd = self.root.winfo_screenwidth()
        scr_ht = self.root.winfo_screenheight()

        FULL = 0.55

        if max_wd <= scr_wd * FULL:
            gallery_wd = max_wd
        else:
            gallery_wd = scr_wd * FULL
        if max_ht <= scr_ht * FULL:
            gallery_ht = max_ht
        else:
            gallery_ht = scr_ht * FULL

        self.pic_canvas.config(
            scrollregion=(0, 0, self.pil_img.width, self.pil_img.height),
            width=gallery_wd,
            height=gallery_ht)

        if (self.pil_img.width >= gallery_wd and 
                self.pil_img.height >= gallery_ht):
            image = self.pic_canvas.create_image(
                0, 0, anchor='nw', image=self.tk_img)

        elif (self.pil_img.width <= gallery_wd and 
                self.pil_img.height >= gallery_ht):
            image = self.pic_canvas.create_image(
                 self.pic_canvas.winfo_reqwidth()/2, 0, 
                 anchor='n', image=self.tk_img)

        elif (self.pil_img.width >= gallery_wd and 
                self.pil_img.height <= gallery_ht):
            image = self.pic_canvas.create_image(
                0, self.pic_canvas.winfo_reqheight()/2, 
                anchor='w', image=self.tk_img)

        elif (self.pil_img.width <= gallery_wd and 
                self.pil_img.height <= gallery_ht):
            image = self.pic_canvas.create_image(
            self.pic_canvas.winfo_reqwidth()/2,
            self.pic_canvas.winfo_reqheight()/2,
            anchor='center', 
            image=self.tk_img)

    def config_labels(self): 

        for widg in (self.caption_lab, self.picfile_lab, self.picsize_lab):
            widg.config(state='normal')
            widg.delete(1.0, 'end')

        self.caption_lab.insert(1.0, self.caption_text)
        self.picfile_lab.insert(1.0, self.img_path)
        self.picsize_lab.insert(
            1.0, 'width: {}, height: {}'.format(
                self.pil_img.width, self.pil_img.height))

        for widg in (self.caption_lab, self.picfile_lab, self.picsize_lab):
            widg.set_height()

    def set_main_pic(self, val): 

        radio_value = (val,)
        conn = sqlite3.connect(current_file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        cur.execute(select_current_person_id)
        curr_per = cur.fetchone()
        curr_per = curr_per
        cur.execute(select_current_person_image, curr_per)
        old_top_pic = cur.fetchone()
        cur.execute(update_images_entities_zero, curr_per)
        conn.commit()
        cur.execute(update_images_entities_one, radio_value)

        conn.commit()
        cur.close()
        conn.close() 