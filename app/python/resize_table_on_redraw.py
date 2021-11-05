# resize_table_on_redraw

import tkinter as tk
import dev_tools as dt
from dev_tools import looky, seeline

'''The button works once, then reload.'''




HEADS = ("event", "date")

person1 = [
    ["birth", "approximately February 24, 1929 AD"],
    ["death", "1985"],
    ["burial", "March 1985"]
]

person2 = [
    ["father's occupation at birth", "Feb 24 1929"],
    ["death", "1931"],
    ["burial", "btwn estimated September 29, 1931 AD and January 1932"]
]

def change_people(toople=person1):
    draw_table(toople)

def draw_table(toople):
    for child in table.winfo_children():
        child.destroy()
    h = 0
    widths = [0, 0]
    for column in HEADS: 
        head = tk.Entry(table, font=mono_sans, bg="pink")
        head.delete(0, 'end')
        head.insert(0, column.upper())
        head.grid(column=h, row=0, sticky='ew')
        x = 0
        for row in toople: 
            lab = tk.Entry(table, font=mono_sans, width=0, bg="steelblue")
            lab.grid(column=h, row=x+1, sticky='we')
            text = row[h]
            lab.delete(0, 'end')
            lab.insert(0, text)
            length = len(text)
            if length > widths[h]:
                widths[h] = length
            head.config(width=widths[h]+2) # +2 is just padding
            x += 1
        h += 1

root = tk.Tk()
root.geometry("1000x400+700+100")
root.config(bg="blue")

mono_sans = ("dejavu sans mono", 12)

tabbook = tk.Frame(root, bg="tan")
tabbook.grid()

table = tk.Frame(tabbook, bg="bisque")
table.grid(padx=24, pady=24)

change_people()

change = tk.Button(root, text="Change Person", command=lambda toople=person2: change_people(toople))
change.grid()

root.mainloop()