# toykinter_widgets.py

from widgets import Framex, FrameStay, Labelx, Frame, Label, make_formats_dict, LabelStatusbar
from files import app_path
from PIL import Image, ImageTk
import dev_tools as dt
from dev_tools import looky, seeline




formats = make_formats_dict()

def run_statusbar_tooltips(visited, status_label, tooltip_label):
    '''
        Uses lambda to add args to event
        since tkinter expects only one arg in a callback.
    '''

    def handle_statusbar_tooltips(event):
        for tup in visited:
            if tup[0] is event.widget:
                if event.type == '9': # FocusIn
                    status_label.config(text=tup[1])
                elif event.type == '10': # FocusOut
                    status_label.config(text='')
                elif event.type == '7': # Enter
                    tooltip_label.grid(
                        column=1, row=0, 
                        sticky='e', padx=(6,24))
                    tooltip_label.config(
                        text=tup[2],
                        bg='black',
                        fg='white',
                        font=LabelStatusbar.formats["status"])
                elif event.type == '8': # Leave
                    tooltip_label.grid_remove()
                    tooltip_label.config(
                        bg=formats['bg'], text='', fg=formats['bg'])

    statusbar_events = ['<FocusIn>', '<FocusOut>', '<Enter>', '<Leave>']

    for tup in visited:
        widg = tup[0]
        status = tup[1]
        tooltip = tup[2]
        for event_pattern in statusbar_events:
            # error if tup[0] has been destroyed 
            #   so don't use these with destroyable widgets
            # different tooltips are available in utes.py
            widg.bind(event_pattern, handle_statusbar_tooltips, add='+')

        status_label.config(font=formats['status'])






