""" Task Class """

import pandas as pd
from dataclasses import dataclass
import mne 
import mne_bids

import PerceiveImport.methods.metadata_methods as metadatamethods
# import PerceiveImport.classes.Metadata_Class as metaclass

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
                "FingerTapBSSt", # BrainSense Streaming Finger tapping
                "UPDRSBSSt", # BrainSense Streaming UPDRS
        - metaClass:

    Returns:
        - 
    
    """
    
    sub : str
    task: str
    metaClass: any



    def __post_init__(self,):

        # get matpaths and PerceiveMetadata_selection from the Metadata_Class

        metadata_selection = self.metaClass.metadata_selection 

        # attempt to output a concatenated version of a dataframe if self.metaClass.incl_condition > 1
        # task_dict = {}

        # for taskInput in self.task:
        #     task_dict["Metadata_{0}".format(taskInput)] =  metadata_selection[metadata_selection['task'] == taskInput].reset_index(drop=True)
        #     # dictionary {"Metadata_M0S0": Metadata_selection M0S0, ...}
        
        # # from dictionary concatenate all dataframes together to one dataframe -> pd.concat
        # self.metadata_selection = pd.concat(task_dict.values(), ignore_index=True).reset_index(drop=True)
        
        # # select the input sessions, save the selection in metadata_selection 
        # self.matpath_list = []
        # matfile_list = self.metadata_selection["perceiveFilename"]

        # # select only the paths included in the new matfile_list from paths of preselected matpath_list in MetaClass
        # for path in self.metaClass.matpath_list:
        #     for f in matfile_list:
        #         if f in path:
        #             self.matpath_list.append(path)


        # #select the PerceiveMetadata DataFrame for the correct task:
        self.metadata_selection = metadata_selection[metadata_selection["task"] == self.task].reset_index(drop=True)
        matfile_list = self.metadata_selection["perceiveFilename"].to_list() # make a matfile_list of the values of the column "perceiveFilename" from the new selection of the Metadata DataFrame

        # select from the matpath_list from the MetadataClass 
        # only append paths with the selected .mat filenames to the new self.matpath_list
        self.matpath_list = []
        for path in self.metaClass.matpath_list:
            for f in matfile_list:
                if f in path:
                    self.matpath_list.append(path)
        # # einfacherer Weg ???


        # store the new values of the selected matpaths and DataFrame selection to the attributes stored in Metadata_Class
        setattr(
            self.metaClass,
            "metadata_selection",
            self.metadata_selection)

        setattr(
            self.metaClass,
            "matpath_list",
            self.matpath_list)
        

        #self.data is a dictionary with keys(raw_1,2,3,n)
        # each key stores one mne loaded .mat file from the selected paths
        # e.g. 021.Survey.FU3M.M0S0.data -> loads a list of 6 .mat files 

        # self.data = {}
        # count = -1

        # for f in self.matpath_list:  # matselection stores a list of the selected .mat paths 
    
        #     count +=1

        #     self.data["raw_{0}".format(count)] = mne.io.read_raw_fieldtrip(
        #     f,
        #     info={},
        #     data_name='data'
        #     )
        
        self.data = metadatamethods.load_mne_raw(self.matpath_list)
    

        
    

