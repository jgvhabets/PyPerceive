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
        - sub: e.g. "021"
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

        allowed_session = ["PostOp", "FU3M", "FU12M", "FU18M", "FU24M"]

        modality_abbreviations_dict = {
            "Survey": "LMTD",
            "StreamingBrainSense": "BrainSense", 
            "StreamingBSTD": "BSTD",
            "Timeline": "CHRONIC",
            "IndefiniteStreaming": "IS"
        }

       
        # select all rows with modality abbreviations in filename
        abbr = modality_abbreviations_dict[self.modality]  # current modality abbreviations
        sel = [abbr in fname for fname in self.metaClass.metadata["perceiveFilename"]]
        sel_meta_df = self.metaClass.metadata[sel].reset_index(drop=True)
        sel_meta_df.copy(sel_meta_df)
        
        print("sel_meta_df: ", sel_meta_df, sel)

        #store the new selection of the DataFrame into Metadata_Class
        setattr(self.metaClass, "metadata", sel_meta_df)
        

        # loop through every session input in the incl_session list 
        # and set the session value for each session

        #session_list = sel_meta_df['session'].unique().tolist() # list of the existing sessions in metadata column "session"

        for ses in self.metaClass.incl_session:
            
            assert ses in allowed_session, (
                f'inserted modality ({ses}) should'
                f' be in {allowed_session}'
            )

            # Error checking: is sessionInput in session_list of Metadata?
            # assert ses in session_list, (
            #     f'inserted session ({ses}) has not been recorded'
            #     f' and can not be found in the metadata, which only contains sessions {session_list}'
            #     )

            # setting the attribute in this class here for tim to a value, which is the timing class with defined attributes
            setattr(
                self,
                ses,
                sesClass.sessionClass( 
                    sub = self.sub,
                    session = ses,
                    metaClass = self.metaClass
                )
            )  



    def __str__(self,):
        return f'The recModality Class will select all .mat files of the subject {self.sub} and the BrainSense recording modality {self.modality}.'
    
