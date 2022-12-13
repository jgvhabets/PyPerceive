'''
this is a tool to relabel any file, filecontent or directory based on regular expressions
made by Jonathan Vanhoecke for the Neumann ICN Lab
01/01/2021
last update: 17.02.2022
'''
literal=False
doyouwanttkinter=True
#get target folder
#path_target_folder=r"C:\Users\Jonathan\Documents\DATA\PROJECT_Tiantan\conversion_room\rawdata"
#path_target_folder=r"C:\Users\Jonathan\Charité - Universitätsmedizin Berlin\Interventional Cognitive Neuromodulation - Data\BIDS_Tuebingen"
#path_target_folder=r"C:\Users\Jonathan\Documents\DATA\PROJECT_Tiantan\conversion_room\electrodes"
path_target_folder=r"C:\Users\Jonathan\Charité - Universitätsmedizin Berlin\Interventional Cognitive Neuromodulation - Data\BIDS_Berlin_ECOG_LFP\rawdata"
back_up_folder=r"C:\Users\Jonathan\Documents\DATA\PROJECT_Berlin_dev\backup"

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from datetime import datetime
from functools import partial
import glob
import os
from os.path import splitext
import re
import pandas as pd
import numpy
import pathlib
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import time
from functools import partial
import tkinter as tk
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from datetime import datetime
from functools import partial
import webbrowser


#################### INITIATE VARIABLES

ext_excluded = set()
dirs_excluded =set()
# what are you looking for?
#target_expression = "ses-001"
#change_into = "ses-20171014"



######################################### OPTEN TKINTER PART 1 ###########################################
###########################################################################################################

######################################### define functions ###################################################
def browse_button():
    global path_target_folder
    path_target_folder = filedialog.askdirectory()
    global lb_22
    lb_22.config(text=path_target_folder)

def callback(url):

    webbrowser.open_new(url)

go1=False
def setgo1():
    global go1
    go1=True
    search()
    global target_expression_list, change_into_list
    target_expression_list=entry_target_expression.get("1.0", tk.END)
    target_expression_list=target_expression_list.split("\n")
    change_into_list = entry_change_into.get("1.0", tk.END)
    change_into_list = change_into_list.split("\n")
    target_expression_list[:] = [x for x in target_expression_list if x]
    change_into_list[:] = [x for x in change_into_list if x]


    window.destroy()

    if len(target_expression_list)!=len(change_into_list):
        if len(target_expression_list)==1:
            change_into_list=[''] # which means you will remove the target expression
        else:
            error("len target_expression must be equal to len change into")





def confirm_checkboxes():


        if 'cbs_ext' in globals():
            global ext_excluded
            for i, checks in enumerate(cbs_ext):
                if checks.instate(['!selected']):
                    ext_excluded.add(ext_found[i])

        if 'cbs_subfolders' in globals():
            global dirs_excluded
            for i, checks in enumerate(cbs_subfolders):
                if checks.instate(['!selected']):
                    dirs_excluded.add(list_of_paths_subfolders[i])

def search():

    confirm_checkboxes()
    global search_subfolders_boolean, list_of_paths_subfolders, list_of_paths_files, ext_found

    search_subfolders_boolean = chk_include_subfolders.instate(['selected'])

    list_of_paths_subfolders, list_of_paths_files, ext_found = list_dirs_and_files(path_target_folder, ext_excluded,
                                                                                   dirs_excluded,
                                                                                   search_subfolders_boolean)



    global Frame_ext

    lb_8 = tk.Label(text="included filetypes: ", master=frame, bg="deep pink",
                    anchor="e")
    lb_8.grid(row=8, column=1, sticky=E + W, padx=5, pady=5)

    Frame_ext = tk.Frame(master=frame, bg="blue")
    Frame_ext.grid(row=8, column=2, padx=5, pady=5, sticky=W)

    #button_confirm = tk.Button(master=Frame_ext, text="Confirm selection to search my regex",
                               # command= partical(blabalbal) #
                               #command=confirm_checkboxes)  # print(3))#(
    # root).confirm_checkboxes(3))
    #button_confirm.pack(padx=5, pady=5, side="left")

    vsb = tk.Scrollbar(Frame_ext, orient="vertical")
    text = tk.Text(Frame_ext, height=15, width=150,
                   yscrollcommand=vsb.set)
    vsb.config(command=text.yview)
    vsb.pack(side="left", fill="y")
    text.pack(side="left", fill="both")#, expand=True)

    #vars = []
    global cbs_ext
    cbs_ext = []

    for i, ext in enumerate(ext_found):
        #var = tk.IntVar()

        cb = ttk.Checkbutton(Frame_ext, text="file%s" % ext)  # ,onvalue=1,offvalue=0)

        cb.state(['!alternate'])
        cb.state(['selected'])

        text.window_create("end", window=cb)
        text.insert("end", "\n")  # to force one checkbox per line
        #vars.append(var)
        cbs_ext.append(cb)
    text.config(state="disabled")
    #### seach in subfolders

    if search_subfolders_boolean:

        global Frame_subfolders

        lb_9 = tk.Label(text="included subfolders: ", master=frame, bg="deep pink",
                        anchor="e")
        lb_9.grid(row=9, column=1, sticky=E + W, padx=5, pady=5)

        Frame_subfolders = tk.Frame(master=frame, bg="black")
        Frame_subfolders.grid(row=9, column=2, padx=5, pady=5, sticky=W)

        #button_confirm = tk.Button(master=Frame_ext, text="Confirm selection to search my regex",
         #                          # command= partical(blabalbal) #
          #                         command=confirm_checkboxes)  # print(3))#(
        # root).confirm_checkboxes(3))
        #button_confirm.pack(padx=5, pady=5, side="left")

        vsb2 = tk.Scrollbar(Frame_subfolders, orient="vertical")
        vsb3 = tk.Scrollbar(Frame_subfolders, orient="horizontal")
        text2 = tk.Text(Frame_subfolders, height=15, width=150,
                       yscrollcommand=vsb2.set, xscrollcommand=vsb3.set)
        vsb2.config(command=text2.yview)
        vsb2.pack(side="left", fill="y")


        vsb3.config(command=text2.xview)
        vsb3.pack(side="bottom", fill="x")
        text2.pack(side="left", fill="both")#, expand=True)

        global cbs_subfolders
        cbs_subfolders = []

        for i, subfolder in enumerate(list_of_paths_subfolders):
            #var = tk.IntVar()

            cb = ttk.Checkbutton(Frame_subfolders, text="%s " % subfolder)  # ,onvalue=1,offvalue=0)

            cb.state(['!alternate'])
            cb.state(['selected'])

            text2.window_create("end", window=cb)
            text2.insert("end", "\n")  # to force one checkbox per line
            #vars.append(var)
            cbs_subfolders.append(cb)
        text2.config(state="disabled")


# how to find all files and dirs regardless of what you are looking for but filtered on extension
def splitext_strong(path):
    return ''.join(pathlib.Path(path).suffixes)


def list_dirs_and_files(dirs, ext_excluded, dirs_excluded, search_subfolders_boolean=True):  # dir: str, ext: set
    list_of_paths_subfolders, list_of_paths_files, ext_found = [], [], []
    ext_found = set()
    for f in os.scandir(dirs):
        if f.is_dir() and search_subfolders_boolean:
            fpath = f.path
            if fpath not in dirs_excluded:
                list_of_paths_subfolders.append(fpath)
        if f.is_file():
            current_ext = str(splitext_strong(f.name))
            print(current_ext)
            current_ext = current_ext.lower()
            if current_ext not in ext_excluded:  # check whether you get the right extension in nii.gz
                # files
                list_of_paths_files.append(f.path)
                ext_found.add(current_ext)
    if search_subfolders_boolean:
        for dirs in list(list_of_paths_subfolders):
            if dirs not in dirs_excluded:
                sf, f, exs = list_dirs_and_files(dirs, ext_excluded, dirs_excluded)
                list_of_paths_subfolders.extend(sf)
                list_of_paths_files.extend(f)
                ext_found.update(exs)
    return list_of_paths_subfolders, list_of_paths_files, list(ext_found)


def onFrameConfigure(canvas): # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


############################### start of the MAIN CODE ###########################################################################

window = tk.Tk()
window.geometry("1230x620")
window.title("Relabelling Tool - ICN Neumann Lab")
window.resizable(True, True)
#path_target_folder="none"

canvas = tk.Canvas(window, borderwidth=0, background="black")
frame = tk.Frame(canvas, background="black")
vsb = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))



lb_1 = tk.Label(text="select the folder: ", master=frame, bg="deep pink", anchor="e")
lb_1.grid(row=1,column=1, sticky=E+W,  padx=5, pady=5)

button_browse = tk.Button(master=frame, text="Browse folder", command=browse_button)
button_browse.grid(row=1 , column=2, sticky="w", padx=5, pady=5)

lb_2 = tk.Label(text="selected folder: ", master=frame, bg="deep pink", anchor="e")
lb_2.grid(row=2,column=1, sticky=E+W,  padx=5, pady=5)

lb_22 = tk.Label(text=path_target_folder, master=frame, bg="white", anchor="w")
lb_22.grid(row=2,column=2, sticky=E+W,  padx=5, pady=5)

lb_3 = tk.Label(text="find regular expression: ", master=frame, bg="deep pink",
                anchor="e")
lb_3.grid(row=3,column=1, sticky=E+W,  padx=5, pady=5)

current_folder_structure = ScrolledText(master=frame, width=100, background='white')
current_folder_structure.grid(row=3 , column=2, sticky="w", padx=5, pady=5)


entry_target_expression = ScrolledText(master=frame, width=100, background='white')
entry_target_expression.grid(row=3 , column=2, sticky="w", padx=5, pady=5)
#entry_target_expression.insert("e.g. ses-[0-9]*")

lb_4 = tk.Label(text="change match into: ", master=frame, bg="deep pink", anchor="e")
lb_4.grid(row=4,column=1, sticky=E+W,  padx=5, pady=5)

entry_change_into = ScrolledText(master=frame, width=100, background='green')
entry_change_into.grid(row=4, column=2, sticky="w", padx=5, pady=5)
#entry_change_into.insert(0,"e.g. session-ecog")

lb_5 = tk.Label(text="further information: ", master=frame, bg="deep pink", anchor="e")
lb_5.grid(row=5,column=1, sticky=E+W,  padx=5, pady=5)

link1 = Label(text="click here to test my regexr", master=frame, fg="white", bg="black", cursor="hand2", anchor="w")
link1.grid(row=5,column=2, sticky=E+W)
link1.bind("<Button-1>", lambda e: callback("https://regexr.com/"))

lb_6 = tk.Label(text="search for subfolders: ", master=frame, bg="deep pink", anchor="e")
lb_6.grid(row=6,column=1, sticky=E+W,  padx=5, pady=5)

chk_include_subfolders = ttk.Checkbutton(master=frame)
chk_include_subfolders.grid(row=6, column=2, sticky=W, padx=5, pady=5)
chk_include_subfolders.state(['!alternate'])
chk_include_subfolders.state(['selected'])

lb_7 = tk.Label(text="determine filetypes and/or subfolders: ", master=frame,
                bg="deep pink",
                anchor="e")
lb_7.grid(row=7, column=1, sticky=E+W,  padx=5, pady=5)

button_search = tk.Button(master=frame, text="Explore current selection/ update my selection", command=search)
button_search.grid(row=7 , column=2, sticky="w", padx=5, pady=5)

button_confirm = tk.Button(master=frame, text="Save selection and search my regex",
                                      command=setgo1)
button_confirm.grid(row=10, column=2, sticky="w", padx=5, pady=5)


#######


window.mainloop()

# confirm your chose for regex into changes
window = tk.Tk()
for i in range(len(target_expression_list)):  # Rows

    b = tk.Label(window,text=target_expression_list[i])
    b.grid(row=i, column=1)
    b = tk.Label(window,text=change_into_list[i])
    b.grid(row=i, column=2)

window.mainloop()
