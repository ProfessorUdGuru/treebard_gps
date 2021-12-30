# convert_rgb_color_to_hex

# https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
# code by Jeremy Cantrell

import tkinter as tk



def hex_to_rgb(value):
    '''
        Return (red, green, blue) for the color given as #rrggbb.

    '''
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red, green, blue):
    '''
        Return color as #rrggbb for the given color values.
        In the function, rgb is a tuple of 3 ints. The format string is just a 
        # followed by three %02x which just gives a zero padded 2 digit hex 
        value of the int. 

    '''
    # return '#%02x%02x%02x' % (red, green, blue)
    return "#{0:02X}{1:02X}{2:02X}".format(red, green, blue)

print(hex_to_rgb("#ffffff"))          #==> (255, 255, 255)
print(hex_to_rgb("#ffffffffffff"))    #==> (65535, 65535, 65535)
print(rgb_to_hex(255, 255, 255))       #==> '#ffffff'
print(rgb_to_hex(65535, 65535, 65535)) #==> '#ffffffffffff'
print(hex_to_rgb("#121212"))

# mbw below this point
# goal is:
#   user-input fg is used for text on labels that show bg color
#   but on label that shows fg color, bg is shown

bg = "#121212"
fg = "#51755a"

def change_fg_to_visible(bg):
    bg_rgb = hex_to_rgb(bg)
    print("bg_rgb:", bg_rgb)
    if max(bg_rgb) < 125:
        fg = "white"
    else:
        fg = "black"
    return fg

root = tk.Tk()



labels = []
lab1 = tk.Label(root, bg=bg, text=bg, width=10)
lab2 = tk.Label(root, bg=fg, text=fg, width=10)
lab1.grid()
lab2.grid()
labels.append(lab1)
labels.append(lab2)

for lab in labels:
    bg = lab.cget("bg")
    fg = change_fg_to_visible(bg)
    lab.config(fg=fg)

root.mainloop()