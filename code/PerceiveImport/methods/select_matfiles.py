""" this method will select all .mat files from the chosen subject in respect of the chosen timing (postop, 3MFU, 12MFU, 18MFU, 24MFU) and datatype (Survey/Streaming/Timeline)
"""

# import packages
import os 
import json

import PerceiveImport.classes.PerceiveMainClass as MainClass


# import PerceiveImport.filefunctions as filefuncs -> use this line to import other .py files
# select all .mat files in respect of the correct datatype (Survey/Streaming/Timeline) 

datatype_dict = {
    "Survey": "LMTD",
    "Streaming": "BrainSense",
    "Timeline": "CHRONIC"
    }

matfile_list = [] # this list will contain all matfile names    
paths_list = [] # this list will contain all paths to the selected matfiles


# def select_matdatatype():
#      """
#     select_matdatatype() selects all .mat files within your chosen subject folder
#     Return: tuple[str, str] -> matfile_list, paths_list        
#     """
#     matfile_list = [] # this list will contain all matfile names
#     paths_list = [] # this list will contain all paths to the selected matfiles

#     with open('datatype_dict.json', 'r') as f: # read datatype_dict.json file with dictionary of datatypes
#         datatype_dict = json.loads(f.read())

#     for root, dirs, files in os.walk(MainClass.PerceiveData.data_path): # walking through every root, directory and file of the given path
#         for file in files: # looping through every file 
#             if file.endswith(".mat") and datatype_dict[MainClass.PerceiveData.data_type] in file: # matpart is defined earlier
#                 print(file) # printing makes sure, that every selected file is saved after a loop
#                 matfile_list.append(file) # adding every file to the list of matfile names
            
#                 single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
#                 paths_list.append(single_path) # add each path to the list selection_paths
        
# print('\n\tFilenames of the selected .mat files:') 
# print(matfile_list)
        
# print('\n\tList of paths to the selected .mat files:') 
# print(paths_list)


# # select all .mat files in respect of the correct timing (3MFU/12MFU/Postop)
# def select_mattiming():
#     """
#     select_mattiming() selects all .mat files within your project folder of a specific timing (postop, 3MFU, 12MFU, 18MFU, 24MFU)
#     Return: tuple[str, str] -> matfile_list, paths_list
#     """
#     matfile_list = [] # this list will contain all matfile names
#     paths_list = [] # this list will contain all paths to the selected matfiles

#     for root, dirs, files in os.walk(MainClass.PerceiveData.data_path): # walking through every root, directory and file of the given path
#         for file in files: # looping through every file 
#             if MainClass.PerceiveData.timing in root and file.endswith(".mat"):
#                 print(file) # printing makes sure, that every selected file is saved after a loop
#                 matfile_list.append(file) # adding every file to the list of matfile names
            
#                 single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
#                 paths_list.append(single_path) # add each path to the list selection_paths
        
# print('\n\tFilenames of the selected .mat files:') 
# print(matfile_list)
        
# print('\n\tList of paths to the selected .mat files:') 
# print(paths_list)
    
    
# selecting final selection of .mat files
# in respect of timing and datatype
def select_mat_timing_datatype():
    """
    select_mat_timing_datatype() selects all .mat files within your project folder 
    of a specific timing (postop, 3MFU, 12MFU, 18MFU, 24MFU) 
    and of a specific datatype (Survey, Streaming, Timeline)

    Return: tuple[str, str] -> matfile_list, paths_list
    """

    for root, dirs, files in os.walk(MainClass.PerceiveData.data_path): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            if MainClass.PerceiveData.timing in root and file.endswith(".mat") and datatype_dict[MainClass.PerceiveData.data_type] in file: # datatype_dict is defined earlier
                print(file) # printing makes sure, that every selected file is saved after a loop
                matfile_list.append(file) # adding every file to the list of matfile names
            
                single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                paths_list.append(single_path) # add each path to the list selection_paths
        
    print ('\n\tFilenames of the selected .mat files:', matfile_list)

    print ('\n\tList of paths to the selected .mat files:', paths_list)

