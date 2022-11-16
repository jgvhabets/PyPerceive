"""PyFile"""

# import packages
import os 
from dataclasses import dataclass

import json
import pandas as pd
import xlrd

# import openpyxl
# from openpyxl import Workbook, load_workbook

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.RecModality_class as rec_Mod
# import PerceiveImport.classes.PerceiveMetadataClass as metadata


@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: subject name called sub-xxx, e.g. "sub-021" (make sure to use exactly the same str as your subject folder is called)

    post-initialized parameters:
        - data_path: path to your "Data" folder with all subject files 
        - Streaming: returns a tuple[str, str] -> matfile_list, paths_list of all Streaming.mat files of the given subject
        - Survey: returns a tuple[str, str] -> matfile_list, paths_list of all Survey.mat files of the given subject
        - Timeline: returns a tuple[str, str] -> matfile_list, paths_list of all Timeline.mat files of the given subject
        
    Returns:
        - 
    """
    
    # these fields will be initialized 
    sub: str            # note that : is used, not =  
        
    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation

        _, self.data_path = find_folder.find_project_folder() # path to "Data" folder
        self.subject_path = os.path.join(self.data_path, self.sub) # path to "subject" folder

        self.Streaming = rec_Mod.recModality(
                sub = self.sub,
                rec_modality = "Streaming"
                )
        
        self.Survey = rec_Mod.recModality(
                sub = self.sub,
                rec_modality = "Survey"
                )
        
        self.Timeline = rec_Mod.recModality(
                sub = self.sub,
                rec_modality = "Timeline"
                )
        
        # load the Perceive_Metadata.xlsx file as pandas DataFrame
        # os.chdir(self.data_path)
        # self.PerceiveMetadata = pd.read_excel('Perceive_Metadata.xlsx')

        # self.Streaming.Postop = metadata.PerceiveMetadata(
        # sub=self.sub, rec_modality="Streaming", timing = "Postop")
        # self.3MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "3MFU")
        # self.12MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "12MFU")
        # self.18MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "18MFU")
        # self.24MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "24MFU")


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


    def __str__(self,):
        return f'The Perceived data from subject {self.sub} are being selected.'
    
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
