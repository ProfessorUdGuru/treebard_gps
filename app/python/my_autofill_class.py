# my_autofill_class
import tkinter as tk

class EntryAutofill(tk.Entry):

    def __init__(self, master, *args, **kwargs):
        tk.Entry.__init__(self, master, *args, **kwargs)

        self.values = ['red', 'black', 'blue', 'rust', 'Bill', 'Bilbo']
        self.var = tk.StringVar()
        self.bind('<KeyRelease>', self.get_typed)
        self.bind('<Key>', self.detect_pressed)

    def match_string(self):
        hits = []
        got = self.var.get()
        for item in self.values:
            if item.lower().startswith(got.lower()):
                hits.append(item)
        return hits    

    def get_typed(self, event):
        if len(event.keysym) == 1:
            hits = self.match_string()
            self.show_hit(hits)

    def detect_pressed(self, event):
        print("detect_pressed running")
        key = event.keysym
        if len(key) == 1:
            pos = self.index('insert')
            print(pos)
            self.delete(pos, 'end')

    def show_hit(self, lst):
        print("show_hit running")
        if len(lst) == 1:
            print("lst:", lst)
            self.var.set(lst[0])

short_values = [
    'red', 'white', 'blue', 'black', 'rust', 'Bill',
    'pink', 'steelblue', 'mom', 'dad', 'Bilbo']

if __name__ == '__main__':

    root = tk.Tk()
    root.title("OFFICIAL AUTOFILL CLASS TESTER")
    root.geometry('+800+300')    

    auto = EntryAutofill(root, width=200)
    auto.config(textvariable=auto.var)
    auto.values = short_values
    auto.focus_set()    

    move = tk.Entry(root)

    auto.grid()
    move.grid()

    root.mainloop()