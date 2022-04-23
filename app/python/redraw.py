# redraw.py

import sqlite3
from files import get_current_file
from query_strings import update_current_person
import dev_tools as dt
from dev_tools import looky, seeline




def redraw_person_tab(
        evt=None, main_window=None, current_person=None, current_name=None):
    current_file, current_dir = get_current_file()
    findings_table = main_window.findings_table
    findings_table.root.update_idletasks()
    if current_person:
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_person, (current_person,))
        conn.commit()
        cur.close()
        conn.close()
    unbind_widgets(findings_table)
    redraw_current_person_area(
        current_person, main_window, current_name, current_file, current_dir)
    redraw_events_table(findings_table)
    if current_person:
        redraw_families_table(evt, current_person, main_window)

    resize_scrollbar(findings_table.root, findings_table.main_canvas)

def unbind_widgets(findings_table):
    for k,v in findings_table.kintip_bindings.items():
        if k == "on_enter":
            for lst in v:
                lst[0].unbind("<Enter>", lst[1])                    
        elif k == "on_leave":
            for lst in v:
                lst[0].unbind("<Leave>", lst[1])
        findings_table.kintip_bindings = {"on_enter": [], "on_leave": []}

    for k,v in findings_table.main_window.nukefam_table.idtip_bindings.items():
        if k == "on_enter":
            for lst in v:
                lst[0].unbind("<Enter>", lst[1])                    
        elif k == "on_leave":
            for lst in v:
                lst[0].unbind("<Leave>", lst[1])
        findings_table.main_window.nukefam_table.idtip_bindings = {
            "on_enter": [], "on_leave": []}

def redraw_current_person_area(
        current_person, main_window, current_name, current_file, current_dir):
    main_window.person_entry.delete(0, 'end')
    main_window.show_top_pic(current_file, current_dir, current_person)
    main_window.person_entry.current_id = None
    main_window.current_person_name = current_name
    main_window.show_top_pic(current_file, current_dir, current_person)
    main_window.current_person_label.config(
        text="Current Person (ID): {} ({})".format(current_name, current_person))

def redraw_families_table(evt, current_person, main_window):
    main_window.findings_table.kin_widths = [0, 0, 0, 0, 0, 0]
    for ent in main_window.nukefam_table.nukefam_inputs:
        ent.delete(0, "end")
    main_window.nukefam_table.ma_input.delete(0, "end")
    main_window.nukefam_table.pa_input.delete(0, "end")
    main_window.nukefam_table.new_kid_input.delete(0, "end")
    main_window.nukefam_table.new_kid_frame.grid_forget()
    main_window.nukefam_table.current_person_alt_parents = []
    main_window.nukefam_table.compound_parent_type = "Children's"        
    for widg in main_window.nukefam_table.nukefam_containers: 
        widg.destroy() 
    main_window.nukefam_table.parent_types = []
    main_window.nukefam_table.nukefam_containers = []

    main_window.nukefam_table.family_data = initialize_family_data_dict()

    if evt: # user pressed CTRL+S for example
        main_window.nukefam_table.make_nukefam_inputs(
            current_person=main_window.findings_table.current_person)
    else: # user pressed OK to change current person for example  
        main_window.nukefam_table.make_nukefam_inputs()







def redraw_events_table(findings_table):

    for lst in findings_table.cell_pool:
        for widg in lst[1]:
            if widg.winfo_subclass() == 'EntryAuto':
                widg.delete(0, 'end')
            elif widg.winfo_subclass() == 'LabelButtonText':
                widg.config(text='')
            widg.grid_forget()
    findings_table.event_input.grid_forget()
    findings_table.add_event_button.grid_forget()

    findings_table.new_row = 0 
    findings_table.widths = [0, 0, 0, 0, 0]
    findings_table.kin_widths = [0, 0, 0, 0, 0, 0]
    findings_table.set_cell_content()
    findings_table.show_table_cells()



# def redraw_person_tab(evt=None, current_person=None, findings_table=None):
    # current_file = get_current_file()[0]
    # conn = sqlite3.connect(current_file)
    # conn.execute('PRAGMA foreign_keys = 1')
    # cur = conn.cursor()
    # cur.execute(update_current_person, (current_person,))
    # conn.commit()
    # cur.close()
    # conn.close()
    # forget_cells(findings_table)
    # findings_table.new_row = 0 
    # findings_table.widths = [0, 0, 0, 0, 0]
    # findings_table.kin_widths = [0, 0, 0, 0, 0, 0]
    # findings_table.set_cell_content()
    # findings_table.show_table_cells()
    # if evt: # user pressed CTRL+S for example
        # findings_table.main_window.nukefam_table.make_nukefam_inputs(
            # current_person=findings_table.current_person)
    # else: # user pressed OK to change current person for example  
        # findings_table.main_window.nukefam_table.make_nukefam_inputs()

    # resize_scrollbar(findings_table.root, findings_table.main_canvas)

# def forget_cells(findings_table):
    # findings_table.root.update_idletasks()
    # for k,v in findings_table.kintip_bindings.items():
        # if k == "on_enter":
            # for lst in v:
                # lst[0].unbind("<Enter>", lst[1])                    
        # elif k == "on_leave":
            # for lst in v:
                # lst[0].unbind("<Leave>", lst[1])
        # findings_table.kintip_bindings = {"on_enter": [], "on_leave": []}

    # for k,v in findings_table.main_window.nukefam_table.idtip_bindings.items():
        # if k == "on_enter":
            # for lst in v:
                # lst[0].unbind("<Enter>", lst[1])                    
        # elif k == "on_leave":
            # for lst in v:
                # lst[0].unbind("<Leave>", lst[1])
        # findings_table.main_window.nukefam_table.idtip_bindings = {
            # "on_enter": [], "on_leave": []}

    # for lst in findings_table.cell_pool:
        # for widg in lst[1]:
            # if widg.winfo_subclass() == 'EntryAuto':
                # widg.delete(0, 'end')
            # elif widg.winfo_subclass() == 'LabelButtonText':
                # widg.config(text='')
            # widg.grid_forget()
    # findings_table.event_input.grid_forget()
    # findings_table.add_event_button.grid_forget()

    # findings_table.main_window.person_entry.current_id = None

    # for ent in findings_table.main_window.nukefam_table.nukefam_inputs:
        # ent.delete(0, "end")
    # findings_table.main_window.nukefam_table.ma_input.delete(0, "end")
    # findings_table.main_window.nukefam_table.pa_input.delete(0, "end")
    # findings_table.main_window.nukefam_table.new_kid_input.delete(0, "end")
    # findings_table.main_window.nukefam_table.new_kid_frame.grid_forget()
    # findings_table.main_window.nukefam_table.current_person_alt_parents = []
    # findings_table.main_window.nukefam_table.compound_parent_type = "Children's"        
    # for widg in findings_table.main_window.nukefam_table.nukefam_containers: 
        # widg.destroy() 
    # findings_table.main_window.nukefam_table.parent_types = []
    # findings_table.main_window.nukefam_table.nukefam_containers = []

    # findings_table.main_window.nukefam_table.family_data = initialize_family_data_dict()

def resize_scrollbar(root, canvas):
    root.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

def initialize_family_data_dict():
    """ This is mainly used in families.py but also used here in redraw.py
        for redrawing the person tab when changes are made by the user. Imports
        go from here to families.py.
    """
    family_data = [
        [
            [
                {'finding': None, 'sorter': [0, 0, 0]}, 
                {'id': None, 'name': '', 'kin_type_id': 2, 
                    'kin_type': 'father', 'labwidg': None, 'inwidg': None}, 
                {'id': None, 'name': '', 'kin_type_id': 1, 
                    'kin_type': 'mother', 'labwidg': None, 'inwidg': None}
            ],
        ],
        {},
    ]
    return family_data















    # def redraw(self, evt=None, current_person=None):
        # self.formats = make_formats_dict()
        # current_file = get_current_file()[0]
        # conn = sqlite3.connect(current_file)
        # conn.execute('PRAGMA foreign_keys = 1')
        # cur = conn.cursor()
        # cur.execute(update_current_person, (self.current_person,))
        # conn.commit()
        # cur.close()
        # conn.close()
        # self.forget_cells()
        # self.new_row = 0 
        # self.widths = [0, 0, 0, 0, 0]
        # self.kin_widths = [0, 0, 0, 0, 0, 0]
        # self.set_cell_content()
        # self.show_table_cells()
        # if evt: # user pressed CTRL+S for example
            # self.main_window.nukefam_table.make_nukefam_inputs(
                # current_person=self.current_person)
        # else: # user pressed OK to change current person for example  
            # self.main_window.nukefam_table.make_nukefam_inputs()

        # self.resize_scrollbar(self.root, self.main_canvas)

    # def forget_cells(self):
        # self.update_idletasks()
        # for k,v in self.kintip_bindings.items():
            # if k == "on_enter":
                # for lst in v:
                    # lst[0].unbind("<Enter>", lst[1])                    
            # elif k == "on_leave":
                # for lst in v:
                    # lst[0].unbind("<Leave>", lst[1])
            # self.kintip_bindings = {"on_enter": [], "on_leave": []}

        # for k,v in self.main_window.nukefam_table.idtip_bindings.items():
            # if k == "on_enter":
                # for lst in v:
                    # lst[0].unbind("<Enter>", lst[1])                    
            # elif k == "on_leave":
                # for lst in v:
                    # lst[0].unbind("<Leave>", lst[1])
            # self.main_window.nukefam_table.idtip_bindings = {"on_enter": [], "on_leave": []}

        # for lst in self.cell_pool:
            # for widg in lst[1]:
                # if widg.winfo_subclass() == 'EntryAuto':
                    # widg.delete(0, 'end')
                # elif widg.winfo_subclass() == 'LabelButtonText':
                    # widg.config(text='')
                # widg.grid_forget()
        # self.event_input.grid_forget()
        # self.add_event_button.grid_forget()

        # self.main_window.person_entry.current_id = None

        # for ent in self.main_window.nukefam_table.nukefam_inputs:
            # ent.delete(0, "end")
        # self.main_window.nukefam_table.ma_input.delete(0, "end")
        # self.main_window.nukefam_table.pa_input.delete(0, "end")
        # self.main_window.nukefam_table.new_kid_input.delete(0, "end")
        # self.main_window.nukefam_table.new_kid_frame.grid_forget()
        # self.main_window.nukefam_table.current_person_alt_parents = []
        # self.main_window.nukefam_table.compound_parent_type = "Children's"        
        # for widg in self.main_window.nukefam_table.nukefam_containers: 
            # widg.destroy() 
        # self.main_window.nukefam_table.parent_types = []
        # self.main_window.nukefam_table.nukefam_containers = []

        # self.main_window.nukefam_table.family_data = initialize_family_data_dict()

    # def resize_scrollbar(self, root, canvas):
        # root.update_idletasks()
        # canvas.config(scrollregion=canvas.bbox('all'))