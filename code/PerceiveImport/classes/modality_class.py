""" Create a recording modality Class """

from dataclasses import dataclass
import os

import pandas as pd
import copy

import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.session_class as sesClass


@dataclass (init=True, repr=True)
class Modality:
    """
    BrainSense recording modality Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming"
        - metaClass: all original attributes set in Main_Class
        - meta_table: modality selected meta_table set in Main_Class

    Returns:
        - sel_meta_table: session selected meta_table 
    
    """
    sub: str
    modality: str   # input from MainClass: copy from the metaclass from Mainclass
    metaClass: any
    meta_table: pd.DataFrame
    
    def __post_init__(self,):

        allowed_session = ["postop", "fu3m", "fu12m", "fu18m", "fu24m"]

        
        # loop through every session input in the incl_session list 
        # and set the session value for each session
        # only used in assertion to check if defined sessions are in meta_table
        session_list = self.meta_table['session'].unique().tolist() # list of the existing sessions in metadata column "session"

        for ses in self.metaClass.incl_session:
            
            assert ses.lower() in [s.lower() for s in allowed_session], (
                f'inserted session ({ses}) should'
                f' be in {allowed_session}'
            )

            #Error checking: is sessionInput in session_list of Metadata?
            if ses.lower() not in [s.lower() for s in session_list]:
                
                print(
                    f'inserted session ({ses}) can not be found in the metadata table'
                )
            
            else:

                # select out only meta_table for current session
                sel = [ses.lower() == s.lower() for s in self.meta_table["session"]]
                sel_meta_table = self.meta_table[sel].reset_index(drop=True)

                # if no files after selection, dont create subclasses
                if len(sel_meta_table) == 0:
                    continue

                setattr(
                    self,
                    ses,
                    sesClass.sessionClass( 
                        sub=self.sub,
                        modality=self.modality,
                        session=ses,
                        metaClass=self.metaClass,
                        meta_table=sel_meta_table,
                    )
                )  


    def __str__(self,):
        return f'The recModality Class will select all .mat files of the subject {self.sub} and the BrainSense recording modality {self.modality}.'
    
