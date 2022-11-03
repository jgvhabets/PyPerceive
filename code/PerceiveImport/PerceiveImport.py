"""PyFile"""

# import packages
import os 
from dataclasses import dataclass

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
        
    Returns    
    """
    
    # these fields will be initialized 
    sub: str            # note that : is used, not = 
    data_path: str 
    timing: str
    data_type: str
        
    # note the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        print(self.sub)
        self.files=os.listdir(self.data_path) # self.files can only run after initialisation because it needs self.data_path
        
    def __str__(self,):
        return f'From the Perceived data from subject {self.sub} all BrainSense {self.data_type} .mat files from the {self.timing} session are being selected.'
    
    # find correct folder with correct timing
    # def find_timingfolder():
        
    
    # find all matfiles within the correct timing folder
    # def find_matfiles():
        
        
    # select matfiles only for of correct datatype
    # therefore load matpart.json file with dictionary
    # def select_datatypefiles():
        
    
    # load the final selection of files into the correct datatype structure
    # e.g. load files from .selected_datatypefiles() into Survey_class.py
    # def load_finalselection():
    
    
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