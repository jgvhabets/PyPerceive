"""PyFile"""

# import packages
import os 
from dataclasses import dataclass

import json

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.RecModality_class as rec_Mod


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

        - timingdatatype_matfilenames: returns a list of .mat filenames of the chosen timing and datatype
        - timing_matfilenames: returns a list of .mat filenames of the chosen timing 
        - datatype_matfilenames: returns a list of .mat filenames of the chosen datatype

        - timingdatatype_matfilenames: returns a list of .mat filepaths of the chosen timing and datatype
        - timing_matfilenames: returns a list of .mat filepaths of the chosen timing
        - datatype_matfilenames: returns a list of .mat filepaths of the chosen datatype
        
    Returns:
        - 
    """
    
    # these fields will be initialized 
    sub: str            # note that : is used, not = 
    timing: str 
    rec_modality: str
        
    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation

        _, self.data_path = find_folder.find_project_folder() #self.data_path stores path to "Data" folder
        
       # load Excel sheet
        
        if self.rec_modality == "Streaming":
            self.Streaming = rec_Mod.recModality(
                sub = self.sub,
                rec_modality = self.rec_modality
                )
        
        elif self.rec_modality == "Survey":
            self.Survey = rec_Mod.recModality(
                sub = self.sub,
                rec_modality = self.rec_modality
                )
        
        elif self.rec_modality == "Timeline":
            self.Timeline = rec_Mod.recModality(
                sub = self.sub,
                rec_modality = self.rec_modality
                )

        # if timing == "3MFU":
        #   self.3MFU = loadmat.load_timingmatfiles(self.sub, self.timing) 
        #   or...???
        #   self.3MFU =  (matfiles.select_mattiming(self.sub, self.timing))[1] # only store a list of 3MFU filepaths
        #       if datatype == "Streaming":
        #           self.3MFU.Streaming ... etc
        #
        #       else loadmat.load_timingmatfiles(self.sub, self.timing)
        
        #setattr()
        #getattr()

        # if data_type == "Streaming":   


        


    def __str__(self,):
        return f'From the Perceived data from subject {self.sub} all BrainSense {self.rec_modality} .mat files from the {self.timing} session are being selected.'
    
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
