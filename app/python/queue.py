# recent_files_queue




import tkinter as tk
import sqlite3
from widgets import LabelHilited3
import dev_tools as dt
from dev_tools import looky, seeline






class RecentFilesQueue():

    def __init__(self, inwidg, outwidg):

        self.inwidg = inwidg
        self.outwidg = outwidg
        self.stored_string = ""
        self.recent_files = []

    def save_filename(self):
        file = self.inwidg.get()
        if len(file) == 0: return
        self.recent_files.insert(0, file)
        if len(self.recent_files) > 20:
            self.recent_files = self.recent_files[0:20]
        self.inwidg.delete(0, 'end')
        self.inwidg.focus_set()
        self.display_list()

    def use_filename(self, evt):
        chosen = evt.widget.cget("text")
        self.recent_files.pop(self.recent_files.index(chosen))
        self.display_list()

    def display_list(self):
        self.store_list()
        if len(self.stored_string) == 0:
            return
        for child in self.outwidg.winfo_children():
            child.destroy()
        x = 0
        for i in range(20):
            lab = LabelHilited3(self.outwidg)
            if len(self.recent_files) >= x + 1:
                lab.config(text=self.recent_files[x])
                lab.grid()
                lab.bind("<Button-1>", self.use_filename)
            else:
                break
            x += 1

    def store_list(self):
        self.stored_string = "_+_".join(self.recent_files)

if __name__ == "__main__":

    from widgets import Button, Frame, Entry

    root = tk.Tk()

    entry = Entry(root)
    entry.grid()


    frm = Frame(root)
    frm.grid()

    recent_files = RecentFilesQueue(entry, frm)
    update = Button(root, text="UPDATE", command=recent_files.save_filename)
    update.grid()

    root.mainloop()
