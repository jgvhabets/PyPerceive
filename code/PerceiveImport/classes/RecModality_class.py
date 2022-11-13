""" Create a recording modality Class """

from dataclasses import dataclass
import os

import PerceiveImport.methods.find_folders as find_folder
# import PerceiveImport.classes.PerceiveMetadataClass as metadata


@dataclass (init=True, repr=True)
class recModality:
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
    rec_modality: str

    # files: list
    # timingfiles: list

    # initialized fields
    
    def __post_init__(self,):
    
        #self.recmod_matfilenames, self.recmod_matfilepaths = matfiles.select_matfiles(self.sub, self.rec_modality)
        rec_modality_dict = {
        "Survey": "LMTD",
        "Streaming": "BrainSense",
        "Timeline": "CHRONIC"
        }
    
        self.matfile_list = [] # this list will contain all matfile names    
        self.paths_list = [] # this list will contain all paths to the selected matfiles

        _, self.data_path = find_folder.find_project_folder()
        self.subject_path = os.path.join(self.data_path, self.sub)

        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if file.endswith(".mat") and rec_modality_dict[self.rec_modality] in file: # matpart is defined earlier
                    # print file????
                    self.matfile_list.append(file) # adding every file to the list of matfile names
                    
                    self.paths_list.append(os.path.join(root, file)) 
                    # keep root and file joined together so the path won´t get lost
                    # add each path to the list selection_paths

        # conditions timing

        # self.Postop = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality, timing = "Postop")
        # self.3MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "3MFU")
        # self.12MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "12MFU")
        # self.18MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "18MFU")
        # self.24MFU = metadata.PerceiveMetadata(sub=self.sub, rec_modality=self.rec_modality,timing = "24MFU")


    def __str__(self,):
        return f'The recModality Class will select all .mat files of the subject {self.sub} and the BrainSense recording modality {self.rec_modality}.'
    
