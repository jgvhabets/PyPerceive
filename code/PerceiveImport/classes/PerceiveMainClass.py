"""PyFile"""

# import packages
import os 
from dataclasses import dataclass

import json

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
#import PerceiveImport.classes.Streaming_class as streamingClass
#import PerceiveImport.methods.select_matfiles as matfiles   # importing matfiles with methods from select_matfiles.py



@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: subject name called sub-xxx, e.g. "sub-021" (make sure to use exactly the same str as your subject folder is called)
        - timing: timing of session, e.g. "3MFU", "12MFU", "Postop"
        - data_type: choose between "Survey", "Streaming", "Timeline"

    post-initialized parameters:
        - data_path: path to your "Data" folder with all subject files 
        - subject_list: list with all subject folder names within your "Data" folder
        - subject_path: path to your chosen subject folder according to your self.sub
        
    Returns:
        - 
    """
    
    # these fields will be initialized 
    sub: str            # note that : is used, not = 
    timing: str
    data_type: str
        
    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation

        _, self.data_path = find_folder.find_project_folder() #self.data_path stores path to "Data" folder
        self.subject_list= os.listdir(self.data_path) # self.subject_list stores a list with subject folders inside of "Data" folder
        self.subject_path = os.path.join(self.data_path, self.sub) # self.subject_path stores the path to your chosen "sub" folder

        
        


        # STREAMING_FILES = .....
        # self.Streaming = streamingClass.StreamingData(
        #     sub=self.sub,
        #     # files=
        #     files=self.files,
        #)


        
        # selected_matfiles = matfiles.select_matfiles()
        
    def __str__(self,):
        return f'From the Perceived data from subject {self.sub} all BrainSense {self.data_type} .mat files from the {self.timing} session are being selected.'


    def select_mat_timing_datatype(self,):
        """
        select_mat_timing_datatype() selects all .mat files within your project folder 
        of a specific timing (postop, 3MFU, 12MFU, 18MFU, 24MFU) 
        and of a specific datatype (Survey, Streaming, Timeline)

        Return: tuple[str, str] -> matfile_list, paths_list
        """

        datatype_dict = {
            "Survey": "LMTD",
            "Streaming": "BrainSense",
            "Timeline": "CHRONIC"
            }

        matfile_list = [] # this list will contain all matfile names    
        paths_list = [] # this list will contain all paths to the selected matfiles

        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if self.timing in root and file.endswith(".mat") and datatype_dict[self.data_type] in file: # datatype_dict is defined earlier
                    print(file) # printing makes sure, that every selected file is saved after a loop
                    matfile_list.append(file) # adding every file to the list of matfile names
            
                    single_path = os.path.join(root, file) # keep root and file joined together so the path won´t get lost
                    paths_list.append(single_path) # add each path to the list selection_paths
        
        print ('\n\tFilenames of the selected .mat files:', matfile_list)

        print ('\n\tList of paths to the selected .mat files:', paths_list)

 
    
    
    # load the final selection of files into the correct datatype structure
    # e.g. load files from .select_matfiles() into Survey_class.py
    # def load_selection(self,):
    #     for file in paths_list: # paths_list is only defined after running select_matfinal() method ?!?
    #         raw = mne.io.read_raw_fieldtrip(paths_list[file],info={},data_name='data',)
        
    
    
    
    
        # xxx = filefuncs.FUNCTIon()
        
        # find all files
        
        # select files on datatype (Survey) -> survey files
        # select on timing (postop)
        
        # final selection of files of interest
        
            # load files
            
            # load into Survey structure -> class Survey (with selected files)
            
            
            # goal: PerceiveData.Survey.Postop.
            
            # sub021 = PerceiveData(xxxxxx)
            # sub021.Streaming.12mfu.data.LFP_L
            
            
        
        
        
        
# file_handling.py -> mit 


# functions

# 1) find files
# 2) load files