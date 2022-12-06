""" Task Class """

import pandas as pd
from dataclasses import dataclass

import copy

import mne 
import mne_bids

import PerceiveImport.methods.metadata_methods as metadatamethods

@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - task: "RestBSSuRingR", # BrainSense Survey Rest, Ring contacts 23, 01, 12, 02, 13, 03, right hemisphere
                "RestBSSuRingL", # BrainSense Survey Rest, Ring contacts 23, 01, 12, 02, 13, 03, left hemisphere
                "RestBSSuSegmInterR", # BrainSense Survey Rest, Segment contacts 1C2C, 1B2B, 1A2A (inter levels), right hemisphere
                "RestBSSuSegmInterL", # BrainSense Survey Rest, Segment contacts 1C2C, 1B2B, 1A2A (inter levels), left hemisphere
                "RestBSSuSegmIntraR", # BrainSense Survey Rest, Segment contacts 2A2C, 2B2C, 2A2B, 1A1C, 1B1C, 1A1B (intra levels), right hemisphere
                "RestBSSuSegmIntraL", # BrainSense Survey Rest, Segment contacts 2A2C, 2B2C, 2A2B, 1A1C, 1B1C, 1A1B (intra levels), left hemisphere
                "RestBSSt", # BrainSense Streaming Rest
                "FTBSSt", # BrainSense Streaming Finger tapping
                "UPDRSBSSt", # BrainSense Streaming UPDRS
        - metaClass:

    Returns:
        - 
    
    """
    
    sub : str
    task: str
    metaClass: any



    def __post_init__(self,):


        # select all rows with the chosen tasks in the column "task" of the metadata DF 
        sel = [self.task in task for task in self.metaClass.metadata["task"]]
        sel_meta_df = self.metaClass.metadata[sel].reset_index(drop=True)
        
        # create a copy of the metaclass metadata which will stay the same and won´t be modified by other classes
        self.sel_meta_df = copy.deepcopy(sel_meta_df)


        #store the new selection of the DataFrame into Metadata_Class
        setattr(self.metaClass, "metadata", sel_meta_df)

        
        # self.data = metadatamethods.load_mne_path(self.matpath_list)
    

        
    

