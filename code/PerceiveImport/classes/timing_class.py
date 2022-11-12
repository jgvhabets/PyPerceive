### create a Timing class """

from dataclasses import dataclass

import os

import PerceiveImport.methods.find_folders as find_folder

@dataclass (init=True, repr=True)
class timingClass:
    """
    timing Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - timing: "Postop", "3MFU", "12MFU", "18MFU", "24MFU"

    Returns:
        - 
    
    """

    sub = str
    timing = str

    def __post_init__(self,):

        PerceiveMetadata_wb = load_workbook('Perceive_Metadata.xlsx')
        PerceiveMetadata_ws = PerceiveMetadata_wb.active # this gets the current active worksheet

        self.matfile_list = [] # this list will contain all matfile names    
        self.paths_list = [] # this list will contain all paths to the selected matfiles

        _, self.data_path = find_folder.find_project_folder()
        self.subject_path = os.path.join(self.data_path, self.sub)

        # if matfilename from column matfile (1) in self.matfile_list (from RecModality Class)
        # AND cell in column timing (4) == self.timing
        # the add matfile to self.matfile_list
        # else delete matfile from self.matfile list
        

        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if file.endswith(".mat") and rec_modality_dict[self.rec_modality] in file: # matpart is defined earlier
                    # print file????
                    self.matfile_list.append(file) # adding every file to the list of matfile names
                    
                    self.paths_list.append(os.path.join(root, file)) 
                    # keep root and file joined together so the path won´t get lost
                    # add each path to the list selection_paths

