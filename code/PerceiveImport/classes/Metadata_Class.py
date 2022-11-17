""" Metadata Class """

from dataclasses import dataclass, field

import pandas as pd
import xlrd


@dataclass(init=True, repr=True) 
class MetadataClass:
    """
    Metadata class to store repetitive variables that are changing constantly throughout the hierarchy
    
    parameters:
        - sub: subject name called sub-xxx, e.g. "sub-021" (make sure to use exactly the same str as your subject folder is called)
        - incl_modalities: list
        - incl_timing: list 
        - incl_medication: list 
        - incl_stim: list 
        - incl_task: list
        - matpath_list: list
        - PerceiveMetadata_selection: any

    post-initialized parameters:
        
    Returns:
        - 
    """
    

    sub: str            
    incl_modalities: list
    incl_timing: list 
    incl_medication: list 
    incl_stim: list 
    incl_task: list
    matpath_list: list
    PerceiveMetadata_selection: any # pd.DataFrame



    def __post_init__(self,): 

        print("MetadataClass has been loaded")


        # allowed_modalities = ["Streaming", "Survey", "Timeline"] # this shows allowed values for incl_modalities
        # allowed_timing = ["Postop", "3MFU", "12MFU"]
        # allowed_medication = ["M0S0", "M0S1", "M1S0", "M1S1"]
        #allowed_stim = ["On", "Off", "12MFU"]
        # allowed_task = ["Rest", "DirectionalStimulation", "FatigueTest"]

        #_, self.data_path = find_folder.find_project_folder() # path to "Data" folder
        #self.subject_path = os.path.join(self.data_path, self.sub) # path to "subject" folder

        #self.PerceiveMetadata_selection = pd.read_excel(os.path.join(self.subject_path, f'Perceive_Metadata_{self.sub}.xlsx'))






