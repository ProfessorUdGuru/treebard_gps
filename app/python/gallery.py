# gallery

import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from files import get_current_file, current_drive, app_path
from styles import make_formats_dict, config_generic
from scrolling import Scrollbar, resize_scrolled_content
from widgets import (
    Frame, Canvas, Button, Label, Radiobutton, FrameHilited4, 
    LabelH3, MessageCopiable, LabelStay)
from toykinter_widgets import run_statusbar_tooltips
from right_click_menu import RightClickMenu, make_rc_menus
from messages_context_help import gallery_help_msg, gallery_thumbnail_help_msg
from utes import create_tooltip
from names import get_current_person
from query_strings import (
    select_all_place_images, select_all_source_images, 
    select_all_person_images, select_current_person_id, 
    select_current_person_image, update_images_elements_zero,
    update_images_elements_one
)
import dev_tools as dt
from dev_tools import looky, seeline




formats = make_formats_dict()

class Gallery(Frame):

    def __init__(
            self, master, tabbook, 
            graphics_tab, 
            root, treebard, SCREEN_SIZE, dialog=None,
            current_person_name=None, current_place_name=None, 
            current_source_name=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master # canvas
        self.tabbook = tabbook
        self.graphics_tab = graphics_tab
        self.root = root
        self.treebard = treebard
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_SIZE
        self.dialog = dialog

        self.rc_menu = RightClickMenu(self.root)

        self.current_file, self.current_dir = get_current_file()

        self.main_pic = "default_image_unisex.jpg"
        self.caption_text = ""

        if current_person_name:
            self.current_entity_name = current_person_name
        elif current_place_name:
            self.current_entity_name = current_place_name
        elif current_source_name:
            self.current_entity_name = current_source_name
        else:
            print("line", looky(seeline()).lineno, "case_not_handled:")

        self.counter = 0
        self.thumb_labels = []
        self.maxwidth = 0
        self.maxheight = 0

        self.current_person = get_current_person()[0]

        pix_data = self.get_current_pix_data()
        if self.dialog:
            if len(pix_data) != 0:
                self.filter_pix_data(pix_data)
                self.make_widgets()
                self.make_gallery()
            else:
                self.dialog.destroy()
        else:
            self.filter_pix_data(pix_data)
            self.make_gallery()

    def cancel(self):
        self.dialog.grab_release()
        self.dialog.destroy()

    def make_widgets(self):        
        self.dialog.geometry('+100+20')
        self.master.title_1.config(text="Current Person Image Gallery")
        self.master.title_2.config(text="")
        self.master.create_window(0, 0, anchor='nw', window=self)
        scridth = 16
        scridth_n = Frame(self, height=scridth)
        scridth_w = Frame(self, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.treebard.scroll_mouse.append_to_list([self.master, self])
        self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        self.vsb = Scrollbar(
            self.dialog, 
            hideable=True, 
            command=self.master.yview,
            width=scridth)
        self.hsb = Scrollbar(
            self.dialog, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=self.master.xview)
        self.master.config(
            xscrollcommand=self.hsb.set, 
            yscrollcommand=self.vsb.set)
        self.vsb.grid(column=2, row=4, sticky='ns')
        self.hsb.grid(column=1, row=5, sticky='ew')

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')

    def make_gallery(self):

        thumb_frame = Frame(self)        

        self.thumb_canvas = Canvas(thumb_frame, bg=formats['bg'])

        thumb_sbh = Scrollbar(
            thumb_frame, 
            orient='horizontal', 
            command=self.thumb_canvas.xview, 
            hideable=True)
        self.thumb_canvas.config(xscrollcommand=thumb_sbh.set)
        
        viewer = FrameHilited4(self)

        self.thumbstrip = Frame(self.thumb_canvas)

        self.buttonbox = Frame(self)
        self.prevbutt = Button(self.buttonbox, text='<<', width=7)

        self.pic_canvas = Canvas(viewer)
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
            pic_col.grid(column=z, row=0)

            pic_file = img
            self.img_path = '{}treebard_gps\data\{}\images\{}'.format(
                current_drive, self.image_dir, pic_file)
            idx = len(pic_file)
            bare = pic_file[0:idx-4]
            thumbsy = Image.open(self.img_path)
            if thumbsy.width > self.maxwidth:
                self.maxwidth = thumbsy.width
            if thumbsy.height > self.maxheight:
                self.maxheight = thumbsy.height
            thumbsy.thumbnail((185,85))
            thumb_path = '{}images/{}_tmb.png'.format(app_path, bare)
            # overwrites file by same name if it exists 
            thumbsy.save(thumb_path)
            small = ImageTk.PhotoImage(file=thumb_path, master=self.thumbstrip)

            thumb = Label(
                pic_col,
                image=small)
            thumb.grid(column=0, row=0)
            thumb.image = small
            self.rc_menu.loop_made[thumb] = gallery_thumbnail_help_msg

            self.thumb_labels.append(thumb)

            if self.dialog:
                rad = Radiobutton(
                    pic_col,
                    takefocus=0,
                    value=pic_file,
                    command=lambda pic_file=pic_file: self.set_main_pic(
                        pic_file))   
                rad.grid(column=0, row=1)
                if rad['value'] == self.main_pic:
                    rad.select()
            else:   
                if self.master.winfo_name() == 'sourcetab':
                    pic_file = '{}, {}'.format(self.source, pic_file) 
            create_tooltip(pic_col, pic_file)
            z += 1

        self.pil_img = img_big
        self.fit_canvas_to_pic()

        self.thumb_dict = dict(zip(self.thumb_labels, self.current_pictures))

        self.nextbutt = Button(self.buttonbox, text='>>', width=7)
        self.editbutt = Button(
            self.buttonbox, text="EDIT", width=7, 
            command=lambda graphics=self.graphics_tab: self.go_to_graphics(graphics))
        self.b2 = Button(self.buttonbox, text="CLOSE", width=7, command=self.cancel)
        
        spacer = Frame(self.buttonbox)       
        panel = Frame(self.buttonbox)
        subject = LabelH3(panel, text=self.current_entity_name)

        self.caption_lab = MessageCopiable(panel)
        self.picfile_lab = MessageCopiable(panel)
        self.picsize_lab = MessageCopiable(panel)

        self.prevbutt.config(command=self.back)
        self.nextbutt.config(command=self.forward)

        self.caption_lab.insert(1.0, self.caption_text)
        self.picfile_lab.insert(1.0, self.img_path)
        self.picsize_lab.insert(
            1.0, 
            'width: {}, height: {}'.format(
                self.pil_img.width, self.pil_img.height))

        self.caption_lab.set_height()
        self.picfile_lab.set_height()
        self.picsize_lab.set_height()

        # children of self
        thumb_frame.grid(column=0, row=0, padx=24, pady=24, columnspan=2, sticky='w')
        thumb_sbh.grid(column=0, row=1, sticky="ew")
        viewer.grid(column=0, row=2, padx=24)
        self.buttonbox.grid(column=0, row=3, pady=24, padx=24, sticky='ew')

        # children of thumb_frame
        self.thumb_canvas.grid(column=0, row=0, sticky="news")
        thumb_sbh.grid(column=0, row=1, sticky="ew")

        # children of self.thumb_canvas
        self.thumbstrip.grid(column=0, row=0)

        # children of viewer
        self.pic_canvas.grid(column=0, row=0, columnspan=2)

        # children of panel
        subject.grid(column=0, row=0, sticky='w', pady=(12,0))
        self.caption_lab.grid(column=0, row=1, pady=(12,12), sticky='w')
        self.picfile_lab.grid(column=0, row=2, pady=(12,0), sticky='w')
        self.picsize_lab.grid(column=0, row=3, pady=(0,24), sticky='w')

        # children of self.buttonbox
        self.buttonbox.columnconfigure(2, weight=10)
        self.prevbutt.grid(column=0, row=0, sticky='e')
        self.nextbutt.grid(column=1, row=0, sticky='e', padx=(6,0))
        self.editbutt.grid(column=0, row=1, sticky='e')
        if self.dialog:
            self.b2.grid(column=1, row=1, sticky='e', padx=(6,0))
        spacer.grid(column=2, row=0, rowspan=3, sticky='news')
        panel.grid(column=3, row=0, rowspan=3, pady=(0,24), padx=24, sticky='w')

        for thumb in self.thumb_labels:
            thumb.bind('<Button-1>', self.show_clicked)

        self.pic_canvas.bind('<Key-Left>', lambda evt: self.back())

        self.pic_canvas.bind('<Key-Right>', lambda evt: self.forward())

        self.thumb_canvas.create_window(0, 0, anchor='nw', window=self.thumbstrip)
        self.thumb_canvas.config(
            scrollregion=(
                0, 0, 
                self.thumbstrip.winfo_reqwidth(),
                self.thumbstrip.winfo_reqheight()))

        self.config_labels()

        visited = (
            (self.thumbstrip, 
                "Thumbnail Views", 
                "Click thumbnail to display. Hover to see the file name. "
                    "Select radio button to make this the main image."),
            (self.pic_canvas, 
                "Image", 
                "Arrow keys change image when it's in focus."),
            (self.prevbutt, 
                "Left Button", 
                "Click with mouse or when highlighted click with spacebar."),
            (self.nextbutt, 
                "Right Button", 
                "Click with mouse or when highlighted click with spacebar."),
            (self.editbutt,
                "Edit Button",
                "Open the current image in the Graphics Tab.")) 
        if self.dialog:
            run_statusbar_tooltips(
                visited, 
                self.master.statusbar.status_label, 
                self.master.statusbar.tooltip_label)
            config_generic(self.dialog)

        rcm_widgets = (
            self.pic_canvas, self.prevbutt, self.nextbutt, self.editbutt)
        make_rc_menus(
            rcm_widgets, 
            self.rc_menu,
            gallery_help_msg)

        self.thumb_canvas.config(width=self.winfo_reqwidth(), height=130)
        if self.dialog:
            resize_scrolled_content(self.dialog, self.master, self)
        self.pic_canvas.focus_set()

    def focus_clicked(self, evt):
        evt.widget.focus_set()

    def hilite(evt):
        evt.widget.config(bg=formats['highlight_bg'])

    def unhilite(evt):
        evt.widget.config(bg=formats['bg'])

    def show_clicked(self, evt):
        select_pic = self.current_pictures.index(self.thumb_dict[evt.widget])

        self.chosen_picfile = self.current_pictures[select_pic]
        self.img_path = '{}treebard_gps\data\{}\images\{}'.format(
            current_drive, self.current_dir, self.chosen_picfile)

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

    def go_to_graphics(self, graphics):
        '''
            If frame with this name already exists it's replaced: https://stackoverflow.com/questions/59518905/
                naming-a-widget-to-auto-destroy-replace-it
        '''

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
        self.treebard.canvas.yview_moveto(0.0)
        
        if self.dialog:
            self.dialog.lower(belowThis=self.tabbook)

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
            print("line", looky(seeline()).lineno, "lst:", lst)
            if lst[2] == 1:
                self.main_pic = lst[0]
                self.caption_text = lst[1]
                if self.master.winfo_name() == 'sourcetab':
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
            current_drive, self.current_dir, self.caption_path[self.counter][0])
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
            current_drive, self.current_dir, self.caption_path[self.counter][0])
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
        
        self.image_dir = self.current_dir
        conn = sqlite3.connect(self.current_file)
        cur = conn.cursor()
        if self.master.winfo_name() == 'placetab':
            cur.execute(select_all_place_images)
        elif self.master.winfo_name() == 'sourcetab':
            cur.execute(select_all_source_images)
        elif self.dialog:
            cur.execute(select_all_person_images, (self.current_person,))
        pix_data = cur.fetchall()
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

        # don't show overly large images at their full size
        FULL = 0.55
        if self.maxwidth <= self.SCREEN_WIDTH * FULL:
            gallery_wd = self.maxwidth
        else:
            gallery_wd = self.SCREEN_WIDTH * FULL
        if self.maxheight <= self.SCREEN_HEIGHT * FULL:
            gallery_ht = self.maxheight
        else:
            gallery_ht = self.SCREEN_HEIGHT * FULL

        self.pic_canvas.config(
            scrollregion=(0, 0, self.pil_img.width, self.pil_img.height),
            width=gallery_wd,
            height=gallery_ht)

        # position image in canvas depending on image size
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
        conn = sqlite3.connect(self.current_file)
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        cur.execute(select_current_person_id)
        curr_per = cur.fetchone()
        curr_per = curr_per
        cur.execute(select_current_person_image, curr_per)
        old_top_pic = cur.fetchone()
        cur.execute(update_images_elements_zero, curr_per)
        conn.commit()
        cur.execute(update_images_elements_one, radio_value)

        conn.commit()
        cur.close()
        conn.close() 