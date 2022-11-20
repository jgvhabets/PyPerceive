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
import PerceiveImport.classes.Metadata_Class as metadata


@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: subject name called sub-xxx, e.g. "sub-021" (make sure to use exactly the same str as your subject folder is called)
        - incl_modalities: a list of recording modalities to include ["Streaming", "Survey", "Timeline", "IndefiniteStreaming"] 
        - incl_timing: a list of timing sessions to include ["Postop", "_3MFU", "_12MFU", "_18MFU", "_24MFU"]
        - incl_medication: a list of medication conditions to include  ["Off", "On"]
        - incl_stim: a list of stimulation conditions to include ["On", "Off"]
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
    incl_timing: list = field(default_factory=lambda: ["Postop", "_3MFU", "_12MFU", "_18MFU", "_24MFU"])
    incl_medication: list = field(default_factory=lambda: ["M0S0", "M0S1", "M1S0", "M1S1"])
    incl_stim: list = field(default_factory=lambda: ["On", "Off"])
    incl_task: list = field(default_factory=lambda: ["Rest", "DirectionalStimulation", "FatigueTest"])

    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        
        allowed_modalities = ["Streaming", "Survey", "Timeline"] # this shows allowed values for incl_modalities

        _, self.data_path = find_folder.find_project_folder() # path to "Data" folder
        self.subject_path = os.path.join(self.data_path, self.sub) # path to "subject" folder

        self.PerceiveMetadata = pd.read_excel(os.path.join(self.subject_path, f'Perceive_Metadata_{self.sub}.xlsx'))
        
        matfile_list = self.PerceiveMetadata["Perceive_filename"].to_list() # make a matfile_list of the values of the column "Perceive_filename" from the new selection of the Metadata DataFrame
        # -> Error occurs: InvalidIndexError 'Perceive_filename' ???

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
            incl_timing = self.incl_timing,
            incl_medication = self.incl_medication,
            incl_stim = self.incl_stim,
            incl_task = self.incl_task,
            matpath_list = self.matpath_list,
            PerceiveMetadata_selection = self.PerceiveMetadata) 

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
