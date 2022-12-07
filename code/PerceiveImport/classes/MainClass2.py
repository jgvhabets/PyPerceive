"""Main Class"""

# import packages
import os 
from dataclasses import dataclass, field

import pandas as pd
import copy

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.Metadata_Class as metadata
import PerceiveImport.classes.Modality_Class as modalityClass
#import PerceiveImport.methods.load_mne as loadmne


import warnings

def read_excel_wOut_warning(path: str, sheet_name: None):
    """
    Load data from an Excel file, and surpress warning
    bceause of Excel-Dropdown menus
    """
    warnings.simplefilter(action='ignore', category=UserWarning)
    return pd.read_excel(path, sheet_name=sheet_name)


@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: subject name called sub-xxx, input e.g. "021" (make sure to use exactly the same str as your subject folder is called)
        - incl_modalities: a list of recording modalities to include ["Streaming", "Survey", "Timeline", "IndefiniteStreaming"] 
        - incl_timing: a list of timing sessions to include ["Postop", "FU3M", "FU12M", "FU18M", "FU24M"]
        - incl_cond: a list of conditions to include  ["M0S0", "M1S0", "M0S1", "M1S1"]
        - incl_task: a list of tasks to include ["Rest", "DirectionalStimulation", "FatigueTest"]

    post-initialized parameters:
        - data_path: path to your "Data" folder with all subject files 
        - subject_path: path to your "sub-0XX" folder
        - PerceiveMetadata: reads the Excel file 'Perceive_Metadata_sub-0XX'.xlsx
        - matpath_list: a list of all paths to the .mat files of the column 'Perceive_filename' in PerceiveMetadata
        - Streaming: a paths_list of all Streaming.mat files of the given subject
        - Survey: a paths_list of all Survey.mat files of the given subject
        - Timeline: a paths_list of all Timeline.mat files of the given subject
        #- IndefiniteStreaming: a paths_list of all IndefiniteStreaming.mat files of the given subject

    Returns:
        - 
    """
    
    # these fields will be initialized 
    sub: str             # note that : is used, not =  
    incl_modalities: list = field(default_factory=lambda: ["Survey", "Streaming", "Timeline", "IndefiniteStreaming"])  # default:_ if no input is given -> automatically input the full list
    incl_session: list = field(default_factory=lambda: ["PostOp", "FU3M", "FU12M", "FU18M", "FU24M"])
    incl_condition: list = field(default_factory=lambda: ["M0S0", "M1S0", "M0S1", "M1S1"])
    incl_task: list = field(default_factory=lambda: ["Rest", "FT", "UPDRS"])


    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        
        allowed_modalities = [
            "Survey",
            "Streaming", 
            "Timeline",
            "IndefiniteStreaming"] # this shows allowed values for incl_modalities

        self.perceivedata = find_folder.get_onedrive_path("perceivedata")
        self.subject_path = os.path.join(self.perceivedata, f'sub-{self.sub}')
        self.meta_table = read_excel_wOut_warning(os.path.join(self.subject_path, f'metadata_{self.sub}.xlsx'), sheet_name="recordingInfo")
        
        
        # define and store all variables in self.metaClass, from where they can continuously be called and modified from further subclasses
        self.metaClass = metadata.MetadataClass(
            sub = self.sub,
            incl_modalities = self.incl_modalities,
            incl_session = self.incl_session,
            incl_condition = self.incl_condition,
            incl_task = self.incl_task,
            orig_meta_table = self.meta_table
        )

        # loop through every modality input in the incl_modalities list 
        # and set the modality value for each modality
        for mod in self.incl_modalities:

            assert mod in allowed_modalities, (
                f'inserted modality ({mod}) should'
                f' be in {allowed_modalities}'
            )

            modality_abbreviations_dict = {
                "Survey": "LMTD",
                "Streaming": "BrainSense", 
                "Timeline": "CHRONIC",
                "IndefiniteStreaming": "IS"
            }

            # select all rows with modality abbreviations in filename
            abbr = modality_abbreviations_dict[mod]  # current modality abbreviations
            sel = [abbr in fname for fname in self.metaClass.orig_meta_table["perceiveFilename"]]
            sel_meta_table = self.metaClass.orig_meta_table[sel].reset_index(drop=True)
            
            # if no files after selection, dont create subclasses
            if len(sel_meta_table) == 0:
                continue

            setattr(
                self, 
                mod, 
                modalityClass.Modality(
                    sub=self.sub,
                    modality=mod,
                    metaClass=self.metaClass,
                    meta_table=sel_meta_table)
            )
            

