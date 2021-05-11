# treebard_backup

import tkinter as tk
import os
import shutil
import datetime
import time
import dev_tools as dt

#

class BackupTreebard(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        self.title("Backup Treebard during development")
        self.now = datetime.datetime.now()
        self.make_widgets()

    def back_up_treebard(self):
        lm_logs_concat = []
        paths = (
            "/treebard_gps/app/python",
            "/treebard_gps/app/default",
            "/treebard_gps",
            "/treebard_gps/www",
            "/treebard_gps/www/css",
            "/treebard_gps/etc",
            "/treebard_gps/data/sample_tree",
            "/treebard_gps/data/settings")

        new_backups_folder = "tbard_dev_" + self.now.strftime("%Y%m%d%H%M")

        for folder in paths:



            default_path = folder
 
            # default_path = "/treebard_gps/app/python"

            os.chdir(default_path) 

            src = os.getcwd()
            print('26 src is', src) # C:\treebard_gps\app\python
            os.chdir("/treebard_2021/backups")

            if os.path.isdir(new_backups_folder) is False:
                os.mkdir(new_backups_folder)

            # os.mkdir(new_backups_folder)

            print('29 new_backups_folder is', new_backups_folder) # tbard_dev_202103041804

            last_modified_datetimes = []
            src_files = os.listdir(src)
            # print('33 src_files is', src_files)
    # 33 src_files is ['backup.pyw', 'colorizer.py', 'custom_listbox_widget.py', 'custom_window_border.py', 'dates.py', 'date_validation_model_refactor.py', 'date_validation_new_model_02.py', 'date_validation_new_model_03.py', 'date_validation_new_model_part_2.py', 'dev_tools.py', 'events_table.py', 'favicon.ico', 'files.py', 'gallery.py', 'images', 'insert_many_tool_sqlite.py', 'label_turns_into_entry.py', 'messages.py', 'message_strings.py', 'model_treebard_structure_2021.py', 'names.py', 'new 1.py', 'new 1.txt', 'new_concept_combobox.py', 'notes.py', 'pedigree_chart.py', 'person_maker.py', 'resurrect_notes_table.txt', 'right_click_menu.py', 'roles.py', 'sample_tree_feb_8.tbd', 'styles.py', 'test_date_in_out.db', 'toykinter_combobox_widget.py', 'treebard_root_017.py', 'treebard_root_018.py', 'utes.py', 'widgets.py', '__pycache__']
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, new_backups_folder)
                    lm = (
                        "\n" + file_name + 
                        "\n\tLast modified: %s" % 
                        time.ctime(os.path.getmtime(full_file_name)))
                    last_modified_datetimes.append(lm)
            lm_log = "".join(last_modified_datetimes) # a string
        # print('45 lm_log is', lm_log)
            lm_logs_concat.append(lm_log)

        lm_logs_concat = '\n'.join(lm_logs_concat)




        tried = self.texts["completed/begun/attempted since last backup"].get(1.0, tk.END)
        problems = self.texts["description of known problems"].get(1.0, tk.END)
        goals = self.texts["immediate goals"].get(1.0, tk.END)
        notes = self.texts["notes"].get(1.0, tk.END)

        log_text = (
            self.now.strftime("%c") + 
            "\nTried: " + tried + 
            "Problems: " + problems + 
            "Goals: " + goals + 
            "Notes: " + notes +
            # lm_log)
            lm_logs_concat)

        os.chdir(new_backups_folder) 

        log = open("rollback_log.txt", "w+")
        log.write(log_text)
        log.close()

        self.withdraw()
        self.cancel()

    def make_widgets(self):

        self.texts = {}

        self.text_names = [
            "completed/begun/attempted since last backup",
            "description of known problems",
            "immediate goals",
            "notes"]

        datestamp_display = tk.Label(
            self,
            text="This window opened at " + self.now.strftime("%c"))
        datestamp_display.grid(column=0, row=0, padx=24, pady=24)

        self.row_counter = len(self.text_names)
        y = 0
        for name in self.text_names:
            lab = tk.Label(
                self,
                text=self.text_names[y])
            lab.grid(column=0, row=self.row_counter+y, sticky='e')
            txt = tk.Text(
                self,
                width=50, height=5)
            txt.grid(column=1, row=self.row_counter+y, padx=24, pady=6)
            self.texts[name] = txt
            y+= 1

        ok = tk.Button(
            self,
            text="BACKUP",
            command=self.back_up_treebard)
        cancel_button = tk.Button(
            self,
            text="CANCEL",
            command=self.cancel)

        last_text_row = self.texts["notes"].grid_info()["row"]

        self.texts["completed/begun/attempted since last backup"].focus_set()
        ok.grid(row=last_text_row+1, column=0, padx=24, pady=24)
        cancel_button.grid(row=last_text_row+1, column=1, padx=24, pady=24)

        self.bind_class("Text", "<Tab>", self.focus_next_window)
        self.bind_class("Text", "<Shift-Tab>", self.focus_prev_window)

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    def focus_prev_window(self, event):
        event.widget.tk_focusPrev().focus()
        return("break")

    def cancel(self):
        self.destroy() 

if __name__ == '__main__':

    root = tk.Tk()

    root.withdraw()
    backup_dialog = BackupTreebard(root)

    root.mainloop()