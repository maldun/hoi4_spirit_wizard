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
        self.set_basic_params(1,1)


    def set_basic_params(self, row, col):
        self.idea_name_label = tk.Label(self.master,text='Idea Name: ')
        self.idea_name_label.grid(row=row, column=col,columnspan=1, rowspan=1)
        self.entries[Idea.NAME_KEY] = self.set_entry(row, col +1 )
        
    def set_entry(self,row,col):
        entry = tk.Entry(self.master)
        entry.grid(row=row,column=col,columnspan=2, rowspan=1)
        return entry

    def set_write_button(self,row,col):
        
        self.writeButton = tk.Button(self.master, text="Write", command=self.write_idea)
        self.writeButton.grid(row=row,column=col)

    def write_idea(self):
        pass
        
    def close_app(self):
        """
        Clean shutdown
        """
        self.master.quit()

def runApp():
    root = tk.Tk()
    app = WizardGui(master=root,height=200,width=200)
    app.mainloop()

if __name__ == "__main__":
    runApp()

    
    
