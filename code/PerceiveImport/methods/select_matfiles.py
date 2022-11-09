""" this method will select all .mat files from the chosen subject in respect of the chosen timing (postop, 3MFU, 12MFU, 18MFU, 24MFU) and datatype (Survey/Streaming/Timeline)
"""

# import packages
import os 
import json

import PerceiveImport.methods.find_folders as find_folder


# import PerceiveImport.filefunctions as filefuncs -> use this line to import other .py files
# select all .mat files in respect of the correct datatype (Survey/Streaming/Timeline) 

datatype_dict = {
    "Survey": "LMTD",
    "Streaming": "BrainSense",
    "Timeline": "CHRONIC"
    }

matfile_list = [] # this list will contain all matfile names    
paths_list = [] # this list will contain all paths to the selected matfiles

def select_matdatatype(sub, data_type):
    """
    select_matdatatype() selects all .mat files within your chosen subject folder with respect to a specific datatype

    sub = name of subject folder, for example -> "sub-021"
    data_type = "Survey", "Streaming", "Timeline"

    Return: tuple[str, str] -> matfile_list, paths_list        
    """
    
    _, data_path = find_folder.find_project_folder()
    subject_path = os.path.join(data_path, sub)

    for root, dirs, files in os.walk(subject_path): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            if file.endswith(".mat") and datatype_dict[data_type] in file: # matpart is defined earlier
                print(file) # printing makes sure, that every selected file is saved after a loop
                matfile_list.append(file) # adding every file to the list of matfile names
            
                single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                paths_list.append(single_path) # add each path to the list selection_paths
        
    return matfile_list, paths_list


# # select all .mat files in respect of the correct timing (3MFU/12MFU/Postop)
def select_mattiming(sub, timing):
    """
    select_mattiming() selects .mat files within your project folder of a specific timing (postop, 3MFU, 12MFU, 18MFU, 24MFU)
    
    sub = name of subject folder, for example -> "sub-021")
    timing = str for example -> "postop", "3MFU", "12MFU", "18MFU", "24MFU"

    Return: tuple[str, str] -> matfile_list, paths_list
    """

    _, data_path = find_folder.find_project_folder()
    subject_path = os.path.join(data_path, sub)

    for root, dirs, files in os.walk(subject_path): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            if timing in root and file.endswith(".mat"):
                print(file) # printing makes sure, that every selected file is saved after a loop
                matfile_list.append(file) # adding every file to the list of matfile names
            
                single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                paths_list.append(single_path) # add each path to the list selection_paths
        
    return matfile_list, paths_list
    
    
# selecting final selection of .mat files
# in respect of timing and datatype
def select_mat_timing_datatype(sub, timing, data_type):
    """
    select_mat_timing_datatype() selects all .mat files within your project folder 
    of a specific timing (postop, 3MFU, 12MFU, 18MFU, 24MFU) 
    and of a specific datatype (Survey, Streaming, Timeline)

    sub = name of subject folder, for example -> "sub-021"
    timing = "postop", "3MFU", "12MFU", "18MFU", "24MFU"
    data_type = "Survey", "Streaming", "Timeline"

    Return: tuple[str, str] -> matfile_list, paths_list
    """

    _, data_path = find_folder.find_project_folder()
    subject_path = os.path.join(data_path, sub)

    for root, dirs, files in os.walk(subject_path): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            if timing in root and file.endswith(".mat") and datatype_dict[data_type] in file: # datatype_dict is defined earlier
                print(file) # printing makes sure, that every selected file is saved after a loop
                matfile_list.append(file) # adding every file to the list of matfile names
            
                single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                paths_list.append(single_path) # add each path to the list selection_paths
        
    return matfile_list, paths_list

