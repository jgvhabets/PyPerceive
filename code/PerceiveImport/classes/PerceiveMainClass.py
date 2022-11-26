"""Main Class"""

# import packages
import os 
from dataclasses import dataclass, field

import pandas as pd
import xlrd

# import openpyxl
# from openpyxl import Workbook, load_workbook

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.Modality_class as modalityClass
# import PerceiveImport.classes.Timing_class as TimClass
# import PerceiveImport.classes.Medication_Class as medclass
# import PerceiveImport.classes.Stim_Class as stimclass
# import PerceiveImport.classes.Task_Class as taskclass
import PerceiveImport.classes.Metadata_Class as metadata


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
    sub: str            # note that : is used, not =  
    incl_modalities: list = field(default_factory=lambda: ["Streaming", "Survey", "Timeline"])  # default:_ if no input is given -> automatically input the full list
    incl_session: list = field(default_factory=lambda: ["PostOp", "FU3M", "FU12M", "FU18M", "FU24M"])
    incl_condition: list = field(default_factory=lambda: ["M0S0", "M1S0", "M0S1", "M1S1"])
    incl_task: list = field(default_factory=lambda: ["RestBSSuRingR", "RestBSSuRingL", "RestBSSuSegmInterR", "RestBSSuSegmInterL",  "RestBSSuSegmIntraR", "RestBSSuSegmIntraL", "RestBSSt", "FingerTapBSSt", "UPDRSBSSt"])


    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        
        allowed_modalities = ["Streaming", "Survey", "Timeline"] # this shows allowed values for incl_modalities
        # allowed_session = ["Postop", "FU3M", "FU12M"]
        # allowed_conditions = ["M0S0", "M0S1", "M1S0", "M1S1"]
        # allowed_task = [""RestBSSuRingR", "RestBSSuRingL", "RestBSSuSegmInterR", "RestBSSuSegmInterL",  "RestBSSuSegmIntraR", "RestBSSuSegmIntraL", "RestBSSt", "FingerTapBSSt", "UPDRSBSSt"]


        # _, self.data_path = find_folder.find_project_folder() # path to "Data" folder
        # self.subject_path = os.path.join(self.data_path, self.sub) # path to "subject" folder

        # self.onedrive = find_folder.get_onedrive_path("onedrive")
        # self.perceivedata = find_folder.get_onedrive_path("perceivedata")
        # self.subject_path = os.path.join(self.perceivedata, f'sub-{self.sub}')
        # self.results = find_folder.get_onedrive_path("results")

        # self.metadata = pd.read_excel(os.path.join(self.subject_path, f'metadata_{self.sub}.xlsx'), sheet_name="recordingInfo")
        
        path_local = 'c:\\Users\\jebe12\\Research\\Longterm_beta_project\\Data'
        self.subject_path = os.path.join(path_local, f'sub-{self.sub}')


        self.metadata = pd.read_excel(os.path.join(self.subject_path, f'metadata_{self.sub}.xlsx'), sheet_name="recordingInfo")


        # make a matfile_list of the values of the column "perceiveFilename" from the new selection of the Metadata DataFrame
        matfile_list = self.metadata["perceiveFilename"].to_list()

        self.matpath_list = [] # this list will contain all paths to the matfiles in PerceiveMetadata
        
        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if file.endswith(".mat") and file in matfile_list: # matpart is defined earlier
                    self.matpath_list.append(os.path.join(root, file)) 
                    # keep root and file joined together so the path won´t get lost
                    # add each path to the list selection_paths


        # define and store all variables in self.metaClass, from where they can continuously be called and modified from further subclasses
        self.metaClass = metadata.MetadataClass(
            sub = self.sub,
            incl_modalities = self.incl_modalities,
            incl_session = self.incl_session,
            incl_condition = self.incl_condition,
            incl_task = self.incl_task,
            matpath_list = self.matpath_list,
            metadata_selection = self.metadata) 

        # loop through every modality input in the incl_modalities list 
        # and set the modality value for each modality
        for mod in self.incl_modalities:

            assert mod in allowed_modalities, (
                f'inserted modality ({mod}) should'
                f' be in {allowed_modalities}'
            )

            # seattr(object,name,value) -> object=instance whose attribute is to be set, name=attribute name, value=value to be set for the attribute
            setattr(
                self, 
                mod, 
                modalityClass.Modality(
                    sub = self.sub,
                    modality = mod,
                    metaClass = self.metaClass)
            )

        # if you don´t give any modality input -> jump to timing class
        # for tim in self.incl_timing:

        #     assert tim in allowed_timing, (
        #         f'inserted modality ({tim}) should'
        #         f' be in {allowed_timing}'
        #     )

        #     setattr(
        #         self,
        #         tim,
        #         TimClass.timingClass( 
        #             timing = tim,
        #             metaClass = self.metaClass
        #         )
        #     )  
        
        # # jump to med class
        # for med in self.metaClass.incl_medication:

        #     assert med in allowed_medication, (
        #         f'inserted modality ({med}) should'
        #         f' be in {allowed_medication}'
        #     )

        #     setattr(
        #         self,
        #         med,
        #         medclass.medicationClass(
        #             medication = med,
        #             metaClass = self.metaClass
        #         )
        #     ) 
        

        # # jump to stim class
        # for stim in self.metaClass.incl_stim:

        #     # Error checking: if stim is not in allowed_stimulation -> Error message
        #     assert stim in allowed_stimulation, (
        #         f'inserted modality ({stim}) should'
        #         f' be in {allowed_stimulation}'
        #     )

        #     setattr(
        #         self,
        #         stim,
        #         stimclass.stimulationClass(
        #             stimulation = stim,
        #             metaClass = self.metaClass
        #         )
        #     ) 


        # # jump to task class
        # for task in self.metaClass.incl_task:

        #     # Error checking: if stim is not in allowed_stimulation -> Error message
        #     assert task in allowed_task, (
        #         f'inserted modality ({task}) should'
        #         f' be in {allowed_task}'
        #     )

        #     setattr(
        #         self,
        #         task,
        #         taskclass.taskClass(
        #             task = task,
        #             metaClass = self.metaClass
        #         )
        #     )   
    
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
