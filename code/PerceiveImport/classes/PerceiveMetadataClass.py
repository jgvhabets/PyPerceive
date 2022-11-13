""" PerceiveMetadata Class"""

from dataclasses import dataclass
import os

import pandas as pd
import xlrd

import PerceiveImport.methods.find_folders as find_folder


@dataclass (init=True, repr=True)
class PerceiveMetadata:
    """
    PerceiveMetadata Class 
    
    parameters:
        - sub: e.g. "sub-021"
        - rec_modality: "Streaming", "Survey", "Timeline"
        - timing: 
        - condition:
        - task: 

    Returns:
        - data_path: path to the "Data" folder
        - matfile_selection: all .mat files of the given subject and conditions
        - paths_list: all paths to the given .mat files of the given subject and modality
    
    """
    sub: str
    rec_modality: str = None # default, if no input, it will run anyways
    timing: str = None
    condition: str = None
    task: str = None

    
    def __post_init__(self,):

        _, self.data_path = find_folder.find_project_folder() #self.data_path stores path to "Data" folder

        # load the Perceive_Metadata.xlsx file as pandas DataFrame
        os.chdir(self.data_path)
        PerceiveMetadata_df = pd.read_excel('Perceive_Metadata.xlsx')

        # define conditions for the selection of .mat filenames
        cond_sub = PerceiveMetadata_df["sub"] == str(self.sub)
        cond_rec_modality = PerceiveMetadata_df.rec_modality == str(self.rec_modality)
        cond_timing = PerceiveMetadata_df.timing == str(self.timing)
        cond_condition = PerceiveMetadata_df.condition == str(self.condition)
        cond_task = PerceiveMetadata_df.task == str(self.task)


        # note all() means all conditions have to be true (alternatively: any() -> printing if any argument is true)
        PerceiveMetadata_selection = PerceiveMetadata_df[[all([a,b,c,d,e]) for a, b, c, d, e in zip(cond_sub, cond_rec_modality, cond_timing, cond_condition, cond_task)]]
        
        # how can I set default, if not every condition has an input value?

        self.matfile_selection = [PerceiveMetadata_selection.Perceive_filename.values]
        # self.matfile_paths

        
        
        

