""" this method will select all .mat files from the chosen subject 
"""

# import packages
import os 
from dataclasses import dataclass

import json

# import PerceiveImport.filefunctions as filefuncs -> use this line to import other .py files
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
