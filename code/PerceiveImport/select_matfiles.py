""" this method will select all .mat files from the chosen subject 
"""

# import packages
import os 
from dataclasses import dataclass

import json

# import PerceiveImport.filefunctions as filefuncs -> use this line to import other .py files

@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: subject name called sub-xxx, e.g. sub-021
        - data_path: path to the sub-xxx folder with all files from this subject
        - timing: timing of session, e.g. "3MFU", "12MFU", "Postop"
        - data_type: choose between "Survey", "Streaming", "Timeline"
        
    Returns:
        - every method returns a list of the selected .mat filenames and of their paths
        
        select_mat()
        - selects all .mat files
        
        select_timing()
        - selects all .mat files from a certain timing (3MFU, 12MFU,Postop)
        
        select_final():
        - selects .mat files of the correct subject, from a certain timing folder and of a certain data_type
    

        
    """
    
    # these fields will be initialized 
    sub: str            # note that : is used, not = 
    data_path: str 
    timing: str
    data_type: str
        
    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        print(self.sub)
        self.files=os.listdir(self.data_path) # self.files can only run after initialisation because it needs self.data_path
        
    def __str__(self,):
        return f'From the Perceived data from subject {self.sub} all BrainSense {self.data_type} .mat files from the {self.timing} session are being selected.'

             
    # select all .mat files in respect of the correct datatype (Survey/Streaming/Timeline) 
    def select_matdatatype(self,):
        matfile_list = [] # this list will contain all matfile names
        paths_list = [] # this list will contain all paths to the selected matfiles

        with open('matpart.json', 'r') as f: # read matpart.json file with dictionary of datatypes
            matpart = json.loads(f.read())

        for root, dirs, files in os.walk(self.data_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if file.endswith(".mat") and matpart[self.data_type] in file: # matpart is defined earlier
                    print(file) # printing makes sure, that every selected file is saved after a loop
                    matfile_list.append(file) # adding every file to the list of matfile names
            
                    single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                    paths_list.append(single_path) # add each path to the list selection_paths
        
        print('\n\tFilenames of the selected .mat files:') 
        print(matfile_list)
        
        print('\n\tList of paths to the selected .mat files:') 
        print(paths_list)


    # select all .mat files in respect of the correct timing (3MFU/12MFU/Postop)
    def select_mattiming(self,):
        matfile_list = [] # this list will contain all matfile names
        paths_list = [] # this list will contain all paths to the selected matfiles

        for root, dirs, files in os.walk(self.data_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if self.timing in root and file.endswith(".mat"):
                    print(file) # printing makes sure, that every selected file is saved after a loop
                    matfile_list.append(file) # adding every file to the list of matfile names
            
                    single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                    paths_list.append(single_path) # add each path to the list selection_paths
        
        print('\n\tFilenames of the selected .mat files:') 
        print(matfile_list)
        
        print('\n\tList of paths to the selected .mat files:') 
        print(paths_list)
    
    
    # selecting final selection of .mat files
    # in respect of timing and datatype
    def select_matfinal(self,):
        matfile_list = [] # this list will contain all matfile names
        paths_list = [] # this list will contain all paths to the selected matfiles

        with open('matpart.json', 'r') as f: # read matpart.json file with dictionary of datatypes
            matpart = json.loads(f.read())

        for root, dirs, files in os.walk(self.data_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if self.timing in root and file.endswith(".mat") and matpart[self.data_type] in file: # matpart is defined earlier
                    print(file) # printing makes sure, that every selected file is saved after a loop
                    matfile_list.append(file) # adding every file to the list of matfile names
            
                    single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                    paths_list.append(single_path) # add each path to the list selection_paths
        
        print('\n\tFilenames of the selected .mat files:') 
        print(matfile_list)
        
        print('\n\tList of paths to the selected .mat files:') 
        print(paths_list)
