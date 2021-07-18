# messages.py (import as msg)

import tkinter as tk
from styles import ThemeStyles
from widgets import Frame, Label, LabelItalic, Button, Entry
from winsound import PlaySound, SND_ASYNC
import dev_tools as dt

ST = ThemeStyles()

class Toplevelx(tk.Toplevel):

    def __init__(self, parent=None, title=None, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

    def winfo_subclass(self):
        ''' Works like built-in tkinter method
            winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

class MessageModel(Toplevelx):
    ''' 
        parent: modal dialog has no minimize/maximize buttons, goes where parent goes
        gparent: parent of parent might need to be destroyed on click of msg button
        title: goes on title bar of dialog using w.title('title') method
        prompt: tells the user to enter some data in an entry or combobox
        message: multiline Message widget text to inform user why dialog opened
        input: bad input from user displayed in dialog so he sees his typo/bad data
        x = inst.show(): data input by user into dialog is returned on dialog close
    '''
    def __init__(
        self, parent,
            gparent=None, 
            title=None, 
            prompt=None, message=None, input_text=None, 
            *args, **kwargs):
        Toplevelx.__init__(self, parent, title=None, *args, **kwargs)

        self.edit_input = False
        self.add_data_to_db = True

        self.parent = parent
        self.gparent = gparent
        self.prompt = prompt
        self.message = message
        self.input_text = input_text

        if title:
            self.title(title)

        self.grab_set()
        self.transient(parent)

        self.make_widgets()

    def make_widgets(self):

        self.frm = Frame(self)
        self.frm.grid(column=0, row=0, pady=(0,18))

        self.errlab = Label(self.frm, text='Input was: ')
        self.errlab.grid(column=0, row=0, padx=24, pady=(24,0), sticky='w')
        self.errshow = LabelItalic(self.frm)
        self.errshow.grid(column=1, row=0, pady=(24,0), sticky='w')

        self.errmsg = tk.Message(
            self.frm, text=self.message, bd=3, relief='raised', aspect=400)
        self.errmsg.grid(
            column=0, row=1, padx=36, pady=(0, 18), columnspan=2)

        self.promptlab = Label(self.frm)
        self.var = tk.StringVar()
        self.altentry = Entry(self.frm)
        self.altentry.config(textvariable=self.var)

        self.promptlab.grid(column=0, row=2, pady=24, padx=24, sticky='w')
        self.altentry.grid(column=1, row=2, pady=24, sticky='w')
        self.promptlab.grid_remove()
        self.altentry.grid_remove()

        self.altentry.focus_set()
        self.altentry.bind('<Return>', self.on_ok)   
     
        self.bbox = Frame(self)
        self.bbox.grid(column=0, row=3, columnspan=2)

        self.done = Button(
            self.bbox, 
            text='DONE', 
            command=self.on_ok, 
            width=9)
        self.done.grid(column=0, row=0, padx=24, pady=(12,24))
        self.done.grid_remove()

        self.stop = Button(
            self.bbox, 
            text='CANCEL1', 
            command=self.on_cancel, 
            width=9)
        self.stop.grid(column=1, row=0, padx=24, pady=(12,24))
        self.stop.grid_remove()     

        self.done.focus_set()

        self.accept = Button(
            self.bbox, 
            text='Accept Original Input', 
            command=self.on_ok, 
            width=36)
        self.accept.grid(column=0, row=0, padx=24, pady=12)
        self.accept.grid_remove()

        self.edit = Button(
            self.bbox, 
            text='Submit Edited Input', 
            command=self.on_alt, width=36)
        self.edit.grid(column=0, row=1, padx=24, pady=12)
        self.edit.grid_remove()

        self.cancel_all = Button(
            self.bbox, 
            text="Cancel (Don't Submit Anything)", 
            command=self.on_cancel, 
            width=36)
        self.cancel_all.grid(column=0, row=2, padx=24, pady=(12,36))
        self.cancel_all.grid_remove()

        self.bind('<Escape>', self.on_cancel)

        PlaySound('SystemHand', SND_ASYNC)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_ok(self, event=None):
        print('original input is OK; input is:', self.input)

    def on_alt(self, event=None):
        self.edit_input = True
        self.destroy()

    def on_cancel(self, event=None):
        self.add_data_to_db = False
        self.destroy()

class AltInputMessage(MessageModel):
    def __init__(
            self, 
            parent, 
            gparent=None, 
            prompt=None, 
            message=None, 
            input_text=None, *args, **kwargs):
        MessageModel.__init__(self, parent, *args, **kwargs)

        self.gparent = gparent

        self.promptlab.grid()
        self.altentry.grid()

        self.promptlab.config(text=prompt)

        self.errshow.config(text=input_text)
        self.input_text = input_text

        self.errmsg.config(text=message)

        self.accept.grid()
        self.edit.grid()
        self.cancel_all.grid()

        ST.config_generic(self)

    def show(self):
        self.wm_deiconify()
        self.altentry.focus_force()
        self.wait_window() # won't work without this
        # Get return values accurate on window closing:
        return self.var.get(), self.edit_input, self.add_data_to_db      

class YesNoMessage(MessageModel):
    def __init__(self, parent, message=None, show_input=None, *args, **kwargs):
        MessageModel.__init__(self, parent, *args, **kwargs)

        self.show_input = show_input

        self.errshow.config(text=self.show_input)

        self.errmsg.config(text=message)
        self.done.config(text='SUBMIT')
        self.done.grid()
        self.stop.grid()

        ST.config_generic(self)

    def on_ok(self):
        self.parent.focus_set()
        self.destroy() 

    def show(self):
        self.wm_deiconify()
        self.wait_window() # won't work without this
        # Get return values accurate on window closing:
        return self.add_data_to_db

class ErrorMessage(MessageModel):
    def __init__(self, parent, message=None, input_text=None, *args, **kwargs):
        MessageModel.__init__( self, parent, *args, **kwargs)

        if input_text:
            self.errshow.config(text=input_text)
        else:
            self.errlab.grid_forget()

        self.errmsg.config(text=message)

        self.done.grid()

        self.done.config(command=self.cancel)

        ST.config_generic(self)

    def cancel(self):
        self.destroy()

if __name__ == "__main__":

    def open_generic_dialog():
        model = MessageModel(root)

    root = tk.Tk()
    root.geometry("400x200")
    root.iconbitmap(default='c:/treebard_gps/favicon.ico')

    button = Button(root, text="generic dialog", command=open_generic_dialog)
    label = tk.Label(root, text="", width=20)
    button.grid()
    label.grid()
    label2 = tk.Label(root, text="", width=20)
    label2.grid()

    input_text = 'abcdefg'


    # # SAMPLE INSTANCE ERROR MESSAGE
    # err = ErrorMessage(
        # root,
        # title='About Your Mistake',
        # message="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ac arcu quis justo maximus ultrices ac dignissim risus. In vitae facilisis nisl, eu pretium magna. Cras eros lacus, elementum nec odio vitae, dignissim vulputate diam. Pellentesque eget nulla semper, rhoncus leo tristique, hendrerit ligula. ",
        # input_text=input_text)

    # SAMPLE INSTANCE YES/NO MESSAGE

    yn = YesNoMessage(
        root,
        title='What Next?',
        message="Vestibulum feugiat mattis aliquet. Nunc et diam sed quam aliquam elementum sit amet ac dui. Aliquam convallis mi nec elit rutrum luctus. Vestibulum sed erat vitae est faucibus ullamcorper. Curabitur lacinia non arcu vitae varius.",
        input_text=input_text)

    # # SAMPLE INSTANCE ALT INPUT MESSAGE

    # altin = AltInputMessage(
        # root,
        # title='Change That?',
        # message="Maecenas quis elit eleifend, lobortis turpis at, iaculis odio. Phasellus congue, urna sit amet posuere luctus, mauris risus tincidunt sapien, vulputate scelerisque ipsum libero at neque. Nunc accumsan pellentesque nulla, a ultricies ex convallis sit amet. Etiam ut sollicitudin felis, sit amet dictum lacus. Mauris sed mattis diam.",
        # prompt='Replace input:',
        # input_text=input_text)
    # # data = altin.show() # run selectively per button not like this
    # # label2.config(text='You entered:\n' + data)

    root.mainloop()

# ORIGINAL CODE BY BRYAN OAKLEY DO NOT DELETE (how to return input from dialog)

# class CustomDialog(tk.Toplevel):
    # def __init__(self, parent, prompt):
        # tk.Toplevel.__init__(self, parent)

        # self.var = tk.StringVar()

        # self.label = tk.Label(self, text=prompt)
        # self.entry = tk.Entry(self, textvariable=self.var)
        # self.ok_button = Button(self, text="OK", command=self.on_ok)

        # self.label.pack(side="top", fill="x")
        # self.entry.pack(side="top", fill="x")
        # self.ok_button.pack(side="right")

        # self.entry.bind("<Return>", self.on_ok)

    # def on_ok(self, event=None):
        # self.destroy()

    # def show(self):
        # self.wm_deiconify()
        # self.entry.focus_force()
        # self.wait_window() # won't work without this
        # return self.var.get() # ?Because this gets the value of var on close?

# class Example(tk.Frame):
    # def __init__(self, parent):
        # tk.Frame.__init__(self, parent)
        # self.button = Button(self, text="Get Input", command=self.on_button)
        # self.label = tk.Label(self, text="", width=20)
        # self.button.pack(padx=8, pady=8)
        # self.label.pack(side="bottom", fill="both", expand=True)

    # def on_button(self):
        # string = CustomDialog(self, "Enter something:").show()
        # self.label.configure(text="You entered:\n" + string)


# if __name__ == "__main__":
    # root = tk.Tk()
    # root.wm_geometry("400x200")
    # Example(root).pack(fill="both", expand=True)
    # root.mainloop()
