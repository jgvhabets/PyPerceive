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
    import_json: bool = False

    def __post_init__(self,):

        # remove contact column from metadata (not relevant for streaming recordings)
        # , to prevent incorrect NaN-row-removal
        if self.modality == 'streaming':
            self.meta_table = self.meta_table.drop(['contacts'], axis=1)
        
        # remove contact column for streaming recordings, to prevent NaN-row-removal
        elif self.modality == 'indefinitestreaming':
            self.meta_table = self.meta_table.drop(['contacts'], axis=1)

        allowed_session = ["postop", "fu3m", "fu12m", "fu18m", "fu20m", "fu22m", "fu23m", "fu24m"]


        # for STREAMING OR SURVEY
        # loop through every session input in the incl_session list 
        # and set the session value for each session
        # only used in assertion to check if defined sessions are in meta_table
        allowed_session = ["postop", "fu3m", "fu12m", "fu18m", "fu20m", "fu22m", "fu23m", "fu24m"]
        session_list = self.meta_table['session'].unique().tolist() # list of the existing sessions in metadata column "session"

        for ses in self.metaClass.incl_session:
            
            assert ses.lower() in [s.lower() for s in allowed_session], (
                f'inserted session ({ses}) should'
                f' be in {allowed_session}'
            )

            #Error checking: is sessionInput in session_list of Metadata?
            if ses.lower() not in [s.lower() for s in session_list]:

                print(
                    f'inserted session ({ses}, {self.modality}) can not be found in the metadata table'
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
                        import_json = self.import_json
                    )
                )  
    
