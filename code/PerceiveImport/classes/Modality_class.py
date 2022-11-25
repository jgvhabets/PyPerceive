""" Create a recording modality Class """

from dataclasses import dataclass
import os

import pandas as pd

import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.Session_Class as sesClass
# import PerceiveImport.classes.Medication_Class as medclass
# import PerceiveImport.classes.Stim_Class as stimclass
# import PerceiveImport.classes.Task_Class as taskclass

@dataclass (init=True, repr=True)
class Modality:
    """
    BrainSense recording modality Class 
    
    parameters:
        - sub: e.g. "sub-021"
        - modality: "Streaming", "Survey", "Timeline"
        - metaClass

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

        allowed_session = ["Postop", "FU3M", "FU12M", "FU18M", "FU24M"]
        # allowed_conditions = ["M0S0"]
        # allowed_task = ["Rest", "DirectionalStimulation", "FatigueTest"]

        modality_dict = {
            "Survey": "LMTD",
            "Streaming": "BrainSense",
            "Timeline": "CHRONIC"
        }

        # _, self.data_path = find_folder.find_project_folder()
        # self.subject_path = os.path.join(self.data_path, self.sub)

        self.perceivedata = find_folder.get_onedrive_path("perceivedata")
        self.subject_path = os.path.join(self.perceivedata, f'sub-{self.sub}')

        self.matpath_list = [] # this list will contain all paths to the selected matfiles
        matfile_list = []

        for root, dirs, files in os.walk(self.subject_path): # walking through every root, directory and file of the given path
            for file in files: # looping through every file 
                if file.endswith(".mat") and modality_dict[self.modality] in file:
                    matfile_list.append(file)
                    self.matpath_list.append(os.path.join(root, file)) 
                    # keep root and file joined together so the path won´t get lost
                    # add each path to the matpath_list 
        
        # alternatively, select from existing matpath_list from MetadataClass
        # for path in metaclass.MetadataClass.matpath_list:
        #    if modality_dict[self.modality] in path:
        #        self.matpath_list.append(path)
        
        # seattr() changes the value of the attribute matpath_list of self.metaClass 
        
        setattr(
            self.metaClass,
            "matpath_list",
            self.matpath_list)



        # store a selection of rows of the PerceiveMetadata DataFrame into a new selection variable, with the condition that the filename in column Perceive_filename is in the self.matfile_list        
        metadata = self.metaClass.metadata_selection
        self.metadata_selection = metadata[metadata["Perceive_filename"].isin(matfile_list)].reset_index(drop=True)
        # reset.index setzt die Index im DF nochmal neu

        #store the new selection of the DataFrame into Metadata_Class
        setattr(
            self.metaClass,
            "metadata_selection",
            self.metadata_selection)

        # can we take both setattr (matpath_list and PerceiveMetadata_selection) together ??

        for ses in self.metaClass.incl_session:

            assert ses in allowed_session, (
                f'inserted modality ({ses}) should'
                f' be in {allowed_session}'
            )

            # setting the attribute in this class here for tim to a value, which is the timing class with defined attributes
            setattr(
                self,
                ses,
                sesClass.sessionClass( 
                    session = ses,
                    metaClass = self.metaClass
                )
            )  


        # jump to med class
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


    def __str__(self,):
        return f'The recModality Class will select all .mat files of the subject {self.sub} and the BrainSense recording modality {self.modality}.'
    
