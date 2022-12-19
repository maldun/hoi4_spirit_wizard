import time, sched
import threading
import multiprocessing
import sys
import os

import tkinter as tk
from tkinter import dialog as Dialog
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox 
from tkinter import simpledialog as tkSimpleDialog

class WizardGui(tk.frame):

    def __init__(self,master=None,**options):
        """
        Init method. 
        Args:
          time_interval: Working time interval in minutes
          pause_interval: Pause interval in minutes
          master: tk master
          options: tk options
        """
        super(SnakeTomato,self).__init__(master,options)
        
        # set default states
        #self.setStates()
        # Set config file
        #self.getConfig(config_file_name)
        #self.setIntervals(self.work_time_in_units,self.pause_time_in_units)
        
        # Make x Button use inside method
        self.master.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        #self.setGUI()
        #self.getScratch(self.scratch_file)

def runApp():
    root = tk.Tk()
    app = SnakeTomato(master=root,height=200,width=200)
    app.mainloop()

if __name__ == "__main__":
    runApp()

    
    
