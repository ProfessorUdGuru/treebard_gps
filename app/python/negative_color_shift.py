# negative_color_shift
# when user chooses a background color and a foreground color the two trade places in the swatch so font can be seen and user can see if he's chosen badly contrasting colors

import tkinter as tk


def change():
    bg = bg_ent.get()
    fg = fg_ent.get()
    lab1.config(bg=bg, text=bg, fg=fg)
    lab2.config(bg=fg, text=fg, fg=bg)

root = tk.Tk()

bg_ent = tk.Entry(root)
fg_ent = tk.Entry(root)
bg_ent.grid()
fg_ent.grid()


labels = []
lab1 = tk.Label(root, width=10)
lab2 = tk.Label(root, width=10)
lab1.grid()
lab2.grid()
labels.append(lab1)
labels.append(lab2)

b = tk.Button(root, text="OK", command=change)
b.grid()



root.mainloop()