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
    sub: str             # note that : is used, not =  
    incl_modalities: list = field(default_factory=lambda: ["Streaming", "Survey", "Timeline"])  # default:_ if no input is given -> automatically input the full list
    incl_session: list = field(default_factory=lambda: ["PostOp", "FU3M", "FU12M", "FU18M", "FU24M"])
    incl_condition: list = field(default_factory=lambda: ["M0S0", "M1S0", "M0S1", "M1S1"])
    incl_task: list = field(default_factory=lambda: ["RestBSSuRingR", "RestBSSuRingL", "RestBSSuSegmInterR", "RestBSSuSegmInterL",  "RestBSSuSegmIntraR", "RestBSSuSegmIntraL", "RestBSSt", "FingerTapBSSt", "UPDRSBSSt"])


    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        
        allowed_modalities = ["Streaming", "Survey", "Timeline"] # this shows allowed values for incl_modalities

        # _, self.data_path = find_folder.find_project_folder() # path to "Data" folder
        # self.subject_path = os.path.join(self.data_path, self.sub) # path to "subject" folder

        # self.onedrive = find_folder.get_onedrive_path("onedrive")
        # self.perceivedata = find_folder.get_onedrive_path("perceivedata")
        # self.subject_path = os.path.join(self.perceivedata, f'sub-{self.sub}')
        # self.results = find_folder.get_onedrive_path("results")

        # self.metadata = pd.read_excel(os.path.join(self.subject_path, f'metadata_{self.sub}.xlsx'), sheet_name="recordingInfo")
        
        path_local = 'c:\\Users\\jebe12\\Research\\Longterm_beta_project\\Data'
        self.subject_path = os.path.join(path_local, f'sub-{self.sub}')

        # modality_dict = {
        #     "Survey": "LMTD",
        #     "Streaming": "BSTD", 
        #     "Timeline": "CHRONIC"
        # }
        
        # write into new excel file -> columns: perceiveFilenames (existing in directory) + paths
        # create tuple list of all files + paths into new Dataframe and then to Excel
        # filename_path_tuple = []
        
        # for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
        #     for file in files: # looping through every file 
        #         for i in modality_dict:
        #             if file.endswith(".mat") and modality_dict[i] in file: # filter matfiles only for relevant modalities
        #                 filename_path_tuple.append([file, os.path.join(root, file)])


        # # create new excel table only with perceiveFilenames and paths
        # filename_pathDF = pd.DataFrame(filename_path_tuple, columns=['perceiveFilename', 'path_to_perceive'])

        # filename_pathDF.to_excel(os.path.join(self.subject_path, f'perceiveFilename_path_{self.sub}.xlsx'), sheet_name="perceiveFilename_path", index=False)
        # # filename_path = pd.read_excel(os.path.join(self.subject_path, f'metadata_{self.sub}_perceiveFilename_path.xlsx'), sheet_name="perceiveFilename_path")
        
        # # make a matfile_list of the values of the column "perceiveFilename" from the perceiveFilename_path excel table
        # matfile_list = filename_pathDF["perceiveFilename"].to_list()
        # matfile_list_endings = [u.split('_run-')[-1] for u in matfile_list] # will keep name after '_run-'

        # matpath_list = filename_pathDF["path_to_perceive"].to_list()

        # bei LMTD filenames
        # if LMTD in filename and _ses- to _run- identical to other LMTD filenames -> append _1, _2 etc to file and run os.walk again


        # get completed metadata table 
        # metadata filenames in Metadata table from JB and JK start differently to the .mat filenames in directory, only ending is the same
        
        # for every file in perceiveFilename from recordingInfo 
        # if filename from filename_path sheet in file from recordingInfo: -> save row + add path in new column path in Dataframe (not in Excel)
       
        # load manually completed Excel (as long as DF isn´t completed yet)
        self.metadata = pd.read_excel(os.path.join(self.subject_path, f'metadata_{self.sub}.xlsx'), sheet_name="recordingInfo")
        # matfile_list = self.metadata["perceiveFilename"].to_list()

        self.matpath_list = []

        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                for f in self.metadata["perceiveFilename"]:
                    if file == f:
                        self.matpath_list.append(os.path.join(root, file)) 

        
        # self.matpath_list = self.metadata["path_to_perceive"].to_list()
                    

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