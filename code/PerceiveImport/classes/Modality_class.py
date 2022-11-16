""" Create a recording modality Class """

from dataclasses import dataclass
import os

import pandas as pd

import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Timing_class as TimClass

@dataclass (init=True, repr=True)
class Modality:
    """
    BrainSense recording modality Class 
    
    parameters:
        - sub: e.g. "sub-021"
        - rec_modality: "Streaming", "Survey", "Timeline"

    Returns:
        - data_path: path to the "Data" folder
        - subject_path: path to the "sub" folder with all files of the given subject
        - matfile_list: all .mat files of the given subject and recording modality
        - paths_list: all paths to the given .mat files of the given subject and modality
    
    """
    sub: str
    modality: str
    metaClass: any
    
    def __post_init__(self,):

        allowed_timing = ["Postop", "3MFU", "12MFU"]

        modality_dict = {
            "Survey": "LMTD",
            "Streaming": "BrainSense",
            "Timeline": "CHRONIC"
        }

        self.matpath_list = [] # this list will contain all paths to the selected matfiles

        _, self.data_path = find_folder.find_project_folder()
        self.subject_path = os.path.join(self.data_path, self.sub)

        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if file.endswith(".mat") and modality_dict[self.modality] in file: # matpart is defined earlier
                    self.matpath_list.append(os.path.join(root, file)) 
                    # keep root and file joined together so the path won´t get lost
                    # add each path to the list selection_paths
        

        # selected matfiles and matpaths are being stored into the the Metadata_Class

        setattr(
            self.metaClass,
            "matpath_list",
            metaclass.MetadataClass(matpath_list = self.matpath_list)
        )


        # store a selection of rows of the PerceiveMetadata DataFrame into a new selection variable, with the condition that the filename in column Perceive_filename is in the self.matfile_list
        # PerceiveMetadata = pd.read_excel(os.path.join(self.subject_path, f'Perceive_Metadata_{self.sub}.xlsx'))
        
        PerceiveMetadata = metaclass.MetadataClass.PerceiveMetadata_selection
        self.PerceiveMetadata_selection = PerceiveMetadata[PerceiveMetadata["Perceive_filename"].isin(self.matfile_list)]

        #store the new selection of the DataFrame into Metadata_Class
        setattr(
            self.metaClass,
            "PerceiveMetadata_selection",
            metaclass.MetadataClass(PerceiveMetadata_selection = self.PerceiveMetadata_selection)
        )


        for tim in metaclass.MetadataClass.incl_timing:

            assert tim in allowed_timing, (
                f'inserted modality ({tim}) should'
                f' be in {allowed_timing}'
            )

            setattr(
                self,
                tim,
                TimClass.timingClass( 
                    sub = self.sub,
                    timing = tim,
                    metaClass = self.metaClass
                )
            )  



    def __str__(self,):
        return f'The recModality Class will select all .mat files of the subject {self.sub} and the BrainSense recording modality {self.modality}.'
    
