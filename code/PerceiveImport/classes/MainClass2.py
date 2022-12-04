"""Main Class"""

# import packages
import os 
from dataclasses import dataclass, field

import pandas as pd
import copy


# import openpyxl
# from openpyxl import Workbook, load_workbook

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.Metadata_Class as metadata
import PerceiveImport.classes.Modality_class as modalityClass
import PerceiveImport.methods.load_mne as loadmne


# import PerceiveImport.classes.Timing_class as TimClass
# import PerceiveImport.classes.Medication_Class as medclass
# import PerceiveImport.classes.Stim_Class as stimclass
# import PerceiveImport.classes.Task_Class as taskclass



@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: subject name called sub-xxx, input e.g. "021" (make sure to use exactly the same str as your subject folder is called)
        - incl_modalities: a list of recording modalities to include ["Streaming", "Survey", "Timeline", "IndefiniteStreaming"] 
        - incl_timing: a list of timing sessions to include ["Postop", "FU3M", "FU12M", "FU18M", "FU24M"]
        - incl_med: a list of conditions to include  ["On", "Off"]
        - incl_stim: list = field(default_factory=lambda: ["Off", "On"]
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
    incl_modalities: list = field(default_factory=lambda: ["Survey", "StreamingBrainSense", "StreamingBSTD", "Timeline", "IndefiniteStreaming"])  # default:_ if no input is given -> automatically input the full list
    incl_session: list = field(default_factory=lambda: ["PostOp", "FU3M", "FU12M", "FU18M", "FU24M"])
    incl_condition: list = field(default_factory=lambda: ["M0S0", "M1S0", "M0S1", "M1S1"])
    incl_task: list = field(default_factory=lambda: ["RestBSSuRingR", "RestBSSuRingL", "RestBSSuSegmInterR", "RestBSSuSegmInterL",  "RestBSSuSegmIntraR", "RestBSSuSegmIntraL", "RestBSSt", "FingerTapBSSt", "UPDRSBSSt"])


    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        
        allowed_modalities = [
            "Survey",
            "StreamingBrainSense", 
            "StreamingBSTD",
            "Timeline",
            "IndefiniteStreaming"] # this shows allowed values for incl_modalities

        self.perceivedata = find_folder.get_onedrive_path("perceivedata")
        self.subject_path = os.path.join(self.perceivedata, f'sub-{self.sub}')

        self.metadata = pd.read_excel(os.path.join(self.subject_path, f'metadata_{self.sub}.xlsx'), sheet_name="recordingInfo")
        
        
        # define and store all variables in self.metaClass, from where they can continuously be called and modified from further subclasses
        metaClass = metadata.MetadataClass(
            sub = self.sub,
            incl_modalities = self.incl_modalities,
            incl_session = self.incl_session,
            incl_condition = self.incl_condition,
            incl_task = self.incl_task,
            metadata = self.metadata
            )


        # create a copy of the metaclass which will stay the same and won´t be modified by other classes
        self.metaClass_copy = copy.deepcopy(metaClass)


        # loop through every modality input in the incl_modalities list 
        # and set the modality value for each modality
        for mod in self.incl_modalities:

            assert mod in allowed_modalities, (
                f'inserted modality ({mod}) should'
                f' be in {allowed_modalities}'
            )
            print(f'CHECK METACLASS: shape metadata {metaClass.metadata.shape}')
            # seattr(object,name,value) -> object=instance whose attribute is to be set, name=attribute name, value=value to be set for the attribute
            setattr(
                self, 
                mod, 
                modalityClass.Modality(
                    sub = self.sub,
                    modality = mod,
                    metaClass = self.metaClass_copy)
            )
            
            print(f'CHECK 2 METACLASS: shape metadata {self.metaClass_copy.metadata.shape}')

