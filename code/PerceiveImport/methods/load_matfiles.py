""" loading the selection of matfiles with MNE """

import os 
from dataclasses import dataclass

import json

# import PerceiveImport.select_matfiles as matfiles   # use this line to import other .py files
# import importlib
# importlib.reload(matfiles) 

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
        - 
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
        
        # selected_matfiles = matfiles.select_matfiles()
        
    def __str__(self,):
        return f'From the Perceived data from subject {self.sub} all BrainSense {self.data_type} .mat files from the {self.timing} session are being selected.'

    # load selected files
    def load_selection(self,):
        for file in paths_list: # paths_list is only defined after running select_matfinal() method ?!?
            raw = mne.io.read_raw_fieldtrip(paths_list[file],info={},data_name='data',)
        
    # store every loaded file in a different variable
    # e.g. matfile1, matfile2, matfile3 etc
    