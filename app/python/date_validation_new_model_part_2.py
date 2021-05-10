# date_validation_new_model_part_2

# sample widgets which give input to a dates validation module and get input back from that module

import tkinter as tk
from tkinter import ttk
import sqlite3
import widgets as wdg
import date_validation_new_model_03 as dates
import styles as st
import files

ST = st.ThemeStyles()
formats = st.make_formats_dict()

def use_input(input, widg):
    ''' for EntryLabel '''
    dates.get_widg_type(widg)

def get_event(evt):
    ''' for widgets other than EntryLabel '''
    widg = evt.widget
    dates.get_widg_type(widg)    

date_in = ''

root = tk.Tk()
root.geometry('+10+600')

label = wdg.Label(
    root, 
    text='Dates validation procedure must work equally\n'
         'from any kind of input widget')
label.grid(columnspan=3, pady=24)

simple = wdg.Entry(root)
simple.grid(column=0, row=1)
simple.insert(0, '1810 10 18')
simple.focus_set()

mostring = wdg.Entry(root)
mostring.grid(column=1, row=1)
mostring.insert(0, '1912 4 jan')

clarif3 = wdg.Entry(root)
clarif3.grid(column=2, row=1)
clarif3.insert(0, '11 oct 0012 ad to 1884 bc')

clarif2 = wdg.Entry(root)
clarif2.grid(column=3, row=1)
clarif2.insert(0, '1811 4 3')

ranje = wdg.Entry(root)
ranje.grid(column=4, row=1)
ranje.insert(0, '1822 and 1818')

span = wdg.Entry(root)
span.grid(column=5, row=1)
span.insert(0, '1815 to 1808')

span1 = wdg.Entry(root)
span1.grid(column=6, row=1)
span1.insert(0, '? to 1818')

span2 = wdg.Entry(root)
span2.grid(column=7, row=1)
span2.insert(0, '1822 to ?')

label2 = wdg.Label(root, text='EntryLabel:')
label2.grid(column=0, row=3)

entrylabel = wdg.EntryLabel(root, use_input)
entrylabel.grid(column=1, row=3)
# entrylabel.config(text='1500')

conn = sqlite3.connect('c:/treebard_gps/app/python/test_date_in_out.db')
cur = conn.cursor()
cur.execute('SELECT dates FROM date_test WHERE date_test_id = 1')
stored_date = cur.fetchone()[0]
entrylabel.config(text=stored_date)




# DO NOT DELETE THESE WIDGETS
# label3 = wdg.Label(root,text='Combobox:')
# label3.grid(column=0, row=4)

# combobox = wdg.ClickAnywhereCombo(root, values=vals)
# combobox.grid(column=1, row=4)
# combobox.insert(0, '1499')

# label4 = wdg.Label(root,text='Text:')
# label4.grid(column=0, row=5)

# text = wdg.Text(root, width=40, height=1)
# text.grid(column=1, row=5, columnspan=2)
# text.insert(1.0, '1601')

show = wdg.Label(root)
show.grid(column=0, row=6, columnspan=2)

widgets = [simple, mostring, clarif3, clarif2, ranje, span, span1, span2]

u = 0
for widg in widgets:
    button = wdg.Button(
        root, 
        text='Validate', 
        command=lambda widg=widg: dates.get_widg_type(widg))
    button.grid(column=u, row=2)
    u += 1 

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

# DO NOT DELETE 
# text.bind("<Tab>", focus_next_window)
# for widg in (combobox, text):
    # widg.bind('<FocusOut>', get_event)

ST.config_generic(root)

root.mainloop()