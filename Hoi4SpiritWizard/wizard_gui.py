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
        # internal dicts
        self.labels = {}
        self.entries = {}
        self.spacers = []
        self.cat_add_buttons = {}
        self.cat_rem_buttons = {}
        self.cat_start_row = {}
        self.cat_end_row = {}
        self.cat_row_dist = {}
        self.cat_start_col = {}
        self.cat_end_col = {}
        self.cat_entries = {}
        self.category_map = {cat.get_name(): cat for cat in Idea.CATEGORIES}
        
        # Make x Button use inside method
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        
        self.set_gui()
        #self.getScratch(self.scratch_file)

    def set_gui(self):
        self.master.title("HOI4 Idea Wizard")
        self.setup_menu()
        self.set_basic_params(1,1)
        self.write_button_col = 0
        row, col  = self.set_idea_fields(2,1)
        self.spacer = self.set_label(row, col,"")
        row += 1;
        for cat in Idea.CATEGORIES:
            row, col = self.init_category(cat, row, col)
        
        self.set_write_button(row+1,self.write_button_col)
        self.write_button_row = row+1
        


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

    def init_category(self, category_cls, row, col):
        cat_name = category_cls.get_name()
        orig_col = col
        self.cat_start_row[cat_name] = row
        self.cat_start_col[cat_name] = col
        self.labels[cat_name] = self.set_label(row, col, cat_name + ': ')
        self.cat_entries[cat_name] = []
        
        row += 1; col += 1
        for i, key in enumerate(category_cls.get_fields()):
            self.labels[cat_name+key] = self.set_label(row, col+i, key, anchor="center", columnspan=1)
        row +=1; col += 1
        self.cat_end_row[cat_name] = row
        self.cat_end_col[cat_name] = col
        def add_category_line(): self.add_category_line(category_cls)
        self.cat_add_buttons[cat_name] = self.set_button(row,col,' + ', add_category_line,
                                                         fg='#00FF00', bg='#000000')
 
        def rem_category_line(): self.rem_category_line(category_cls)
        self.cat_rem_buttons[cat_name] = self.set_button(row,col+1,' - ', rem_category_line,
                                                         fg='#FF0000', bg='#000000')
        
        self.cat_row_dist[cat_name] = self.cat_end_row[cat_name] - self.cat_start_row[cat_name]
        
        return row + 1, orig_col

    def get_categories_below(self, category_cls):
        cat_name = category_cls.get_name()
        ind = self.cat_end_row[cat_name]
        below = [cat for cat in Idea.CATEGORIES if self.cat_start_row[cat.get_name()] >= ind]
        return below

    def shift_category(self, category_cls, shift=-1):
        cat_name = category_cls.get_name()
        cat_srow = self.cat_start_row[cat_name]
        
        cat_col = self.cat_start_col[cat_name]
        # shift labels
        self.labels[cat_name].grid(row=cat_srow + shift, column=cat_col)
        for i, key in enumerate(category_cls.get_fields()):
            self.labels[cat_name+key].grid(row=cat_srow + shift + 1, column=cat_col+1+i)
        # shift entries
        entries = self.cat_entries[cat_name]
        for k,entry in enumerate(entries):
            for i, key in enumerate(category_cls.get_fields()):
                entry[key].grid(row=cat_srow+k+shift + 2, column=cat_col+i+1)

        self.cat_add_buttons[cat_name].grid(row=cat_srow+shift+3+len(entries),
                                            column=cat_col+len(category_cls.get_fields())+1)
        self.cat_rem_buttons[cat_name].grid(row=cat_srow+shift+3+len(entries),
                                            column=cat_col+len(category_cls.get_fields())+2)
        
        self.cat_start_row[cat_name] += shift
        self.cat_end_row[cat_name] += shift
        self.write_button_row += shift
        self.writeButton.grid(row=self.write_button_row,
                              column=self.write_button_col) 
        
    
    def add_category_line(self, category_cls):
        cat_name = category_cls.get_name()
        fields = {}
        col = self.cat_start_col[cat_name] + 1
        self.cat_end_row[cat_name] += 1
        row = self.cat_end_row[cat_name]
        
        for i, key in enumerate(category_cls.get_fields()):
            col += i
            fields[key] = self.set_entry(row, col, width=20,columnspan=1)
        col +=1
        
        self.cat_entries[cat_name] += [fields]
        self.cat_add_buttons[cat_name].grid(row=row,column=col+1)
        self.cat_rem_buttons[cat_name].grid(row=row,column=col+2)
        self.writeButton.grid(row=self.cat_end_row[cat_name]+1,
                              column=self.write_button_col)

        below = self.get_categories_below(category_cls)
        for bcat in below:
            self.shift_category(bcat,shift=1)

        self.write_button_row += 1
        self.writeButton.grid(row=self.write_button_row,
                              column=self.write_button_col) 
    
    def rem_category_line(self, category_cls):
        cat_name = category_cls.get_name()
        if self.cat_end_row[cat_name] - self.cat_start_row[cat_name] <= self.cat_row_dist[cat_name]:
            return
        
        entries = self.cat_entries[cat_name].pop()
        for entry in entries.values():
            self.remove(entry)
        self.cat_end_row[cat_name] -= 1
        row = self.cat_end_row[cat_name]
        col = self.cat_end_col[cat_name]
        self.cat_add_buttons[cat_name].grid(row=row,column=col+1)
        self.cat_rem_buttons[cat_name].grid(row=row,column=col+2)
        self.write_button_row -= 1
        self.writeButton.grid(row=self.write_button_row,
                              column=self.write_button_col) 

    def write_category(self, category_cls):
        cat_name = category_cls.get_name()
        entry_rows = self.cat_entries[cat_name]
        cobjs = []
        for entry_row in entry_rows:
            cobjs += [category_cls({key:val.get() for key,val in entry_row.items()})]
        self.idea.set_category_objs(category_cls, cobjs)
        
        
    def set_entry(self,row,col, master = None, columnspan=2, **kwargs):
        master = self.master if master is None else master
        entry = tk.Entry(master,**kwargs)
        entry.grid(row=row,column=col,columnspan=columnspan, rowspan=1)
        return entry

    def set_label(self,row,col, text, master = None, columnspan=1, rowspan=1, **kwargs):
        master = self.master if master is None else master
        entry = tk.Label(master, text=text, **kwargs)
        entry.grid(row=row,column=col,columnspan=columnspan, rowspan=rowspan)
        return entry

    def set_button(self, row, col, text, command, master=None, columnspan=1, rowspan=1,**kwargs):
        master = self.master if master is None else master
        button = tk.Button(master, text=text, command=command,**kwargs)
        button.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan)
        return button

    @staticmethod
    def remove(widget):
        widget.destroy()
    
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

        for category_cls in Idea.CATEGORIES:
            self.write_category(category_cls)
                
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

    
    
