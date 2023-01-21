""" Task Class """

import pandas as pd
from dataclasses import dataclass


import PerceiveImport.methods.load_rawfile as load_rawfile
import PerceiveImport.classes.contact_class as contactclass

import warnings



@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming" set in condition_class
        - session: "postop", "fu3m", "fu12m", "fu18m", "fu24m" set in condition_class
        - condition: "m0s0", "m1s0", "m0s1", "m1s1" set in condition_class
        - task: "rest", "tapping", "rota", "updrs", "monopolar" set in condition_class
        - contact: a list of contacts to include ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"]
        - metaClass: all original attributes set in Main_Class
        - meta_table: selected meta_table set in condition_class

    Returns:
        - sel_meta_table: session selected meta_table 
        - self.data: dictionary,  keys will be named after task, values will be the raw data of one perceived .mat file loaded with mne.io.read_raw_fieldtrip
    
    """
    
    sub : str
    modality: str
    session: str
    condition: str
    task: str
    metaClass: any
    meta_table: pd.DataFrame


    def __post_init__(self,):


        allowed_contacts = ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"]

        # continue to next class: Task_Class and set the attribute of the new selection of metaClass
        for cont in self.metaClass.incl_contact:

            # Error checking: if stim is not in allowed_stimulation -> Error message
            assert cont.lower() in [c.lower() for c in allowed_contacts], (
                f'inserted contact ({cont}) should'
                f' be in {allowed_contacts}'
            )

            # select out only meta_table for current session
            sel = [cont.lower() in s.lower() for s in self.meta_table["contacts"]]
            sel_meta_table = self.meta_table[sel].reset_index(drop=True)

            if len(sel_meta_table) == 0:
                continue

            # set the task value for each task
            setattr(
                self,
                cont,
                contactclass.contactClass(
                    sub=self.sub,
                    modality=self.modality,
                    session=self.session,
                    condition=self.condition,
                    task=self.task,
                    contact=cont,
                    metaClass=self.metaClass,
                    meta_table=sel_meta_table,
                )
            )  












        

        ############ LOAD MATLAB FILES ############
        self.data = {} # keys named after task, values will be the raw data of one perceived .mat file loaded with mne.io.read_raw_fieldtrip
        
        for row, fname in enumerate(self.meta_table['perceiveFilename']):

            dict_name = self.meta_table.iloc[row]['task'] # .iloc[index][columnname] will give you one cell value (Python index starting from 0)
            
            # suppress RuntimeWarning
            warnings.simplefilter(action='ignore', category=RuntimeWarning)
            
            # .data[dict_name] loading only one file based on the row is selected 'task'
            self.data[dict_name] = load_rawfile.load_matfile(self.sub, fname) # load with mne.read_raw_fieldtrip()

            # KeyError exception:
            # try: 
            #     self.task in self.data.keys()
            
            # except KeyError:
            #     coninue

            print('LOADED', fname)

        


        ############ LOAD SOURCE JSON FILES ############
        self.sourceJSON = {} # keys will be named after task, values will be the raw JSON file of the correct row of metadata
        
        for row, fname in enumerate(self.meta_table['report']):
            
            dict_name = self.meta_table.iloc[row]['task'] # .iloc[index][columnname] will give you one cell value (Python index starting from 0)
            
            # suppress RuntimeWarning
            warnings.simplefilter(action='ignore', category=RuntimeWarning)
            
            # .sourceJSON[dict_name] loading only one file based on the row of the selected 'task'
            self.sourceJSON[dict_name] = load_rawfile.load_sourceJSON(self.sub, fname) 

            # Troubleshooting: will load the same JSON file multple times e.g. BSSu files all from the same JSON object...

            # KeyError exception:
            # try: 
            #     self.task in self.data.keys()
            
            # except KeyError:
            #     coninue

            print('LOADED', fname)


            



        
    

