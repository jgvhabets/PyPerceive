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

        # get rownumbers row_x - row_y of self.matfile_list (of chosen RecModality)
        # for name in column4 from row_x - row_y:
        #     if cell == self.timing:
        #         append matfilename(row_of_cell,column1) to self.matfile_list

        # for file in self.matfile_list:
        #     if cell in column_timing(4) in same row == self.timing:
        #         self.matfile_list.keep(file)
        #     else:
        #         self.matfile_list.delete(file)
        
        
        # is it possible to detect the path of a unique path? then we don´t have to safe the 

