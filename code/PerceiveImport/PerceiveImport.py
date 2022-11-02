"""PyFile"""

# import packages
import os 
from dataclasses import dataclass

# import PerceiveImport.filefunctions as filefuncs

@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: ....
        - ...
        -
        
    Returns    
    """
    
    # these fields will be initialized 
    sub: str            # note that : is used, not = 
    data_path: str 
    data_type: str
        
    
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        print(self.sub)
        self.files=os.listdir(self.data_path) # self.files can only run after initialisation because it needs self.data_path
        
        
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