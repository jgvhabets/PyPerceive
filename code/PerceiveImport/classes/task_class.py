""" Task Class """

import pandas as pd
from dataclasses import dataclass


import PerceiveImport.methods.load_rawfile as load_rawfile

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


            



        
    

