import time, sched
import threading
import multiprocessing
import sys
import os
from .ideas import Idea

import tkinter as tk
from tkinter import dialog as Dialog
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox 
from tkinter import simpledialog as tkSimpleDialog

class WizardGui(tk.Frame):

    def __init__(self,master=None,**options):
        """
        Init method.
        Args:
          time_interval: Working time interval in minutes
          pause_interval: Pause interval in minutes
          master: tk master
          options: tk options
        """
        super().__init__(master,options)
        self.labels = {}
        self.entries = {}
        # set default states
        #self.setStates()
        # Set config file
        #self.getConfig(config_file_name)
        #self.setIntervals(self.work_time_in_units,self.pause_time_in_units)
        
        # Make x Button use inside method
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        
        self.set_gui()
        #self.getScratch(self.scratch_file)

    def set_gui(self):
        self.master.title("HOI4 Idea Wizard")
        self.setup_menu()
        self.set_basic_params(1,1)
        row, col  = self.set_idea_fields(2,1)
        self.set_write_button(row+1,col//2 + 1)


    def set_basic_params(self, row, col):
        self.labels[Idea.NAME_KEY] = tk.Label(self.master,text='Idea Name: ')
        self.labels[Idea.NAME_KEY].grid(row=row, column=col,columnspan=1, rowspan=1)
        self.entries[Idea.NAME_KEY] = self.set_entry(row, col +1 )

    def set_idea_fields(self, row, col):
        for key in Idea.KEYS:
            self.set_idea_row(row, col, key)
            row += 1
        return row, col

    def set_idea_row(self, row, col, key):
        self.labels[key] = self.set_label(row, col, key)
        self.entries[key] = self.set_entry(row, col + 1)
        
        
    def set_entry(self,row,col, master = None):
        master = self.master if master is None else master
        entry = tk.Entry(master)
        entry.grid(row=row,column=col,columnspan=2, rowspan=1)
        return entry

    def set_label(self,row,col, text, master = None):
        master = self.master if master is None else master
        entry = tk.Label(master, text=text)
        entry.grid(row=row,column=col,columnspan=1, rowspan=1)
        return entry

    def set_write_button(self,row,col):
        self.writeButton = tk.Button(self.master, text="Write", command=self.write_idea)
        self.writeButton.grid(row=row,column=col)

    def fields2idea(self):
        for key, entry in self.entries.items():
            content = entry.get()
            if content == '':
                if tkMessageBox.showwarning("Entry Missing", Idea.MISSING_ERROR_MSG.format(key)):
                    pass
                return
            else:
                setattr(self.idea, key, content)
                
    def get_file_names(self):
        gfx_file = self.file_prefix + Idea.GFX_SUFF
        loc_file = self.file_prefix + Idea.LOC_SUFF
        pdx_file = self.file_prefix + Idea.PDX_SUFF
        return gfx_file, loc_file, pdx_file
                
    def write_idea(self):
        self.fields2idea()
        idea_list = [self.idea]
        gfx_file, loc_file, pdx_file = self.get_file_names()
        Idea.write_gfx_file(idea_list, gfx_file)
        Idea.write_localisation_file(idea_list, loc_file)
        Idea.write_paradox_file(idea_list, pdx_file)
        
    def close_app(self):
        """
        Clean shutdown
        """
        self.master.quit()

    def start_new_idea(self):
        row = 0
        col = 0
        self.top_window = tk.Toplevel(self.master)
        self.top_window.wm_title('New Idea')
        self.new_name_label = tk.Label(self.top_window,text='Idea Identifier: ')
        self.new_name_label.grid(row=row, column=col,columnspan=1, rowspan=1)
        self.new_name_entry = self.set_entry(row, col +1, master = self.top_window)
        row += 1
        self.new_file_label = self.set_label(row, col, "File Prefix: ", master=self.top_window)
        self.new_file_entry = self.set_entry(row, col + 1, master=self.top_window)

        self.top_window.set_button = tk.Button(self.top_window,text='Start Idea',
                                               command=self.init_idea)
        self.top_window.set_button.grid(row=row,column=4)
        
    @staticmethod
    def set_entry_text(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)
        
    def init_idea(self):
        name = self.new_name_entry.get()
        if name == '':
            if tkMessageBox.showwarning("Name Missing", "Please Enter a Name!"):
                pass
            return
        
        self.idea = Idea(name)
        file_prefix = self.new_file_entry.get()
        self.file_prefix = name if file_prefix == '' else file_prefix
        self.set_entry_text(self.entries[Idea.NAME_KEY], name)
        self.top_window.destroy()

    def setup_menu(self):
        menubar = tk.Menu(self.master)
        
        mainmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=mainmenu)
        mainmenu.add_command(label="New Idea", command=self.start_new_idea)
        mainmenu.add_command(label="Quit", command=self.close_app)
        
        self.master.config(menu=menubar)

def runApp():
    root = tk.Tk()
    app = WizardGui(master=root,height=200,width=200)
    app.mainloop()

if __name__ == "__main__":
    runApp()

    
    
